"""Logging utilities for the application."""

import logging
import socket


class EndpointFilter(logging.Filter):
    """Filter out logs for specific endpoints (e.g. health checks)."""

    def __init__(self, path: str):
        """Initialize the filter with a path to ignore."""
        super().__init__()
        self.path = path

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out log records containing the ignored path."""
        return record.getMessage().find(self.path) == -1


class HostnameFilter(logging.Filter):
    """Inject hostname into log records."""

    hostname = socket.gethostname()

    def filter(self, record: logging.LogRecord) -> bool:
        """Inject the hostname into the log record."""
        record.hostname = self.hostname
        return True


def setup_logging(
    log_level: str = "INFO", ignored_paths: list[str] | None = None
) -> None:
    """Configure logging with hostname and endpoint filtering.

    Args:
        log_level: The logging level (default: "INFO")
        ignored_paths: List of paths to ignore in access logs (default: ["GET /health"])
    """
    if ignored_paths is None:
        ignored_paths = ["GET /health"]

    # Define format with hostname
    log_format = "%(asctime)s - [%(hostname)s] - %(name)s - %(levelname)s - %(message)s"

    # 1. Configure Root Logger
    # We use force=True to override any existing configuration
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format=log_format,
        force=True,
    )

    hostname_filter = HostnameFilter()

    # Add filter to root logger handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(hostname_filter)

    # 2. Configure Uvicorn Loggers
    # We need to ensure Uvicorn loggers also use our format and filters
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
        logger = logging.getLogger(logger_name)
        logger.addFilter(hostname_filter)

        # Apply endpoint filtering to access logs
        if logger_name == "uvicorn.access":
            for path in ignored_paths:
                logger.addFilter(EndpointFilter(path))
