"""Merges HDF5 files by combining their top-level groups.

This script automates the process of finding pairs of HDF5 files (referred
to as 'rec' and 'rosbag' files) from specified folders. It matches these
files based on their time intervals to find corresponding pairs.

For each matched pair, it creates a new HDF5 file that contains all the
top-level groups from both of the original files. For example, if one file
has a '/perception' group and the other has a '/vehicle_data' group, the
merged file will contain both.

The script maintains a log of processed files to avoid re-processing on
subsequent runs.
"""

import h5py
import numpy as np
import glob
import os
from typing import List, Dict, Tuple, Set
import pickle
from .metadata_functions import default_metadata_adder
from loguru import logger
import gc
from contextlib import contextmanager
from tqdm import tqdm

@contextmanager
def safe_h5_merge(output_path: str):
    """
    Context manager for safe HDF5 merge operations.
    Removes output file if error occurs during merge.
    """
    try:
        yield output_path
    except Exception as e:
        if os.path.exists(output_path):
            logger.error(f"Cleaning up failed merge: {output_path}")
            os.remove(output_path)
        raise

def merge_hdf5_files(file1: str, file2: str, output_path: str, show_progress: bool = True):
    """
    Merges two HDF5 files with progress tracking and automatic cleanup on error.
    On dataset conflict, renames original with '_rec' suffix and new with '_ros' suffix.
    """
    gc.collect()

    with safe_h5_merge(output_path):
        with h5py.File(file1, 'r') as f1, \
             h5py.File(file2, 'r') as f2, \
             h5py.File(output_path, 'w') as out:

            logger.info(f"Copying from {os.path.basename(file1)}...")
            copy_h5_structure(f1, out, show_progress=show_progress)

            logger.info(f"Merging from {os.path.basename(file2)}...")
            merge_h5_structure(f2, out, rec_suffix="rec", ros_suffix="ros", show_progress=show_progress)
    


def copy_h5_structure(source, dest, chunk_size=64, show_progress=False):
    """Recursively copies HDF5 structure using chunked reads."""
    for name, item in source.items():
        if isinstance(item, h5py.Group):
            new_group = dest.create_group(name)
            copy_h5_structure(item, new_group, chunk_size, show_progress)
        else:
            copy_dataset_chunked(item, dest, name, chunk_size, show_progress)

def merge_h5_structure(source, dest, rec_suffix, ros_suffix, chunk_size=64, show_progress=False):
    """Recursively merges using chunked reads."""
    for name, item in source.items():
        if isinstance(item, h5py.Group):
            if name not in dest:
                dest.create_group(name)
            merge_h5_structure(item, dest[name], rec_suffix, ros_suffix, chunk_size, show_progress)
        else:
            if name in dest:
                renamed_rec_path = f"{name}_{rec_suffix}"
                logger.info(f"Conflict on '{name}'. Renaming original to '{renamed_rec_path}'")
                dest.move(name, renamed_rec_path)
                
                new_ros_path = f"{name}_{ros_suffix}"
                logger.info(f"Storing new as '{new_ros_path}'")
                copy_dataset_chunked(item, dest, new_ros_path, chunk_size, show_progress)
            else:
                copy_dataset_chunked(item, dest, name, chunk_size, show_progress)


def validate_dataset_compatibility(source_ds, dest_ds):
    """Validates source and destination datasets are compatible for copying."""
    if source_ds.shape != dest_ds.shape:
        raise ValueError(f"Shape mismatch: {source_ds.shape} vs {dest_ds.shape}")
    if source_ds.dtype != dest_ds.dtype:
        raise ValueError(f"Dtype mismatch: {source_ds.dtype} vs {dest_ds.dtype}")
    

