"""
Custom exception hierarchy for the ETL pipeline.
Provides rich error classification for logging, alerting, and retry decisions.
"""


class ETLError(Exception):
    """Base class for all ETL pipeline errors."""

    def __init__(self, message: str, file_key: str = "", step: str = ""):
        self.file_key = file_key
        self.step = step
        super().__init__(message)


class ExtractionError(ETLError):
    """Raised when file discovery or download from MinIO fails."""
    pass


class ValidationError(ETLError):
    """Raised when schema validation encounters unrecoverable issues."""
    pass


class TransformationError(ETLError):
    """Raised when data transformation fails."""
    pass


class LoadError(ETLError):
    """Raised when PostgreSQL load/upsert fails after retries."""
    pass


class AuditError(ETLError):
    """Raised when audit table write fails."""
    pass


class FileMoveError(ETLError):
    """Raised when moving files in MinIO fails."""
    pass


class ConnectionError(ETLError):
    """Raised when a service connection cannot be established."""
    pass
