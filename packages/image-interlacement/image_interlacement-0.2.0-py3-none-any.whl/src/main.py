"""Main CLI entry point for the image interlacing program."""

import argparse
import sys
from pathlib import Path

# Support both direct execution (python src/main.py) and package imports (pip install / image-interlacement)
try:
    from .composite import composite, interlace
except ImportError:
    from composite import composite, interlace


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Image Interlacing Program - Create composites by alternating rows/columns from two images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py composite image1.png image2.png output.png --mode rows
  python main.py composite image1.png image2.png output.png --mode columns
  python main.py composite image1.png white output.png --mode rows
  python main.py composite image1.png black output.png --mode rows
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Composite command
    composite_parser = subparsers.add_parser('composite', help='Create a composite from two images')
    composite_parser.add_argument('image1', type=str, help='First input image path, or "white"/"black" for solid color')
    composite_parser.add_argument('image2', type=str, help='Second input image path, or "white"/"black" for solid color')
    composite_parser.add_argument('output', type=str, help='Output image path')
    composite_parser.add_argument('--mode', type=str, default='rows', 
                                  choices=['rows', 'columns'],
                                  help='Alternation mode: rows or columns (default: rows)')

    # Interlace command (same-size interlacing)
    interlace_parser = subparsers.add_parser('interlace', help='Interlace two images into a same-size image')
    interlace_parser.add_argument('image1', type=str, help='First input image path, or "white"/"black" for solid color')
    interlace_parser.add_argument('image2', type=str, help='Second input image path, or "white"/"black" for solid color')
    interlace_parser.add_argument('output', type=str, help='Output image path')
    interlace_parser.add_argument('--mode', type=str, default='rows', 
                                  choices=['rows', 'columns'],
                                  help='Interlace mode: rows or columns (default: rows)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'composite':
            composite(args.image1, args.image2, args.output, args.mode)
            print(f"✓ Composite created successfully: {args.output}")
        elif args.command == 'interlace':
            interlace(args.image1, args.image2, args.output, args.mode)
            print(f"✓ Interlaced image created successfully: {args.output}")
    except FileNotFoundError as e:
        print(f"✗ Error: File not found - {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
