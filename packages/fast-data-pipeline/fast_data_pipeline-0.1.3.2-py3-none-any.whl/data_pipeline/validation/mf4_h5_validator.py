#!/usr/bin/env python3
"""
MF4 to H5 Validation Script

Validates that an H5 file correctly represents the data from its source MF4 file.
Compares datasets, values, and structure to ensure conversion integrity.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

import numpy as np
import yaml
from asammdf import MDF
import tables


@dataclass
class ValidationResult:
    """Results from validating a single channel."""
    channel_name: str
    h5_path: str
    passed: bool
    mf4_rows: Optional[int] = None
    h5_rows: Optional[int] = None
    timestamp_match: Optional[bool] = None
    value_match: Optional[bool] = None
    max_timestamp_diff: Optional[float] = None
    max_value_diff: Optional[float] = None
    mean_abs_error: Optional[float] = None
    error_message: Optional[str] = None


@dataclass
class ValidationSummary:
    """Overall validation summary."""
    total_channels: int = 0
    passed_channels: int = 0
    failed_channels: int = 0
    missing_channels: List[str] = field(default_factory=list)
    extra_datasets: List[str] = field(default_factory=list)
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_channels == 0:
            return 0.0
        return (self.passed_channels / self.total_channels) * 100


class MF4H5Validator:
    """Validates MF4 to H5 conversion."""

    def __init__(
        self,
        mf4_path: str,
        h5_path: str,
        layout_yaml: str,
        rtol: float = 1e-9,
        atol: float = 1e-12,
        verbose: bool = False,
    ):
        """
        Initialize validator.

        Args:
            mf4_path: Path to source MF4 file
            h5_path: Path to converted H5 file
            layout_yaml: Path to layout specification YAML
            rtol: Relative tolerance for float comparisons
            atol: Absolute tolerance for float comparisons
            verbose: Enable verbose output
        """
        self.mf4_path = Path(mf4_path)
        self.h5_path = Path(h5_path)
        self.layout_yaml = Path(layout_yaml)
        self.rtol = rtol
        self.atol = atol
        self.verbose = verbose

        self.layout_config = None
        self.mf4_obj = None
        self.h5_obj = None

    def load_layout_config(self) -> Dict:
        """Load and parse layout YAML configuration."""
        if self.verbose:
            print(f"Loading layout configuration from {self.layout_yaml}")

        with open(self.layout_yaml, 'r') as f:
            config = yaml.safe_load(f)

        # Handle different YAML structures
        if isinstance(config, dict) and 'mapping' in config:
            # YAML has a 'mapping:' key at top level
            mappings = config['mapping']
        elif isinstance(config, list):
            # YAML is directly a list of mappings
            mappings = config
        else:
            raise ValueError(f"Unexpected YAML structure: {type(config)}")

        # Filter for MF4 sources only
        mf4_mappings = [
            entry for entry in mappings
            if entry.get('source') == 'mf4'
        ]

        if self.verbose:
            print(f"Found {len(mf4_mappings)} MF4 channel mappings")

        return mf4_mappings

    def validate_files_exist(self) -> None:
        """Check that all required files exist."""
        if not self.mf4_path.exists():
            raise FileNotFoundError(f"MF4 file not found: {self.mf4_path}")

        if not self.h5_path.exists():
            raise FileNotFoundError(f"H5 file not found: {self.h5_path}")

        if not self.layout_yaml.exists():
            raise FileNotFoundError(f"Layout YAML not found: {self.layout_yaml}")

    def validate_channel(
        self,
        mf4_channel_name: str,
        h5_dataset_path: str,
        is_hostservice: bool = False,
    ) -> ValidationResult:
        """
        Validate a single channel/dataset.

        Args:
            mf4_channel_name: Channel name in MF4 file
            h5_dataset_path: Full path to dataset in H5 file
            is_hostservice: Whether this is the special HostService channel

        Returns:
            ValidationResult with comparison details
        """
        result = ValidationResult(
            channel_name=mf4_channel_name,
            h5_path=h5_dataset_path,
            passed=False,
        )

        try:
            # Extract MF4 data
            if self.verbose:
                print(f"  Extracting MF4 channel: {mf4_channel_name}")

            if is_hostservice:
                # HostService: Use DataFrame index as timestamps
                df = self.mf4_obj.to_dataframe(
                    channels=[],
                    time_from_zero=False,
                    time_as_date=False,
                )
                mf4_data = df.index.to_numpy(dtype=np.float64)
                mf4_timestamps = None  # No separate timestamps for HostService
            else:
                # Regular channel: Extract signal with timestamps
                signal = self.mf4_obj.get(mf4_channel_name)
                mf4_data = signal.samples
                mf4_timestamps = signal.timestamps

            result.mf4_rows = len(mf4_data)

            # Navigate to H5 dataset
            if self.verbose:
                print(f"  Reading H5 dataset: {h5_dataset_path}")

            # Parse the path to navigate through groups
            path_parts = h5_dataset_path.strip('/').split('/')
            h5_node = self.h5_obj.root

            for part in path_parts:
                try:
                    h5_node = getattr(h5_node, part)
                except AttributeError:
                    result.error_message = f"H5 dataset path not found: {h5_dataset_path}"
                    return result

            # Check dataset type and extract data
            if is_hostservice:
                # HostService should be a simple Array
                if not isinstance(h5_node, tables.Array):
                    result.error_message = f"Expected Array for HostService, got {type(h5_node).__name__}"
                    return result

                h5_data = h5_node.read()
                result.h5_rows = len(h5_data)

                # Compare data directly
                if len(mf4_data) != len(h5_data):
                    result.error_message = f"Row count mismatch: MF4={len(mf4_data)}, H5={len(h5_data)}"
                    return result

                # Compare values
                try:
                    np.testing.assert_allclose(
                        mf4_data, h5_data,
                        rtol=self.rtol, atol=self.atol
                    )
                    result.max_value_diff = float(np.max(np.abs(mf4_data - h5_data)))
                    result.mean_abs_error = float(np.mean(np.abs(mf4_data - h5_data)))
                    result.value_match = True
                    result.passed = True
                except AssertionError as e:
                    result.error_message = f"Value comparison failed: {str(e)}"
                    result.max_value_diff = float(np.max(np.abs(mf4_data - h5_data)))
                    result.mean_abs_error = float(np.mean(np.abs(mf4_data - h5_data)))
                    result.value_match = False
                    return result

            else:
                # Regular signal should be a Table with timestamp_s and value columns
                if not isinstance(h5_node, tables.Table):
                    result.error_message = f"Expected Table, got {type(h5_node).__name__}"
                    return result

                # Check columns exist
                if 'timestamp_s' not in h5_node.colnames or 'value' not in h5_node.colnames:
                    result.error_message = f"Missing columns. Found: {h5_node.colnames}"
                    return result

                h5_timestamps = h5_node.col('timestamp_s')
                h5_values = h5_node.col('value')
                result.h5_rows = len(h5_values)

                # Check row counts
                if len(mf4_data) != len(h5_values):
                    result.error_message = f"Row count mismatch: MF4={len(mf4_data)}, H5={len(h5_values)}"
                    return result

                # Compare timestamps
                try:
                    np.testing.assert_allclose(
                        mf4_timestamps, h5_timestamps,
                        rtol=self.rtol, atol=self.atol
                    )
                    result.timestamp_match = True
                    result.max_timestamp_diff = float(np.max(np.abs(mf4_timestamps - h5_timestamps)))
                except AssertionError as e:
                    result.error_message = f"Timestamp comparison failed: {str(e)}"
                    result.timestamp_match = False
                    result.max_timestamp_diff = float(np.max(np.abs(mf4_timestamps - h5_timestamps)))
                    return result

                # Compare values (accounting for NaN -> 0.0 conversion)
                mf4_values_processed = np.nan_to_num(mf4_data.astype(np.float64))

                try:
                    np.testing.assert_allclose(
                        mf4_values_processed, h5_values,
                        rtol=self.rtol, atol=self.atol
                    )
                    result.value_match = True
                    result.max_value_diff = float(np.max(np.abs(mf4_values_processed - h5_values)))
                    result.mean_abs_error = float(np.mean(np.abs(mf4_values_processed - h5_values)))
                    result.passed = True
                except AssertionError as e:
                    result.error_message = f"Value comparison failed: {str(e)}"
                    result.value_match = False
                    result.max_value_diff = float(np.max(np.abs(mf4_values_processed - h5_values)))
                    result.mean_abs_error = float(np.mean(np.abs(mf4_values_processed - h5_values)))
                    return result

        except Exception as e:
            result.error_message = f"Unexpected error: {type(e).__name__}: {str(e)}"
            return result

        return result

    def get_all_h5_datasets(self) -> List[str]:
        """Get list of all dataset paths in H5 file."""
        datasets = []

        # Walk through all nodes in the H5 file
        for node in self.h5_obj.walk_nodes("/", classname="Leaf"):
            if isinstance(node, (tables.Table, tables.Array)):
                datasets.append(node._v_pathname)

        return datasets

    def validate(self) -> ValidationSummary:
        """
        Run full validation.

        Returns:
            ValidationSummary with all results
        """
        summary = ValidationSummary()

        # Validate files exist
        print("Validating file paths...")
        self.validate_files_exist()
        print("✓ All files exist")

        # Load configuration
        print("\nLoading layout configuration...")
        self.layout_config = self.load_layout_config()
        summary.total_channels = len(self.layout_config)
        print(f"✓ Loaded {summary.total_channels} channel mappings")

        # Open files
        print(f"\nOpening MF4 file: {self.mf4_path}")
        self.mf4_obj = MDF(str(self.mf4_path), memory="low")

        print(f"Opening H5 file: {self.h5_path}")
        self.h5_obj = tables.open_file(str(self.h5_path), mode='r')

        try:
            # Get all H5 datasets for comparison
            h5_datasets = set(self.get_all_h5_datasets())
            expected_datasets = set()

            # Validate each channel
            print(f"\nValidating {summary.total_channels} channels...\n")

            for i, mapping in enumerate(self.layout_config, 1):
                original_name = mapping['original_name']
                target_name = mapping['target_name']
                expected_datasets.add(target_name)

                # Check if this is HostService
                is_hostservice = original_name == "HostService"

                if self.verbose:
                    print(f"[{i}/{summary.total_channels}] Validating: {original_name}")
                else:
                    # Progress indicator
                    if i % 10 == 0 or i == summary.total_channels:
                        print(f"Progress: {i}/{summary.total_channels} channels processed")

                result = self.validate_channel(
                    original_name,
                    target_name,
                    is_hostservice=is_hostservice
                )

                summary.results.append(result)

                if result.passed:
                    summary.passed_channels += 1
                    if self.verbose:
                        print(f"  ✓ PASSED")
                else:
                    summary.failed_channels += 1
                    print(f"  ✗ FAILED: {result.error_message}")

            # Check for extra datasets in H5
            extra = h5_datasets - expected_datasets
            if extra:
                summary.extra_datasets = list(extra)

            # Check for missing datasets
            missing = expected_datasets - h5_datasets
            if missing:
                summary.missing_channels = list(missing)

        finally:
            # Close files
            if self.mf4_obj:
                self.mf4_obj.close()
            if self.h5_obj:
                self.h5_obj.close()

        return summary

    def print_summary(self, summary: ValidationSummary) -> None:
        """Print validation summary report."""
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        print(f"\nTotal channels validated: {summary.total_channels}")
        print(f"Passed: {summary.passed_channels} ({summary.success_rate:.1f}%)")
        print(f"Failed: {summary.failed_channels}")

        if summary.missing_channels:
            print(f"\n⚠ Missing datasets in H5 ({len(summary.missing_channels)}):")
            for channel in summary.missing_channels:
                print(f"  - {channel}")

        if summary.extra_datasets:
            print(f"\n⚠ Extra datasets in H5 not in layout ({len(summary.extra_datasets)}):")
            for dataset in summary.extra_datasets:
                print(f"  - {dataset}")

        if summary.failed_channels > 0:
            print(f"\n✗ FAILED CHANNELS ({summary.failed_channels}):")
            for result in summary.results:
                if not result.passed:
                    print(f"\n  Channel: {result.channel_name}")
                    print(f"  H5 Path: {result.h5_path}")
                    if result.mf4_rows is not None:
                        print(f"  MF4 rows: {result.mf4_rows}")
                    if result.h5_rows is not None:
                        print(f"  H5 rows: {result.h5_rows}")
                    print(f"  Error: {result.error_message}")

        if self.verbose and summary.passed_channels > 0:
            print(f"\n✓ PASSED CHANNELS ({summary.passed_channels}):")
            for result in summary.results:
                if result.passed:
                    print(f"\n  Channel: {result.channel_name}")
                    print(f"  Rows: {result.h5_rows}")
                    if result.max_timestamp_diff is not None:
                        print(f"  Max timestamp diff: {result.max_timestamp_diff:.2e}")
                    if result.max_value_diff is not None:
                        print(f"  Max value diff: {result.max_value_diff:.2e}")
                    if result.mean_abs_error is not None:
                        print(f"  Mean absolute error: {result.mean_abs_error:.2e}")

        print("\n" + "=" * 80)

        if summary.failed_channels == 0 and len(summary.missing_channels) == 0:
            print("✓ VALIDATION PASSED: All channels match!")
        else:
            print("✗ VALIDATION FAILED: Issues detected")

        print("=" * 80 + "\n")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate MF4 to H5 conversion integrity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic validation
  python -m data_pipeline.validation.mf4_h5_validator input.mf4 output.h5 layout.yaml

  # Verbose output with custom tolerance
  python -m data_pipeline.validation.mf4_h5_validator input.mf4 output.h5 layout.yaml -v --rtol 1e-6
        """
    )

    parser.add_argument(
        'mf4_file',
        help='Path to source MF4 file'
    )

    parser.add_argument(
        'h5_file',
        help='Path to converted H5 file'
    )

    parser.add_argument(
        'layout_yaml',
        help='Path to layout specification YAML'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--rtol',
        type=float,
        default=1e-9,
        help='Relative tolerance for float comparisons (default: 1e-9)'
    )

    parser.add_argument(
        '--atol',
        type=float,
        default=1e-12,
        help='Absolute tolerance for float comparisons (default: 1e-12)'
    )

    args = parser.parse_args()

    # Create validator
    validator = MF4H5Validator(
        mf4_path=args.mf4_file,
        h5_path=args.h5_file,
        layout_yaml=args.layout_yaml,
        rtol=args.rtol,
        atol=args.atol,
        verbose=args.verbose,
    )

    try:
        # Run validation
        summary = validator.validate()

        # Print results
        validator.print_summary(summary)

        # Exit with appropriate code
        if summary.failed_channels > 0 or len(summary.missing_channels) > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    except Exception as e:
        print(f"\n✗ FATAL ERROR: {type(e).__name__}: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
