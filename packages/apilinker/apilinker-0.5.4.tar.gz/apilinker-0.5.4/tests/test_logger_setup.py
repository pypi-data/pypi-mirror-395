import json
import logging
from pathlib import Path

from apilinker.core.logger import (
    CorrelationFilter,
    CorrelationFormatter,
    JsonFormatter,
    clear_correlation_id,
    log_with_context,
    set_correlation_id,
    setup_logger,
    with_correlation_id,
)


def test_setup_logger_writes_file_text(tmp_path):
    log_file = tmp_path / "text.log"
    logger = setup_logger("DEBUG", str(log_file), format_as_json=False)
    with with_correlation_id("cid-1"):
        logger.info("hello text")
    assert log_file.exists()
    content = log_file.read_text()
    assert "hello text" in content
    assert "cid-1" in content


def test_setup_logger_writes_file_json(tmp_path):
    log_file = tmp_path / "json.log"
    logger = setup_logger("INFO", str(log_file), format_as_json=True)
    logger.info("hello json")
    lines = [ln for ln in log_file.read_text().splitlines() if ln.strip()]
    assert lines, "expected some json logs"
    obj = json.loads(lines[-1])
    assert obj["message"] == "hello json"
    assert "correlation_id" in obj


def test_correlation_filter_set_and_clear():
    """Test setting and clearing correlation IDs."""
    filter = CorrelationFilter()
    filter.set_correlation_id("test-id")
    assert filter._context_correlation_id == "test-id"
    filter.clear_correlation_id()
    assert filter._context_correlation_id is None


def test_correlation_filter_adds_id():
    """Test that correlation filter adds ID to records."""
    filter = CorrelationFilter()
    filter.set_correlation_id("test-id")
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test",
        args=(),
        exc_info=None,
    )
    filter.filter(record)
    assert record.correlation_id == "test-id"


def test_correlation_filter_preserves_existing_id():
    """Test that correlation filter preserves existing ID."""
    filter = CorrelationFilter()
    filter.set_correlation_id("context-id")
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test",
        args=(),
        exc_info=None,
    )
    record.correlation_id = "record-id"
    filter.filter(record)
    assert record.correlation_id == "record-id"


def test_correlation_filter_no_id_default():
    """Test that correlation filter adds default when no ID set."""
    filter = CorrelationFilter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test",
        args=(),
        exc_info=None,
    )
    filter.filter(record)
    assert record.correlation_id == "no-correlation-id"


def test_correlation_formatter():
    """Test CorrelationFormatter adds correlation_id."""
    formatter = CorrelationFormatter(
        "[%(levelname)s] [%(correlation_id)s] %(message)s"
    )
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test message",
        args=(),
        exc_info=None,
    )
    formatted = formatter.format(record)
    assert "no-correlation-id" in formatted


def test_json_formatter_basic():
    """Test JsonFormatter produces valid JSON."""
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test message",
        args=(),
        exc_info=None,
    )
    formatted = formatter.format(record)
    data = json.loads(formatted)
    assert data["message"] == "test message"
    assert data["level"] == "INFO"
    assert data["logger"] == "test"
    assert "correlation_id" in data


def test_json_formatter_with_correlation_id():
    """Test JsonFormatter includes correlation ID."""
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test",
        args=(),
        exc_info=None,
    )
    record.correlation_id = "test-cid"
    formatted = formatter.format(record)
    data = json.loads(formatted)
    assert data["correlation_id"] == "test-cid"


def test_json_formatter_with_exception():
    """Test JsonFormatter includes exception info."""
    formatter = JsonFormatter()
    try:
        raise ValueError("test error")
    except ValueError:
        import sys

        exc_info = sys.exc_info()
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="error occurred",
            args=(),
            exc_info=exc_info,
        )
        formatted = formatter.format(record)
        data = json.loads(formatted)
        assert "exception" in data
        assert "ValueError" in data["exception"]


