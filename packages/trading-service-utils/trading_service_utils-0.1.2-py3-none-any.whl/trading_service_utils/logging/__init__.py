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


class IdentityFilter(logging.Filter):
    """Inject hostname and service name into log records."""

    hostname = socket.gethostname()

    def __init__(self, service_name: str = "unknown-service"):
        """Initialize with service name."""
        super().__init__()
        self.service_name = service_name

    def filter(self, record: logging.LogRecord) -> bool:
        """Inject identity info into the log record."""
        record.hostname = self.hostname
        record.service_name = self.service_name
        return True


def setup_logging(
    log_level: str = "INFO",
    ignored_paths: list[str] | None = None,
    service_name: str = "unknown-service",
) -> None:
    """Configure logging with hostname, service name and endpoint filtering.

    Args:
        log_level: The logging level (default: "INFO")
        ignored_paths: List of paths to ignore in access logs
            (default: ["GET /health"])
        service_name: The name of the service for log identification
            (default: "unknown-service")
    """
    if ignored_paths is None:
        ignored_paths = ["GET /health"]

    # Define format with hostname and service name
    log_format = (
        "%(asctime)s - [%(hostname)s] - [%(service_name)s] - "
        "%(name)s - %(levelname)s - %(message)s"
    )

    # 1. Configure Root Logger
    # We use force=True to override any existing configuration
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format=log_format,
        force=True,
    )

    identity_filter = IdentityFilter(service_name=service_name)

    # Add filter to root logger handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(identity_filter)

    # 2. Configure Uvicorn Loggers
    # We need to ensure Uvicorn loggers also use our format and filters
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
        logger = logging.getLogger(logger_name)
        logger.addFilter(identity_filter)

        # Apply endpoint filtering to access logs
        if logger_name == "uvicorn.access":
            for path in ignored_paths:
                logger.addFilter(EndpointFilter(path))
