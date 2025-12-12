"""
Test script for continuous application logging behavior.
This simulates a long-running application that logs sporadically.
"""
import time
import os
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from loghtml import log, info, debug, warning, error, log_html_config, close

def test_immediate_flush():
    """Test that logs are immediately written to file"""
    print("Testing immediate flush mode for continuous applications...")

    # Configure logger
    log_html_config(
        log_dir="test_logs",
        main_filename="continuous_test.html",
        immediate_flush=True  # Enable immediate flush
    )

    log("Application started - this should be visible immediately", tag="startup")

    # Wait and check if file was written
    time.sleep(0.1)

    log_file = os.path.join("test_logs", "continuous_test.html")
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "Application started" in content:
                print("✓ First log was written immediately")
            else:
                print("✗ First log NOT found in file")

            # Check if HTML is valid
            if content.endswith("</html>"):
                print("✓ HTML file is valid (has closing tag)")
            else:
                print("✗ HTML file is incomplete")
    else:
        print("✗ Log file was not created")

    # Simulate sporadic logging like a continuous app
    for i in range(5):
        time.sleep(1)
        info(f"Processing item {i}", tag="processing")

        # Check immediately if it was written
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if f"Processing item {i}" in content:
                print(f"✓ Log {i} written immediately")
            else:
                print(f"✗ Log {i} NOT written yet")

    warning("Testing warning message", tag="test")
    error("Testing error message", tag="test")

    # Final check
    time.sleep(0.1)
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.count('<font color=')
        print(f"\nTotal log entries in file: {lines}")

        if content.endswith("</html>"):
            print("✓ HTML file remains valid throughout execution")
        else:
            print("✗ HTML file became invalid")

    # Close logger
    close()

    # Final validation after close
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.endswith("</html>"):
            print("✓ HTML file properly closed")
        else:
            print("✗ HTML file not properly closed")

    print("\nTest completed! Check test_logs/continuous_test.html")

if __name__ == "__main__":
    test_immediate_flush()
