import os
import logging
from typing import Dict, List, Any, Optional, Type, Tuple

import numpy as np
import pandas as pd
import tables
from asammdf import MDF


from .base_ingestor import BaseIngester
from ..common.state_manager import StateManager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MF4Ingester(BaseIngester):
    """Ingests MF4 files based on a YAML layout and saves them to HDF5.

    This class discovers MF4 files in a specified input directory, extracts
    data for channels defined in a YAML layout file, and saves the processed
    data into HDF5 files. The HDF5 file structure is dynamically determined
    by the same YAML layout specification, with each signal being saved to its
    own dataset.

    Attributes:
        file_pattern (str): The glob pattern to match MF4 files.
        channel_mapper (Dict[str, str]): A mapping from the original channel
            name in the MF4 file to the desired column name in the HDF5 file.
    """

    def __init__(
        self,
        input_folder: str,
        output_folder: str,
        state_manager,
        file_pattern: str,
        layout_yaml_path: str,
    ):
        """Initializes the MF4Ingester.

        Args:
            input_folder (str): The path to the directory containing input MF4 files.
            output_folder (str): The path to the directory where HDF5 files will be saved.
            state_manager: An object responsible for tracking processed files.
                It must have `get_unprocessed_items` and `update_state` methods.
            file_pattern (str): A file pattern (e.g., "*.mf4") to identify
                files to process within the input folder.
            layout_yaml_path (str): The path to the YAML file that defines the
                data mapping and HDF5 structure.
        """
        super().__init__(input_folder, output_folder, state_manager, layout_yaml_path)
        if "*" not in file_pattern:
            logger.warning(
                "file_pattern does not contain a wildcard '*'. It will only match exact filenames."
            )
        self.file_pattern = file_pattern
        self.channel_mapper = self._create_channel_mapper_from_layout()

    def _create_channel_mapper_from_layout(self) -> Dict[str, str]:
        """Creates a channel name mapping from the loaded YAML layout.

        This method parses the `mapping` section of the layout specification,
        extracting 'original_name' and 'target_name' for entries where the
        source is 'mf4'. It creates a dictionary that maps the source channel
        name to the final dataset name (the last part of the target path).

        Returns:
            Dict[str, str]: A dictionary mapping the original MF4 channel name
                to the target HDF5 dataset name.

        Raises:
            ValueError: If the layout specification is not loaded or is missing
                the 'mapping' key.
        """
        if not self.layout_spec or "mapping" not in self.layout_spec:
            raise ValueError("Layout specification is missing or invalid.")

        mapper = {}
        for mapping in self.layout_spec["mapping"]:
            if mapping.get("source") == "mf4":
                hdf5_path = mapping["target_name"]
                if isinstance(hdf5_path, list):
                    hdf5_path = hdf5_path[0]
                column_name = hdf5_path.split("/")[-1]
                mapper[mapping["original_name"]] = column_name

        logger.info(
            f"Dynamically created channel mapper with {len(mapper)} entries from layout."
        )
        return mapper

    def discover_files(self) -> List[str]:
        """Discovers MF4 files recursively in the input folder that match the file pattern.

        Returns:
            List[str]: A list of absolute paths to the discovered files.
                Returns an empty list if the input directory is not found.
        """
        if not os.path.isdir(self.input_folder):
            logger.error(f"Input directory not found: {self.input_folder}")
            return []
        prefix = (
            self.file_pattern.split("*")[0]
            if "*" in self.file_pattern
            else self.file_pattern
        )
        suffix = self.file_pattern.split("*")[-1] if "*" in self.file_pattern else ""

        matched_files = []
        # Walk through all subdirectories
        for root, dirs, files in os.walk(self.input_folder):
            for f in files:
                if f.startswith(prefix) and f.endswith(suffix):
                    matched_files.append(os.path.join(root, f))

        return matched_files

    def process_file(self, file_path: str) -> Optional[str]:
        """Processes a single MF4 file.

        This method orchestrates the processing of a single MF4 file by
        extracting the relevant data and then saving it to an HDF5 file
        according to the loaded layout specification. It handles exceptions
        during the process and cleans up partially created output files.

        Args:
            file_path (str): The absolute path to the MF4 file to process.

        Returns:
            The file_path if processing was successful, None otherwise.
        """
        file_name = os.path.basename(file_path)
        output_name = os.path.splitext(file_name)[0] + ".h5"
        output_path = os.path.join(self.output_folder, output_name)

        try:
            extracted_data = self._extract_from_mf4(file_path)
            if not extracted_data:
                return None

            if self.layout_spec is None:
                logger.error("Cannot save file: Layout specification was not loaded.")
                return None

            success = self._save_to_hdf5_by_layout(
                output_path, extracted_data, self.layout_spec
            )
            return file_path if success else None

        except Exception as e:
            logger.error(
                f"Unexpected error processing MF4 file {file_name}: {e}", exc_info=True
            )
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except OSError:
                    pass
            return None

    def _save_to_hdf5_by_layout(
        self,
        output_path: str,
        extracted_data: Dict[str, Any],
        layout_spec: Dict[str, Any],
    ) -> bool:
        """Saves extracted data to an HDF5 file, creating one dataset per signal.

        This method iterates through the layout specification and saves each
        signal into its own dataset within the HDF5 file. Regular signals are
        saved as a two-column table ('timestamp_s', 'value'). The 'HostService'
        signal is treated as a special case and saved as a simple 1D array of
        timestamps.

        Args:
            output_path (str): The path for the output HDF5 file.
            extracted_data (Dict[str, Any]): A dictionary containing the
                'timestamps' and a 'data' dictionary of signal arrays.
            layout_spec (Dict[str, Any]): The parsed YAML layout specification.

        Returns:
            bool: True if the save operation was successful, False otherwise.
        """
        logger.info(f"Writing signals to {output_path}.")

        try:
            with tables.open_file(
                output_path, mode="w", title=layout_spec.get("title", "Processed Data")
            ) as h5file:
                timestamps = extracted_data["timestamps"]

                for mapping in layout_spec["mapping"]:
                    if mapping.get("source") != "mf4":
                        continue

                    original_name = mapping["original_name"]
                    output_channel_name = self.channel_mapper.get(original_name)

                    if (
                        not output_channel_name
                        or output_channel_name not in extracted_data["data"]
                    ):
                        logger.warning(
                            f"--> SKIPPING '{original_name}' because its key ('{output_channel_name}') was not found in the extracted data dictionary."
                        )
                        continue

                    signal_data = extracted_data["data"][output_channel_name]
                    target_path = mapping["target_name"]

                    parts = target_path.strip("/").split("/")
                    parent_group = "/" + "/".join(parts[:-1]) if len(parts) > 1 else "/"
                    dataset_name = parts[-1]

                    if original_name == "HostService":
                        h5file.create_array(
                            where=parent_group,
                            name=dataset_name,
                            obj=signal_data,
                            title="Master HostService Timestamps",
                            createparents=True,
                        )
                        logger.info(
                            f"Successfully wrote {len(signal_data)} rows to standalone array '{target_path}'"
                        )
                    else:
                        num_rows = len(timestamps)

                        # Check if signal_data is multi-dimensional (contains arrays)
                        if signal_data.ndim > 1:
                            # Multi-dimensional data: create table with timestamp and multiple value columns
                            num_cols = signal_data.shape[1]

                            # Create dtype with timestamp and multiple value columns
                            dtype_list = [("timestamp_s", "f8")]
                            for i in range(num_cols):
                                dtype_list.append((f"value_{i}", "f8"))

                            table_dtype = np.dtype(dtype_list)
                            structured_array = np.empty(num_rows, dtype=table_dtype)
                            structured_array["timestamp_s"] = timestamps

                            # Fill in each value column
                            for i in range(num_cols):
                                structured_array[f"value_{i}"] = np.nan_to_num(signal_data[:, i])

                            h5file.create_table(
                                where=parent_group,
                                name=dataset_name,
                                obj=structured_array,
                                title=f"Data for {original_name} ({num_cols} columns)",
                                createparents=True,
                                filters=tables.Filters(complib="zlib", complevel=5),
                            )
                            logger.info(
                                f"Successfully wrote {len(structured_array)} rows x {num_cols} columns to dataset '{target_path}'"
                            )
                        else:
                            # 1D data: use original logic
                            table_dtype = np.dtype(
                                [("timestamp_s", "f8"), ("value", signal_data.dtype)]
                            )
                            structured_array = np.empty(num_rows, dtype=table_dtype)
                            structured_array["timestamp_s"] = timestamps
                            structured_array["value"] = np.nan_to_num(signal_data)
                            h5file.create_table(
                                where=parent_group,
                                name=dataset_name,
                                obj=structured_array,
                                title=f"Data for {original_name}",
                                createparents=True,
                                filters=tables.Filters(complib="zlib", complevel=5),
                            )
                            logger.info(
                                f"Successfully wrote {len(structured_array)} rows to dataset '{target_path}'"
                            )
            return True
        except Exception as e:
            logger.error(
                f"Failed during PyTables write operation for {output_path}: {e}",
                exc_info=True,
            )
            if os.path.exists(output_path):
                os.remove(output_path)
            return False

    def _extract_from_mf4(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Extracts specified channels from an MF4 file into NumPy arrays.

        Opens an MF4 file using `asammdf`, checks if all required channels are
        present, and extracts them into a pandas DataFrame. The DataFrame is
        then converted into a dictionary of NumPy arrays, with timestamps
        stored separately.

        Args:
            file_path (str): The path to the MF4 file.

        Returns:
            Optional[Dict[str, Any]]: A dictionary with 'timestamps' (a NumPy array)
                and 'data' (a dictionary mapping channel names to NumPy arrays).
                Returns None if extraction fails for any reason (e.g., file not
                found, missing channels, empty data).
        """
        logger.info(f"Attempting extraction from: {os.path.basename(file_path)}")
        channels_to_extract = list(self.channel_mapper.keys())

        if not channels_to_extract:
            logger.warning("Channel mapper is empty. Skipping.")
            return None

        try:
            with MDF(file_path, memory="low") as mdf_obj:
                if not self._check_channel_completeness(mdf_obj):
                    logger.warning(
                        f"Channel completeness check failed for {file_path}. Skipping."
                    )
                    return None

                # Get list of available channels in the MDF file
                mdf_channel_list = []
                for group in mdf_obj.groups:
                    mdf_channel_list.extend(channel.name for channel in group.channels)

                # Filter out computed channels that don't exist in the file
                # is_brake_actuated can be computed from brake_actuator_position_mm
                if "Model Root/recorder/rfmu/is_brake_actuated" in channels_to_extract:
                    if "Model Root/recorder/rfmu/is_brake_actuated" not in mdf_channel_list:
                        if "Model Root/recorder/rfmu/brake_actuator_position_mm" in mdf_channel_list:
                            logger.info(
                                "Excluding is_brake_actuated from extraction - will be computed from brake_actuator_position_mm"
                            )
                            channels_to_extract.remove("Model Root/recorder/rfmu/is_brake_actuated")

                df_intermediate = mdf_obj.to_dataframe(
                    channels=channels_to_extract,
                    time_from_zero=False,
                    time_as_date=False,
                    empty_channels="skip",
                )

                if df_intermediate.empty:
                    logger.warning(
                        f"DataFrame is empty after extraction for {file_path}. Skipping."
                    )
                    return None

                timestamps_np = df_intermediate.index.to_numpy(dtype=np.float64)
                numpy_data: Dict[str, np.ndarray] = {}

                for input_channel, output_channel in self.channel_mapper.items():
                    if input_channel in df_intermediate.columns:
                        col_data = df_intermediate[input_channel]

                        # Check if column contains list/array values (dtype object)
                        if col_data.dtype == object:
                            # Peek at first non-null value to see what we're dealing with
                            first_val = None
                            for val in col_data:
                                if val is not None and not (isinstance(val, float) and np.isnan(val)):
                                    first_val = val
                                    break

                            if first_val is not None and isinstance(first_val, (list, np.ndarray)):
                                first_val_array = np.array(first_val)
                                logger.info(
                                    f"Channel '{input_channel}' contains array/list values "
                                    f"(shape: {first_val_array.shape}). Storing as arrays."
                                )
                                # Store the arrays as-is
                                try:
                                    # Convert list of arrays to 2D numpy array
                                    array_list = []
                                    for x in col_data:
                                        if isinstance(x, (list, np.ndarray)):
                                            array_list.append(np.array(x, dtype=np.float64))
                                        else:
                                            # Handle missing values with NaN array of same shape
                                            array_list.append(np.full(first_val_array.shape, np.nan, dtype=np.float64))
                                    numpy_data[output_channel] = np.array(array_list, dtype=np.float64)
                                except (ValueError, TypeError) as e:
                                    logger.error(
                                        f"Failed to convert arrays from '{input_channel}': {e}. "
                                        f"Using NaN values."
                                    )
                                    numpy_data[output_channel] = np.full((len(col_data), *first_val_array.shape), np.nan, dtype=np.float64)
                            else:
                                # Object type but not arrays, try to convert to numeric
                                numpy_data[output_channel] = pd.to_numeric(
                                    col_data, errors="coerce"
                                ).to_numpy(dtype=np.float64)
                        else:
                            # Regular numeric column
                            numpy_data[output_channel] = pd.to_numeric(
                                col_data, errors="coerce"
                            ).to_numpy(dtype=np.float64)
                    else:
                        logger.warning(
                            f"Channel '{input_channel}' not in DataFrame for {file_path}."
                        )

                # After the loop, explicitly handle the case where HostService was the index.
                # This ensures it's added to numpy_data with the correct key from the mapper.
                host_service_key = self.channel_mapper.get("HostService")
                if host_service_key and host_service_key not in numpy_data:
                    logger.info(
                        f"Adding '{host_service_key}' to extracted data from the main timestamp index."
                    )
                    numpy_data[host_service_key] = timestamps_np

                # Compute is_brake_actuated if missing but brake_actuator_position_mm exists
                is_brake_actuated_key = self.channel_mapper.get("Model Root/recorder/rfmu/is_brake_actuated")
                brake_actuator_position_key = self.channel_mapper.get("Model Root/recorder/rfmu/brake_actuator_position_mm")

                if is_brake_actuated_key and brake_actuator_position_key:
                    if is_brake_actuated_key not in numpy_data and brake_actuator_position_key in numpy_data:
                        logger.info(
                            f"Computing '{is_brake_actuated_key}' from '{brake_actuator_position_key}' > 1.0"
                        )
                        brake_position = numpy_data[brake_actuator_position_key]
                        numpy_data[is_brake_actuated_key] = (brake_position > 1.0).astype(np.float64)

                if not numpy_data:
                    logger.error(
                        f"No channels successfully extracted for {file_path}. Skipping."
                    )
                    return None

                return {"timestamps": timestamps_np, "data": numpy_data}
        except FileNotFoundError:
            logger.error(f"Input file not found during extraction: {file_path}")
            return None
        except Exception as e:
            logger.error(
                f"Error during extraction for {os.path.basename(file_path)}: {e}",
                exc_info=True,
            )
            return None

    def _check_channel_completeness(self, mdf_obj: MDF) -> bool:
        """Checks if all required channels exist AND have data in the MF4 file.

        Args:
            mdf_obj (MDF): An `asammdf.MDF` object representing the opened file.

        Returns:
            bool: True if all channels specified in `self.channel_mapper` are
                found in the MDF object and contain valid data, False otherwise.
        """
        mdf_channel_list = []
        for group in mdf_obj.groups:
            mdf_channel_list.extend(channel.name for channel in group.channels)

        logger.info(f"All available channels found in file: {sorted(mdf_channel_list)}")

        # Check 1: Do all required channels exist in structure?
        missing_channels = set(self.channel_mapper.keys()) - set(mdf_channel_list)

        # Special case: is_brake_actuated can be computed if brake_actuator_position_mm exists
        if "Model Root/recorder/rfmu/is_brake_actuated" in missing_channels:
            if "Model Root/recorder/rfmu/brake_actuator_position_mm" in mdf_channel_list:
                logger.info(
                    "is_brake_actuated is missing but can be computed from brake_actuator_position_mm"
                )
                missing_channels.remove("Model Root/recorder/rfmu/is_brake_actuated")

        if missing_channels:
            logger.warning(
                f"File is missing required channels: {sorted(list(missing_channels))}"
            )
            return False

        # Check 2: Do all required channels have actual data?
        empty_channels = []
        for channel_name in self.channel_mapper.keys():
            # Skip is_brake_actuated if it can be computed
            if channel_name == "Model Root/recorder/rfmu/is_brake_actuated":
                if "Model Root/recorder/rfmu/brake_actuator_position_mm" in mdf_channel_list:
                    continue

            try:
                signal = mdf_obj.get(channel_name)
                # Check if signal has any non-NaN values
                if signal is None or len(signal.samples) == 0:
                    empty_channels.append(channel_name)
                else:
                    # Try to check for NaN values, but handle array/structured types
                    try:
                        # For numeric types, check if all values are NaN
                        if np.issubdtype(signal.samples.dtype, np.floating):
                            if np.all(np.isnan(signal.samples)):
                                empty_channels.append(channel_name)
                        elif signal.samples.dtype == object or signal.samples.dtype.names is not None:
                            # Array/structured/object types - just check if we have data
                            # If we got here, signal exists and has samples, so it's valid
                            pass
                        else:
                            # Integer or other numeric types can't be NaN, so they're valid
                            pass
                    except (TypeError, ValueError):
                        # If we can't check for NaN, assume the channel is valid if it has data
                        pass
            except Exception as e:
                logger.warning(f"Error reading channel '{channel_name}': {e}")
                empty_channels.append(channel_name)

        if empty_channels:
            logger.warning(
                f"File has empty/all-NaN channels: {sorted(empty_channels)}"
            )
            return False

        return True


if __name__ == "__main__":


    TEST_INPUT_DIR = "/mnt/kit_workspace/new_rosbags/2025_11_24/mf4s"
    TEST_OUTPUT_DIR = "/mnt/kit_workspace/new_rosbags/2025_11_24/mf4-h5"
    LAYOUT_YAML_PATH = "data-pipeline/configs/h5_layout_specification_no_lidar2.yaml"

    state_manager = StateManager(output_folder=TEST_OUTPUT_DIR, state_filename="mf4_processing_state.pkl") 

    os.makedirs(TEST_INPUT_DIR, exist_ok=True)
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

    logger.warning(
        f"This test requires a valid MF4 file in: {os.path.abspath(TEST_INPUT_DIR)}"
    )
    logger.warning(
        "The script will run but may fail at the extraction step if no valid file is found."
    )

    mf4_ingester = MF4Ingester(
        input_folder=TEST_INPUT_DIR,
        output_folder=TEST_OUTPUT_DIR,
        state_manager=state_manager,
        file_pattern="*.mf4",
        layout_yaml_path=LAYOUT_YAML_PATH,
    )

    mf4_ingester.run()