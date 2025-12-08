#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""
xcf2png - Convert GIMP XCF files to PNG format

This script converts XCF (GIMP) files to PNG format using ImageMagick,
flattening visible layers while preserving transparency.
"""

import argparse
import glob
import shutil
import subprocess
import sys
from pathlib import Path


def check_imagemagick() -> bool:
    """
    Check if ImageMagick is installed and available.

    Returns:
        True if ImageMagick is available, False otherwise
    """
    return shutil.which('magick') is not None


def flatten_xcf_to_png(xcf_path: Path, png_path: Path) -> bool:
    """
    Convert an XCF file to PNG using ImageMagick.

    Args:
        xcf_path: Path to the input XCF file
        png_path: Path to the output PNG file

    Returns:
        True if conversion was successful, False otherwise
    """
    try:
        # Run ImageMagick conversion
        result = subprocess.run(
            ['magick', str(xcf_path), '-flatten', str(png_path)],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: ImageMagick conversion failed: {e.stderr}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: Unexpected error during conversion: {e}", file=sys.stderr)
        return False


def convert_xcf_to_png(xcf_path: Path, overwrite: bool = False) -> tuple[bool, bool]:
    """
    Convert a single XCF file to PNG.

    Args:
        xcf_path: Path to the XCF file
        overwrite: If True, overwrite without prompting

    Returns:
        Tuple of (success, overwrite_all) where:
        - success: True if conversion was successful
        - overwrite_all: True if user chose to overwrite all remaining files
    """
    # Generate output path
    png_path = xcf_path.with_suffix('.png')

    # Check if output file exists
    if png_path.exists() and not overwrite:
        response = input(f"File '{png_path}' already exists. Overwrite? (y/n/a [all]): ").strip().lower()
        if response in ('a', 'all'):
            # User chose to overwrite all remaining files
            pass  # Continue with conversion
        elif response not in ('y', 'yes'):
            print(f"Skipping {xcf_path}")
            return False, False

        # Return overwrite_all flag
        overwrite_all = response in ('a', 'all')
    else:
        overwrite_all = False

    print(f"Converting {xcf_path} to {png_path}...")

    # Convert XCF to PNG using ImageMagick
    success = flatten_xcf_to_png(xcf_path, png_path)

    if success:
        print(f"Successfully converted {xcf_path} to {png_path}")
    else:
        print(f"Failed to convert {xcf_path}", file=sys.stderr)

    return success, overwrite_all


def main():
    """Main entry point for the script."""
    # Check if ImageMagick is available
    if not check_imagemagick():
        print("Error: ImageMagick is not installed or not found in PATH.", file=sys.stderr)
        print("Please install ImageMagick to use this script.", file=sys.stderr)
        print("Visit https://imagemagick.org/script/download.php for installation instructions.", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description='Convert GIMP XCF files to PNG format, flattening visible layers.'
    )
    parser.add_argument(
        'files',
        nargs='+',
        help='XCF file(s) to convert (wildcards supported)'
    )
    parser.add_argument(
        '-o', '--overwrite',
        action='store_true',
        help='Overwrite existing PNG files without prompting'
    )

    args = parser.parse_args()

    # Expand wildcards and collect all XCF files
    xcf_files = []
    for pattern in args.files:
        matches = glob.glob(pattern)
        if matches:
            xcf_files.extend([Path(f) for f in matches if Path(f).is_file()])
        else:
            # If no matches, try as literal filename
            path = Path(pattern)
            if path.is_file():
                xcf_files.append(path)

    if not xcf_files:
        print("Error: No XCF files found.", file=sys.stderr)
        sys.exit(1)

    # Convert each file
    success_count = 0
    overwrite_all = args.overwrite  # Start with command-line flag

    for xcf_path in xcf_files:
        success, overwrite_all_chosen = convert_xcf_to_png(xcf_path, overwrite_all)
        if success:
            success_count += 1
        # If user chose "overwrite all", remember it for subsequent files
        if overwrite_all_chosen:
            overwrite_all = True

    print(f"\nConversion complete: {success_count}/{len(xcf_files)} files converted.")

    # Exit with error code if no files were converted
    if success_count == 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
