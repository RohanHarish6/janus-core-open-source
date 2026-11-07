"""
Production Logging Configuration for Agentic Cityscape.
Directs structured logs to:
- Windows: %LOCALAPPDATA%\\JanusCore\\logs\\app.log
- Non-Windows / Fallback: ./logs/app.log
Supports rotating file handling (10MB per file, 5 backups) and structured JSON format.
"""

import json
import logging
import os
import platform
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict


class StructuredJsonFormatter(logging.Formatter):
    """Formats log records into machine-readable JSON payloads."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process_id": record.process,
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj, ensure_ascii=False)


def resolve_log_directory() -> Path:
    """Determines the appropriate local application data log path."""
    if platform.system() == "Windows":
        base = os.environ.get("LOCALAPPDATA")
        if base:
            target = Path(base) / "JanusCore" / "logs"
            try:
                target.mkdir(parents=True, exist_ok=True)
                return target
            except Exception:
                pass

    # Fallback to workspace local logs directory
    local_target = Path("./logs").resolve()
    local_target.mkdir(parents=True, exist_ok=True)
    return local_target


def setup_logging(
    level: int = logging.INFO,
    enable_json_file: bool = True,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> logging.Logger:
    """Configures rotating file handlers and console output."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers to prevent duplicates
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Console Handler (Human-readable)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_fmt = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_fmt)
    root_logger.addHandler(console_handler)

    # Rotating File Handler
    if enable_json_file:
        log_dir = resolve_log_directory()
        log_file = log_dir / "app.log"
        try:
            file_handler = RotatingFileHandler(
                filename=str(log_file),
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8"
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(StructuredJsonFormatter())
            root_logger.addHandler(file_handler)
        except Exception as e:
            root_logger.warning(f"Could not initialize rotating log file at {log_file}: {e}")

    logger = logging.getLogger("JanusCore")
    logger.info("Logging subsystem initialized successfully.")
    return logger
