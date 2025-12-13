"""Telegram notification service."""

import asyncio
import logging
from typing import Optional

from telegram import Bot  # type: ignore

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Generic Telegram notification service."""

    def __init__(
        self, token: str, default_chat_id: Optional[str] = None
    ) -> None:
        """Initialize the Telegram notifier.

        Args:
            token: Telegram Bot Token.
            default_chat_id: Default Chat ID to send messages to.
        """
        self.token = token
        self.default_chat_id = default_chat_id
        self.bot: Optional[Bot] = None

        if self.token:
            try:
                self.bot = Bot(token=self.token)
            except Exception as e:
                logger.error("Failed to initialize Telegram bot: %s", e)
        else:
            logger.warning(
                "No Telegram token provided. Notifications disabled."
            )

    async def send_message(
        self,
        message: str,
        chat_id: Optional[str] = None,
        parse_mode: str = "Markdown",
    ) -> None:
        """Send a message via Telegram asynchronously.

        Args:
            message: The message text to send.
            chat_id: Override default chat ID.
            parse_mode: Parse mode for the message (default: Markdown).
        """
        target_chat_id = chat_id or self.default_chat_id

        if not self.bot:
            logger.debug("Notification skipped: Bot not initialized")
            return

        if not target_chat_id:
            logger.debug("Notification skipped: No chat ID provided")
            return

        try:
            # Run in a separate task to avoid blocking if not already in one
            await self.bot.send_message(
                chat_id=target_chat_id,
                text=message,
                parse_mode=parse_mode,
            )
            logger.debug("Notification sent to %s", target_chat_id)
        except Exception as e:
            logger.error("Failed to send notification: %s", e)

    def send_message_background(
        self,
        message: str,
        chat_id: Optional[str] = None,
        parse_mode: str = "Markdown",
    ) -> None:
        """Send a message in the background (fire and forget).

        Args:
            message: The message text to send.
            chat_id: Override default chat ID.
            parse_mode: Parse mode for the message.
        """
        asyncio.create_task(
            self.send_message(message, chat_id, parse_mode)
        )
