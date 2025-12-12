"""
Reusable logging module for C1G projects.

Provides a configurable logger with:
- Colorized console output via Rich
- Optional file logging
- Configurable log levels and formats
"""

import logging
from pathlib import Path
from typing import Literal

from rich.console import Console
from rich.logging import RichHandler

try:
    import google.cloud.logging
    from google.cloud.logging.handlers import CloudLoggingHandler

    HAS_CLOUD_LOGGING = True
except ImportError:
    HAS_CLOUD_LOGGING = False

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

DEFAULT_FORMAT = "%(message)s"
DEFAULT_FILE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_logger(
    name: str,
    level: LogLevel = "INFO",
    console_format: str = DEFAULT_FORMAT,
    file_format: str = DEFAULT_FILE_FORMAT,
    log_dir: str | Path | None = None,
    log_filename: str | None = None,
) -> logging.Logger:
    """
    Create and configure a logger with colorized console output and optional file logging.

    Args:
        name: Logger name (typically __name__ of the calling module).
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        console_format: Format string for console output.
        file_format: Format string for file output.
        log_dir: Directory for log files. If None, file logging is disabled.
        log_filename: Log file name. Defaults to "{name}.log" if log_dir is provided.

    Returns:
        Configured logging.Logger instance.

    Example:
        >>> from c1gpy.logging import get_logger
        >>> logger = get_logger(__name__, level="DEBUG", log_dir="./logs")
        >>> logger.info("Application started")
        >>> logger.debug("Debug information")
        >>> logger.error("Something went wrong")
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))

    # Avoid adding duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # Rich console handler with colors
    console = Console(stderr=True)
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        markup=True,
    )
    rich_handler.setFormatter(logging.Formatter(console_format))
    rich_handler.setLevel(getattr(logging, level))
    logger.addHandler(rich_handler)

    # File handler (optional)
    if log_dir is not None:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        filename = log_filename or f"{name.replace('.', '_')}.log"
        file_handler = logging.FileHandler(log_path / filename)
        file_handler.setFormatter(logging.Formatter(file_format))
        file_handler.setLevel(getattr(logging, level))
        logger.addHandler(file_handler)

    # Prevent propagation to root logger to avoid duplicate logs
    logger.propagate = False

    return logger


class C1GLogger:
    """
    Logger class for C1G projects with fluent configuration.

    Example:
        >>> from c1gpy.logging import C1GLogger
        >>> logger = C1GLogger("my_app").with_file_logging("./logs").build()
        >>> logger.info("Hello, World!")
    """

    def __init__(
        self,
        name: str,
        level: LogLevel = "INFO",
    ) -> None:
        self._name = name
        self._level = level
        self._console_format = DEFAULT_FORMAT
        self._file_format = DEFAULT_FILE_FORMAT
        self._log_dir: Path | None = None
        self._log_filename: str | None = None

    def with_level(self, level: LogLevel) -> "C1GLogger":
        """Set the log level."""
        self._level = level
        return self

    def with_console_format(self, fmt: str) -> "C1GLogger":
        """Set the console output format."""
        self._console_format = fmt
        return self

    def with_file_format(self, fmt: str) -> "C1GLogger":
        """Set the file output format."""
        self._file_format = fmt
        return self

    def with_file_logging(
        self, log_dir: str | Path, filename: str | None = None
    ) -> "C1GLogger":
        """Enable file logging to the specified directory."""
        self._log_dir = Path(log_dir)
        self._log_filename = filename
        return self

    def build(self) -> logging.Logger:
        """Build and return the configured logger."""
        return get_logger(
            name=self._name,
            level=self._level,
            console_format=self._console_format,
            file_format=self._file_format,
            log_dir=self._log_dir,
            log_filename=self._log_filename,
        )


def get_cloud_logger(
    name: str,
    level: LogLevel = "INFO",
    log_format: str = DEFAULT_FILE_FORMAT,
) -> logging.Logger:
    """
    Create a logger configured for Google Cloud Logging.

    Logs are sent to Google Cloud Logging and can be viewed in the GCP Console.
    Requires google-cloud-logging package and proper GCP authentication.

    Args:
        name: Logger name (typically __name__ of the calling module).
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_format: Format string for log messages.

    Returns:
        Configured logging.Logger instance for Google Cloud.

    Raises:
        ImportError: If google-cloud-logging is not installed.

    Example:
        >>> from c1gpy.logging import get_cloud_logger
        >>> logger = get_cloud_logger(__name__, level="INFO")
        >>> logger.info("Application started")
        >>> logger.error("Something went wrong")  # Visible in GCP Error Reporting
    """
    if not HAS_CLOUD_LOGGING:
        raise ImportError(
            "google-cloud-logging is required for Cloud Logging. "
            "Install it with: pip install google-cloud-logging"
        )

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))

    # Avoid adding duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # Initialize Google Cloud Logging client
    client = google.cloud.logging.Client()

    # Cloud Logging handler
    cloud_handler = CloudLoggingHandler(client, name=name)
    cloud_handler.setFormatter(logging.Formatter(log_format))
    cloud_handler.setLevel(getattr(logging, level))
    logger.addHandler(cloud_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


class C1GCloudLogger:
    """
    Logger class for Google Cloud Logging with fluent configuration.

    Example:
        >>> from c1gpy.logging import C1GCloudLogger
        >>> logger = C1GCloudLogger("my_app").with_level("DEBUG").build()
        >>> logger.info("Hello from GCP!")
    """

    def __init__(
        self,
        name: str,
        level: LogLevel = "INFO",
    ) -> None:
        self._name = name
        self._level = level
        self._log_format = DEFAULT_FILE_FORMAT

    def with_level(self, level: LogLevel) -> "C1GCloudLogger":
        """Set the log level."""
        self._level = level
        return self

    def with_format(self, fmt: str) -> "C1GCloudLogger":
        """Set the log format."""
        self._log_format = fmt
        return self

    def build(self) -> logging.Logger:
        """Build and return the configured Cloud logger."""
        return get_cloud_logger(
            name=self._name,
            level=self._level,
            log_format=self._log_format,
        )
