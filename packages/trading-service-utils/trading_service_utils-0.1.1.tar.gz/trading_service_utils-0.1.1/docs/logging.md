# Logging Utilities

The logging module provides a standardized logging configuration for all trading microservices. It is designed to work well in a Kubernetes environment.

## Features

- **Hostname Injection**: Automatically injects the pod hostname into every log record. This is crucial for distinguishing logs from different pods in a centralized logging system (like Grafana/Loki).
- **Health Check Filtering**: Automatically filters out access logs for the `/health` endpoint to prevent log spam from Kubernetes probes.
- **Unified Formatting**: Enforces a consistent log format across all services.

## Usage

In your application's entry point (e.g., `app.py` or `main.py`), import and call `setup_logging`.

```python
from trading_service_utils import setup_logging
from signal_crypto_endgame_trading.config import settings

# Configure logging with the service's log level
setup_logging(log_level=settings.LOG_LEVEL)
```

### Customizing Ignored Paths

By default, `GET /health` is ignored. You can customize this by passing a list of paths to `ignored_paths`.

```python
setup_logging(
    log_level="DEBUG",
    ignored_paths=["GET /health", "GET /metrics"]
)
```

## Log Format

The default log format is:

```text
%(asctime)s - [%(hostname)s] - %(name)s - %(levelname)s - %(message)s
```

Example output:

```text
2025-12-06 15:30:00 - [signal-crypto-endgame-trading-76f8bz55vh] - uvicorn.access - INFO - 10.42.0.1:56902 - "GET /api/hello HTTP/1.1" 200 OK
```
