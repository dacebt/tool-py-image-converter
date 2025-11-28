#!/usr/bin/env python3
"""
Main entry point for PNG to WebP batch converter GUI tool.
"""

import tkinter as tk
from pathlib import Path

from PIL import Image

from ui.app import ConverterApp

# Named constant for WebP quality setting (no magic numbers per code rules)
WEBP_QUALITY = 85


def find_png_files(source_dir: Path) -> list[Path]:
    """
    Recursively find all PNG files in the source directory.

    Args:
        source_dir: Root directory to search for PNG files

    Returns:
        List of Path objects for all PNG files found
    """
    png_files: list[Path] = []
    if not source_dir.exists() or not source_dir.is_dir():
        return png_files

    # Recursively search for .png files (case-insensitive)
    for file_path in source_dir.rglob("*.png"):
        if file_path.is_file():
            png_files.append(file_path)

    # Also check for uppercase .PNG
    for file_path in source_dir.rglob("*.PNG"):
        if file_path.is_file() and file_path not in png_files:
            png_files.append(file_path)

    return sorted(png_files)


def transform_path(source_path: Path, source_root: Path, dest_root: Path) -> Path:
    """
    Transform a source file path to its destination path, preserving directory structure.

    Transforms: /src/a/b/image.png → /dest/a/b/image.webp
    Preserves the relative path structure from source_root to dest_root.

    Args:
        source_path: Full path to the source PNG file
        source_root: Root source directory
        dest_root: Root destination directory

    Returns:
        Path object for the destination WebP file
    """
    # Resolve paths to absolute to handle relative paths and symlinks
    source_path = source_path.resolve()
    source_root = source_root.resolve()
    dest_root = dest_root.resolve()

    # Get the relative path from source_root to source_path
    # This preserves the directory structure (e.g., "a/b/image.png")
    try:
        relative_path = source_path.relative_to(source_root)
    except ValueError:
        # If source_path is not under source_root, use just the filename
        relative_path = source_path.name

    # Change extension from .png/.PNG to .webp
    # Handle both lowercase and uppercase extensions
    stem = relative_path.stem
    dest_relative = Path(stem).with_suffix(".webp")

    # If there was a parent directory structure, preserve it
    if relative_path.parent != Path("."):
        dest_relative = relative_path.parent / dest_relative

    # Combine with destination root
    dest_path = dest_root / dest_relative

    return dest_path


def convert_png_to_webp(source: Path, dest: Path) -> bool:
    """
    Convert a PNG file to WebP format.

    Creates destination directories as needed. Handles errors gracefully
    per-file so one failure doesn't stop the batch.

    Args:
        source: Path to source PNG file
        dest: Path to destination WebP file

    Returns:
        True if conversion succeeded, False otherwise
    """
    try:
        # Verify source file exists
        if not source.exists() or not source.is_file():
            return False

        # Create destination directory structure if needed
        # This preserves the folder structure: /src/a/b/image.png → /dest/a/b/image.webp
        dest.parent.mkdir(parents=True, exist_ok=True)

        # Open and convert the image
        with Image.open(source) as img:
            # Convert RGBA to RGB if necessary (WebP supports both)
            # Save with specified quality setting
            img.save(dest, "WEBP", quality=WEBP_QUALITY)

        return True
    except Exception:  # pylint: disable=broad-exception-caught
        # Error handling: return False on any exception
        # This allows per-file error handling without stopping the batch
        return False


def main() -> None:
    """Main entry point for the application."""
    root = tk.Tk()

    # Set application icon
    try:
        icon_path = Path(__file__).parent / "assets" / "logo_favicon.png"
        if icon_path.exists():
            # Use iconphoto for better cross-platform support
            icon_image = tk.PhotoImage(file=str(icon_path))
            root.iconphoto(True, icon_image)
    except Exception:  # pylint: disable=broad-exception-caught
        # Icon loading failed, continue without icon
        pass

    # Create app instance with conversion functions
    # Store reference to prevent garbage collection
    _ = ConverterApp(
        root,
        find_png_files_func=find_png_files,
        transform_path_func=transform_path,
        convert_png_to_webp_func=convert_png_to_webp
    )
    root.mainloop()


if __name__ == "__main__":
    main()
