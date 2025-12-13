"""Tests for notification services."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from trading_service_utils.notification.telegram import TelegramNotifier
from trading_service_utils.notification.service import StandardNotificationService


# --- TelegramNotifier Tests ---

@pytest.mark.asyncio
async def test_notifier_init_with_token():
    """Test initializing notifier with a token."""
    with patch("trading_service_utils.notification.telegram.Bot") as MockBot:
        notifier = TelegramNotifier(token="test_token")
        MockBot.assert_called_once_with(token="test_token")
        assert notifier.bot is not None


def test_notifier_init_without_token():
    """Test initializing notifier without a token."""
    notifier = TelegramNotifier(token="")
    assert notifier.bot is None


@pytest.mark.asyncio
async def test_notifier_send_message():
    """Test sending a message."""
    with patch("trading_service_utils.notification.telegram.Bot") as MockBot:
        mock_bot_instance = MockBot.return_value
        mock_bot_instance.send_message = AsyncMock()
        
        notifier = TelegramNotifier(token="test_token", default_chat_id="123")
        await notifier.send_message("test message")
        
        mock_bot_instance.send_message.assert_called_once_with(
            chat_id="123",
            text="test message",
            parse_mode="Markdown"
        )


@pytest.mark.asyncio
async def test_notifier_send_message_override_chat_id():
    """Test sending a message with overridden chat ID."""
    with patch("trading_service_utils.notification.telegram.Bot") as MockBot:
        mock_bot_instance = MockBot.return_value
        mock_bot_instance.send_message = AsyncMock()
        
        notifier = TelegramNotifier(token="test_token", default_chat_id="123")
        await notifier.send_message("test message", chat_id="456")
        
        mock_bot_instance.send_message.assert_called_once_with(
            chat_id="456",
            text="test message",
            parse_mode="Markdown"
        )


@pytest.mark.asyncio
async def test_notifier_send_message_no_bot():
    """Test sending message when bot is not initialized."""
    notifier = TelegramNotifier(token="")
    # Should not raise error
    await notifier.send_message("test")


@pytest.mark.asyncio
async def test_notifier_send_message_no_chat_id():
    """Test sending message when no chat ID is provided."""
    with patch("trading_service_utils.notification.telegram.Bot") as MockBot:
        notifier = TelegramNotifier(token="test_token")
        # Should not raise error and not call send_message
        await notifier.send_message("test")
        notifier.bot.send_message.assert_not_called()


# --- StandardNotificationService Tests ---

@pytest.fixture
def mock_notifier():
    with patch("trading_service_utils.notification.service.TelegramNotifier") as MockNotifier:
        mock_instance = MockNotifier.return_value
        yield mock_instance


@pytest.mark.asyncio
async def test_service_startup(mock_notifier):
    """Test sending startup notification."""
    service = StandardNotificationService(token="t", chat_id="c", service_name="TestSvc")
    
    await service.send_startup("1.0", "PROD")
    
    mock_notifier.send_message_background.assert_called_once()
    args = mock_notifier.send_message_background.call_args[0]
    msg = args[0]
    assert "Service: `TestSvc`" in msg
    assert "Version: `1.0`" in msg
    assert "Environment: `PROD`" in msg
    assert "🚀 **Service Started**" in msg


@pytest.mark.asyncio
async def test_service_startup_with_extra_info(mock_notifier):
    """Test sending startup notification with extra info."""
    service = StandardNotificationService(token="t", chat_id="c", service_name="TestSvc")
    
    await service.send_startup("1.0", "PROD", extra_info={"Config": "A"})
    
    mock_notifier.send_message_background.assert_called_once()
    msg = mock_notifier.send_message_background.call_args[0][0]
    assert "Config: `A`" in msg


@pytest.mark.asyncio
async def test_service_signal(mock_notifier):
    """Test sending signal notification."""
    service = StandardNotificationService(token="t", chat_id="c")
    
    signal_data = {"symbol": "BTC", "price": 100}
    await service.send_signal("Buy Signal", signal_data)
    
    mock_notifier.send_message_background.assert_called_once()
    msg = mock_notifier.send_message_background.call_args[0][0]
    assert "🚨 **Buy Signal**" in msg
    assert "Symbol: `BTC`" in msg
    assert "Price: `100`" in msg


@pytest.mark.asyncio
async def test_service_info(mock_notifier):
    """Test sending info notification."""
    service = StandardNotificationService(token="t", chat_id="c")
    
    await service.send_info("Status Update", {"Status": "OK"})
    
    mock_notifier.send_message_background.assert_called_once()
    msg = mock_notifier.send_message_background.call_args[0][0]
    assert "ℹ️ **Status Update**" in msg
    assert "Status: `OK`" in msg


@pytest.mark.asyncio
async def test_service_warning(mock_notifier):
    """Test sending warning notification."""
    service = StandardNotificationService(token="t", chat_id="c")
    
    await service.send_warning("Disk Space", "Low disk space")
    
    mock_notifier.send_message_background.assert_called_once()
    msg = mock_notifier.send_message_background.call_args[0][0]
    assert "⚠️ **Disk Space**" in msg
    assert "Low disk space" in msg


@pytest.mark.asyncio
async def test_service_error(mock_notifier):
    """Test sending error notification."""
    service = StandardNotificationService(token="t", chat_id="c")
    
    await service.send_error("DB Error", "Connection failed")
    
    mock_notifier.send_message_background.assert_called_once()
    msg = mock_notifier.send_message_background.call_args[0][0]
    assert "❌ **DB Error**" in msg
    assert "Error: `Connection failed`" in msg
