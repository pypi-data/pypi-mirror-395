# HTML Logger

A Python library for generating HTML logs with support for colors, file rotation, tagging, and JavaScript filters.

## Features

- ✅ Colored logs in HTML format
- ✅ Automatic file rotation
- ✅ Clean interface with integrated JavaScript filters
- ✅ Thread-safe and high performance
- ✅ Exception support with full traceback
- ✅ Flexible configuration for file size and quantity
- ✅ Tagging system for message categorization
- ✅ Advanced filtering by tags and text content
- ✅ Default color mapping for specific tags

## Installation

```bash
pip install loghtml
```

## Basic Usage

```python
from loghtml import log, error, report_exception

# Simple messages
log("Normal informative message")
log("Blue message", color="blue")

# Error messages
error("This is an error message")

# Log exceptions
try:
    # Your code here
    raise ValueError("Example error")
except Exception as e:
    report_exception(e)
```

## Enhanced Tagging System

The logger supports tagging messages for better organization and filtering:

```python
from loghtml import log, info, debug, warning

# Tagged messages
log("User login", tag="auth")
info("Data processed", tag="processing")
debug("Variable value", tag="debug")
warning("Resource low", tag="system")
```

## Setting Default Tag Colors

You can define default colors for specific tags:

```python
from loghtml import set_default_tag_color

default_tag_colors = {
    "database": "LightGrey",
    "connection": "LightBlue",
    "heartbeat": "Yellow"
}
set_default_tag_color(default_tag_colors)
```

## Configuration

```python
from loghtml import log_html_config

# Customize logger settings
log_html_config(
    log_files_limit_count=15,     # Maximum number of log files
    log_files_limit_size=5000000, # Maximum size per file (5MB)
    main_filename="log.html",     # Main file name
    log_dir="logs",               # Directory for logs
    immediate_flush=True          # Flush after every write (default: True)
)
```

## Continuous Applications Support

The logger is optimized for continuous (long-running) applications with **immediate flush** mode enabled by default. This ensures that log messages are written to the file immediately, making them visible even if the application doesn't terminate.

### Key Features for Continuous Apps:

1. **Immediate Flush**: Every log message is written to disk immediately (configurable)
2. **Valid HTML Always**: The HTML file maintains a valid structure even while the application is running
3. **Periodic Flush Daemon**: A background thread ensures buffered content is flushed every 500ms as a backup
4. **No Lost Messages**: Messages are never "stuck" in buffer waiting for application termination

### Performance Tuning:

For high-volume logging scenarios, you can disable immediate flush for better performance:

```python
from loghtml import log_html_config

# Optimize for high-volume logging
log_html_config(
    immediate_flush=False  # Use buffering (flushes every 1s or 64KB)
)
```

**Note**: For typical continuous applications (servers, daemons, monitoring tools), keep `immediate_flush=True` (default) to ensure real-time log visibility.

## File-based Control Features

The logger includes two file-based validation features that provide runtime control over logging behavior:

### Debug Mode Control

Debug messages can be enabled by creating a control file in your application directory. The logger will automatically detect the presence of any of these files:

- `DebugEnable`
- `debug_enable`
- `enable_debug`
- `EnableDebug`

```python
from loghtml import debug, log

# Create a control file to enable debug messages
# On Windows:
# type nul > DebugEnable
# On Linux/Mac:
# touch debug_enable

debug("This debug message will only appear if debug control file exists")
log("This regular message always appears")
```

**Example usage:**
```bash
# Enable debug mode
touch debug_enable

# Run your application - debug messages will now be visible
python your_app.py

# Disable debug mode
rm debug_enable

# Run again - debug messages will be hidden
python your_app.py
```

### Log Disable Control

All log writing to files can be disabled by creating a control file in your application directory. The logger will automatically detect the presence of any of these files:

- `DisableLog`
- `disable_log`
- `log_disable`
- `LogDisable`

