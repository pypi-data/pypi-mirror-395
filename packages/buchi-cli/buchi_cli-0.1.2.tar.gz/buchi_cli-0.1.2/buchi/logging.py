"""
Structured logging system for Buchi CLI.
Provides separate logs for debugging, auditing, and error tracking.
"""

import json
import logging
import uuid
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any


class StructuredFormatter(logging.Formatter):
    """Format logs as JSON for easy parsing and analysis"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        # Add session_id if available
        if hasattr(record, "session_id"):
            log_data["session_id"] = record.session_id

        # Add model if available
        if hasattr(record, "model"):
            log_data["model"] = record.model

        # Add working_dir if available
        if hasattr(record, "working_dir"):
            log_data["working_dir"] = record.working_dir

        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


class BuchiLogger:
    """
    Centralized logging for Buchi CLI with multiple log files.

    Log Types:
    - debug.log: Detailed execution trace (rotates at 10MB)
    - audit.log: File operations and security events (rotates at 5MB)
    - error.log: Errors and exceptions only (rotates at 5MB)
    """

    def __init__(self, working_dir: str):
        """
        Initialize logging for a working directory.

        Args:
            working_dir: Project directory for log storage
        """
        self.working_dir = Path(working_dir).resolve()
        self.log_dir = self.working_dir / ".buchi" / "logs"
        self.session_id = str(uuid.uuid4())[:8]  # Short session ID

        # Create logs directory
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup loggers
        self.debug_logger = self._setup_logger(
            "buchi.debug",
            self.log_dir / "debug.log",
            level=logging.DEBUG,
            max_bytes=10 * 1024 * 1024,  # 10MB
        )

        self.audit_logger = self._setup_logger(
            "buchi.audit",
            self.log_dir / "audit.log",
            level=logging.INFO,
            max_bytes=5 * 1024 * 1024,  # 5MB
        )

        self.error_logger = self._setup_logger(
            "buchi.error",
            self.log_dir / "error.log",
            level=logging.ERROR,
            max_bytes=5 * 1024 * 1024,  # 5MB
        )

        # Context to attach to all logs
        self.context = {
            "session_id": self.session_id,
            "working_dir": str(self.working_dir),
        }

    def _setup_logger(
        self, name: str, log_file: Path, level: int, max_bytes: int
    ) -> logging.Logger:
        """Setup a rotating file logger with structured output"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False  # Don't propagate to root logger

        # Remove existing handlers
        logger.handlers.clear()

        # Rotating file handler
        handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=3,  # Keep 3 backup files
            encoding="utf-8",
        )
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)

        return logger

    def _log_with_context(
        self,
        logger: logging.Logger,
        level: int,
        message: str,
        extra_data: dict[str, Any] | None = None,
    ):
        """Log with session context attached"""
        # Merge context with extra data
        log_extra = {"extra_data": {**self.context}}
        if extra_data:
            log_extra["extra_data"].update(extra_data)

        logger.log(level, message, extra=log_extra)

    # ===== Debug Logs (Detailed Execution) =====

    def debug(self, message: str, **kwargs):
        """Log debug information"""
        self._log_with_context(self.debug_logger, logging.DEBUG, message, kwargs)

    def info(self, message: str, **kwargs):
        """Log general information"""
        self._log_with_context(self.debug_logger, logging.INFO, message, kwargs)

    # ===== Audit Logs (Security & Operations) =====

    def audit_file_read(self, file_path: str, success: bool, error: str = None):
        """Log file read operation"""
        self._log_with_context(
            self.audit_logger,
            logging.INFO,
            f"File read: {file_path}",
            {
                "operation": "read",
                "file_path": file_path,
                "success": success,
                "error": error,
            },
        )

    def audit_file_write(
        self, file_path: str, size: int, success: bool, error: str = None
    ):
        """Log file write operation"""
        self._log_with_context(
            self.audit_logger,
            logging.INFO,
            f"File write: {file_path}",
            {
                "operation": "write",
                "file_path": file_path,
                "size_bytes": size,
                "success": success,
                "error": error,
            },
        )

    def audit_file_delete(self, file_path: str, success: bool, error: str = None):
        """Log file deletion"""
        self._log_with_context(
            self.audit_logger,
            logging.WARNING,
            f"File delete: {file_path}",
            {
                "operation": "delete",
                "file_path": file_path,
                "success": success,
                "error": error,
            },
        )

    def audit_tool_call(self, tool_name: str, args: dict[str, Any], success: bool):
        """Log tool invocation"""
        self._log_with_context(
            self.audit_logger,
            logging.INFO,
            f"Tool called: {tool_name}",
            {"tool": tool_name, "args": args, "success": success},
        )

    # ===== Error Logs =====

    def error(self, message: str, exception: Exception = None, **kwargs):
        """Log error with optional exception"""
        if exception:
            self._log_with_context(
                self.error_logger,
                logging.ERROR,
                message,
                {**kwargs, "exception_type": type(exception).__name__},
            )
            # Also log to debug for full context
            self.debug_logger.exception(message, extra={"extra_data": self.context})
        else:
            self._log_with_context(self.error_logger, logging.ERROR, message, kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning"""
        self._log_with_context(self.debug_logger, logging.WARNING, message, kwargs)
        # Also log to error log for visibility
        self._log_with_context(self.error_logger, logging.WARNING, message, kwargs)

    # ===== Session Management =====

    def start_session(self, model: str, prompt: str):
        """Log session start"""
        self.context["model"] = model
        self.info("Session started", prompt=prompt, model=model)

    def end_session(self, success: bool, duration_seconds: float):
        """Log session end"""
        self.info(
            "Session ended",
            success=success,
            duration_seconds=round(duration_seconds, 2),
        )

    # ===== Performance Tracking =====

    def log_performance(self, operation: str, duration_seconds: float, **kwargs):
        """Log performance metrics"""
        self._log_with_context(
            self.debug_logger,
            logging.INFO,
            f"Performance: {operation}",
            {
                "operation": operation,
                "duration_seconds": round(duration_seconds, 3),
                **kwargs,
            },
        )

    # ===== Utility Methods =====

    def get_session_id(self) -> str:
        """Get current session ID"""
        return self.session_id

    def get_log_dir(self) -> Path:
        """Get logs directory path"""
        return self.log_dir

    @staticmethod
    def cleanup_old_logs(working_dir: str, days: int = 30) -> int:
        """
        Delete log files older than specified days.

        Args:
            working_dir: Project directory
            days: Delete logs older than this many days

        Returns:
            Number of files deleted
        """
        log_dir = Path(working_dir) / ".buchi" / "logs"
        if not log_dir.exists():
            return 0

        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        deleted = 0

        for log_file in log_dir.glob("*.log*"):
            if log_file.stat().st_mtime < cutoff:
                try:
                    log_file.unlink()
                    deleted += 1
                except OSError:
                    pass

        return deleted

    @staticmethod
    def get_log_stats(working_dir: str) -> dict[str, Any]:
        """
        Get statistics about log files.

        Returns:
            dictionary with log file statistics
        """
        log_dir = Path(working_dir) / ".buchi" / "logs"
        if not log_dir.exists():
            return {"exists": False, "total_files": 0, "total_size_bytes": 0}

        files = {}
        total_size = 0

        for log_type in ["debug", "audit", "error"]:
            log_files = list(log_dir.glob(f"{log_type}.log*"))
            if log_files:
                size = sum(f.stat().st_size for f in log_files)
                files[log_type] = {
                    "count": len(log_files),
                    "size_bytes": size,
                    "size_mb": round(size / (1024 * 1024), 2),
                }
                total_size += size

        return {
            "exists": True,
            "log_dir": str(log_dir),
            "files": files,
            "total_files": sum(f["count"] for f in files.values()),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }
