# Market Data Fetcher

The fetcher module provides API clients and helper functions for interacting with various prediction markets. Currently, it supports **Polymarket**.

## Polymarket Fetcher

The Polymarket fetcher allows you to retrieve event details, series data, and market tokens.

### Key Functions

All functions are available directly under `trading_service_utils.fetcher`.

#### `fetch_event(event_id: str | int)`
Fetches the full payload for a specific event by its ID.

#### `fetch_event_by_slug(slug: str)`
Fetches the full payload for a specific event by its slug.

#### `fetch_series(series_id: int)`
Fetches the full payload for a series (a collection of events).

#### `get_series_open_events_with_id(series_id: int)`
Fetches all *active* and *open* events for a given series. This is useful for scanning for new opportunities.

#### `export_event_market_tokens(event_id: str, output_path: Path | None = None)`
Fetches an event and exports a simplified JSON mapping of markets and their Yes/No tokens. Useful for configuration generation.

### Usage Examples

```python
from trading_service_utils.fetcher import (
    fetch_event,
    get_series_open_events_with_id
)

# 1. Fetch a single event
event = fetch_event("12345")
print(event["title"])

# 2. Scan a series for open events
# Example: Series ID 10016 (Bitcoin)
open_events = get_series_open_events_with_id(10016)

for event in open_events:
    print(f"Event: {event['title']}")
    for market in event['markets']:
        print(f"  - Market: {market['question']}")
        print(f"    Yes Token: {market['yes_token']}")
        print(f"    No Token:  {market['no_token']}")
```
