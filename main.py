#!/usr/bin/env python3
"""
Main entry point for PNG to WebP batch converter GUI tool.
"""

import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, scrolledtext

from PIL import Image

# Named constant for WebP quality setting (no magic numbers per code rules)
WEBP_QUALITY = 85


class ConverterApp:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Main application window for PNG to WebP batch converter."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the GUI application."""
        self.root = root
        self.root.title("PNG to WebP Converter")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # State variables
        self.source_dir: Path | None = None
        self.dest_dir: Path | None = None
        self.png_files: list[Path] = []

        # Threading support - queue for thread-safe GUI updates
        self.message_queue: queue.Queue = queue.Queue()
        self.conversion_thread: threading.Thread | None = None
        self.is_converting = False

        self._create_widgets()
        self._update_convert_button_state()

        # Start processing messages from worker thread
        self._process_queue()

    def _create_widgets(self) -> None:
        """Create and layout all GUI widgets."""
        # Source folder selection
        source_frame = tk.Frame(self.root, padx=10, pady=5)
        source_frame.pack(fill=tk.X)

        tk.Label(source_frame, text="Source Folder:").pack(anchor=tk.W)
        source_entry_frame = tk.Frame(source_frame)
        source_entry_frame.pack(fill=tk.X, pady=(5, 0))

        self.source_entry = tk.Entry(source_entry_frame)
        self.source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.source_entry.bind("<KeyRelease>", self._on_source_change)

        tk.Button(
            source_entry_frame,
            text="Browse",
            command=self._browse_source
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Destination folder selection
        dest_frame = tk.Frame(self.root, padx=10, pady=5)
        dest_frame.pack(fill=tk.X)

        tk.Label(dest_frame, text="Destination Folder:").pack(anchor=tk.W)
        dest_entry_frame = tk.Frame(dest_frame)
        dest_entry_frame.pack(fill=tk.X, pady=(5, 0))

        self.dest_entry = tk.Entry(dest_entry_frame)
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.dest_entry.bind("<KeyRelease>", self._on_dest_change)

        tk.Button(
            dest_entry_frame,
            text="Browse",
            command=self._browse_dest
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Convert button
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack(fill=tk.X)

        self.convert_button = tk.Button(
            button_frame,
            text="Convert",
            command=self._on_convert_click,
            state=tk.DISABLED
        )
        self.convert_button.pack()

        # Status/log area
        log_frame = tk.Frame(self.root, padx=10, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(log_frame, text="Status:").pack(anchor=tk.W)
        self.status_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    def _browse_source(self) -> None:
        """Open folder dialog for source directory selection."""
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_dir = Path(folder)
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, str(self.source_dir))
            self._discover_png_files()
            self._update_convert_button_state()
            self._log_status(f"Source folder selected: {self.source_dir}")

    def _browse_dest(self) -> None:
        """Open folder dialog for destination directory selection."""
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.dest_dir = Path(folder)
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, str(self.dest_dir))
            self._update_convert_button_state()
            self._log_status(f"Destination folder selected: {self.dest_dir}")

    def _on_source_change(self, event: tk.Event) -> None:  # pylint: disable=unused-argument
        """Handle source entry field changes."""
        text = self.source_entry.get().strip()
        if text:
            try:
                self.source_dir = Path(text)
                if self.source_dir.exists() and self.source_dir.is_dir():
                    self._discover_png_files()
                    self._update_convert_button_state()
                else:
                    self.source_dir = None
                    self.png_files = []
                    self._update_convert_button_state()
            except Exception:  # pylint: disable=broad-exception-caught
                self.source_dir = None
                self.png_files = []
                self._update_convert_button_state()
        else:
            self.source_dir = None
            self.png_files = []
            self._update_convert_button_state()

    def _on_dest_change(self, event: tk.Event) -> None:  # pylint: disable=unused-argument
        """Handle destination entry field changes."""
        text = self.dest_entry.get().strip()
        if text:
            try:
                self.dest_dir = Path(text)
                self._update_convert_button_state()
            except Exception:  # pylint: disable=broad-exception-caught
                self.dest_dir = None
                self._update_convert_button_state()
        else:
            self.dest_dir = None
            self._update_convert_button_state()

    def _update_convert_button_state(self) -> None:
        """Enable/disable convert button based on folder selection state."""
        if self.source_dir and self.dest_dir:
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.convert_button.config(state=tk.DISABLED)

    def _log_status(self, message: str) -> None:
        """
        Append message to status text area.

        Thread-safe: Can be called from any thread. Messages are queued
        and processed on the main thread via _process_queue().
        """
        self.message_queue.put(("log", message))

    def _log_status_direct(self, message: str) -> None:
        """Append message directly to status text area (main thread only)."""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def _update_button_progress(self, current: int, total: int) -> None:
        """
        Update convert button text to show progress.

        Thread-safe: Can be called from any thread. Updates are queued
        and processed on the main thread via _process_queue().
        """
        self.message_queue.put(("progress", current, total))

    def _conversion_complete(self, success_count: int, error_count: int) -> None:
        """
        Signal that conversion is complete.

        Thread-safe: Can be called from any thread. Completion is queued
        and processed on the main thread via _process_queue().
        """
        self.message_queue.put(("complete", success_count, error_count))

    def _process_queue(self) -> None:
        """
        Process messages from the worker thread queue.

        This method runs on the main thread and handles all GUI updates
        from the background conversion thread. tkinter isn't thread-safe,
        so all GUI operations must happen here.
        """
        try:
            while True:
                try:
                    message = self.message_queue.get_nowait()
                    msg_type = message[0]

                    if msg_type == "log":
                        # Log message from worker thread
                        self._log_status_direct(message[1])
                    elif msg_type == "progress":
                        # Update button with progress
                        current, total = message[1], message[2]
                        self.convert_button.config(
                            text=f"Converting... ({current}/{total})",
                            state=tk.DISABLED
                        )
                    elif msg_type == "complete":
                        # Conversion complete - restore button and show summary
                        success_count, error_count = message[1], message[2]
                        self.convert_button.config(
                            text="Convert",
                            state=tk.NORMAL
                        )
                        summary = (
                            f"\nConversion complete: {success_count} succeeded, "
                            f"{error_count} failed"
                        )
                        self._log_status_direct(summary)
                        self.is_converting = False
                        self.conversion_thread = None
                except queue.Empty:
                    break
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Handle any errors in queue processing
            self._log_status_direct(f"Error processing queue: {str(e)}")

        # Schedule next check (runs every 100ms)
        self.root.after(100, self._process_queue)

    def _discover_png_files(self) -> None:
        """Discover PNG files in the source directory and update status."""
        if self.source_dir and self.source_dir.exists() and self.source_dir.is_dir():
            self.png_files = find_png_files(self.source_dir)
            count = len(self.png_files)
            # Called from main thread, so use direct logging
            self._log_status_direct(f"Found {count} PNG file{'s' if count != 1 else ''}")
        else:
            self.png_files = []

    def _on_convert_click(self) -> None:
        """Handle convert button click - start conversion in background thread."""
        if not self.source_dir or not self.dest_dir or not self.png_files:
            # Called from main thread, so use direct logging
            self._log_status_direct(
                "Error: Source and destination folders must be selected"
            )
            return

        # Prevent multiple conversion threads
        if self.is_converting:
            return

        # Disable convert button and update state
        self.is_converting = True
        self.convert_button.config(state=tk.DISABLED, text="Starting...")
        # Called from main thread, so use direct logging
        self._log_status_direct(
            f"Starting conversion of {len(self.png_files)} file(s)..."
        )

        # Start conversion in background thread
        self.conversion_thread = threading.Thread(
            target=self._convert_worker,
            daemon=True,
            args=(self.source_dir, self.dest_dir, self.png_files)
        )
        self.conversion_thread.start()

    def _convert_worker(self, source_dir: Path, dest_dir: Path, png_files: list[Path]) -> None:
        """
        Worker thread function that performs the actual conversion.

        This runs in a background thread to prevent UI freezing.
        All GUI updates are sent via message queue to be processed
        on the main thread.

        Args:
            source_dir: Source directory root
            dest_dir: Destination directory root
            png_files: List of PNG files to convert
        """
        success_count = 0
        error_count = 0
        try:
            # Process each file individually - one failure doesn't stop the batch
            for i, source_file in enumerate(png_files, 1):
                try:
                    # Update progress on button
                    self._update_button_progress(i, len(png_files))

                    # Transform path to preserve directory structure
                    dest_file = transform_path(source_file, source_dir, dest_dir)

                    # Convert the file
                    if convert_png_to_webp(source_file, dest_file):
                        success_count += 1
                        self._log_status(f"[{i}/{len(png_files)}] ✓ {source_file.name}")
                    else:
                        error_count += 1
                        self._log_status(f"[{i}/{len(png_files)}] ✗ Failed: {source_file.name}")
                except Exception as e:  # pylint: disable=broad-exception-caught
                    # Handle errors per-file - one failure shouldn't stop the batch
                    error_count += 1
                    self._log_status(
                        f"[{i}/{len(png_files)}] ✗ Error: {source_file.name} - {str(e)}"
                    )
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Handle thread-level exceptions (don't let them crash silently)
            self._log_status(f"Fatal error in conversion thread: {str(e)}")
            error_count += len(png_files) - success_count - error_count
        finally:
            # Signal completion (will restore button state on main thread)
            self._conversion_complete(success_count, error_count)


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
    ConverterApp(root)  # Store reference to prevent garbage collection
    root.mainloop()


if __name__ == "__main__":
    main()
