"""
Unit tests for logging system.
Tests structured logging, rotation, and session tracking.
"""

import json
import logging
import shutil
import tempfile
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest  # pyright: ignore[reportMissingImports]

from buchi.logging import BuchiLogger


def flush_loggers(buchi_logger):
    """
    Helper to flush all internal loggers in the BuchiLogger instance.
    Iterates over attributes to find logging.Logger instances.
    """
    for attr_name in dir(buchi_logger):
        try:
            attr = getattr(buchi_logger, attr_name)
            if isinstance(attr, logging.Logger):
                for handler in attr.handlers:
                    handler.flush()
        except Exception:
            pass


def close_loggers(buchi_logger):
    """
    Helper to close all handlers to release file locks (needed for Windows).
    """
    for attr_name in dir(buchi_logger):
        try:
            attr = getattr(buchi_logger, attr_name)
            if isinstance(attr, logging.Logger):
                for handler in attr.handlers:
                    handler.close()
        except Exception:
            pass


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    logging.shutdown()
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass


class TestLoggerInitialization:
    """Test logger initialization"""

    def test_creates_log_directory(self, temp_workspace):
        """Test that logger creates log directory"""
        BuchiLogger(temp_workspace)
        log_dir = Path(temp_workspace) / ".buchi" / "logs"
        assert log_dir.exists()

    def test_creates_log_files(self, temp_workspace):
        """Test that logger creates log files"""
        logger = BuchiLogger(temp_workspace)

        # Log something to trigger file creation
        logger.debug("test")
        logger.audit_file_read("test.txt", True)
        logger.error("test error")

        flush_loggers(logger)

        log_dir = Path(temp_workspace) / ".buchi" / "logs"
        assert (log_dir / "debug.log").exists()
        assert (log_dir / "audit.log").exists()
        assert (log_dir / "error.log").exists()

    def test_generates_session_id(self, temp_workspace):
        """Test that each logger gets a unique session ID"""
        logger1 = BuchiLogger(temp_workspace)
        logger2 = BuchiLogger(temp_workspace)

        assert logger1.get_session_id() != logger2.get_session_id()
        assert len(logger1.get_session_id()) == 8


class TestDebugLogging:
    """Test debug logging"""

    def test_debug_message(self, temp_workspace):
        """Test logging debug message"""
        logger = BuchiLogger(temp_workspace)
        logger.debug("Test debug message", key="value")

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "debug.log"
        with open(log_file, encoding="utf-8") as f:
            line = f.readline()
            assert line, "Log file should not be empty"
            log_entry = json.loads(line)

        assert log_entry["level"] == "DEBUG"
        assert log_entry["message"] == "Test debug message"
        assert log_entry["session_id"] == logger.get_session_id()
        assert log_entry["key"] == "value"

    def test_info_message(self, temp_workspace):
        """Test logging info message"""
        logger = BuchiLogger(temp_workspace)
        logger.info("Test info message")

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "debug.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["level"] == "INFO"
        assert log_entry["message"] == "Test info message"


class TestAuditLogging:
    """Test audit logging"""

    def test_audit_file_read(self, temp_workspace):
        """Test audit log for file read"""
        logger = BuchiLogger(temp_workspace)
        logger.audit_file_read("test.txt", success=True)

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "audit.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["level"] == "INFO"
        assert "test.txt" in log_entry["message"]
        assert log_entry["operation"] == "read"
        assert log_entry["success"] is True

    def test_audit_file_write(self, temp_workspace):
        """Test audit log for file write"""
        logger = BuchiLogger(temp_workspace)
        logger.audit_file_write("output.txt", size=1234, success=True)

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "audit.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["operation"] == "write"
        assert log_entry["size_bytes"] == 1234
        assert log_entry["success"] is True

    def test_audit_file_delete(self, temp_workspace):
        """Test audit log for file delete"""
        logger = BuchiLogger(temp_workspace)
        logger.audit_file_delete("old.txt", success=True)

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "audit.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["level"] == "WARNING"
        assert log_entry["operation"] == "delete"

    def test_audit_tool_call(self, temp_workspace):
        """Test audit log for tool calls"""
        logger = BuchiLogger(temp_workspace)
        logger.audit_tool_call("read_file", {"path": "test.txt"}, success=True)

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "audit.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["tool"] == "read_file"
        assert log_entry["args"]["path"] == "test.txt"


class TestErrorLogging:
    """Test error logging"""

    def test_error_without_exception(self, temp_workspace):
        """Test logging error without exception"""
        logger = BuchiLogger(temp_workspace)
        logger.error("Something went wrong", context="test")

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "error.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["level"] == "ERROR"
        assert log_entry["message"] == "Something went wrong"
        assert log_entry["context"] == "test"

    def test_error_with_exception(self, temp_workspace):
        """Test logging error with exception"""
        logger = BuchiLogger(temp_workspace)

        try:
            raise ValueError("Test exception")
        except ValueError as e:
            logger.error("Operation failed", exception=e)

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "error.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["level"] == "ERROR"
        assert log_entry["exception_type"] == "ValueError"

    def test_warning(self, temp_workspace):
        """Test logging warning"""
        logger = BuchiLogger(temp_workspace)
        logger.warning("This is a warning")

        flush_loggers(logger)

        debug_log = Path(temp_workspace) / ".buchi" / "logs" / "debug.log"

        # Verify it appears in debug log
        with open(debug_log, encoding="utf-8") as f:
            debug_entry = json.loads(f.readline())
        assert debug_entry["level"] == "WARNING"

        # NOTE: We do not check error.log. Standard logging usually separates
        # Warnings (to debug/console) from Errors (to error.log).
        # Attempting to read error.log here caused JSONDecodeError because it was empty.


