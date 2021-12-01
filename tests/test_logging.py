# -*- coding: utf-8 -*-
import logging
import os
from matchms.logging_functions import add_logging_to_file
from matchms.logging_functions import reset_matchms_logger
from matchms.logging_functions import set_matchms_logger_level


def test_initial_logging(caplog):
    """Test logging functionality."""
    logger = logging.getLogger("matchms")
    logger.info("info test")
    logger.warning("warning test")
    assert logger.name == "matchms", "Expected different logger name"
    assert logger.getEffectiveLevel() == 30, "Expected different logging level"
    assert "info test" not in caplog.text, "Info log should not be shown."
    assert "warning test" in caplog.text, "Warning log should have been shown."


def test_set_and_reset_matchms_logger_level(caplog):
    """Test logging functionality."""
    logger = logging.getLogger("matchms")
    assert logger.getEffectiveLevel() == 30, "Expected different logging level"

    set_matchms_logger_level("INFO")
    logger.debug("debug test")
    logger.info("info test")

    assert logger.name == "matchms", "Expected different logger name"
    assert logger.getEffectiveLevel() == 20, "Expected different logging level"
    assert "debug test" not in caplog.text, "Debug log should not be shown."
    assert "info test" in caplog.text, "Info log should have been shown."

    reset_matchms_logger()
    assert logger.getEffectiveLevel() == 30, "Expected different logging level"


def test_add_logging_to_file(tmp_path, caplog):
    """Test writing logs to file."""
    logger = logging.getLogger("matchms")
    set_matchms_logger_level("INFO")
    filename = os.path.join(tmp_path, "test.log")
    add_logging_to_file(filename)
    logger.info("test message no.1")

    expected_log_entry = "test message no.1"
    # Test streamed logs
    assert expected_log_entry in caplog.text, "Expected different log message"

    # Test log file
    assert os.path.isfile(filename), "Log file not found."
    with open(filename, "r", encoding="utf-8") as file:
        logs = file.read()
    assert expected_log_entry in logs, "Expected different log file content"


def test_add_logging_to_file_only_file(tmp_path, caplog):
    """Test writing logs to file."""
    logger = logging.getLogger("matchms")
    set_matchms_logger_level("INFO")
    filename = os.path.join(tmp_path, "test.log")
    add_logging_to_file(filename, remove_stream_handlers=True)
    logger.info("test message no.1")

    expected_log_entry = "INFO:matchms:test_logging:test message no.1"
    # Test streamed logs
    assert expected_log_entry not in caplog.text, "Expected different log message"

    # Test log file
    assert os.path.isfile(filename), "Log file not found."
    with open(filename, "r", encoding="utf-8") as file:
        logs = file.read()
    assert expected_log_entry in logs, "Expected different log file content"
