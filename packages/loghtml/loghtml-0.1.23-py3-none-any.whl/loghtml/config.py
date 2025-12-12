# Configuration file for the logger
import os

# Directories and files
log_dir = "logs"
main_filename = "log.html"

# File rotation settings
log_files_limit_count = 30
log_files_limit_size = 3 * 1024 * 1024  # 3MB

# Template file
template_file = "template.html"

# Flush behavior
# immediate_flush: When True, flushes after every log write (best for continuous apps)
# When False, uses buffering with periodic flush (better performance for high-volume logging)
immediate_flush = True