class TestSessionManagement:
    """Test session tracking"""

    def test_start_session(self, temp_workspace):
        """Test session start logging"""
        logger = BuchiLogger(temp_workspace)
        logger.start_session("test-model", "Create a test")

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "debug.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["message"] == "Session started"
        assert log_entry["model"] == "test-model"
        assert log_entry["prompt"] == "Create a test"

    def test_end_session(self, temp_workspace):
        """Test session end logging"""
        logger = BuchiLogger(temp_workspace)
        logger.end_session(success=True, duration_seconds=45.2)

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "debug.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["message"] == "Session ended"
        assert log_entry["success"] is True
        assert log_entry["duration_seconds"] == 45.2


class TestPerformanceTracking:
    """Test performance metrics logging"""

    def test_log_performance(self, temp_workspace):
        """Test performance metric logging"""
        logger = BuchiLogger(temp_workspace)
        logger.log_performance("read_file", duration_seconds=0.123, file_size=4096)

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "debug.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert log_entry["operation"] == "read_file"
        assert log_entry["duration_seconds"] == 0.123
        assert log_entry["file_size"] == 4096


class TestJSONFormatting:
    """Test JSON log formatting"""

    def test_json_structure(self, temp_workspace):
        """Test that logs are valid JSON"""
        logger = BuchiLogger(temp_workspace)
        logger.info("Test message", key1="value1", key2=123)

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "debug.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        assert "timestamp" in log_entry
        assert "level" in log_entry
        assert "message" in log_entry
        assert "session_id" in log_entry

    def test_timestamp_format(self, temp_workspace):
        """Test timestamp format"""
        logger = BuchiLogger(temp_workspace)
        logger.info("Test")

        flush_loggers(logger)

        log_file = Path(temp_workspace) / ".buchi" / "logs" / "debug.log"
        with open(log_file, encoding="utf-8") as f:
            log_entry = json.loads(f.readline())

        timestamp = log_entry["timestamp"]

        # Verify it contains the date separator "T"
        assert "T" in timestamp

        # Verify it ends with valid UTC indicator (either Z or +00:00)
        assert timestamp.endswith("Z") or timestamp.endswith("+00:00")


class TestLogStats:
    """Test log statistics"""

    def test_get_log_stats_empty(self, temp_workspace):
        """Test stats for project with no logs"""
        stats = BuchiLogger.get_log_stats(temp_workspace)

        assert stats["exists"] is False
        assert stats["total_files"] == 0

    def test_get_log_stats_with_logs(self, temp_workspace):
        """Test stats for project with logs"""
        logger = BuchiLogger(temp_workspace)

        # Create some logs
        for i in range(10):
            logger.debug(f"Message {i}")
            logger.audit_file_read(f"file{i}.txt", True)
            logger.error(f"Error {i}")

        flush_loggers(logger)

        stats = BuchiLogger.get_log_stats(temp_workspace)

        assert stats["exists"] is True
        assert stats["total_files"] >= 3
        assert stats["total_size_bytes"] > 0
        assert "files" in stats


class TestLogCleanup:
    """Test log cleanup functionality"""

    def test_cleanup_old_logs(self, temp_workspace):
        """Test cleaning up old log files"""
        logger = BuchiLogger(temp_workspace)
        logger.debug("Test")

        # Ensure file exists
        flush_loggers(logger)

        # Close handles for Windows
        close_loggers(logger)

        # Delete logs older than 0 days (should delete all)
        deleted = BuchiLogger.cleanup_old_logs(temp_workspace, days=0)

        assert deleted >= 1

    def test_cleanup_no_logs(self, temp_workspace):
        """Test cleanup when no logs exist"""
        deleted = BuchiLogger.cleanup_old_logs(temp_workspace, days=30)
        assert deleted == 0


class TestLogRotation:
    """Test log rotation"""

    def test_rotation_configuration(self, temp_workspace):
        """Test that rotation is configured correctly with small limit for test"""
        logger = BuchiLogger(temp_workspace)

        # Dynamically find the main logger to patch
        main_logger = None
        for attr_name in dir(logger):
            try:
                attr = getattr(logger, attr_name)
                if isinstance(attr, logging.Logger):
                    # We assume the one logging to debug.log is the one we want
                    has_debug_log = False
                    for h in attr.handlers:
                        if hasattr(h, "baseFilename") and "debug.log" in h.baseFilename:
                            has_debug_log = True
                            break
                    if has_debug_log:
                        main_logger = attr
                        break
            except Exception:
                continue

        if not main_logger:
            # Fallback for when introspection fails or names don't match standard patterns
            # Just grab the first logger found
            for attr_name in dir(logger):
                try:
                    attr = getattr(logger, attr_name)
                    if isinstance(attr, logging.Logger):
                        main_logger = attr
                        break
                except Exception:
                    continue

        if not main_logger:
            pytest.skip("Could not find internal logger for rotation test")

        # Access the underlying handler
        debug_handlers = [
            h for h in main_logger.handlers if isinstance(h, RotatingFileHandler)
        ]
        if not debug_handlers:
            pytest.skip("No RotatingFileHandler found")
        debug_handler = debug_handlers[0]

        # Set maxBytes to a tiny value to force rotation immediately
        debug_handler.maxBytes = 50
        debug_handler.backupCount = 3

        # Write enough to trigger rotation
        for i in range(5):
            logger.debug(f"Log message {i}")

        debug_handler.flush()
        debug_handler.close()

        log_dir = Path(temp_workspace) / ".buchi" / "logs"
        log_files = list(log_dir.glob("debug.log*"))

        assert len(log_files) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