```python
from loghtml import log, info, error

# Create a control file to disable all log file writing
# On Windows:
# type nul > DisableLog
# On Linux/Mac:
# touch disable_log

log("This message will still appear on screen but not in log files")
info("Screen output continues normally")
error("Errors are still displayed on screen")
```

**Example usage:**
```bash
# Disable log file writing (console output still works)
touch disable_log

# Run your application - no log files will be created/updated
python your_app.py

# Re-enable log file writing
rm disable_log

# Run again - log files will be created/updated normally
python your_app.py
```

**Note:** These control files only need to exist in the same directory where your application runs. The content of the files is irrelevant - only their presence matters. Screen output (console logging) continues to work regardless of these settings.

## File Structure

Logs are stored in the specified directory (default: `logs/`) with the following structure:

```
logs/
└── log.html (current file)
└── 2023-10-05_12-30-45_log.html (rotated file)
└── 2023-10-05_10-15-32_log.html (rotated file)
```

## Integrated JavaScript Filters

Generated HTML files include advanced filtering capabilities to facilitate analysis:

- Text filtering with AND/OR logic
- Tag-based filtering
- Time period filtering
- Real-time highlighting of matched terms
- Preserved original log view

## Complete Example

```python
from loghtml import log, info, debug, warning, error, report_exception, log_html_config, set_default_tag_color

# Configure logger
log_html_config(
    log_files_limit_count=10,
    log_files_limit_size=2000000,  # 2MB
    log_dir="my_logs"
)

# Set default tag colors
default_tag_colors = {
    "system": "green",
    "processing": "cyan",
    "checkpoint": "magenta"
}
set_default_tag_color(default_tag_colors)

# Log with different tags and levels
log("Application started", tag="system")
info("Loading configuration", tag="config")
debug("Initializing modules", tag="debug")

for i in range(100):
    if i % 10 == 0:
        log(f"Checkpoint {i}", tag="checkpoint")
    info(f"Processing item {i}", tag="processing")

try:
    # Code that might raise an error
    result = 10 / 0
except Exception as e:
    error("Division by zero detected")
    report_exception(e)

log("Application finished", tag="system")
```

## API Reference

### log(message, color=None, tag="log")
Logs a message with optional color and tag(s).

### info(message, color=None, tag="info")
Logs an informational message.

### debug(message, color=None, tag="debug")
Logs a debug message.

### warning(message, color=None, tag="warning")
Logs a warning message.

### error(message, tag="error")
Logs an error message (in red).

### report_exception(exc, timeout=None)
Logs an exception with its full traceback.

### log_html_config(**kwargs)
Configures logger options:
- `log_files_limit_count`: Maximum number of files to maintain
- `log_files_limit_size`: Maximum size in bytes per file
- `main_filename`: Main log file name
- `log_dir`: Directory where logs will be stored

### set_default_tag_color(color_dict)
Sets default colors for specific tags:
- `color_dict`: Dictionary mapping tag names to color values

### flush()
Processes all pending messages before termination.

## Using with PyInstaller

The package is now fully compatible with PyInstaller and includes automatic hook detection:

```bash
# Basic usage
pyinstaller --onefile your_script.py

# If you need additional debugging
pyinstaller --collect-all loghtml --onefile your_script.py
```

The package includes:
- Automatic PyInstaller hook (`hook-loghtml.py`)
- Proper resource management using `importlib.resources`
- `zip-safe = false` configuration for maximum compatibility

See `PYINSTALLER_GUIDE.md` for detailed instructions and troubleshooting.

## Development

To contribute to the project:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

If you encounter issues or have questions:

1. Check the [documentation](https://github.com/rphpires/py-html-logger)
2. Open an [issue](https://github.com/rphpires/py-html-logger/issues)
3. Contact: rphspires@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Developed by Raphael Pires
- Inspired by the need for better log visualization and analysis tools