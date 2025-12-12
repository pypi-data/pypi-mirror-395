#!/usr/bin/env python3
"""
Favicon generation tools.

This module provides functionality to convert images to favicon (.ico) format
with multiple sizes for web compatibility.
"""

from pathlib import Path
from typing import Optional, List, Tuple

from super_pocket.settings import click
from rich.console import Console

try:
    from PIL import Image
except ImportError:
    Console().print(
        "[red]Error:[/red] Pillow is not installed. "
        "Install it with: pip install Pillow",
        style="bold"
    )
    raise


console = Console()

# Standard favicon sizes
DEFAULT_FAVICON_SIZES: List[Tuple[int, int]] = [
    (256, 256),
    (128, 128),
    (64, 64),
    (48, 48),
    (32, 32),
    (16, 16)
]


def convert_to_favicon(
    input_file: str,
    output_file: str = 'favicon.ico',
    sizes: Optional[List[Tuple[int, int]]] = DEFAULT_FAVICON_SIZES
) -> None:
    """
    Convert an image to a favicon (.ico) file with multiple sizes.

    Args:
        input_file: Path to the input image file.
        output_file: Path to the output .ico file.
        sizes: List of (width, height) tuples for icon sizes.
               Defaults to standard favicon sizes.

    Raises:
        FileNotFoundError: If input file doesn't exist.
        ImportError: If PIL/Pillow is not installed.
        ValueError: If output file doesn't have .ico extension.
    """

    input_file = Path(input_file)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if not output_file.endswith('.ico'):
        output_file = output_file.split('.')[0] + '.ico'

    # Open and convert image
    img = Image.open(input_file)
    for i in range(len(sizes)-1):
        img.save(f"{i}_{output_file}", format="ICO", sizes=sizes[i])

    console.print(
        f"[green]✓[/green] Favicon saved to '{output_file}' with {len(sizes)} sizes",
        style="bold"
    )


@click.command()
@click.argument(
    'input_file',
    type=str
)
@click.option(
    '-o', '--output',
    type=str,
    default='favicon.ico',
    help='Output favicon file path. Default: favicon.ico'
)
@click.option(
    '-s', '--sizes',
    type=List[Tuple[int, int]],
    default=DEFAULT_FAVICON_SIZES,
    help='Custom sizes as comma-separated WxH values (e.g., "64x64,32x32,16x16"). '
)
def favicon(
    input_file: str,
    output: str,
    sizes: List[Tuple[int, int]]
) -> None:
    """
    Convert an image to a favicon (.ico) file.

    This command-line tool generates a multi-size .ico favicon file from any
    image format (PNG, JPG, etc.). The favicon includes multiple sizes for
    optimal compatibility across different devices and browsers. Default sizes
    include 256x256, 128x128, 64x64, 48x48, 32x32, and 16x16 pixels.

    Args:
        input_file: Path to the input image file (PNG, JPG, etc.).
        output: Optional output .ico file path (default: favicon.ico in current directory).
        sizes: Custom sizes as comma-separated WxH values (e.g., "64x64,32x32,16x16").

    Raises:
        click.Abort: If the conversion fails or required libraries are missing.

    Examples:
        pocket web favicon logo.png
        pocket web favicon logo.png -o custom-favicon.ico
        pocket web favicon logo.png --sizes "64x64,32x32,16x16"
        favicon logo.png -o favicon.ico
    """
    if isinstance(sizes, str):
        sizes = [tuple(map(int, size.split('x'))) for size in sizes.split(',')]
    convert_to_favicon(input_file, output, sizes)

def main():
    """Main entry point for standalone script."""
    favicon()

if __name__ == '__main__':
    main()