def copy_dataset_chunked(source_dataset, dest_group, name, chunk_size=1024, show_progress=False):
    """Copies dataset in chunks to minimize memory usage."""
    shape = source_dataset.shape
    dtype = source_dataset.dtype
    
    # Handle scalar datasets
    if len(shape) == 0:
        dest_dataset = dest_group.create_dataset(name, shape=shape, dtype=dtype)
        copy_attrs(source_dataset, dest_dataset)
        dest_dataset[()] = source_dataset[()]
        return
    
    # Handle empty datasets
    if shape[0] == 0:
        dest_dataset = dest_group.create_dataset(
            name, shape=shape, dtype=dtype,
            chunks=None, compression=None
        )
        copy_attrs(source_dataset, dest_dataset)
        return
    
    # Check if structured dtype
    is_structured = dtype.names is not None

    logger.debug(
        f"Copying dataset '{name}': shape={shape}, dtype={dtype}, "
        f"structured={is_structured}, chunks={source_dataset.chunks}"
    )
    
    # Determine chunking
    original_chunks = source_dataset.chunks
    if original_chunks is not None:
        dest_chunks = tuple(min(c, s) for c, s in zip(original_chunks, shape))
    else:
        if is_structured:
            dest_chunks = (min(chunk_size, shape[0]),)
        else:
            dest_chunks = (min(chunk_size, shape[0]),) + shape[1:]

    logger.debug(f"Using chunks: {dest_chunks} for dataset '{name}'")
    
    # Create destination dataset
    dest_dataset = dest_group.create_dataset(
        name,
        shape=shape,
        dtype=dtype,
        chunks=dest_chunks,
        compression=source_dataset.compression,
        compression_opts=source_dataset.compression_opts
    )

    validate_dataset_compatibility(source_dataset, dest_dataset)
    
    copy_attrs(source_dataset, dest_dataset)
    
    # Copy data in chunks
    total_chunks = (shape[0] + chunk_size - 1) // chunk_size
    chunk_iterator = range(0, shape[0], chunk_size)
    if show_progress and total_chunks > 1:
        chunk_iterator = tqdm(
            chunk_iterator,
            total=total_chunks,
            desc=f"Copying {name}",
            unit="chunk",
            leave=False
        )
    
    is_vlen_str = dtype == np.object_ or dtype.kind == 'O'

    for i in chunk_iterator:
        end_idx = min(i + chunk_size, shape[0])
        try:
            if is_vlen_str:
                # Variable-length strings need special handling
                chunk_data = source_dataset[i:end_idx]
                for j, item in enumerate(chunk_data):
                    dest_dataset[i + j] = item
            else:
                # Direct copy for other dtypes
                dest_dataset[i:end_idx] = source_dataset[i:end_idx]
        except (TypeError, ValueError) as e:
            logger.error(
                f"Copy failed for '{name}' at chunk [{i}:{end_idx}]: "
                f"source shape={source_dataset.shape}, dest shape={dest_dataset.shape}, "
                f"source dtype={source_dataset.dtype}, dest dtype={dest_dataset.dtype}, "
                f"is_vlen_str={is_vlen_str}"
            )
            raise


def copy_attrs(source, dest):
    """Copies all attributes from source to destination."""
    for attr_name, attr_value in source.attrs.items():
        dest.attrs[attr_name] = attr_value


