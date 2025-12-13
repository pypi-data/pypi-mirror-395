"""Tests for the fetcher module."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from trading_service_utils.fetcher.pm_fetcher import (
    get_event_summary_with_slug,
    get_series_open_events_with_id,
)
from trading_service_utils.fetcher.pm_utils import (
    format_market_summary,
    is_event_active,
    parse_token_ids,
)


def test_parse_token_ids_handles_stringified_list() -> None:
    """Test that parse_token_ids correctly handles a stringified list of tokens."""
    tokens = parse_token_ids('["yes-token","no-token"]')
    assert tokens == ["yes-token", "no-token"]


def test_format_market_summary_extracts_tokens() -> None:
    """Test that format_market_summary correctly extracts token IDs."""
    market = {
        "id": "m1",
        "question": "Q?",
        "groupItemTitle": "T",
        "outcomes": ["Y", "N"],
        "outcomePrices": ["0.1", "0.9"],
        "active": True,
        "closed": False,
        "clobTokenIds": '["token_y", "token_n"]',
    }
    summary = format_market_summary(market)

    assert summary["market_id"] == "m1"
    assert summary["yes_token"] == "token_y"
    assert summary["no_token"] == "token_n"
    assert summary["active"] is True


def test_format_market_summary_handles_missing_tokens() -> None:
    """Test that format_market_summary handles missing token IDs gracefully."""
    market = {"id": "m1", "clobTokenIds": "[]"}
    summary = format_market_summary(market)
    assert summary["yes_token"] == ""
    assert summary["no_token"] == ""


def test_is_event_active_filters_closed_and_expired() -> None:
    """Test that is_event_active correctly filters closed and expired events."""
    now = datetime.now(timezone.utc)

    active_event = {
        "id": "active",
        "closed": False,
        "endDate": (now + timedelta(days=1)).isoformat(),
    }
    assert is_event_active(active_event) is True

    closed_event = {
        "id": "closed",
        "closed": True,
        "endDate": (now + timedelta(days=1)).isoformat(),
    }
    assert is_event_active(closed_event) is False

    expired_event = {
        "id": "expired",
        "closed": False,
        "endDate": (now - timedelta(days=1)).isoformat(),
    }
    assert is_event_active(expired_event) is False


@patch("trading_service_utils.fetcher.pm_fetcher.fetch_series")
@patch("trading_service_utils.fetcher.pm_fetcher.fetch_event")
def test_get_series_open_events_enriches_markets(
    mock_fetch_event, mock_fetch_series
) -> None:
    """Test that get_series_open_events_with_id enriches events with market details."""
    future = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()

    # Mock Series Response
    mock_fetch_series.return_value = {
        "events": [
            {
                "id": "evt-1",
                "title": "Series Level Title",
                "slug": "series-level",
                "startDate": future,
                "endDate": future,
                "ticker": "PM99",
                "volume": "100",
                "liquidity": "50",
                "closed": False,
            }
        ]
    }

    # Mock Event Detail Response
    mock_fetch_event.return_value = {
        "id": "evt-1",
        "title": "Detailed Title",
        "slug": "detailed",
        "startDate": future,
        "endDate": future,
        "markets": [
            {
                "id": "m-active",
                "question": "Will it rain?",
                "groupItemTitle": "Weather",
                "active": True,
                "closed": False,
                "clobTokenIds": '["yes","no"]',
            },
            {
                "id": "m-closed",
                "active": False,
                "closed": True,
                "clobTokenIds": '["x","y"]',
            },
        ],
    }

    events = get_series_open_events_with_id(series_id=99)

    assert len(events) == 1
    event = events[0]
    assert event["event_id"] == "evt-1"
    assert event["markets"] == [
        {
            "market_id": "m-active",
            "question": "Will it rain?",
            "groupItemTitle": "Weather",
            "outcomes": None,
            "outcomePrices": None,
            "active": True,
            "closed": False,
            "yes_token": "yes",
            "no_token": "no",
        }
    ]


@patch("trading_service_utils.fetcher.pm_fetcher.fetch_event_by_slug")
def test_get_event_summary_returns_active_markets(mock_fetch_slug) -> None:
    """Test that get_event_summary_with_slug returns only active markets."""
    mock_fetch_slug.return_value = {
        "id": "evt-slug-1",
        "seriesId": 123,
        "markets": [
            {
                "id": "m-1",
                "question": "Q1",
                "groupItemTitle": "T1",
                "outcomes": ["Yes", "No"],
                "outcomePrices": ["0.5", "0.5"],
                "active": True,
                "closed": False,
                "clobTokenIds": '["y1", "n1"]',
            },
            {
                "id": "m-2",
                "active": False,
                "closed": True,
            },
        ],
    }

    summary = get_event_summary_with_slug("some-slug")

    assert summary["event_id"] == "evt-slug-1"
    assert summary["series_id"] == 123
    assert len(summary["markets"]) == 1
    assert summary["markets"][0]["market_id"] == "m-1"
    assert summary["markets"][0]["yes_token"] == "y1"
