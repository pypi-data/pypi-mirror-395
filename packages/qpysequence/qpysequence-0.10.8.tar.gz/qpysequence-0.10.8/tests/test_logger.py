import os
import pytest
from loguru import logger
from qpysequence.logger import set_level, add_file_logging

@pytest.fixture
def clear_logger_handlers():
    """Ensure logger handlers are cleared before each test."""
    logger.remove()
    yield
    logger.remove()

def test_default_logging_level(monkeypatch, capsys, clear_logger_handlers):
    """Test that the default logging level is set correctly."""
    monkeypatch.setenv("QPYSEQUENCE_LOG_LEVEL", "DEBUG")

    # Re-import the logging module to apply the new environment variable
    import importlib
    import qpysequence.logger as logger_module
    importlib.reload(logger_module)

    logger.debug("This is a debug message.")
    captured = capsys.readouterr()

    assert "This is a debug message." in captured.err

def test_set_level(capsys, clear_logger_handlers):
    """Test the dynamic setting of the logging level."""
    set_level("WARNING")
    logger.info("This is an info message.")  # Should not appear
    logger.warning("This is a warning message.")  # Should appear

    captured = capsys.readouterr()
    assert "This is an info message." not in captured.err
    assert "This is a warning message." in captured.err

def test_add_file_logging(tmp_path, clear_logger_handlers):
    """Test adding a file handler for logging."""
    log_file = tmp_path / "test_log.log"
    add_file_logging(str(log_file), level="DEBUG")

    logger.debug("Debug message to file.")
    logger.error("Error message to file.")

    # Ensure the file contains the logs
    with open(log_file, "r") as f:
        log_contents = f.read()

    assert "Debug message to file." in log_contents
    assert "Error message to file." in log_contents
