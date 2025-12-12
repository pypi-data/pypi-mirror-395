"""
Logging Fixtures for Pytest Testing
Netrun Systems - Service #70 Unified Test Fixtures

Provides logging fixtures for testing logging functionality and
ensuring test isolation by resetting logging state between tests.

Usage:
    def test_logging(reset_logging, caplog):
        logger = logging.getLogger("test")
        logger.info("Test message")
        assert "Test message" in caplog.text

Fixtures:
    - reset_logging: Auto-cleanup of logging handlers (autouse)
    - sample_log_record: Sample LogRecord for testing formatters
    - logger_with_handler: Logger with in-memory handler for testing
    - capture_logs: Capture logs to list for assertion
"""

import pytest
import logging
from typing import List, Generator
from io import StringIO


@pytest.fixture(autouse=True)
def reset_logging():
    """
    Reset logging configuration between tests.

    Autouse fixture that clears all handlers from root logger
    before and after each test to ensure logging isolation.

    This prevents tests from interfering with each other's
    logging configuration and prevents handler accumulation.

    Yields:
        None

    Example:
        # No explicit use needed - runs automatically
        def test_logging():
            logger = logging.getLogger("test")
            handler = logging.StreamHandler()
            logger.addHandler(handler)
            # Handler automatically cleaned up after test
    """
    # Clear all handlers from root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.DEBUG)

    # Clear handlers from all other loggers
    for logger_name in list(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.setLevel(logging.NOTSET)
        logger.propagate = True

    yield

    # Cleanup after test
    root_logger.handlers.clear()
    for logger_name in list(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()


@pytest.fixture
def sample_log_record() -> logging.LogRecord:
    """
    Create a sample log record for testing formatters and handlers.

    Returns:
        logging.LogRecord: Sample log record

    Example:
        def test_custom_formatter(sample_log_record):
            formatter = CustomFormatter()
            formatted = formatter.format(sample_log_record)
            assert "test.logger" in formatted
            assert "Test message" in formatted
    """
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname="/test/path.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    return record


@pytest.fixture
def logger_with_handler():
    """
    Factory for creating logger with in-memory string handler.

    Returns function that creates logger with StringIO handler
    for capturing log output without file I/O.

    Returns:
        Callable: Function that creates logger with handler

    Example:
        def test_log_output(logger_with_handler):
            logger, stream = logger_with_handler("test.app")
            logger.info("Test message")

            output = stream.getvalue()
            assert "Test message" in output
    """
    def _create_logger(name: str = "test", level: int = logging.DEBUG):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Create StringIO handler
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setLevel(level)

        # Add formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger, stream

    return _create_logger


@pytest.fixture
def capture_logs():
    """
    Fixture to capture logs to a list for assertions.

    Returns handler that captures log records to a list.
    Use for testing log output without caplog fixture.

    Returns:
        Tuple[logging.Handler, List]: Handler and log records list

    Example:
        def test_logging_with_capture(capture_logs):
            handler, logs = capture_logs

            logger = logging.getLogger("test")
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

            logger.info("Info message")
            logger.error("Error message")

            assert len(logs) == 2
            assert logs[0].levelname == "INFO"
            assert logs[1].levelname == "ERROR"
    """
    class ListHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.records: List[logging.LogRecord] = []

        def emit(self, record):
            self.records.append(record)

    handler = ListHandler()
    handler.setLevel(logging.DEBUG)

    return handler, handler.records


@pytest.fixture
def json_log_formatter():
    """
    Create JSON log formatter for testing structured logging.

    Returns:
        logging.Formatter: JSON formatter

    Example:
        def test_json_logging(json_log_formatter, capture_logs):
            handler, logs = capture_logs
            handler.setFormatter(json_log_formatter)

            logger = logging.getLogger("test")
            logger.addHandler(handler)
            logger.info("Test message", extra={"user_id": "123"})

            # Check JSON formatting
            formatted = handler.format(logs[0])
            assert '"message": "Test message"' in formatted
    """
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            import json
            log_data = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }

            # Add extra fields
            if hasattr(record, "user_id"):
                log_data["user_id"] = record.user_id
            if hasattr(record, "tenant_id"):
                log_data["tenant_id"] = record.tenant_id
            if hasattr(record, "request_id"):
                log_data["request_id"] = record.request_id

            # Add exception info if present
            if record.exc_info:
                log_data["exception"] = self.formatException(record.exc_info)

            return json.dumps(log_data)

    return JsonFormatter()


@pytest.fixture
def silence_loggers(monkeypatch):
    """
    Silence specific loggers during testing.

    Returns function to silence noisy loggers (uvicorn, sqlalchemy, etc).

    Args:
        monkeypatch: Pytest monkeypatch fixture

    Returns:
        Callable: Function to silence loggers

    Example:
        def test_without_noise(silence_loggers):
            silence_loggers(["uvicorn", "sqlalchemy.engine"])

            # Test runs without noisy log output
            # from uvicorn and SQLAlchemy
    """
    def _silence(*logger_names: str):
        for name in logger_names:
            logger = logging.getLogger(name)
            logger.setLevel(logging.CRITICAL)
            logger.propagate = False

    return _silence


@pytest.fixture
def log_level_setter():
    """
    Factory for temporarily setting log levels.

    Returns function to set log level with automatic cleanup.

    Returns:
        Callable: Function to set log level

    Example:
        def test_debug_logging(log_level_setter):
            log_level_setter("myapp", logging.DEBUG)

            logger = logging.getLogger("myapp")
            # Logger now at DEBUG level
            logger.debug("Debug message")  # This will be captured
    """
    original_levels = {}

    def _set_level(logger_name: str, level: int):
        logger = logging.getLogger(logger_name)
        original_levels[logger_name] = logger.level
        logger.setLevel(level)

    yield _set_level

    # Restore original levels
    for logger_name, level in original_levels.items():
        logging.getLogger(logger_name).setLevel(level)


@pytest.fixture
def mock_log_handler():
    """
    Create mock logging handler for testing handler behavior.

    Returns:
        MagicMock: Mock logging handler

    Example:
        def test_handler_called(mock_log_handler):
            logger = logging.getLogger("test")
            logger.addHandler(mock_log_handler)

            logger.info("Test message")

            mock_log_handler.emit.assert_called_once()
            record = mock_log_handler.emit.call_args[0][0]
            assert record.getMessage() == "Test message"
    """
    from unittest.mock import MagicMock

    handler = MagicMock(spec=logging.Handler)
    handler.level = logging.DEBUG
    return handler


@pytest.fixture
def exception_log_record() -> logging.LogRecord:
    """
    Create log record with exception information.

    Returns:
        logging.LogRecord: Log record with exc_info

    Example:
        def test_exception_formatting(exception_log_record):
            formatter = logging.Formatter()
            formatted = formatter.format(exception_log_record)

            assert "ValueError" in formatted
            assert "Test exception" in formatted
    """
    try:
        raise ValueError("Test exception")
    except ValueError:
        import sys
        exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="test.logger",
            level=logging.ERROR,
            pathname="/test/path.py",
            lineno=42,
            msg="An error occurred",
            args=(),
            exc_info=exc_info,
        )
        return record
