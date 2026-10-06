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
2. Reads the canvas size from the XCF file header (rejecting files that aren't XCF)
3. Calls ImageMagick's `magick` command with `-background none -repage WxH -flatten` to convert XCF to PNG
4. ImageMagick handles reading the XCF format, processing visible layers, and compositing them onto a transparent canvas of the original image size
5. Saves the flattened result as a PNG file with the same base filename

## Notes

- ImageMagick must be installed separately - the script will exit with a helpful error message if it's not found
- ImageMagick natively supports the XCF format and handles layer flattening automatically
- ImageMagick does not preserve the XCF canvas size when loading layers, so the script reads it from the file header. Layers that extend beyond the image bounds are clipped, and layers entirely outside it are ignored, matching GIMP's own export
- All visible layers are flattened while maintaining proper alpha channel transparency
