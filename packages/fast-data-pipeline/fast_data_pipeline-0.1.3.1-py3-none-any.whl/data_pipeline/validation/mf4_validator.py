#!/usr/bin/env python3
"""
MF4 File Validator

Validates that all channels specified in the layout mapping exist in the MF4 file.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass, field

import yaml
from asammdf import MDF


@dataclass
class ValidationSummary:
    """Overall validation summary."""
    file_path: Path
    file_valid: bool = True
    total_expected_channels: int = 0
    present_channels: int = 0
    missing_channels: List[str] = field(default_factory=list)
    extra_channels: List[str] = field(default_factory=list)
    file_errors: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_expected_channels == 0:
            return 0.0
        return (self.present_channels / self.total_expected_channels) * 100


class MF4Validator:
    """Validates MF4 files against layout specification."""

    def __init__(
        self,
        mf4_path: str,
        layout_yaml: str,
        verbose: bool = False,
    ):
        """
        Initialize validator.

        Args:
            mf4_path: Path to MF4 file to validate
            layout_yaml: Path to layout specification YAML
            verbose: Enable verbose output
        """
        self.mf4_path = Path(mf4_path)
        self.layout_yaml = Path(layout_yaml)
        self.verbose = verbose

        self.layout_config = None
        self.mdf = None

    def load_layout_config(self) -> List[Dict]:
        """Load and parse layout YAML configuration."""
        if self.verbose:
            print(f"Loading layout configuration from {self.layout_yaml}")

        with open(self.layout_yaml, 'r') as f:
            config = yaml.safe_load(f)

        # Handle different YAML structures
        if isinstance(config, dict) and 'mapping' in config:
            mappings = config['mapping']
        elif isinstance(config, list):
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

    def validate_file_integrity(self) -> List[str]:
        """
        Validate basic file integrity.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Check file exists
        if not self.mf4_path.exists():
            errors.append(f"File not found: {self.mf4_path}")
            return errors

        # Check file size
        file_size = self.mf4_path.stat().st_size
        if file_size == 0:
            errors.append("File is empty (0 bytes)")
            return errors

        # Try to open the file
        try:
            if self.verbose:
                print(f"Opening MF4 file: {self.mf4_path}")
            self.mdf = MDF(str(self.mf4_path), memory="low")

            if self.verbose:
                print(f"✓ File opened successfully")
                print(f"  MDF version: {self.mdf.version}")
                print(f"  Channel groups: {len(self.mdf.groups)}")
                print(f"  Total channels: {len(self.mdf.channels_db)}")

        except Exception as e:
            errors.append(f"Failed to open MF4 file: {type(e).__name__}: {str(e)}")
            return errors

        return errors

    def validate(self) -> ValidationSummary:
        """
        Run full validation.

        Returns:
            ValidationSummary with all results
        """
        summary = ValidationSummary(file_path=self.mf4_path)

        # Validate file integrity
        print("Validating file integrity...")
        file_errors = self.validate_file_integrity()

        if file_errors:
            summary.file_valid = False
            summary.file_errors = file_errors
            print("✗ File validation failed")
            for error in file_errors:
                print(f"  - {error}")
            return summary

        print("✓ File is valid and readable")

        # Load layout configuration
        print("\nLoading layout configuration...")
        try:
            self.layout_config = self.load_layout_config()
            summary.total_expected_channels = len(self.layout_config)
            print(f"✓ Loaded {summary.total_expected_channels} expected MF4 channels")
        except Exception as e:
            summary.file_errors.append(f"Failed to load layout: {str(e)}")
            summary.file_valid = False
            return summary

        # Get all actual channels
        actual_channels = set(self.mdf.channels_db.keys())
        expected_channels = set()

        # Check each expected channel exists
        print(f"\nValidating channel presence...\n")

        for mapping in self.layout_config:
            original_name = mapping['original_name']
            expected_channels.add(original_name)

            if original_name in actual_channels:
                summary.present_channels += 1
                if self.verbose:
                    print(f"  ✓ {original_name}")
            else:
                summary.missing_channels.append(original_name)
                print(f"  ✗ MISSING: {original_name}")

        # Check for extra channels
        extra = actual_channels - expected_channels
        if extra:
            summary.extra_channels = sorted(extra)

        return summary

    def print_summary(self, summary: ValidationSummary) -> None:
        """Print validation summary report."""
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)

        print(f"\nFile: {summary.file_path.name}")
        print(f"Full path: {summary.file_path}")

        if not summary.file_valid:
            print("\n✗ FILE VALIDATION FAILED")
            for error in summary.file_errors:
                print(f"  - {error}")
            print("=" * 80 + "\n")
            return

        print(f"\nExpected channels: {summary.total_expected_channels}")
        print(f"Present channels: {summary.present_channels} ({summary.success_rate:.1f}%)")
        print(f"Missing channels: {len(summary.missing_channels)}")

        # Missing channels
        if summary.missing_channels:
            print(f"\n✗ MISSING CHANNELS ({len(summary.missing_channels)}):")
            for channel in summary.missing_channels:
                print(f"  - {channel}")

        # Extra channels
        if summary.extra_channels:
            print(f"\n⚠ EXTRA CHANNELS NOT IN LAYOUT ({len(summary.extra_channels)}):")
            for channel in summary.extra_channels[:20]:  # Show first 20
                print(f"  - {channel}")
            if len(summary.extra_channels) > 20:
                print(f"  ... and {len(summary.extra_channels) - 20} more")

        print("\n" + "=" * 80)

        if len(summary.missing_channels) == 0:
            print("✓ VALIDATION PASSED: All required channels present!")
        else:
            print("✗ VALIDATION FAILED: Missing channels detected")

        print("=" * 80 + "\n")

    def close(self):
        """Close MDF file if open."""
        if self.mdf:
            self.mdf.close()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate that MF4 file contains all channels specified in layout",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic validation
  python -m data_pipeline.validation.mf4_validator input.mf4 layout.yaml

  # Verbose output
  python -m data_pipeline.validation.mf4_validator input.mf4 layout.yaml -v
        """
    )

    parser.add_argument(
        'mf4_file',
        help='Path to MF4 file to validate'
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

    args = parser.parse_args()

    # Create validator
    validator = MF4Validator(
        mf4_path=args.mf4_file,
        layout_yaml=args.layout_yaml,
        verbose=args.verbose,
    )

    try:
        # Run validation
        summary = validator.validate()

        # Print results
        validator.print_summary(summary)

        # Exit with appropriate code
        if not summary.file_valid or len(summary.missing_channels) > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"\n✗ FATAL ERROR: {type(e).__name__}: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)

    finally:
        validator.close()


if __name__ == '__main__':
    main()
