# src/create_dump/notifications.py

import anyio
import httpx
from .logging import logger

async def send_ntfy_notification(topic: str, message: str, title: str):
    """Sends a simple, best-effort POST to ntfy.sh."""
    try:
        url = f"https://ntfy.sh/{topic}"
        response = await httpx.post(
            url,
            data=message.encode('utf-8'),
            headers={"Title": title},
            timeout=10.0,
        )
        response.raise_for_status()
        logger.info("Sent ntfy notification", topic=topic)
    except Exception as e:
        logger.warning("Failed to send ntfy notification", topic=topic, error=str(e))

async def send_slack_notification(webhook_url: str, message: str):
    """Sends a notification to Slack."""
    try:
        response = await httpx.post(
            webhook_url,
            json={"text": message},
            timeout=10.0,
        )
        response.raise_for_status()
        logger.info("Sent Slack notification")
    except Exception as e:
        logger.warning("Failed to send Slack notification", error=str(e))

async def send_discord_notification(webhook_url: str, message: str):
    """Sends a notification to Discord."""
    try:
        response = await httpx.post(
            webhook_url,
            json={"content": message},
            timeout=10.0,
        )
        response.raise_for_status()
        logger.info("Sent Discord notification")
    except Exception as e:
        logger.warning("Failed to send Discord notification", error=str(e))

async def send_telegram_notification(chat_id: str, bot_token: str, message: str):
    """Sends a notification to Telegram."""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        response = await httpx.post(
            url,
            json={"chat_id": chat_id, "text": message},
            timeout=10.0,
        )
        response.raise_for_status()
        logger.info("Sent Telegram notification")
    except Exception as e:
        logger.warning("Failed to send Telegram notification", error=str(e))