def get_time_intervals(
    folder: str, file_regex: str, timestamp_spec: str
) -> Dict[str, Tuple[float, float]]:
    """
    Extracts start and end timestamps from HDF5 files.
    Handles multiple timestamp formats:
    - Simple dataset: "/path/to/dataset"
    - Structured single field: "/path/to/dataset::field_name"
    - Structured dual fields: "/path/to/dataset::field_s,field_ns"
    - Separate datasets: "/path/to/dataset_s|/path/to/dataset_ns"
    """
    filepaths = glob.glob(f"{folder}/{file_regex}")
    time_intervals = {}

    # Parse timestamp specification
    if "|" in timestamp_spec:
        # Two separate datasets for seconds and nanoseconds
        dataset_s_path, dataset_ns_path = timestamp_spec.split("|", 1)
        mode = "separate_datasets"
        field_s, field_ns = None, None
    elif "::" in timestamp_spec:
        dataset_path, fields = timestamp_spec.split("::", 1)
        if "," in fields:
            # Structured dataset with two fields
            field_s, field_ns = fields.split(",", 1)
            mode = "structured_dual"
        else:
            # Structured dataset with single field (legacy)
            field_s = fields
            field_ns = None
            mode = "structured_single"
    else:
        # Simple dataset (legacy)
        dataset_path = timestamp_spec
        field_s, field_ns = None, None
        mode = "simple"

    for path in filepaths:
        try:
            with h5py.File(path, "r") as hf5_file:
                if mode == "separate_datasets":
                    # Handle separate datasets for seconds and nanoseconds
                    if dataset_s_path not in hf5_file or dataset_ns_path not in hf5_file:
                        logger.warning(f"Datasets '{dataset_s_path}' or '{dataset_ns_path}' not found in {path}")
                        continue

                    dataset_s = hf5_file[dataset_s_path]
                    dataset_ns = hf5_file[dataset_ns_path]

                    if len(dataset_s) == 0 or len(dataset_ns) == 0:
                        logger.warning(f"Empty datasets in {path}")
                        continue

                    start_time = float(dataset_s[0]) + float(dataset_ns[0]) * 1e-9
                    end_time = float(dataset_s[-1]) + float(dataset_ns[-1]) * 1e-9

                elif mode == "structured_dual":
                    # Handle structured dataset with two fields
                    if dataset_path not in hf5_file:
                        logger.warning(f"Dataset '{dataset_path}' not found in {path}")
                        continue

                    dataset = hf5_file[dataset_path]
                    
                    if len(dataset) == 0:
                        logger.warning(f"Dataset '{dataset_path}' in {path} is empty")
                        continue

                    if not hasattr(dataset.dtype, 'fields') or \
                       field_s not in dataset.dtype.fields or \
                       field_ns not in dataset.dtype.fields:
                        logger.warning(f"Fields '{field_s}' or '{field_ns}' not found in dataset '{dataset_path}' in {path}")
                        continue

                    start_time = float(dataset[0][field_s]) + float(dataset[0][field_ns]) * 1e-9
                    end_time = float(dataset[-1][field_s]) + float(dataset[-1][field_ns]) * 1e-9

                elif mode == "structured_single":
                    # Legacy: structured dataset with single field
                    if dataset_path not in hf5_file:
                        logger.warning(f"Dataset '{dataset_path}' not found in {path}")
                        continue

                    dataset = hf5_file[dataset_path]
                    
                    if len(dataset) == 0:
                        logger.warning(f"Dataset '{dataset_path}' in {path} is empty")
                        continue

                    if not hasattr(dataset.dtype, 'fields') or field_s not in dataset.dtype.fields:
                        logger.warning(f"Field '{field_s}' not found in dataset '{dataset_path}' in {path}")
                        continue

                    start_time = float(dataset[0][field_s])
                    end_time = float(dataset[-1][field_s])

                else:  # mode == "simple"
                    # Legacy: simple dataset
                    if dataset_path not in hf5_file:
                        logger.warning(f"Dataset '{dataset_path}' not found in {path}")
                        continue

                    dataset = hf5_file[dataset_path]
                    
                    if len(dataset) == 0:
                        logger.warning(f"Dataset '{dataset_path}' in {path} is empty")
                        continue

                    start_time = float(dataset[0])
                    end_time = float(dataset[-1])

                time_intervals[path] = (start_time, end_time)

        except (KeyError, IOError, ValueError, IndexError) as e:
            logger.error(f"Could not process {path}. Error: {e}")

    return time_intervals


def load_processed_log(log_path: str) -> Set[str]:
    """Loads a set of processed file paths from a pickle log file."""
    if not os.path.exists(log_path):
        return set()
    try:
        with open(log_path, "rb") as f:
            if os.path.getsize(log_path) > 0:
                return pickle.load(f)
            return set()
    except (pickle.UnpicklingError, EOFError) as e:
        print(f"Warning: Could not read pickle log at {log_path}. Error: {e}")
        return set()


def update_processed_log(
    log_path: str, processed_set: Set[str], filepath1: str, filepath2: str
):
    """Adds newly processed file paths to the log and saves it."""
    processed_set.add(filepath1)
    processed_set.add(filepath2)
    with open(log_path, "wb") as f:
        pickle.dump(processed_set, f)


