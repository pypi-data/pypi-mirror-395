
import os
import sys
import shutil
import pytest
from time import sleep

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loghtml import writer, config

@pytest.fixture
def setup_test_environment(monkeypatch):
    """ Set up a temporary environment for testing log rotation. """
    temp_log_dir = "temp_test_logs"
    monkeypatch.setattr(config, 'log_dir', temp_log_dir)
    monkeypatch.setattr(config, 'log_files_limit_size', 1024)  # 1KB
    monkeypatch.setattr(config, 'log_files_limit_count', 3)
    
    # Create a temporary directory for logs
    if os.path.exists(temp_log_dir):
        shutil.rmtree(temp_log_dir)
    os.makedirs(temp_log_dir, exist_ok=True)
    
    yield temp_log_dir
    
    # Teardown: clean up the temporary directory
    shutil.rmtree(temp_log_dir)

def test_log_rotation_on_size_limit(setup_test_environment):
    """
    Test that the log file is rotated when it reaches the size limit.
    """
    log_dir = setup_test_environment
    
    # Create a LogWriter instance
    log_writer = writer.LogWriter()
    
    # Write messages until the size limit is exceeded
    message = "This is a test log message to fill up the log file."
    while log_writer.current_size < config.log_files_limit_size:
        log_writer.write_direct(message, color='blue', tag='test')

    # Flush the buffer to trigger rotation
    log_writer._flush_buffer()
    sleep(0.1)

    # After rotation, a new log file should be created, and the old one backed up
    main_log_file = os.path.join(log_dir, config.main_filename)
    
    # Check that a backup file was created
    backup_files = [f for f in os.listdir(log_dir) if f.endswith(config.main_filename)]
    assert len(backup_files) >= 1
    
    # The main log file should now be smaller or empty
    assert os.path.getsize(main_log_file) < config.log_files_limit_size

def test_backup_limit_enforcement(setup_test_environment):
    """
    Test that the number of backup files is limited.
    """
    log_dir = setup_test_environment
    
    # Create a LogWriter instance
    log_writer = writer.LogWriter()
    
    # Trigger rotation multiple times to exceed the backup limit
    for i in range(config.log_files_limit_count + 2):
        # Write enough to trigger rotation
        message = f"Rotation cycle {i+1}"
        log_writer.write_direct(message * 200, color='green', tag='cycle')
        log_writer._flush_buffer()
        sleep(0.2)  # Sleep to ensure unique filenames if based on timestamp

    # Check that the number of backup files does not exceed the limit
    backup_files = [f for f in os.listdir(log_dir) if f.endswith(config.main_filename)]
    
    # The number of files should be the limit + the current log file
    assert len(backup_files) <= config.log_files_limit_count + 1

