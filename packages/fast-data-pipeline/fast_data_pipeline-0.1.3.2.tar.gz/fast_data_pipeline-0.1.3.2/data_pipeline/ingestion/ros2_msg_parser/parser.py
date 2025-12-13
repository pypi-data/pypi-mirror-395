import importlib
import logging
from typing import Any, Dict, Optional, TypeVar, Mapping, Tuple

import numpy as np

from .rosbags_image import image_to_numpy_rosbags
from .rosbags_pointcloud import read_points_rosbags

logger = logging.getLogger(__name__)

T = TypeVar('T')

NATIVE_CLASSES: dict[str, type] = {}

def to_native(msg: object) -> object:
    """Convert rosbags message to native message."""
    if not hasattr(msg, '__msgtype__'):
        return msg
        
    msgtype: str = msg.__msgtype__  
    if msgtype not in NATIVE_CLASSES:
        pkg, name = msgtype.rsplit('/', 1)
        NATIVE_CLASSES[msgtype] = getattr(importlib.import_module(pkg.replace('/', '.')), name)

    fields = {}
    for name, field in msg.__dataclass_fields__.items():  
        if 'ClassVar' in field.type:
            continue
        value = getattr(msg, name)
        
        if hasattr(value, '__msgtype__'):
            value = to_native(value)
        elif isinstance(value, list):
            converted_list = []
            for x in value:
                if hasattr(x, '__msgtype__'):
                    converted_list.append(to_native(x))
                else:
                    converted_list.append(x)
            value = converted_list
        elif isinstance(value, np.ndarray):
            value = value.tolist()
        
        fields[name] = value

    return NATIVE_CLASSES[msgtype](**fields)


