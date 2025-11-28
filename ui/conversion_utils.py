"""
Conversion worker utilities for background thread processing.
"""

import threading
import time
from pathlib import Path
from typing import Callable


def run_conversion_worker(  # pylint: disable=too-many-arguments,too-many-locals
    source_dir: Path,
    dest_dir: Path,
    png_files: list[Path],
    transform_path_func: Callable[[Path, Path, Path], Path],
    convert_png_to_webp_func: Callable[[Path, Path], bool],
    update_progress: Callable[[int, int], None],
    log_status: Callable[[str], None],
    on_complete: Callable[[int, int], None],
) -> None:
    """
    Worker function that performs the actual conversion in a background thread.

    Args:
        source_dir: Source directory root
        dest_dir: Destination directory root
        png_files: List of PNG files to convert
        transform_path_func: Function to transform source paths to destination paths
        convert_png_to_webp_func: Function to convert PNG to WebP
        update_progress: Callback to update progress (current, total)
        log_status: Callback to log status messages
        on_complete: Callback when conversion is complete (success_count, error_count)
    """
    thread_start_time = time.time()
    file_count = len(png_files)
    print(f"[THREAD] Conversion thread started - Processing {file_count} file(s)")
    current_thread = threading.current_thread()
    print(f"[THREAD] Thread ID: {current_thread.ident}")
    print(f"[THREAD] Thread name: {current_thread.name}")

    success_count = 0
    error_count = 0
    try:
        # Process each file individually - one failure doesn't stop the batch
        for i, source_file in enumerate(png_files, 1):
            file_start_time = time.time()
            print(f"[THREAD] Processing file {i}/{file_count}: {source_file.name}")

            try:
                # Update progress on button
                progress_update_start = time.time()
                update_progress(i, len(png_files))
                progress_update_time = time.time() - progress_update_start
                if progress_update_time > 0.01:  # Log if it takes more than 10ms
                    print(f"[THREAD] Progress update took {progress_update_time:.3f}s")

                # Transform path to preserve directory structure
                dest_file = transform_path_func(source_file, source_dir, dest_dir)

                # Convert the file
                conversion_start = time.time()
                if convert_png_to_webp_func(source_file, dest_file):
                    conversion_time = time.time() - conversion_start
                    success_count += 1
                    file_time = time.time() - file_start_time
                    msg = (
                        f"[THREAD] ✓ Converted {source_file.name} in "
                        f"{conversion_time:.3f}s (total: {file_time:.3f}s)"
                    )
                    print(msg)
                    log_status(f"[{i}/{file_count}] ✓ {source_file.name}")
                else:
                    conversion_time = time.time() - conversion_start
                    error_count += 1
                    file_time = time.time() - file_start_time
                    print(f"[THREAD] ✗ Failed to convert {source_file.name} (took {conversion_time:.3f}s)")
                    log_status(f"[{i}/{file_count}] ✗ Failed: {source_file.name}")
            except Exception as e:  # pylint: disable=broad-exception-caught
                # Handle errors per-file - one failure shouldn't stop the batch
                error_count += 1
                file_time = time.time() - file_start_time
                err_msg = (
                    f"[THREAD] ✗ Error processing {source_file.name}: "
                    f"{str(e)} (took {file_time:.3f}s)"
                )
                print(err_msg)
                log_status(f"[{i}/{file_count}] ✗ Error: {source_file.name} - {str(e)}")
    except Exception as e:  # pylint: disable=broad-exception-caught
        # Handle thread-level exceptions (don't let them crash silently)
        thread_time = time.time() - thread_start_time
        print(f"[THREAD] Fatal error in conversion thread after {thread_time:.3f}s: {str(e)}")
        log_status(f"Fatal error in conversion thread: {str(e)}")
        error_count += len(png_files) - success_count - error_count
    finally:
        # Signal completion (will restore button state on main thread)
        total_time = time.time() - thread_start_time
        finish_msg = (
            f"[THREAD] Conversion thread finished - {success_count} succeeded, "
            f"{error_count} failed (total time: {total_time:.3f}s)"
        )
        print(finish_msg)
        if png_files:
            avg_time = total_time / file_count
            print(f"[THREAD] Average time per file: {avg_time:.3f}s")
        else:
            print("[THREAD] No files processed")
        on_complete(success_count, error_count)
