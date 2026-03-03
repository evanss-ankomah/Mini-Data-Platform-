"""
Structured JSON logging helper for the ETL pipeline.

Features:
- JSON-formatted log lines with consistent fields
- Contextual logging (task, dag_run, file_key in every line)
- Thread-safe context manager for per-file log enrichment
"""
import json
import logging
import threading
from contextlib import contextmanager
from datetime import datetime, timezone


# Thread-local storage for per-file context
_log_context = threading.local()


class StructuredFormatter(logging.Formatter):
    """Formats log records as JSON lines for structured logging."""

    def format(self, record):
        # Merge thread-local context with record extras
        ctx = getattr(_log_context, "data", {})

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "task": getattr(record, "task_name", ctx.get("task_name", "unknown")),
            "dag_run": getattr(record, "dag_run_id", ctx.get("dag_run_id", "unknown")),
            "file_key": getattr(record, "file_key", ctx.get("file_key", "")),
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def get_logger(name: str) -> logging.Logger:
    """Create a structured JSON logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


@contextmanager
def log_context(**kwargs):
    """
    Context manager that enriches all log lines within the block
    with additional fields (e.g., file_key, dag_run_id, task_name).

    Usage:
        with log_context(file_key="sales/orders.csv", dag_run_id="run_123"):
            logger.info("Processing file")  # automatically includes file_key and dag_run_id
    """
    prev = getattr(_log_context, "data", {})
    _log_context.data = {**prev, **kwargs}
    try:
        yield
    finally:
        _log_context.data = prev
