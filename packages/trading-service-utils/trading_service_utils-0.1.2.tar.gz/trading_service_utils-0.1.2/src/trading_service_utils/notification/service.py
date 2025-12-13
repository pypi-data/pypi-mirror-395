"""Standard notification service implementation."""

import logging
from typing import Any, Optional

from .telegram import TelegramNotifier

logger = logging.getLogger(__name__)


class StandardNotificationService:
    """Standard notification service for trading applications.
    
    Provides high-level methods for common notification patterns
    (startup, signals, status updates) using a notifier backend.
    """

    def __init__(
        self,
        token: str,
        chat_id: Optional[str] = None,
        service_name: str = "Unknown Service",
    ) -> None:
        """Initialize the standard notification service.

        Args:
            token: Telegram Bot Token.
            chat_id: Default Chat ID.
            service_name: Name of the service using this notifier.
        """
        self.service_name = service_name
        self.notifier = TelegramNotifier(token=token, default_chat_id=chat_id)

    def _format_data(self, data: dict[str, Any]) -> str:
        """Format dictionary data into a readable string block."""
        lines = []
        for k, v in data.items():
            # Convert keys like "signal_type" to "Signal Type"
            key_display = k.replace("_", " ").title()
            lines.append(f"{key_display}: `{v}`")
        return "\n".join(lines)

    async def send_startup(
        self,
        version: str,
        environment: str,
        extra_info: Optional[dict[str, Any]] = None,
    ) -> None:
        """Send service startup notification."""
        info_block = (
            f"Service: `{self.service_name}`\n"
            f"Version: `{version}`\n"
            f"Environment: `{environment}`"
        )
        
        if extra_info:
            info_block += "\n" + self._format_data(extra_info)

        msg = f"🚀 **Service Started**\n\n{info_block}"
        self.notifier.send_message_background(msg)

    async def send_signal(
        self, title: str, signal_data: dict[str, Any]
    ) -> None:
        """Send a trading signal alert."""
        details = self._format_data(signal_data)
        msg = f"🚨 **{title}**\n\n{details}"
        self.notifier.send_message_background(msg)

    async def send_info(self, title: str, info_data: dict[str, Any]) -> None:
        """Send a general information/status update."""
        details = self._format_data(info_data)
        msg = f"ℹ️ **{title}**\n\n{details}"
        self.notifier.send_message_background(msg)

    async def send_warning(self, title: str, message: str) -> None:
        """Send a warning message."""
        msg = f"⚠️ **{title}**\n\n{message}"
        self.notifier.send_message_background(msg)

    async def send_error(self, title: str, error: str) -> None:
        """Send an error message."""
        msg = f"❌ **{title}**\n\nError: `{error}`"
        self.notifier.send_message_background(msg)
    
    async def send_custom_message(self, message: str) -> None:
        """Send a raw custom message."""
        self.notifier.send_message_background(message)
