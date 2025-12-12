import os
import sys
import time
import threading
import logging
import json
import atexit
from datetime import datetime
from collections import deque
from pathlib import Path

from . import config
from .template import HTML_TEMPLATE


def get_local_timestamp():
    x = datetime.now()
    return "%04d-%02d-%02d %02d:%02d:%02d.%03d" % (x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond / 1000)


class LogWriter:
    # Pre-compiled constants (class-level for all instances)
    HTML_ESCAPE_TABLE = str.maketrans({
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;'
    })

    # Pre-compiled replacement pairs (order matters: \r\n before \n)
    REPLACEMENTS = (
        ('\r\n', '<br>'),
        ('\n', '<br>'),
        ('=>', '&rArr;')
    )

    def __init__(self):
        os.makedirs(config.log_dir, exist_ok=True)
        self.trace_file = None
        self.__last_color = None
        self.last_flush = 0
        self.trace_lock = threading.RLock()  # Use RLock for better reliability
        self.current_size = 0
        self.write_buffer = deque(maxlen=1000)  # Buffer for high-volume logging
        self.buffer_size = 0
        self.max_buffer_size = 64 * 1024  # 64KB buffer
        self.retry_count = 3
        self.logger = logging.getLogger(__name__)

        # Multi-process coordination
        self.process_id = os.getpid()
        self._process_registered = False

        # Immediate flush mode for continuous applications (from config)
        self.immediate_flush = config.immediate_flush

        # Periodic flush daemon thread
        self._flush_daemon = None
        self._stop_daemon = threading.Event()

        self._remove_existing_footer()

        # Register process AFTER directory exists
        self._register_process()

        # Start periodic flush daemon
        self._start_flush_daemon()

        # Register cleanup on exit
        atexit.register(self._cleanup_on_exit)

    def _get_filename(self):
        return os.path.join(config.log_dir, config.main_filename)

    def _start_flush_daemon(self):
        """Start a daemon thread that periodically flushes the buffer"""
        if self._flush_daemon is None or not self._flush_daemon.is_alive():
            self._stop_daemon.clear()
            self._flush_daemon = threading.Thread(
                target=self._periodic_flush_worker,
                daemon=True,
                name="LogWriter-FlushDaemon"
            )
            self._flush_daemon.start()

    def _periodic_flush_worker(self):
        """Worker thread that flushes buffer every 500ms as backup"""
        while not self._stop_daemon.is_set():
            try:
                # Wait 500ms or until stop signal
                if self._stop_daemon.wait(timeout=0.5):
                    break

                # Flush if there's content in buffer
                with self.trace_lock:
                    if self.write_buffer:
                        self._flush_buffer()
            except Exception as e:
                self.logger.error(f"Error in periodic flush daemon: {e}")

    def _get_lock_filename(self):
        """Get the lock file path for multi-process coordination"""
        base_name = Path(config.main_filename).stem
        return os.path.join(config.log_dir, f".{base_name}.lock")

    def _register_process(self):
        """Register this process as active user of the log file"""
        if self._process_registered:
            return

        lock_file = self._get_lock_filename()

        try:
            # Read existing processes
            processes = {}
            if os.path.exists(lock_file):
                try:
                    with open(lock_file, 'r') as f:
                        processes = json.load(f)
                except (json.JSONDecodeError, IOError):
                    processes = {}

            # Add current process
            processes[str(self.process_id)] = {
                'pid': self.process_id,
                'started': time.time()
            }

            # Write back atomically
            temp_file = lock_file + '.tmp'
            with open(temp_file, 'w') as f:
                json.dump(processes, f)

            # Atomic rename (works on Windows and Unix)
            try:
                os.replace(temp_file, lock_file)
            except OSError:
                # Fallback for some file systems
                if os.path.exists(lock_file):
                    os.remove(lock_file)
                os.rename(temp_file, lock_file)

            self._process_registered = True

        except Exception as e:
            self.logger.warning(f"Could not register process in lock file: {e}")

    def _cleanup_on_exit(self):
        """Cleanup on process exit (called by atexit)"""
        try:
            self._unregister_process()
        except:
            pass

    def _unregister_process(self):
        """Unregister this process and check if we're the last one"""
        if not self._process_registered:
            return False

        lock_file = self._get_lock_filename()

        try:
            if not os.path.exists(lock_file):
                self._process_registered = False
                return True

            # Read existing processes
            processes = {}
            try:
                with open(lock_file, 'r') as f:
                    processes = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._process_registered = False
                return True

            # Remove current process
            processes.pop(str(self.process_id), None)

            # Clean up stale processes (more than 1 hour old or not running)
            current_time = time.time()
            stale_pids = []
            for pid_str, info in list(processes.items()):
                pid = info.get('pid')
                started = info.get('started', 0)

                # Check if process is stale (1 hour timeout or process not running)
                if current_time - started > 3600 or not self._is_process_running(pid):
                    stale_pids.append(pid_str)

            for pid_str in stale_pids:
                processes.pop(pid_str, None)

            # Write back
            if processes:
                # Other processes still active
                temp_file = lock_file + '.tmp'
                with open(temp_file, 'w') as f:
                    json.dump(processes, f)
                try:
                    os.replace(temp_file, lock_file)
                except OSError:
                    if os.path.exists(lock_file):
                        os.remove(lock_file)
                    os.rename(temp_file, lock_file)
            else:
                # Last process - remove lock file
                try:
                    os.remove(lock_file)
                except OSError:
                    pass

            self._process_registered = False
            return len(processes) == 0  # True if we're the last process

        except Exception as e:
            self.logger.warning(f"Could not unregister process from lock file: {e}")
            self._process_registered = False
            return False

    def _is_process_running(self, pid):
        """Check if a process is running (cross-platform)"""
        if pid is None:
            return False

        try:
            if sys.platform == 'win32':
                import ctypes
                kernel32 = ctypes.windll.kernel32
                PROCESS_QUERY_INFORMATION = 0x0400
                handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid)
                if handle:
                    kernel32.CloseHandle(handle)
                    return True
                return False
            else:
                # Unix-like systems
                os.kill(pid, 0)
                return True
        except (OSError, AttributeError):
            return False

    def _is_last_process(self):
        """Check if this is the last active process using the log file"""
        lock_file = self._get_lock_filename()

        try:
            if not os.path.exists(lock_file):
                return True  # No lock file means we're alone

            with open(lock_file, 'r') as f:
                processes = json.load(f)

            # Count active processes (excluding stale ones)
            current_time = time.time()
            active_count = 0

            for pid_str, info in processes.items():
                pid = info.get('pid')
                started = info.get('started', 0)

                # Skip stale processes
                if current_time - started > 3600:
                    continue

                # Check if process is running
                if pid == self.process_id or self._is_process_running(pid):
                    active_count += 1

            return active_count <= 1  # Only us or nobody

        except (json.JSONDecodeError, IOError, FileNotFoundError):
            return True  # If we can't read, assume we're alone

    def _remove_existing_footer(self):
        """Remove footer from existing file to allow appending new content"""
        filename = self._get_filename()
        if os.path.exists(filename):
            try:
                with open(filename, 'r+', encoding='utf-8') as f:
                    content = f.read()
                    footer = "<!-- CONTAINER_END -->\n</div>\n</body>\n</html>"
                    if content.endswith(footer):
                        new_content = content[:-len(footer)]
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
            except Exception:
                pass

    def _write_footer(self):
        """Write HTML footer to make file viewable while application runs"""
        try:
            if self.trace_file and not self.trace_file.closed:
                # Save current position
                current_pos = self.trace_file.tell()

                # Write footer
                self.trace_file.write("<!-- CONTAINER_END -->\n</div>\n</body>\n</html>")
                self.trace_file.flush()

                # Move back to continue writing (footer will be overwritten)
                self.trace_file.seek(current_pos)
        except Exception as e:
            self.logger.warning(f"Failed to write temporary footer: {e}")

    def _ensure_valid_html(self):
        """Ensure HTML file is always valid by maintaining a footer"""
        try:
            filename = self._get_filename()
            if os.path.exists(filename):
                # Check if file ends with footer
                with open(filename, 'rb') as f:
                    f.seek(max(0, os.path.getsize(filename) - 100))
                    tail = f.read().decode('utf-8', errors='ignore')

                    if not tail.endswith("</html>"):
                        # Append footer if missing
                        with open(filename, 'a', encoding='utf-8') as f:
                            f.write("\n<!-- CONTAINER_END -->\n</div>\n</body>\n</html>")
        except Exception as e:
            self.logger.warning(f"Failed to ensure valid HTML: {e}")

    def _load_template(self):
        """Load HTML template from Python module"""
        return HTML_TEMPLATE

    def _remove_extra_files(self, pattern, limit):
        import glob
        try:
            files = glob.glob(pattern)
            if len(files) > limit:
                files.sort()
                for f in files[:-limit]:
                    os.remove(f)
        except Exception:
            pass

    def _handle_new_log_file(self, file_name, file_pattern, fd):
        target = file_pattern % (fd)
        limit_count = config.log_files_limit_count

        target += ".tmp"
        limit_count -= 1

        try:
            os.rename(file_name, target)
        except OSError:
            pass

        self._remove_extra_files(file_pattern % "*", limit_count)

        # Cross-platform file operations
        import platform
        import subprocess
        import glob
        
        try:
            # Compress the target file if gzip is available
            if platform.system() != 'Windows':
                subprocess.run(['gzip', '-c', target], 
                             stdout=open(target[:-4], 'wb'), 
                             stderr=subprocess.DEVNULL,
                             check=False)
            
            # Remove temporary files cross-platform
            os.remove(target) if os.path.exists(target) else None
            
            # Clean up temporary files
            for temp_file in glob.glob("trace_*.dat.tmp") + glob.glob("ErrorLog_*.txt.gz.tmp"):
                try:
                    os.remove(temp_file)
                except OSError:
                    pass
                    
        except (subprocess.SubprocessError, OSError):
            # If compression fails, just remove the original file
            try:
                os.remove(target) if os.path.exists(target) else None
            except OSError:
                pass

    def _safe_file_operation(self, operation, *args, **kwargs):
        """Execute file operation with retry mechanism"""
        for attempt in range(self.retry_count):
            try:
                return operation(*args, **kwargs)
            except (BrokenPipeError, OSError) as e:
                if attempt == self.retry_count - 1:
                    self.logger.error(f"File operation failed after {self.retry_count} attempts: {e}")
                    raise
                time.sleep(0.1 * (attempt + 1))  # Exponential backoff
            except Exception as e:
                self.logger.error(f"Unexpected error in file operation: {e}")
                raise

    def _ensure_file_handle(self):
        """Ensure file handle is valid and open"""
        filename = self._get_filename()

        if not self.trace_file or self.trace_file.closed:
            try:
                if os.path.exists(filename):
                    self.trace_file = open(filename, 'a', encoding='utf-8', buffering=8192)
                else:
                    self.trace_file = open(filename, 'w', encoding='utf-8', buffering=8192)
                    self.trace_file.write(self._load_template())
            except (OSError, IOError) as e:
                self.logger.error(f"Failed to open log file {filename}: {e}")
                raise

    def _write_to_buffer(self, formated_msg):
        """Add message to buffer for batch writing"""
        self.write_buffer.append(formated_msg)
        self.buffer_size += len(formated_msg)

        # Flush buffer if it's getting too large
        if self.buffer_size >= self.max_buffer_size:
            self._flush_buffer()

    def _flush_buffer(self):
        """Flush buffered messages to file with footer management for continuous apps"""
        if not self.write_buffer:
            return

        try:
            # Close and reopen in r+ mode to allow reading and writing
            filename = self._get_filename()
            buffer_content = ''.join(self.write_buffer)
            footer = "<!-- CONTAINER_END -->\n</div>\n</body>\n</html>"

            # If file is currently open in append mode, close it
            if self.trace_file and not self.trace_file.closed:
                self.trace_file.flush()
                self.trace_file.close()

            def write_operation():
                # Open in r+ mode to allow both reading and writing
                if os.path.exists(filename):
                    with open(filename, 'r+b') as f:
                        # Go to end to check for footer
                        f.seek(0, 2)
                        file_size = f.tell()
                        footer_bytes = footer.encode('utf-8')
                        footer_size = len(footer_bytes)

                        # Check if footer exists by reading last bytes
                        if file_size >= footer_size:
                            f.seek(file_size - footer_size)
                            end_bytes = f.read()

                            # If footer exists, truncate it before writing
                            if end_bytes == footer_bytes:
                                f.seek(file_size - footer_size)
                                f.truncate()
                            else:
                                # Position at end
                                f.seek(0, 2)

                        # Write new content and footer
                        f.write(buffer_content.encode('utf-8'))
                        f.write(footer_bytes)
                        f.flush()
                else:
                    # First write - create file with template
                    with open(filename, 'wb') as f:
                        f.write(self._load_template().encode('utf-8'))
                        f.write(buffer_content.encode('utf-8'))
                        f.write(footer.encode('utf-8'))
                        f.flush()

            self._safe_file_operation(write_operation)

            # Reopen file in append mode for next writes
            self.trace_file = None  # Will be reopened on next write

            # Update size tracking (excluding footer size)
            self.current_size += self.buffer_size

            # Clear buffer
            self.write_buffer.clear()
            self.buffer_size = 0

            # Check if we need to rotate the file
            if self.current_size >= config.log_files_limit_size:
                self._rotate_file()

        except Exception as e:
            self.logger.error(f"Failed to flush buffer: {e}")
            # Clear buffer even on error to prevent memory issues
            self.write_buffer.clear()
            self.buffer_size = 0
            # Ensure file handle is reset
            self.trace_file = None

    def write_direct(self, msg, color, tag):
        """Write log message with immediate flush for continuous applications"""
        try:
            # Sanitize input (done outside lock for better concurrency)
            if not isinstance(msg, str):
                msg = str(msg)
            if not isinstance(color, str):
                color = str(color) if color else 'white'
            if not isinstance(tag, str):
                tag = str(tag) if tag else 'log'

            # Escape HTML characters using pre-compiled table
            msg = msg.translate(self.HTML_ESCAPE_TABLE)

            # Apply replacements using pre-compiled tuples
            for old, new in self.REPLACEMENTS:
                msg = msg.replace(old, new)

            # Generate timestamp (optimized format)
            x = datetime.now()
            date_str = "%04d-%02d-%02d %02d:%02d:%02d.%03d" % (
                x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond // 1000
            )

            # Build formatted message
            formated_msg = f'<font color="{color}" tag="{tag}">{date_str} - {msg}</font>\n'

            # Minimal critical section with lock
            with self.trace_lock:
                self._write_to_buffer(formated_msg)

                # IMMEDIATE FLUSH: Always flush after write for continuous applications
                # This ensures all messages are immediately visible in the log file
                if self.immediate_flush:
                    self._flush_buffer()
                    self.last_flush = time.monotonic()
                else:
                    # Legacy behavior: flush based on time or buffer size
                    current_time = time.monotonic()
                    should_flush = (current_time - self.last_flush) > 1.0 or self.buffer_size >= self.max_buffer_size

                    if should_flush:
                        self._flush_buffer()
                        self.last_flush = current_time

        except Exception as e:
            # Log the error but don't raise to prevent breaking the application
            self.logger.error(f"Error in write_direct: {e}")
            try:
                # Emergency fallback - try to write to stderr
                sys.stderr.write(f"LogHTML Error: {e}\n")
                sys.stderr.flush()
            except:
                pass  # Last resort - silent fail

    def _rotate_file(self):
        """Rotate the log file if it exceeds the size limit"""
        try:
            # Flush any remaining buffer first
            self._flush_buffer()

            if self.trace_file and not self.trace_file.closed:
                def rotation_operation():
                    self.trace_file.write("<!-- CONTAINER_END -->\n</div>\n</body>\n</html>")
                    self.trace_file.flush()
                    self.trace_file.close()

                self._safe_file_operation(rotation_operation)
                self.trace_file = None

            # Create a backup of the current file
            import glob
            from datetime import datetime

            filename = self._get_filename()
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_name = os.path.join(config.log_dir, f"{timestamp}_{config.main_filename}")

            try:
                if os.path.exists(filename):
                    os.rename(filename, backup_name)
            except OSError as e:
                self.logger.warning(f"Failed to rotate log file: {e}")

            # Remove old files if exceeding the limit
            try:
                pattern = os.path.join(config.log_dir, f"*_{config.main_filename}")
                files = glob.glob(pattern)
                if len(files) > config.log_files_limit_count:
                    files.sort()
                    for f in files[:-config.log_files_limit_count]:
                        try:
                            os.remove(f)
                        except OSError as e:
                            self.logger.warning(f"Failed to remove old log file {f}: {e}")
            except Exception as e:
                self.logger.warning(f"Failed to clean up old log files: {e}")

            self.current_size = 0

        except Exception as e:
            self.logger.error(f"Error during file rotation: {e}")
            # Reset file handle on rotation error
            self.trace_file = None
            self.current_size = 0

    def close(self):
        """Close the log file with proper cleanup"""
        # Stop the flush daemon first
        try:
            self._stop_daemon.set()
            if self._flush_daemon and self._flush_daemon.is_alive():
                self._flush_daemon.join(timeout=2.0)
        except Exception as e:
            self.logger.warning(f"Error stopping flush daemon: {e}")

        with self.trace_lock:
            try:
                # Flush any remaining buffered content
                self._flush_buffer()

                # Check if we're the last process before writing footer
                is_last = self._is_last_process()

                if self.trace_file and not self.trace_file.closed:
                    def close_operation():
                        # Footer is already written by _flush_buffer, just close
                        self.trace_file.flush()
                        self.trace_file.close()

                    self._safe_file_operation(close_operation)
                    self.trace_file = None

                # Unregister this process from lock file
                self._unregister_process()

            except Exception as e:
                self.logger.error(f"Error closing log file: {e}")
                # Force close file handle if it exists
                if self.trace_file:
                    try:
                        self.trace_file.close()
                    except:
                        pass
                    self.trace_file = None

                # Try to unregister even on error
                try:
                    self._unregister_process()
                except:
                    pass
