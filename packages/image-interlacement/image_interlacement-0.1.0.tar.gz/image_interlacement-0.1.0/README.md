# Image Interlacement Program

A Python CLI tool for creating composites by alternating rows or columns from two images.

## Overview

This program allows you to create unique composite images by interleaving pixels from two images row-by-row or column-by-column. For example, combine two photos so that alternating rows come from each image, creating an interesting blended visual effect.

## Features

- **Row-based Compositing** - Alternate entire rows of pixels from two images
- **Column-based Compositing** - Alternate entire columns of pixels from two images
- **CLI Interface** - Easy-to-use command-line interface
- **Future Enhancements** - GUI and web app support planned

## Installation

You can install and use the Image Interlacement program in two ways:

### Option 1: Standalone Executable (Easiest for Non-Technical Users)

**No Python installation required!**

1. Go to the [Latest Release](../../releases/latest) page
2. Download the executable for your operating system:
   - **macOS (Apple Silicon / M1/M2/M3)**: `image-interlacement` (arm64)
   - **macOS (Intel)**: `image-interlacement` (x86_64)
   - **Linux**: `image-interlacement` (x86_64)
   - **Windows**: `image-interlacement.exe`
3. On macOS/Linux, make it executable and run:
   ```bash
   chmod +x image-interlacement
   ./image-interlacement --help
   ```
4. On Windows, simply double-click or run from Command Prompt:
   ```cmd
   image-interlacement.exe --help
   ```

### Option 2: Python Package via pip (For Developers)

**Requires Python 3.8 or higher and pip**

Install from PyPI:
```bash
pip install image-interlacement
```

Then run from anywhere:
```bash
image-interlacement --help
```

Or clone and install from source:
```bash
git clone <repository-url>
cd image-interlacement-program
pip install -e .
image-interlacement --help
```

### Option 3: Run from Source (For Development)

If you're modifying the code:

1. Clone the repository:
```bash
git clone <repository-url>
cd image-interlacement-program
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the program:
```bash
python src/main.py --help
```

## Usage

### Basic Commands

#### Create a Row-based Composite

Alternate entire rows from two images:

```bash
python src/main.py composite image1.png image2.png output.png --mode rows
```

Pattern: Output rows are interleaved - Row 0 from image1, Row 1 from image2, Row 2 from image1, etc.
The output height will be **2x the input height**.

You can also use solid colors instead of image files:

```bash
python src/main.py composite image1.png white output.png --mode rows
python src/main.py composite image1.png black output.png --mode rows
```

#### Create a Column-based Composite

Alternate entire columns from two images:

```bash
python src/main.py composite image1.png image2.png output.png --mode columns
```

Pattern: Output columns are interleaved - Column 0 from image1, Column 1 from image2, Column 2 from image1, etc.
The output width will be **2x the input width**.

You can also use solid colors instead of image files:

```bash
python src/main.py composite image1.png white output.png --mode columns
python src/main.py composite image1.png black output.png --mode columns
```

#### Interlace (same-size) — legacy behavior

Create a same-size interlaced image where even rows/columns come from the first image and odd rows/columns come from the second image.

```bash
python src/main.py interlace image1.png image2.png output.png --mode rows
python src/main.py interlace image1.png image2.png output.png --mode columns
```

Notes:
- The output image will have the same dimensions as the (tiled) inputs.
- If input sizes differ, the smaller image will be tiled to match the larger one before interlacing.
- You can also use `white` or `black` in place of an image path.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Pillow | >=9.0.0 | Image processing and manipulation |
| NumPy | >=1.21.0 | Efficient array operations for pixel manipulation |

## Project Structure

```
image-interlacement-program/
├── src/
│   ├── __init__.py          # Package initialization
│   └── main.py              # CLI entry point
├── README.md                # This file
├── requirements.txt         # Python dependencies
└── .github/
    └── copilot-instructions.md  # Copilot workspace instructions
```

## Architecture

### Current Implementation

- **main.py**: CLI argument parser and entry point

### Planned Components

- `utils.py` - Utility functions for image handling and validation
- `gui/` - GUI interface module
- `web/` - Web application module
- `tests/` - Unit tests

## Technical Details

### Row-based Compositing

When creating a row-based composite:
- The output image height will be **2x the input height**
- Output row 0, 2, 4, ... come from image1
- Output row 1, 3, 5, ... come from image2
- If one image is smaller, it is tiled (repeated) to match the larger image's size

### Column-based Compositing

When creating a column-based composite:
- The output image width will be **2x the input width**
- Output column 0, 2, 4, ... come from image1
- Output column 1, 3, 5, ... come from image2
- If one image is smaller, it is tiled (repeated) to match the larger image's size

### Requirements for Input Images

- At least one input must be an actual image file (cannot use "white" and "black" together)
- Both inputs must result in the same color channels after processing (RGB)
- **Different dimensions are now supported!** Smaller images will be automatically tiled to match the larger image's size
- Supported formats: PNG, JPG, BMP, TIFF, and other formats supported by Pillow
- **Solid color support**: Use `white` or `black` instead of a file path to create solid color images

## Examples

### Example 1: Combine Two Portraits (Row-based)

```bash
python src/main.py composite portrait_a.jpg portrait_b.jpg blended_portrait.jpg --mode rows
```

Creates a portrait composite where alternating horizontal lines come from each image.

### Example 3: Interleave with White Background

```bash
python src/main.py composite image1.png white output.png --mode rows
```

Creates a composite where the original image alternates with pure white rows.

### Example 4: Interleave with Black Background

```bash
python src/main.py composite image1.png black output.png --mode columns
```

Creates a composite where the original image alternates with pure black columns.



## Development

### Running the Program

```bash
python src/main.py --help
```

View help for specific commands:

```bash
python src/main.py composite --help
```

### Future Enhancements

- [x] Implement row-based compositing algorithm
- [x] Implement column-based compositing algorithm
- [x] Add input validation (matching dimensions and channels)
- [x] Add error handling and user-friendly error messages
- [ ] Add batch processing support
- [ ] Add GUI interface with tkinter or PyQt
- [ ] Add web interface with Flask/Django
- [ ] Add unit tests and integration tests
- [ ] Add performance benchmarks
- [ ] Support for different alternation patterns (e.g., diagonal, custom)

## Quick Start

1. **Clone/navigate to repository**:
```bash
cd image-interlacement-program
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create a composite**:
```bash
python src/main.py composite photo1.jpg photo2.jpg output.jpg --mode rows
```

4. **For additional usage info**:
```bash
python src/main.py --help
python src/main.py composite --help
```

## Troubleshooting

### Image Dimension Mismatch
- **Old Behavior**: Would throw an error
- **New Behavior**: The smaller image is automatically tiled to match the larger image's dimensions
- No action required! The program handles different sized images seamlessly.

### Unsupported Image Format
- **Error**: "Cannot identify image file"
- **Solution**: Convert images to PNG, JPG, or BMP format. Use an image converter tool.

### Different Color Spaces
- **Error**: Image mode mismatch
- **Solution**: The program automatically converts to RGB if needed. No action required.

## License

[Add license information here]

## Contributing

[Add contribution guidelines here]

## Releasing New Versions

To learn how to create and publish new releases, see [RELEASE.md](./RELEASE.md).

## Support

For issues or questions, please open an issue in the repository.

---

**Last Updated**: December 7, 2025  
**Version**: 0.1.0
