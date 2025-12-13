"""Polymarket data fetcher module."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .pm_api import fetch_event, fetch_event_by_slug, fetch_series
from .pm_utils import format_market_summary, is_event_active


def get_event_summary_with_slug(slug: str) -> dict[str, Any]:
    """Fetch event by slug and return a summary with active markets."""
    payload = fetch_event_by_slug(slug)

    active_markets = []
    for market in payload.get("markets", []):
        if market.get("active") and not market.get("closed"):
            active_markets.append(format_market_summary(market))

    return {
        "event_id": payload.get("id"),
        "series_id": payload.get("seriesId"),
        "markets": active_markets,
    }


def get_series_open_events_with_id(series_id: int) -> list[dict[str, Any]]:
    """Fetch all open events for a series, enriched with market details."""
    series_payload = fetch_series(series_id)

    enriched_events = []
    for series_event in series_payload.get("events", []):
        if not is_event_active(series_event):
            continue

        event_id = series_event.get("id")
        if not event_id:
            continue

        detailed_event = fetch_event(event_id)

        markets_payload = [
            format_market_summary(market)
            for market in detailed_event.get("markets", [])
            if market.get("active", False) and not market.get("closed", False)
        ]

        enriched_events.append(
            {
                "event_id": detailed_event.get("id", series_event.get("id")),
                "title": detailed_event.get("title", series_event.get("title")),
                "slug": detailed_event.get("slug", series_event.get("slug")),
                "startDate": detailed_event.get(
                    "startDate", series_event.get("startDate")
                ),
                "endDate": detailed_event.get("endDate", series_event.get("endDate")),
                "seriesSnapshot": {
                    "ticker": series_event.get("ticker"),
                    "volume": series_event.get("volume"),
                    "liquidity": series_event.get("liquidity"),
                },
                "markets": markets_payload,
            }
        )

    return enriched_events


def _series_file(series_id: int) -> Path:
    return Path(__file__).parent / f"series_{series_id}.json"


def _open_events_file(series_id: int) -> Path:
    return Path(__file__).parent / f"series_{series_id}_open_events.json"


def fetch_series_to_json(
    series_id: int,
    output_path: Path | None = None,
) -> Path:
    """Fetch series data by id and persist result as JSON."""
    data = fetch_series(series_id)
    target_path = Path(output_path) if output_path else _series_file(series_id)
    target_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return target_path


def extract_open_events(
    series_id: int,
    series_json_path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    """Load the cached series JSON and persist all open events."""
    source_path = (
        Path(series_json_path) if series_json_path else _series_file(series_id)
    )
    series_payload = json.loads(source_path.read_text(encoding="utf-8"))

    open_events = [
        event for event in series_payload.get("events", []) if is_event_active(event)
    ]

    target_path = Path(output_path) if output_path else _open_events_file(series_id)
    target_path.write_text(json.dumps(open_events, indent=2), encoding="utf-8")
    return target_path


def export_event_market_tokens(
    event_id: str,
    output_path: Path | None = None,
) -> Path:
    """Fetch event detail and export readable market/token mappings."""
    event_payload = fetch_event(event_id)

    markets_data = [
        format_market_summary(market) for market in event_payload.get("markets", [])
    ]

    readable_payload = {
        "event_id": event_payload.get("id", event_id),
        "title": event_payload.get("title"),
        "slug": event_payload.get("slug"),
        "startDate": event_payload.get("startDate"),
        "endDate": event_payload.get("endDate"),
        "markets": markets_data,
    }

    target_path = (
        Path(output_path)
        if output_path
        else Path(__file__).parent / f"event_{event_id}_market_tokens.json"
    )
    target_path.write_text(json.dumps(readable_payload, indent=2), encoding="utf-8")
    return target_path