class ROS2MessageParser:
    """Library for converting specific ROS2 messages to other formats."""

    def __init__(self, target_points: int = 4096):
        """
        Args:
            target_points: Deprecated, kept for compatibility
        """
        self.target_points = target_points
        self.parsing_map = {
            "sensor_msgs/msg/Image": self._parse_sensor_msgs_image,
            "sensor_msgs/msg/PointCloud2": self._parse_sensor_msgs_pointcloud2,
            "hi5_msgs/msg/RoadPatchList": self._parse_road_patch_list,
        }

        self._flattenable_schema: Mapping[
            str, Tuple[Tuple[str, str, bool], ...]
        ] = {}

    def can_parse_type(self, typename: str) -> bool:
        """Checks if given type name has registered parser."""
        return typename in self.parsing_map

    def parse(self, msg: Any, msg_type_str: str) -> Optional[Dict[str, Any]]:
        """Parses message by looking up its type in dispatch dictionary."""
        parser_func = self.parsing_map.get(msg_type_str)
        if parser_func:
            return parser_func(msg, msg_type_str)
        return None
    
    def is_flattenable(self, typename: str) -> bool:
        """Does parser produce flat dictionary that can be written column-wise?"""
        return typename in self._flattenable_schema

    def get_flattened_schema(
        self, typename: str
    ) -> Tuple[Tuple[str, str, bool], ...]:
        """Return tuple of (field_name, numpy_dtype_string, is_multi_dimensional)."""
        return self._flattenable_schema.get(typename, ())

    def _parse_sensor_msgs_image(self, msg: Any, type_str: str) -> Dict[str, Any]:
        """Parses sensor_msgs/msg/Image into dictionary."""
        return {
            "data": image_to_numpy_rosbags(msg),
            "timestamp": {
                "timestamp_s": msg.header.stamp.sec,
                "timestamp_ns": msg.header.stamp.nanosec,
            },
            "metadata": {
                "encoding": msg.encoding,
                "frame_id": msg.header.frame_id,
            },
        }

    def _parse_sensor_msgs_pointcloud2(self, msg: Any, type_str: str) -> Dict[str, Any]:
        """
        Parses PointCloud2 as structured array (ragged).
        Returns variable-size array with field names preserved.
        """
        
        logger.debug(f"PointCloud2: width={msg.width}, height={msg.height}")
        logger.debug(f"Frame ID: {msg.header.frame_id}")
        logger.debug(f"Fields: {[f.name for f in msg.fields]}")
        
        # Map PointCloud2 datatypes to numpy
        dtype_map = {
            1: 'i1',   # INT8
            2: 'u1',   # UINT8
            3: 'i2',   # INT16
            4: 'u2',   # UINT16
            5: 'i4',   # INT32
            6: 'u4',   # UINT32
            7: 'f4',   # FLOAT32
            8: 'f8',   # FLOAT64
        }
        
        # Build structured dtype from fields
        dtype_list = []
        for field in msg.fields:
            np_dtype = dtype_map.get(field.datatype, 'f4')
            dtype_list.append((field.name, np_dtype))
        
        # Read points as tuples
        points_tuples = list(read_points_rosbags(msg, skip_nans=True))
        
        if points_tuples:
            # Convert to structured array with field names
            points_array = np.array(points_tuples, dtype=dtype_list)
            logger.debug(f"Parsed {len(points_array)} points with fields: {points_array.dtype.names}")
        else:
            # Empty structured array
            points_array = np.array([], dtype=dtype_list)
        
        return {
            "points": points_array,  # Variable-size structured array
            "num_points": len(points_array),  # Store count for ragged indexing
            "timestamp": {
                "timestamp_s": msg.header.stamp.sec,
                "timestamp_ns": msg.header.stamp.nanosec,
            },
            "metadata": {
                "is_dense": bool(msg.is_dense),
                "frame_id": str(msg.header.frame_id),
            },
        }
    
    def _parse_road_patch_list(self, msg: Any, type_str: str) -> Dict[str, Any]:
        """Parses RoadPatchList with structured metadata."""

        # Map PointCloud2 datatypes to numpy
        dtype_map = {
            1: 'i1', 2: 'u1', 3: 'i2', 4: 'u2',
            5: 'i4', 6: 'u4', 7: 'f4', 8: 'f8',
        }

        # Build structured dtype from msg.data fields
        dtype_list = []
        for field in msg.data.fields:
            np_dtype = dtype_map.get(field.datatype, 'f4')
            dtype_list.append((field.name, np_dtype))

        # Parse metadata PointCloud2
        try:
            points_tuples = list(read_points_rosbags(msg.data, skip_nans=False))

            if points_tuples:
                # Convert to structured array
                metadata_array = np.array(points_tuples, dtype=dtype_list)
                logger.debug(f"Parsed {len(metadata_array)} patches with fields: {metadata_array.dtype.names}")
            else:
                metadata_array = np.array([], dtype=dtype_list)

        except Exception as e:
            logger.error(f"Failed to parse RoadPatchList metadata: {e}")
            import traceback
            logger.error(traceback.format_exc())

            # Fallback dtype
            dtype_list = [
                ('top_left_u', 'u2'),
                ('top_left_v', 'u2'),
                ('bottom_right_u', 'u2'),
                ('bottom_right_v', 'u2'),
                ('center_x', 'f4'),
                ('center_y', 'f4'),
                ('center_z', 'f4')
            ]
            metadata_array = np.array([], dtype=dtype_list)

        # Parse polygons
        all_polygon_points = []
        polygon_start_indices = []
        current_point_index = 0

        logger.info(f"[DEBUG] RoadPatchList: {len(msg.polygons)} polygons")

        for poly_idx, polygon in enumerate(msg.polygons):
            polygon_start_indices.append(current_point_index)
            if polygon.points:
                # Debug: Print first 3 points of first polygon
                if poly_idx == 0:
                    logger.info(f"[DEBUG] First polygon has {len(polygon.points)} points")
                    for pt_idx, pt in enumerate(polygon.points[:3]):
                        logger.info(f"[DEBUG] Polygon 0, Point {pt_idx}: x={pt.x:.10f}, y={pt.y:.10f}, z={pt.z:.10f}")
                        logger.info(f"[DEBUG] Point type: {type(pt)}, x type: {type(pt.x)}")

                for pt in polygon.points:
                    all_polygon_points.append([pt.x, pt.y, pt.z])
                    current_point_index += 1
        
        if all_polygon_points:
            points_array = np.array(all_polygon_points, dtype=np.float32)
        else:
            points_array = np.empty((0, 3), dtype=np.float32)
            
        indices_array = np.array(polygon_start_indices, dtype=np.int32)
        
        return {
            "pointcloud_data": metadata_array,  # Structured array
            "num_patches": len(metadata_array),
            "polygons": {
                "points": points_array,
                "start_indices": indices_array
            },
            "timestamp": {
                "timestamp_s": msg.header.stamp.sec,
                "timestamp_ns": msg.header.stamp.nanosec,
            },
            "metadata": {
                "frame_id": msg.header.frame_id,
            },
        }