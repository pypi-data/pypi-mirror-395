"""Polymarket API client module."""

from __future__ import annotations

from typing import Any, cast

import requests

API_BASE_URL = "https://gamma-api.polymarket.com"
SERIES_API_URL = f"{API_BASE_URL}/series/{{series_id}}"
EVENT_API_URL = f"{API_BASE_URL}/events/{{event_id}}"
EVENT_SLUG_API_URL = f"{API_BASE_URL}/events/slug/{{slug}}"


def _fetch_json(url: str, timeout: int = 30) -> dict[str, Any]:
    """Helper to perform a GET request and return JSON."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


def fetch_series(series_id: int) -> dict[str, Any]:
    """Fetch full series payload by ID."""
    return _fetch_json(SERIES_API_URL.format(series_id=series_id))


def fetch_event(event_id: str | int) -> dict[str, Any]:
    """Fetch full event payload by ID."""
    return _fetch_json(EVENT_API_URL.format(event_id=event_id))


def fetch_event_by_slug(slug: str) -> dict[str, Any]:
    """Fetch full event payload by slug."""
    return _fetch_json(EVENT_SLUG_API_URL.format(slug=slug))