def test_json_formatter_with_extra_attributes():
    """Test JsonFormatter includes extra attributes."""
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test",
        args=(),
        exc_info=None,
    )
    record.custom_field = "custom_value"
    formatted = formatter.format(record)
    data = json.loads(formatted)
    assert data["custom_field"] == "custom_value"


def test_with_correlation_id_context_manager():
    """Test with_correlation_id context manager."""
    with with_correlation_id("test-cid") as cid:
        assert cid == "test-cid"


def test_with_correlation_id_generates_id():
    """Test with_correlation_id generates UUID when not provided."""
    with with_correlation_id() as cid:
        assert cid is not None
        assert len(cid) > 0


def test_with_correlation_id_restores_previous():
    """Test with_correlation_id restores previous correlation ID."""
    set_correlation_id("original-id")
    with with_correlation_id("temp-id") as cid:
        assert cid == "temp-id"
    # After exiting, should restore original
    filter = CorrelationFilter()
    filter.set_correlation_id("original-id")
    assert filter._context_correlation_id == "original-id"
    clear_correlation_id()


def test_set_and_clear_correlation_id():
    """Test set_correlation_id and clear_correlation_id functions."""
    set_correlation_id("test-id")
    clear_correlation_id()
    # Just verify no errors occur


def test_log_with_context():
    """Test log_with_context function."""
    logger = logging.getLogger("test_logger")
    log_with_context(logger, logging.INFO, "test message", correlation_id="test-cid")
    # Verify no errors occur


def test_log_with_context_extra_kwargs():
    """Test log_with_context with extra kwargs."""
    logger = logging.getLogger("test_logger")
    log_with_context(
        logger, logging.INFO, "test message", correlation_id="test-cid", extra={"key": "value"}
    )
    # Verify no errors occur


def test_setup_logger_custom_name():
    """Test setup_logger with custom logger name."""
    logger = setup_logger(logger_name="custom_logger")
    assert logger.name == "custom_logger"


def test_setup_logger_removes_existing_handlers():
    """Test that setup_logger removes existing handlers."""
    logger = setup_logger(logger_name="test_removal")
    initial_handlers = len(logger.handlers)
    logger = setup_logger(logger_name="test_removal")
    # Should have same number of handlers after re-setup
    assert len(logger.handlers) == initial_handlers


def test_setup_logger_file_creates_directory(tmp_path):
    """Test that setup_logger creates directory for log file."""
    log_file = tmp_path / "subdir" / "logs" / "test.log"
    logger = setup_logger(log_file=str(log_file))
    logger.info("test")
    assert log_file.exists()
    assert log_file.parent.exists()


def test_setup_logger_convenience_methods(tmp_path):
    """Test convenience methods added to logger."""
    log_file = tmp_path / "test.log"
    logger = setup_logger(log_file=str(log_file))
    
    # Test that methods exist
    assert hasattr(logger, "info_with_correlation")
    assert hasattr(logger, "error_with_correlation")
    assert hasattr(logger, "warning_with_correlation")
    assert hasattr(logger, "debug_with_correlation")
    
    # Test calling them
    logger.info_with_correlation("info msg", correlation_id="cid1")
    logger.error_with_correlation("error msg", correlation_id="cid2")
    logger.warning_with_correlation("warning msg", correlation_id="cid3")
    logger.debug_with_correlation("debug msg", correlation_id="cid4")
    
    content = log_file.read_text()
    assert "info msg" in content
    assert "error msg" in content
    assert "warning msg" in content


def test_setup_logger_different_levels():
    """Test setup_logger with different log levels."""
    for level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
        logger = setup_logger(level=level, logger_name=f"test_{level}")
        expected_level = getattr(logging, level)
        assert logger.level == expected_level


def test_json_formatter_timestamp():
    """Test JsonFormatter includes timestamp."""
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test",
        args=(),
        exc_info=None,
    )
    formatted = formatter.format(record)
    data = json.loads(formatted)
    assert "timestamp" in data
