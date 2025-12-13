# Trading Service Utils

Shared utilities for the trading system microservices.

## Features

- **Logging**: Standardized logging configuration with hostname injection and health check filtering. [Read Documentation](docs/logging.md)
- **Fetcher**: API clients and helpers for various markets (Polymarket, etc.). [Read Documentation](docs/fetcher.md)

## Installation

```bash
pip install trading-service-utils
```

## Usage

### Logging

See [docs/logging.md](docs/logging.md) for full details.

```python
from trading_service_utils import setup_logging

setup_logging(log_level="INFO")
```

### Polymarket Fetcher

See [docs/fetcher.md](docs/fetcher.md) for full details.

```python
from trading_service_utils.fetcher import fetch_event

event = fetch_event("event_id")
```
