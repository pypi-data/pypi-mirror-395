"""
Structured logging for UAA.

Provides JSON-formatted logs with execution context.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict


class StructuredFormatter(logging.Formatter):
    """JSON-formatted log output with execution context."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add execution context if available
        if hasattr(record, "execution_id"):
            log_data["execution_id"] = record.execution_id
        if hasattr(record, "graph_name"):
            log_data["graph_name"] = record.graph_name
        if hasattr(record, "adapter"):
            log_data["adapter"] = record.adapter

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_structured_logging(level: str = "INFO", json_format: bool = True) -> None:
    """
    Configure structured logging for UAA.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        json_format: Use JSON formatting (default: True)
    """
    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)

    # Set formatter
    if json_format:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    handler.setFormatter(formatter)

    # Configure root logger
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, level.upper()))

    # Configure UAA loggers
    for logger_name in [
        "universal_agent_nexus",
        "universal_agent",
    ]:
        uaa_logger = logging.getLogger(logger_name)
        uaa_logger.setLevel(getattr(logging, level.upper()))

    logging.info(
        "Structured logging initialized: level=%s, json=%s", level, json_format
    )