def filter_unprocessed_files(
    rec_intervals: Dict[str, Tuple[float, float]],
    rosbag_intervals: Dict[str, Tuple[float, float]],
    processed_paths: Set[str],
) -> Tuple[Dict[str, Tuple[float, float]], Dict[str, Tuple[float, float]]]:
    """Filters out files that have already been processed."""
    unprocessed_rec = {
        p: t for p, t in rec_intervals.items() if p not in processed_paths
    }
    unprocessed_rosbag = {
        p: t for p, t in rosbag_intervals.items() if p not in processed_paths
    }
    return unprocessed_rec, unprocessed_rosbag


def match_files_by_overlap(
    files1_intervals: Dict[str, Tuple[float, float]],
    files2_intervals: Dict[str, Tuple[float, float]],
) -> List[Tuple[str, str]]:
    """Matches pairs of files from two groups based on the longest time overlap where one is contained within the other."""
    if not files1_intervals or not files2_intervals:
        return []

    potential_matches = []
    for path1, (start1, end1) in files1_intervals.items():
        for path2, (start2, end2) in files2_intervals.items():
            if start2 <= start1 and end1 <= end2:
                potential_matches.append(((path1, path2), end1 - start1))
            elif start1 <= start2 and end2 <= end1:
                potential_matches.append(((path1, path2), end2 - start2))

    potential_matches.sort(key=lambda x: x[1], reverse=True)

    matched_pairs = []
    used_files = set()
    for (path1, path2), duration in potential_matches:
        if path1 not in used_files and path2 not in used_files:
            matched_pairs.append((path1, path2))
            used_files.add(path1)
            used_files.add(path2)
            print(
                f"-> Match found: {os.path.basename(path1)} and {os.path.basename(path2)} (Contained duration: {duration:.3f}s)"
            )

    return matched_pairs

def run(**kwargs):
    rec_folder = kwargs["rec_folder"]
    rosbag_folder = kwargs["rosbag_folder"]
    output_folder = kwargs["output_folder"]
    os.makedirs(output_folder, exist_ok=True)
    rec_timestamp_spec = kwargs["rec_timestamp_spec"]
    rosbag_timestamp_spec = kwargs["rosbag_timestamp_spec"]
    rec_global_pattern = kwargs["rec_global_pattern"]
    rosbag_global_pattern = kwargs["rosbag_global_pattern"]
    log_file_path = os.path.join(output_folder, kwargs["logging_file_name"])
    metadata_func = kwargs["metadata_func"]

    processed_files_set = load_processed_log(log_file_path)
    logger.info("Set of processed files loaded")

    all_rec_intervals = get_time_intervals(
        rec_folder, rec_global_pattern, rec_timestamp_spec
    )
    all_rosbag_intervals = get_time_intervals(
        rosbag_folder, rosbag_global_pattern, rosbag_timestamp_spec
    )

    rec_intervals, rosbag_intervals = filter_unprocessed_files(
        all_rec_intervals, all_rosbag_intervals, processed_files_set
    )

    matched_pairs = match_files_by_overlap(rec_intervals, rosbag_intervals)
    logger.info(f"\nFound {len(matched_pairs)} new valid file pairs to process.\n")

    if not matched_pairs:
        logger.warning("No new matched pairs found to merge.")
    else:
        success_count = 0
        for rec_path, rosbag_path in matched_pairs:
            rec_basename = os.path.basename(rec_path).replace(".h5", "")
            rosbag_basename = os.path.basename(rosbag_path).replace(".h5", "")
            output_filename = f"{rosbag_basename}_merged_{rec_basename}.h5"  
            output_file_path = os.path.join(output_folder, output_filename)

            with safe_h5_merge(output_file_path):
                merge_hdf5_files(
                    file1=rec_path,
                    file2=rosbag_path,
                    output_path=output_file_path,
                    show_progress=True
                )
                logger.info(f"Merge successful: Created {output_filename}")

                gc.collect()

                if metadata_func:
                    if metadata_func(output_file_path):
                        logger.info("Metadata added successfully.")
                        success_count += 1
                        update_processed_log(
                            log_file_path, processed_files_set, rec_path, rosbag_path
                        )
                    else:
                        logger.error("Metadata addition failed.")
                        raise RuntimeError("Metadata addition failed")
                else:
                    success_count += 1
                    update_processed_log(
                        log_file_path, processed_files_set, rec_path, rosbag_path
                    )

        logger.info(f"\nSuccessfully processed {success_count} out of {len(matched_pairs)} pairs.")






