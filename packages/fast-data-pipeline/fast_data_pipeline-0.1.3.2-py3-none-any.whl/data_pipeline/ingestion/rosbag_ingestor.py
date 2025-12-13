import gc
import keyword
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import tables
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore, get_types_from_msg, store

from tqdm import tqdm

from .base_ingestor import BaseIngester
from .ros2_msg_parser.parser import ROS2MessageParser
from ..common.state_manager import StateManager

logger = logging.getLogger(__name__)


_original_deserialize_cdr = store.Typestore.deserialize_cdr


def patched_deserialize_cdr(typestore, rawdata, typename, tolerance=64):
    """
    Patched deserialize to handle messages with trailing padding bytes.
    
    Standard rosbags allows only 3 trailing bytes. Some messages have padding
    that exceeds this but is harmless.
    """
    little_endian = bool(rawdata[1])
    msgdef = typestore.get_msgdef(typename)
    func = msgdef.deserialize_cdr_le if little_endian else msgdef.deserialize_cdr_be
    message, pos = func(rawdata[4:], 0, msgdef.cls, typestore)
    
    trailing = len(rawdata) - pos - 4
    if trailing > tolerance:
        logger.warning(
            f"{typename}: excessive trailing {trailing} bytes (tolerance: {tolerance})"
        )
    
    return message


def _initialize_typestore_worker(
    ros_distro: str, custom_msg_folders: List[str]
) -> store.Typestore:
    """Initialize rosbags typestore in worker process."""
    typestore = get_typestore(
        getattr(Stores, f"ROS2_{ros_distro.upper()}", Stores.ROS2_HUMBLE)
    )
    if not custom_msg_folders:
        return typestore
    for folder in custom_msg_folders:
        for path in Path(folder).rglob("*.msg"):
            if path.parent.name == "msg":
                try:
                    typestore.register(
                        get_types_from_msg(
                            path.read_text(),
                            f"{path.parent.parent.name}/msg/{path.stem}",
                        )
                    )
                except Exception as e:
                    logger.error(f"Worker failed to register message {path}: {e}")
    return typestore


def _get_value_recursive_worker(obj: Any, parts: List[str]) -> Any:
    """Retrieve nested attribute from object, handling callables."""
    val = obj
    for part in parts:
        try:
            val = getattr(val, part)
        except AttributeError:
            return None
            
    if callable(val):
        try:
            val = val()
        except TypeError:
            return None

    if hasattr(val, "sec") and hasattr(val, "nanosec"):
        return val.sec + val.nanosec * 1e-9
    return val


