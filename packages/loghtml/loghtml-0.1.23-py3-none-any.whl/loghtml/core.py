import threading
import traceback
import time
import os
from datetime import datetime

from .writer import LogWriter


class Logger:
    def __init__(self):
        self.writer = LogWriter()
        self.html_trace = True
        self.screen_trace = True
        self.default_tag_color = {}

        # Cache for file system checks with TTL
        self._debug_enabled_cache = (False, 0.0)
        self._log_disabled_cache = (False, 0.0)
        self._cache_ttl = 2.0  # 2 second TTL

        # Pre-compile file check lists
        self._debug_files = ("DebugEnable", "debug_enable", "enable_debug", "EnableDebug")
        self._disable_files = ("DisableLog", "disable_log", "log_disable", "LogDisable")

    def set_html_trace(self, value):
        self.html_trace = value
        if not self.html_trace:
            import glob
            # Cross-platform file deletion
            for trace_file in glob.glob("trace*"):
                try:
                    os.remove(trace_file)
                except OSError:
                    pass

    def set_default_tag_color(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError('Invalid Type used to set default tag color.')
        self.default_tag_color = value

    def set_screen_trace(self, value):
        self.screen_trace = value

    def _write_message(self, msg, color, tag):
        if self.screen_trace:
            print(str(msg))

        if self._disable_log():
            return

        if not (_color := self.default_tag_color.get(tag, color)):
            _color = 'White'

        self.writer.write_direct(str(msg), _color, tag)

    def log(self, message, color=None, tag="log"):
        self._write_message(message, color, tag)

    def info(self, message, color=None, tag="info"):
        self._write_message(message, color, tag)

    def debug(self, message, color=None, tag="debug"):
        if self._enable_debug():
            self._write_message("## " + message, color, tag)

    def warning(self, message, color=None, tag="warning"):
        self._write_message('WARNING: ' + message, color="gold", tag=tag)

    def error(self, message, tag="error"):
        self._write_message("****" + str(message), color="red", tag=tag)

    def _enable_debug(self):
        """Check if debug is enabled with caching to avoid repeated file system calls"""
        try:
            result, timestamp = self._debug_enabled_cache
            now = time.monotonic()

            # Return cached result if within TTL
            if now - timestamp < self._cache_ttl:
                return result

            # Check for debug files existence (faster than glob)
            result = any(os.path.exists(name) for name in self._debug_files)

            # Update cache
            self._debug_enabled_cache = (result, now)
            return result
        except Exception:
            return False

    def _disable_log(self):
        """Check if logging is disabled with caching to avoid repeated file system calls"""
        try:
            result, timestamp = self._log_disabled_cache
            now = time.monotonic()

            # Return cached result if within TTL
            if now - timestamp < self._cache_ttl:
                return result

            # Check for disable files existence (faster than glob)
            result = any(os.path.exists(name) for name in self._disable_files)

            # Update cache
            self._log_disabled_cache = (result, now)
            return result
        except Exception:
            return False

    def report_exception(self, exc, sleep=None):
        try:
            t = "{}".format(type(threading.currentThread())).split("'")[1].split('.')[1]
        except IndexError:
            t = 'UNKNOWN'

        self.error(f"Bypassing exception at {t} ({exc})", tag="exception")
        self.error(f"**** Exception: <code>{traceback.format_exc()}</code>", tag="exception")

        if sleep:
            time.sleep(sleep)

    def close(self):
        self.writer.close()
