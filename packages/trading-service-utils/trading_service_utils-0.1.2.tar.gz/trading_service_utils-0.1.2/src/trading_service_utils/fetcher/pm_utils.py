"""Polymarket utility functions module."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any


def parse_token_ids(raw_token_ids: Any) -> list[str]:
    """Parse yes/no token identifiers from a Polymarket market payload."""
    if isinstance(raw_token_ids, str):
        try:
            parsed = json.loads(raw_token_ids)
            return [str(token) for token in parsed]
        except json.JSONDecodeError:
            return []
    if isinstance(raw_token_ids, list):
        return [str(token) for token in raw_token_ids]
    return []


def _parse_iso_datetime(value: str | None) -> datetime | None:
    """Parse ISO datetime string to datetime object."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def is_event_active(event: dict[str, Any]) -> bool:
    """Check if an event is open and not expired."""
    if event.get("closed", False):
        return False

    end_date = _parse_iso_datetime(event.get("endDate"))
    now = datetime.now(timezone.utc)
    if end_date and end_date <= now:
        return False

    return True


def format_market_summary(market: dict[str, Any]) -> dict[str, Any]:
    """Extract relevant fields from a market payload."""
    token_ids = parse_token_ids(market.get("clobTokenIds"))
    return {
        "market_id": market.get("id", ""),
        "question": market.get("question"),
        "groupItemTitle": market.get("groupItemTitle"),
        "outcomes": market.get("outcomes"),
        "outcomePrices": market.get("outcomePrices"),
        "active": market.get("active"),
        "closed": market.get("closed"),
        "yes_token": token_ids[0] if len(token_ids) > 0 else "",
        "no_token": token_ids[1] if len(token_ids) > 1 else "",
    }