class RosbagIngester(BaseIngester):
    """Ingests ROS 2 bag files into HDF5 with smart pattern-based writing."""

    def __init__(
        self,
        input_folder: str,
        output_folder: str,
        state_manager: Any,
        layout_yaml_path: str,
        ros_distro: str = "humble",
        custom_msg_folders: List[str] = None,
        chunk_size: int = 1000,
        n_jobs_messages: int = -1,
        auto_detect_max_points: bool = False,
        default_target_points: int = 4096,
    ):
        super().__init__(input_folder, output_folder, state_manager, layout_yaml_path)
        self.ros_distro = ros_distro
        self.custom_msg_folders = custom_msg_folders or []
        self.chunk_size = chunk_size
        self.n_jobs_messages = n_jobs_messages if n_jobs_messages != 0 else -1
        self.auto_detect_max_points = auto_detect_max_points
        self.default_target_points = default_target_points
        self.topic_map = self._create_topic_map_from_layout()
        self.parser = ROS2MessageParser(target_points=default_target_points)

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        del state["parser"]
        return state

    def __setstate__(self, state: dict):
        self.__dict__.update(state)
        self.parser = ROS2MessageParser(target_points=self.default_target_points)

    def _create_topic_map_from_layout(self) -> Dict[str, str]:
        if not self.layout_spec or "mapping" not in self.layout_spec:
            raise ValueError("Layout spec missing or invalid.")
        return {
            m["original_name"]: m["target_name"]
            for m in self.layout_spec["mapping"]
            if m.get("source") == "ros2bag"
        }

    def discover_files(self) -> List[str]:
        """Discover both ROS 2 bag directories and .mcap files recursively."""
        if not os.path.isdir(self.input_folder):
            return []

        discovered = []

        # Walk through all subdirectories
        for root, dirs, files in os.walk(self.input_folder):
            # Check if current directory is a rosbag2 directory (has metadata.yaml)
            if "metadata.yaml" in files:
                discovered.append(root)
                # Don't descend into subdirectories of rosbag2 directories
                # since they're part of the bag structure
                dirs.clear()
            else:
                # Find standalone .mcap files in current directory
                for file in files:
                    if file.endswith('.mcap'):
                        discovered.append(os.path.join(root, file))

        return discovered

    def process_file(self, rosbag_path: str) -> Optional[str]:
        """
        Process single rosbag (folder or .mcap file) and convert to HDF5.
        Cleans up partial files on failure.
        """
        # Extract base name (works for both directories and files)
        base_name = os.path.splitext(os.path.basename(rosbag_path))[0]
        safe_name = self._sanitize_hdf5_identifier(base_name)
        output_path = os.path.join(self.output_folder, f"{safe_name}.h5")
        h5file = None
        success = False

        try:
            h5file = tables.open_file(
                output_path, mode="w", title=f"Data from {base_name}"
            )

            # Process the rosbag (handles both directories and .mcap files)
            self._stream_and_write_hybrid(rosbag_path, h5file)
            
            # Close file before checking size
            h5file.close()
            h5file = None
            
            # Check if file was actually written (not just empty)
            file_size = os.path.getsize(output_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # Consider files under 1MB as failed (empty or minimal data)
            if file_size < 1024 * 1024:  # 1 MB threshold
                logger.error(
                    f"Output file '{output_path}' is suspiciously small ({file_size_mb:.2f} MB). "
                    "Likely processing failed."
                )
                success = False
            else:
                logger.info(
                    f"Successfully created HDF5 file '{output_path}' with size {file_size_mb:.2f} MB."
                )
                success = True

            if success:
                return rosbag_path
            else:
                return None

        except KeyboardInterrupt:
            logger.warning(f"Processing interrupted by user for {base_name}")
            raise

        except Exception as e:
            logger.error(f"Failed to process rosbag {base_name}: {e}", exc_info=True)
            success = False
            return None
            
        finally:
            # Close file if still open
            if h5file and h5file.isopen:
                try:
                    h5file.close()
                except Exception as e:
                    logger.error(f"Error closing HDF5 file: {e}")

            # Remove file if processing failed
            if not success and os.path.exists(output_path):
                try:
                    file_size = os.path.getsize(output_path) / (1024 * 1024)
                    os.remove(output_path)
                    logger.info(f"Removed failed HDF5 file {output_path} ({file_size:.2f} MB)")
                except OSError as err:
                    logger.error(f"Error removing failed HDF5 file {output_path}: {err}")
            
            # Cleanup memory
            gc.collect()

    def _get_element_type_name(self, field_type_tuple: tuple) -> Optional[str]:
        node_type, details = field_type_tuple
        if node_type == 1:
            return details[0]
        if node_type == 2:
            return details
        if node_type in (3, 4):
            sub_node_type, sub_details = details[0]
            if sub_node_type == 1:
                return sub_details[0]
            if sub_node_type == 2:
                return sub_details
        return None

    def _stream_and_write_hybrid(self, rosbag_path: str, h5file: tables.File):
        """Process rosbag (folder or .mcap file) with unified smart writing for all message types."""
        typestore = self._initialize_typestore()

        # For standalone MCAP files, wrap them in a list like a rosbag2 directory
        # This helps AnyReader properly detect and use the MCAP/ROS2 reader
        path_obj = Path(rosbag_path)

        # AnyReader expects a list of paths and will auto-detect the format
        reader = AnyReader([path_obj], default_typestore=typestore)

        with reader:
            # Get all topics available in the rosbag
            available_topics = {c.topic for c in reader.connections}
            expected_topics = set(self.topic_map.keys())

            # Check if ALL expected topics are present (strict validation)
            missing_topics = expected_topics - available_topics

            if missing_topics:
                logger.warning(
                    f"Skipping {rosbag_path}: Missing {len(missing_topics)} "
                    f"expected topic(s): {sorted(missing_topics)}"
                )
                raise ValueError(
                    f"Rosbag missing required topics: {sorted(missing_topics)}"
                )

            # All topics present, proceed with processing
            connections = [c for c in reader.connections if c.topic in self.topic_map]

            if not connections:
                logger.error(f"No matching topics found in {rosbag_path}")
                raise ValueError(f"No valid topics to process in {rosbag_path}")

            topic_blueprints = {}
            for conn in connections:
                topic_path = self.topic_map[conn.topic]
                if topic_path not in topic_blueprints:
                    topic_blueprints[topic_path] = self._create_topic_blueprint(
                        h5file, conn.msgtype, topic_path, typestore
                    )

            logger.info("Starting streaming processing...")

            message_generator = reader.messages(connections=connections)

            processed_count = 0
            error_count = 0
            max_errors = 10

            with tqdm(desc=f"Processing {os.path.basename(rosbag_path)}", unit="msg") as pbar:
                for conn, ts, raw in message_generator:
                    pbar.update(1)
                    processed_count += 1

                    try:
                        topic_path = self.topic_map[conn.topic]
                        blueprint = topic_blueprints[topic_path]

                        if "group" not in blueprint:
                            logger.error(f"Blueprint for {topic_path} missing 'group'!")
                            continue

                        topic_grp = blueprint["group"]
                        msg = patched_deserialize_cdr(typestore, raw, conn.msgtype)

                        # Unified path: Parser handles conversion, writer handles storage
                        if self.parser.can_parse_type(conn.msgtype):
                            parsed_dict = self.parser.parse(msg, conn.msgtype)
                            if parsed_dict:
                                self._write_dict_to_hdf5(topic_grp, parsed_dict)
                            continue

                        datasets = blueprint["datasets"]

                        # Process complex and flat fields (for non-parseable types)
                        for field_name, field_info in blueprint["fields"].items():
                            if field_info["is_complex"]:
                                field_value = getattr(msg, field_name, None)
                                if field_value:
                                    parsed_data = self.parser.parse(field_value, field_info["type"])
                                    if parsed_data:
                                        self._write_dict_to_hdf5(field_info["group"], parsed_data)
                            else:
                                for flat_name, path, _, _ in field_info["flat_fields"]:
                                    value = self._get_value_recursive(msg, path)
                                    dataset = datasets[flat_name]
                                    if isinstance(dataset, tables.VLArray):
                                        encoded_value = str(value if value is not None else "").encode("utf-8")
                                        dataset.append(encoded_value)
                                    else:
                                        dataset.append([value])
                    
                    except Exception as e:
                        error_count += 1
                        logger.error(
                            f"Error processing message {processed_count} "
                            f"from {conn.topic}: {e}"  
                        )
                        
                        if error_count <= 5:
                            logger.error("Exception details:", exc_info=True)
                        
                        if error_count > max_errors:
                            logger.error(f"Too many errors ({error_count}), aborting")
                            raise
                        
                        continue
            
            logger.info(
                f"Processed {processed_count} messages with {error_count} errors"
            )

            if processed_count == 0:
                raise ValueError(f"No messages processed successfully from {rosbag_path}")

    def _write_dict_to_hdf5(
        self, parent_group: tables.Group, data_dict: Dict[str, Any]
    ):
        """Write dictionary to HDF5 with intelligent pattern detection."""
        h5file = parent_group._v_file
        
        # PATTERN 1: Ragged array (PointCloud2)
        # Has 'points' array and 'num_points' counter
        if 'points' in data_dict and 'num_points' in data_dict:
            self._write_ragged_pointcloud(parent_group, data_dict)
            return
        
        # PATTERN 2: Road patches
        # Has 'pointcloud_data', 'polygons', and 'num_patches'
        if 'pointcloud_data' in data_dict and 'polygons' in data_dict:
            self._write_road_patches(parent_group, data_dict)
            return
        
        # PATTERN 3: Generic dictionary - write recursively
        for key, value in data_dict.items():
            sane_key = self._sanitize_hdf5_identifier(key)
            
            # Create dataset/group if doesn't exist
            if not hasattr(parent_group, sane_key):
                if isinstance(value, str):
                    atom = tables.VLStringAtom()
                    h5file.create_vlarray(parent_group, sane_key, atom)

                elif isinstance(value, dict):
                    subgroup = h5file.create_group(parent_group, sane_key)
                    self._write_dict_to_hdf5(subgroup, value)
                    continue

                elif isinstance(value, np.ndarray):
                    if value.dtype.names:
                        # Structured array → Table
                        h5file.create_table(
                            parent_group, sane_key,
                            description=value.dtype,
                            title=sane_key
                        )
                    else:
                        # Regular array → Stackable EArray
                        # This handles images, fixed-size arrays, etc.
                        # Shape (0, H, W) allows stacking: (N, H, W)
                        atom = tables.Atom.from_dtype(value.dtype)
                        shape = (0,) + value.shape
                        h5file.create_earray(parent_group, sane_key, atom, shape)
                else:
                    # Scalar
                    np_val = np.array(value)
                    atom = tables.Atom.from_dtype(np_val.dtype)
                    h5file.create_earray(parent_group, sane_key, atom, (0,))
                # Fall through to append the first value (don't continue!)
            
            # Append to existing dataset
            dataset = getattr(parent_group, sane_key)
            
            if isinstance(dataset, tables.Table):
                if isinstance(value, np.ndarray) and value.dtype.names:
                    dataset.append(value)
                    dataset.flush()
                    
            elif isinstance(dataset, tables.VLArray):
                if isinstance(value, str):
                    encoded = value.encode("utf-8")
                else:
                    encoded = str(value if value is not None else "").encode("utf-8")
                dataset.append(encoded)
                
            elif isinstance(dataset, tables.EArray):
                if isinstance(value, np.ndarray):
                    if value.size > 0:
                        # Add batch dimension if needed for stacking
                        if value.ndim == dataset.ndim - 1:
                            value = value[np.newaxis, ...]
                        dataset.append(value)
                    else:
                        dataset.append(value if value.ndim > 0 else [value])
                else:
                    dataset.append([value])
                    
            elif isinstance(dataset, tables.Group):
                self._write_dict_to_hdf5(dataset, value)

    def _write_ragged_pointcloud(self, parent_group: tables.Group, data_dict: Dict):
        """Handle ragged PointCloud2 data."""
        h5file = parent_group._v_file
        points = data_dict['points']
        
        # Create data group
        if not hasattr(parent_group, 'data'):
            data_group = h5file.create_group(parent_group, 'data')
            data_group._v_attrs.current_index = 0
        else:
            data_group = parent_group.data
        
        # Create tables on first write
        if not hasattr(data_group, 'all_points'):
            h5file.create_table(
                data_group, 'all_points',
                description=points.dtype,
                title="All point cloud data (ragged)"
            )
            h5file.create_earray(
                data_group, 'frame_start_indices',
                tables.Int32Atom(), (0,),
                title="Start index of each frame"
            )
        
        # Append data
        current_idx = data_group._v_attrs.current_index
        data_group.frame_start_indices.append([current_idx])
        
        if len(points) > 0:
            data_group.all_points.append(points)
            data_group._v_attrs.current_index = current_idx + len(points)
        
        # Write other fields (timestamp, metadata) normally
        other_data = {k: v for k, v in data_dict.items() 
                      if k not in ['points', 'num_points']}
        if other_data:
            self._write_dict_to_hdf5(parent_group, other_data)

    def _write_road_patches(self, parent_group: tables.Group, data_dict: Dict):
        """Handle RoadPatchList data."""
        h5file = parent_group._v_file
        
        # Write pointcloud_data
        if not hasattr(parent_group, 'pointcloud_data'):
            h5file.create_table(
                parent_group, 'pointcloud_data',
                description=data_dict['pointcloud_data'].dtype,
                title="Road patch metadata"
            )
        parent_group.pointcloud_data.append(data_dict['pointcloud_data'])
        
        # Write polygons with cumulative index tracking
        if not hasattr(parent_group, 'polygons'):
            polygons_group = h5file.create_group(parent_group, 'polygons')
            polygons_group._v_attrs.current_polygon_index = 0
            
            h5file.create_earray(
                polygons_group, 'points',
                tables.Float32Atom(), (0, 3),
                title="Polygon vertices"
            )
            h5file.create_earray(
                polygons_group, 'start_indices',
                tables.Int32Atom(), (0,),
                title="Start index of each polygon"
            )
        
        polygons_group = parent_group.polygons
        
        # Adjust indices to be cumulative
        local_indices = data_dict['polygons']['start_indices']
        current_idx = polygons_group._v_attrs.current_polygon_index
        global_indices = local_indices + current_idx
        
        polygons_group.points.append(data_dict['polygons']['points'])
        polygons_group.start_indices.append(global_indices)
        
        # Update cumulative counter
        n_points = len(data_dict['polygons']['points'])
        polygons_group._v_attrs.current_polygon_index = current_idx + n_points
        
        # Write num_patches per frame
        if not hasattr(parent_group, 'num_patches'):
            h5file.create_earray(
                parent_group, 'num_patches',
                tables.Int64Atom(), (0,),
                title="Number of patches per frame"
            )
        parent_group.num_patches.append([data_dict['num_patches']])
        
        # Write other fields (timestamp, metadata)
        other_data = {k: v for k, v in data_dict.items() 
                      if k not in ['pointcloud_data', 'polygons', 'num_patches']}
        if other_data:
            self._write_dict_to_hdf5(parent_group, other_data)
                        
    def _create_topic_blueprint(
        self, h5file: tables.File, msgtype_name: str, topic_path: str, typestore: store.Typestore
    ) -> Dict[str, Any]:
        blueprint: Dict[str, Any] = {"datasets": {}, "fields": {}}

        parts = topic_path.strip("/").split("/")
        parent_group = h5file.root
        for part in parts:
            parent_group = getattr(parent_group, part, None) or h5file.create_group(parent_group, part)

        if self.parser.can_parse_type(msgtype_name):
            blueprint["group"] = parent_group
            return blueprint

        msg_def = typestore.get_msgdef(msgtype_name)

        for field_name, field_type_tuple in msg_def.fields:
            sane_name = self._sanitize_hdf5_identifier(field_name)
            element_type = self._get_element_type_name(field_type_tuple)

            if self.parser.is_flattenable(element_type):
                flat_schema = self.parser.get_flattened_schema(element_type)
                for flat_key, np_dtype_str, is_multi in flat_schema:
                    if np_dtype_str == "object":
                        atom = tables.VLStringAtom()
                        ds = h5file.create_vlarray(parent_group, flat_key, atom)
                    else:
                        atom = tables.Atom.from_dtype(np.dtype(np_dtype_str))
                        shape = (0,) + (()) if is_multi else (0,)
                        ds = h5file.create_earray(parent_group, flat_key, atom, shape)
                    blueprint["datasets"][flat_key] = ds
                continue

            if self.parser.can_parse_type(element_type):
                blueprint["fields"][sane_name] = {
                    "is_complex": True,
                    "type": element_type,
                    "group": h5file.create_group(parent_group, sane_name),
                }
                continue

            blueprint["fields"][sane_name] = {
                "is_complex": False,
                "flat_fields": [],
            }

            flat_fields = self._get_all_fields(
                element_type, typestore, prefix=f"{sane_name}_", path=[field_name]
            )
            blueprint["fields"][sane_name]["flat_fields"] = flat_fields

            for flat_name, _, ros_type, _ in flat_fields:
                if hasattr(parent_group, flat_name):
                    ds = getattr(parent_group, flat_name)
                else:
                    try:
                        if ros_type == "string":
                            atom = tables.VLStringAtom()
                            ds = h5file.create_vlarray(parent_group, flat_name, atom)
                        else:
                            atom = tables.Atom.from_dtype(np.dtype(ros_type))
                            ds = h5file.create_earray(parent_group, flat_name, atom, (0,))
                    except (TypeError, ValueError):
                        atom = tables.VLStringAtom()
                        ds = h5file.create_vlarray(parent_group, flat_name, atom)

                blueprint["datasets"][flat_name] = ds

        blueprint["group"] = parent_group
        return blueprint

    def _get_all_fields(
        self,
        typename: str,
        typestore: store.Typestore,
        prefix: str = "",
        path: Optional[List[str]] = None,
        visited: Optional[set] = None,
    ) -> List[tuple]:
        if visited is None:
            visited = set()
        if path is None:
            path = []
        if typename in visited or self.parser.can_parse_type(typename):
            return []

        visited.add(typename)
        fields_list = []
        try:
            msg_def = typestore.get_msgdef(typename)
            for field_name, field_type_tuple in msg_def.fields:
                flat_name = f"{prefix}{field_name}"
                new_path = path + [field_name]
                element_type_name = self._get_element_type_name(field_type_tuple)
                is_array = field_type_tuple[0] in (3, 4)
                nested_fields = self._get_all_fields(
                    element_type_name, typestore, f"{flat_name}_", new_path, visited.copy()
                )
                if not nested_fields:
                    fields_list.append(
                        (flat_name, new_path, element_type_name, is_array)
                    )
                else:
                    fields_list.extend(nested_fields)
            return fields_list
        except KeyError:
            return [(prefix.strip("_"), path, typename, False)]

    def _get_value_recursive(self, obj: Any, parts: List[str]) -> Any:
        return _get_value_recursive_worker(obj, parts)

    def _initialize_typestore(self) -> store.Typestore:
        return _initialize_typestore_worker(self.ros_distro, self.custom_msg_folders)

    def _sanitize_hdf5_identifier(self, name: str) -> str:
        name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        if name and name[0].isdigit():
            name = "_" + name
        if keyword.iskeyword(name):
            name += "_"
        return name or "unnamed"


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s",
    )

    TEST_INPUT_DIR = "/mnt/kit_workspace/new_rosbags/2025_11_24/rosbags/"
    TEST_OUTPUT_DIR = "/mnt/kit_workspace/new_rosbags/2025_11_24/rosbag-h5/"
    YAML_PATH = "data-pipeline/configs/h5_layout_specification_no_lidar2.yaml"
    CUSTOM_MESSAGES_FOLDER = ["data-pipeline/aivp-ros2-custom-messages"]
    N_JOBS_FOR_FILES = 1
    N_JOBS_FOR_MESSAGES = 1

    os.makedirs(TEST_INPUT_DIR, exist_ok=True)
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

    state_manager = StateManager(
        output_folder=TEST_OUTPUT_DIR,
        state_filename="rosbag_processing_state.pkl"
    )

    if not os.path.exists(TEST_INPUT_DIR) or not os.listdir(TEST_INPUT_DIR):
        logger.warning(f"ACTION REQUIRED: Place rosbag folder in: {os.path.abspath(TEST_INPUT_DIR)}")
    else:
        ingester = RosbagIngester(
            input_folder=TEST_INPUT_DIR,
            output_folder=TEST_OUTPUT_DIR,
            custom_msg_folders=CUSTOM_MESSAGES_FOLDER,
            state_manager=state_manager,
            layout_yaml_path=YAML_PATH,
            n_jobs_messages=N_JOBS_FOR_MESSAGES,
            ros_distro="humble"
        )
        ingester.run(n_jobs=N_JOBS_FOR_FILES)