def main(metadata_adder=default_metadata_adder):
    """
    Main function to discover, match, and merge HDF5 files.
    """

    def print_h5_structure(filepath: str):
        """Prints all object paths within an HDF5 file for verification."""
        print(f"\n--- Structure of {os.path.basename(filepath)} ---")
        try:
            with h5py.File(filepath, 'r') as f:
                f.visit(lambda name: print(f"   - {name}"))
        except Exception as e:
            print(f"Could not read file structure: {e}")
        print("--- End of Structure ---\n")

    # --- Configuration ---
    REC_FOLDER = "/mnt/kit_workspace/new_rosbags/2025_10_29/mf4-h5"
    ROSBAG_FOLDER = "/mnt/kit_workspace/new_rosbags/2025_10_29/rosbag-h5"
    OUTPUT_FOLDER = "/mnt/kit_workspace/new_rosbags/2025_10_29/synchronized"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    REC_TIMESTAMP_SPEC = "hi5/vehicle_data/timestamp_s::value"
    ROSBAG_TIMESTAMP_SPEC = "hi5/road/image/timestamp/timestamp_s|hi5/road/image/timestamp/timestamp_ns"

    rec_glob_pattern = "rec*.h5"
    rosbag_glob_pattern = "rosbag2*.h5"

    LOG_FILE_PATH = os.path.join(OUTPUT_FOLDER, "processed_files.pkl")
    processed_files_set = load_processed_log(LOG_FILE_PATH)
    print(
        f"Loaded {len(processed_files_set)} previously processed file paths from log.\n"
    )

    print("--- Stage 1: Discovering all files and their time intervals ---")
    all_rec_intervals = get_time_intervals(
        REC_FOLDER, rec_glob_pattern, REC_TIMESTAMP_SPEC
    )
        
    all_rosbag_intervals = get_time_intervals(
        ROSBAG_FOLDER, rosbag_glob_pattern, ROSBAG_TIMESTAMP_SPEC
    )

    rec_intervals, rosbag_intervals = filter_unprocessed_files(
        all_rec_intervals, all_rosbag_intervals, processed_files_set
    )
    print(
        f"Found {len(rec_intervals)} new rec files and {len(rosbag_intervals)} new rosbag files to process.\n"
    )

    print("--- Stage 2: Matching new files by longest contained overlap ---")
    matched_pairs = match_files_by_overlap(rec_intervals, rosbag_intervals)
    print(f"\nFound {len(matched_pairs)} new valid file pairs to process.\n")

    print("--- Stage 3: Merging matched pairs ---")
    if not matched_pairs:
        print("No new matched pairs found to merge.")
    else:
        success_count = 0
        for rec_path, rosbag_path in matched_pairs:
            rec_basename = os.path.basename(rec_path).replace(".h5", "")
            rosbag_basename = os.path.basename(rosbag_path).replace(".h5", "")
            output_filename = f"{rosbag_basename}_merged_{rec_basename}.h5"  
            output_file_path = os.path.join(OUTPUT_FOLDER, output_filename)

            with safe_h5_merge(output_file_path):
                merge_hdf5_files(
                    file1=rec_path,
                    file2=rosbag_path,
                    output_path=output_file_path,
                    show_progress=True
                )
                print(f"   - Merge successful: Created {output_filename}")

                gc.collect()

                if metadata_adder:
                    print(f"   - Adding metadata to {output_filename}...")
                    if metadata_adder(output_file_path):
                        print("   - Metadata added successfully.")
                        success_count += 1
                        update_processed_log(
                            LOG_FILE_PATH, processed_files_set, rec_path, rosbag_path
                        )
                    else:
                        print("   - Metadata addition failed.")
                        raise RuntimeError("Metadata addition failed")
                else:
                    success_count += 1
                    update_processed_log(
                        LOG_FILE_PATH, processed_files_set, rec_path, rosbag_path
                    )

        print(f"\nSuccessfully processed {success_count} out of {len(matched_pairs)} pairs.")


if __name__ == "__main__":
    

    main()

    