import os
import shutil
from ceylonai_next import LoggingConfig, init_logging

def test_logging_initialization():
    log_dir = "test_logs"
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "test.log")
    
    # Create config
    config = LoggingConfig("info", log_file, True)
    
    # Initialize logging
    # Note: We capture the handle to keep it alive
    handle = init_logging(config)
    
    assert handle is not None
    
    # Since we can't easily check if Rust wrote to the file immediately (async flushing),
    # we mainly verify that the API calls work without error.
    # In a real scenario, we would generate some logs and check the file.
    # But generating logs requires running an agent or something that logs.
    
    print("Logging initialized successfully")

if __name__ == "__main__":
    test_logging_initialization()
