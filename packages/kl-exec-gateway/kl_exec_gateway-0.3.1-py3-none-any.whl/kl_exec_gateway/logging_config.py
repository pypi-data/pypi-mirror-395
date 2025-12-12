# src/kl_exec_gateway/logging_config.py

from __future__ import annotations

import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """
    Custom formatter that outputs log records as JSON.
    
    Includes trace_id for correlation across the system.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add trace_id if present
        if hasattr(record, "trace_id"):
            log_obj["trace_id"] = record.trace_id

        # Add extra fields
        if hasattr(record, "extra_fields"):
            log_obj.update(record.extra_fields)

        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj)


def setup_logging(
    log_dir: Path | str = Path("logs"),
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    log_level: str = "INFO",
    enable_console: bool = True,
) -> None:
    """
    Configure structured logging for the gateway.

    Creates two handlers:
    - File handler: JSON format with rotation (for machines/analysis)
    - Console handler: Human-readable format (for development)

    Args:
        log_dir: Directory for log files
        max_bytes: Maximum size per log file before rotation (default: 10MB)
        backup_count: Number of backup files to keep (default: 5)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        enable_console: Whether to output to console as well
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Clear existing handlers to avoid duplicates
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Set root level
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # File handler with JSON formatting and rotation
    file_handler = RotatingFileHandler(
        log_path / "gateway.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(file_handler)

    # Console handler with simple formatting
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "[%(levelname)s] %(name)s: %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Usage:
        logger = get_logger(__name__)
        logger.info("Message", extra={"trace_id": trace.trace_id})
    """
    return logging.getLogger(name)


class TraceLoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter that automatically includes trace_id in all log records.

    Usage:
        trace_logger = TraceLoggerAdapter(logger, {"trace_id": trace.trace_id})
        trace_logger.info("Policy decision", extra_fields={"allowed": True})
    """

    def process(self, msg: str, kwargs: Any) -> tuple[str, Any]:
        # Inject trace_id from context
        if "extra" not in kwargs:
            kwargs["extra"] = {}

        # Safely get trace_id from self.extra
        if isinstance(self.extra, dict):
            kwargs["extra"]["trace_id"] = self.extra.get("trace_id")

        # Handle extra_fields
        if "extra_fields" in kwargs:
            kwargs["extra"]["extra_fields"] = kwargs.pop("extra_fields")

        return msg, kwargs

