"""
CLI for managing Pulka test fixtures.

This module provides command-line tools for building, checking, and cleaning
test fixtures according to the manifest.yaml specification.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

# Add src to path for imports
ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pulka.testing.data import make_df, write_df


def load_manifest(manifest_path: Path) -> dict:
    """Load the test data manifest."""
    with manifest_path.open() as f:
        return yaml.safe_load(f)


def build_fixture(fixture_name: str, fixture_config: dict, output_dir: Path) -> list[Path]:
    """
    Build all files for a single fixture.

    Args:
        fixture_name: Name of the fixture
        fixture_config: Configuration from manifest
        output_dir: Directory to write files

    Returns:
        List of created file paths
    """
    created_files = []

    # Generate the DataFrame
    df = make_df(
        fixture_name,
        rows=fixture_config.get("rows"),
        cols=fixture_config.get("cols"),
        seed=fixture_config.get("seed", 42),
    )

    # Write each format
    for file_config in fixture_config.get("files", []):
        file_path = output_dir / file_config["name"]
        format_type = file_config["format"]

        print(f"Building {file_path}")
        write_df(df, file_path, format_type)
        created_files.append(file_path)

    return created_files


def check_fixture(fixture_name: str, fixture_config: dict, output_dir: Path) -> bool:
    """
    Check if a fixture's files exist and are valid.

    Args:
        fixture_name: Name of the fixture
        fixture_config: Configuration from manifest
        output_dir: Directory containing files

    Returns:
        True if all files exist and are valid
    """
    all_valid = True

    for file_config in fixture_config.get("files", []):
        file_path = output_dir / file_config["name"]

        if not file_path.exists():
            print(f"Missing: {file_path}")
            all_valid = False
            continue

        # Basic validation - file is not empty and readable
        try:
            if file_path.stat().st_size == 0:
                print(f"Empty file: {file_path}")
                all_valid = False
                continue

            # Try to validate format-specific properties
            format_type = file_config["format"]
            if format_type == "csv":
                # Check that it's readable as CSV
                with file_path.open() as f:
                    first_line = f.readline()
                    if not first_line.strip():
                        raise ValueError(f"Generated CSV file is empty: {file_path}")

        except Exception as e:
            print(f"Error checking {file_path}: {e}")
            all_valid = False

    return all_valid


def get_total_size(output_dir: Path, committed_only: bool = False) -> int:
    """Get total size of fixture files."""
    total = 0
    manifest_path = output_dir / "manifest.yaml"

    if committed_only and manifest_path.exists():
        manifest = load_manifest(manifest_path)
        for fixture_config in manifest["fixtures"].values():
            for file_config in fixture_config.get("files", []):
                if file_config.get("commit", False):
                    file_path = output_dir / file_config["name"]
                    if file_path.exists():
                        total += file_path.stat().st_size
    else:
        for file_path in output_dir.glob("*"):
            if file_path.is_file() and file_path.name != "manifest.yaml":
                total += file_path.stat().st_size

    return total


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Manage Pulka test fixtures")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build test fixtures")
    build_parser.add_argument("--only", help="Build only specified fixture")
    build_parser.add_argument(
        "--output-dir", type=Path, default=Path("tests/data"), help="Output directory for fixtures"
    )

    # Check command
    check_parser = subparsers.add_parser("check", help="Check test fixtures")
    check_parser.add_argument("--only", help="Check only specified fixture")
    check_parser.add_argument(
        "--output-dir", type=Path, default=Path("tests/data"), help="Directory containing fixtures"
    )

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean generated fixtures")
    clean_parser.add_argument(
        "--all", action="store_true", help="Clean all files including committed ones"
    )
    clean_parser.add_argument(
        "--output-dir", type=Path, default=Path("tests/data"), help="Directory containing fixtures"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    # Load manifest
    manifest_path = args.output_dir / "manifest.yaml"
    if not manifest_path.exists():
        print(f"Error: Manifest not found at {manifest_path}")
        return 1

    manifest = load_manifest(manifest_path)

    if args.command == "build":
        fixtures_to_build = [args.only] if args.only else list(manifest["fixtures"].keys())

        args.output_dir.mkdir(parents=True, exist_ok=True)
        total_created = 0

        for fixture_name in fixtures_to_build:
            if fixture_name not in manifest["fixtures"]:
                print(f"Error: Unknown fixture '{fixture_name}'")
                return 1

            fixture_config = manifest["fixtures"][fixture_name]
            created_files = build_fixture(fixture_name, fixture_config, args.output_dir)
            total_created += len(created_files)

        print(f"\nBuilt {total_created} fixture files")

        # Check total size
        total_size = get_total_size(args.output_dir)
        committed_size = get_total_size(args.output_dir, committed_only=True)
        max_size = manifest.get("policy", {}).get("max_total_size", 102400)

        print(f"Total size: {total_size:,} bytes")
        print(f"Committed size: {committed_size:,} bytes")

        if committed_size > max_size:
            print(f"Warning: Committed size exceeds limit of {max_size:,} bytes")
            return 1

        return 0

    elif args.command == "check":
        fixtures_to_check = [args.only] if args.only else list(manifest["fixtures"].keys())

        all_valid = True
        for fixture_name in fixtures_to_check:
            if fixture_name not in manifest["fixtures"]:
                print(f"Error: Unknown fixture '{fixture_name}'")
                return 1

            fixture_config = manifest["fixtures"][fixture_name]
            if not check_fixture(fixture_name, fixture_config, args.output_dir):
                all_valid = False

        if all_valid:
            print("All fixtures are valid")
            return 0
        else:
            print("Some fixtures are missing or invalid")
            return 1

    elif args.command == "clean":
        if not args.output_dir.exists():
            print("Output directory does not exist")
            return 0

        removed_count = 0
        for fixture_config in manifest["fixtures"].values():
            for file_config in fixture_config.get("files", []):
                file_path = args.output_dir / file_config["name"]

                # Skip committed files unless --all is specified
                if not args.all and file_config.get("commit", False):
                    continue

                if file_path.exists():
                    file_path.unlink()
                    print(f"Removed {file_path}")
                    removed_count += 1

        print(f"Removed {removed_count} files")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
