"""
Main application window for PNG to WebP batch converter.
"""

import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from ui.conversion_utils import run_conversion_worker
from ui.theme import Theme
from ui.widgets import StyledButton, StyledEntry, StyledLabel, StyledText


class ConverterApp:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Main application window for PNG to WebP batch converter."""

    def __init__(
        self,
        root: tk.Tk,
        find_png_files_func,
        transform_path_func,
        convert_png_to_webp_func
    ) -> None:
        """
        Initialize the GUI application.

        Args:
            root: Root tkinter window
            find_png_files_func: Function to find PNG files (from main module)
            transform_path_func: Function to transform paths (from main module)
            convert_png_to_webp_func: Function to convert PNG to WebP (from main module)
        """
        self.root = root
        self.root.title("PNG to WebP Converter")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.configure(bg=Theme.BACKGROUND)

        # Store conversion functions
        self.find_png_files = find_png_files_func
        self.transform_path = transform_path_func
        self.convert_png_to_webp = convert_png_to_webp_func

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
        source_frame = tk.Frame(self.root, padx=10, pady=5, bg=Theme.BACKGROUND)
        source_frame.pack(fill=tk.X)

        StyledLabel(source_frame, text="Source Folder:").pack(anchor=tk.W)
        source_entry_frame = tk.Frame(source_frame, bg=Theme.BACKGROUND)
        source_entry_frame.pack(fill=tk.X, pady=(5, 0))

        self.source_entry = StyledEntry(source_entry_frame)
        self.source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.source_entry.bind("<KeyRelease>", self._on_source_change)

        StyledButton(
            source_entry_frame,
            button_type="SECONDARY",
            text="Browse",
            command=self._browse_source
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Destination folder selection
        dest_frame = tk.Frame(self.root, padx=10, pady=5, bg=Theme.BACKGROUND)
        dest_frame.pack(fill=tk.X)

        StyledLabel(dest_frame, text="Destination Folder:").pack(anchor=tk.W)
        dest_entry_frame = tk.Frame(dest_frame, bg=Theme.BACKGROUND)
        dest_entry_frame.pack(fill=tk.X, pady=(5, 0))

        self.dest_entry = StyledEntry(dest_entry_frame)
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.dest_entry.bind("<KeyRelease>", self._on_dest_change)

        StyledButton(
            dest_entry_frame,
            button_type="SECONDARY",
            text="Browse",
            command=self._browse_dest
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Convert button
        button_frame = tk.Frame(self.root, padx=10, pady=10, bg=Theme.BACKGROUND)
        button_frame.pack(fill=tk.X)

        self.convert_button = StyledButton(
            button_frame,
            button_type="PRIMARY",
            text="Convert",
            command=self._on_convert_click,
            state=tk.DISABLED
        )
        self.convert_button.pack()

        # Status/log area
        log_frame = tk.Frame(self.root, padx=10, pady=5, bg=Theme.BACKGROUND)
        log_frame.pack(fill=tk.BOTH, expand=True)

        StyledLabel(log_frame, text="Status:").pack(anchor=tk.W)
        self.status_text = StyledText(
            log_frame,
            height=15,
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
        try:
            path_obj = Path(text) if text else None
            if path_obj and path_obj.exists() and path_obj.is_dir():
                self.source_dir = path_obj
            else:
                self.source_dir = None
            if not self.source_dir:
                self.png_files = []
            self._discover_png_files()
        except Exception:  # pylint: disable=broad-exception-caught
            self.source_dir = None
            self.png_files = []
        finally:
            self._update_convert_button_state()

    def _on_dest_change(self, event: tk.Event) -> None:  # pylint: disable=unused-argument
        """Handle destination entry field changes."""
        text = self.dest_entry.get().strip()
        try:
            self.dest_dir = Path(text) if text else None
        except Exception:  # pylint: disable=broad-exception-caught
            self.dest_dir = None
        finally:
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
        messages_processed = 0
        try:
            while True:
                try:
                    message = self.message_queue.get_nowait()
                    messages_processed += 1
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
                        msg = (
                            f"[GUI] Queue processing: Conversion complete message "
                            f"received - {success_count} succeeded, {error_count} failed"
                        )
                        print(msg)
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
                        print("[GUI] Conversion state reset, thread reference cleared")
                except queue.Empty:
                    break
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Handle any errors in queue processing
            print(f"[GUI] Error processing queue: {str(e)}")
            self._log_status_direct(f"Error processing queue: {str(e)}")

        if messages_processed > 0:
            print(f"[GUI] Processed {messages_processed} message(s) from queue")

        # Schedule next check (runs every 100ms)
        self.root.after(100, self._process_queue)

    def _discover_png_files(self) -> None:
        """Discover PNG files in the source directory and update status."""
        if self.source_dir and self.source_dir.exists() and self.source_dir.is_dir():
            self.png_files = self.find_png_files(self.source_dir)
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
            print("[GUI] Conversion already in progress, ignoring click")
            return

        # Disable convert button and update state
        self.is_converting = True
        self.convert_button.config(state=tk.DISABLED, text="Starting...")
        # Called from main thread, so use direct logging
        self._log_status_direct(
            f"Starting conversion of {len(self.png_files)} file(s)..."
        )
        file_count = len(self.png_files)
        print(f"[GUI] Convert button clicked - Starting conversion of {file_count} file(s)")

        # Start conversion in background thread
        print("[GUI] Creating conversion thread...")
        self.conversion_thread = threading.Thread(
            target=run_conversion_worker,
            daemon=True,
            args=(
                self.source_dir,
                self.dest_dir,
                self.png_files,
                self.transform_path,
                self.convert_png_to_webp,
                self._update_button_progress,
                self._log_status,
                self._conversion_complete,
            ),
        )
        print(f"[GUI] Thread object created: {self.conversion_thread}")
        print(f"[GUI] Thread is_alive before start: {self.conversion_thread.is_alive()}")
        self.conversion_thread.start()
        thread_alive = self.conversion_thread.is_alive()
        print(f"[GUI] Thread.start() called - is_alive: {thread_alive}")
        thread_info = (
            f"[GUI] Thread name: {self.conversion_thread.name}, "
            f"ID: {self.conversion_thread.ident}"
        )
        print(thread_info)
