# xcf2png

Convert GIMP XCF files to PNG format with flattened visible layers.

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- [ImageMagick](https://imagemagick.org/) (must be installed and available in PATH)

## Usage

The script uses PEP 723 inline dependencies, so you can run it directly with `uv`:

```bash
# Convert a single file
./xcf2png.py image.xcf

# Convert multiple files using wildcards
./xcf2png.py *.xcf

# Overwrite existing PNG files without prompting
./xcf2png.py -o image.xcf
./xcf2png.py --overwrite *.xcf
```

## Features

- Flattens only visible layers from XCF files
- Preserves transparency
- Supports wildcard patterns for batch processing
- Prompts before overwriting existing PNG files (unless `-o`/`--overwrite` is used)
  - When prompted, you can answer:
    - `y` (yes) - overwrite this file
    - `n` (no) - skip this file
    - `a` (all) - overwrite this file and all remaining files without prompting again
- Output PNG files are created in the same directory as the source XCF files

## How it works

The script:
1. Checks that ImageMagick is installed and available
2. Calls ImageMagick's `magick` command with the `-flatten` option to convert XCF to PNG
3. ImageMagick handles reading the XCF format, processing visible layers, and compositing them
4. Saves the flattened result as a PNG file with the same base filename

## Notes

- ImageMagick must be installed separately - the script will exit with a helpful error message if it's not found
- ImageMagick natively supports the XCF format and handles layer flattening automatically
- All visible layers are flattened while maintaining proper alpha channel transparency
