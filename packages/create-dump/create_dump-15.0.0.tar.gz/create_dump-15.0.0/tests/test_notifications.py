# tests/test_notifications.py

import pytest
from unittest.mock import AsyncMock, patch
import httpx

from create_dump.notifications import (
    send_ntfy_notification,
    send_slack_notification,
    send_discord_notification,
    send_telegram_notification
)

@pytest.mark.asyncio
async def test_send_ntfy_notification_success(mocker):
    """
    Tests that send_ntfy_notification calls httpx.post with the correct arguments.
    """
    mock_post = mocker.patch("httpx.post", new_callable=AsyncMock)
    # Configure the mock to avoid 'coroutine not awaited' warnings on the sync method
    mock_post.return_value.raise_for_status = mocker.Mock()

    await send_ntfy_notification("test_topic", "test_message", "test_title")

    mock_post.assert_called_once_with(
        "https://ntfy.sh/test_topic",
        data=b"test_message",
        headers={"Title": "test_title"},
        timeout=10.0,
    )
    mock_post.return_value.raise_for_status.assert_called_once()

@pytest.mark.asyncio
async def test_send_ntfy_notification_http_error(mocker):
    """
    Tests that an httpx.HTTPStatusError is caught and logged.
    """
    mocker.patch(
        "httpx.post",
        side_effect=httpx.HTTPStatusError(
            "Error", request=AsyncMock(), response=AsyncMock()
        ),
    )
    mock_logger_warning = mocker.patch("create_dump.notifications.logger.warning")

    await send_ntfy_notification("test_topic", "test_message", "test_title")

    mock_logger_warning.assert_called_once()

@pytest.mark.asyncio
async def test_send_slack_notification(mocker):
    mock_post = mocker.patch("httpx.post", new_callable=AsyncMock)
    mock_post.return_value.raise_for_status = mocker.Mock()

    webhook = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
    await send_slack_notification(webhook, "Hello Slack")

    mock_post.assert_called_once_with(
        webhook,
        json={"text": "Hello Slack"},
        timeout=10.0
    )

@pytest.mark.asyncio
async def test_send_discord_notification(mocker):
    mock_post = mocker.patch("httpx.post", new_callable=AsyncMock)
    mock_post.return_value.raise_for_status = mocker.Mock()

    webhook = "https://discord.com/api/webhooks/XXX/YYY"
    await send_discord_notification(webhook, "Hello Discord")

    mock_post.assert_called_once_with(
        webhook,
        json={"content": "Hello Discord"},
        timeout=10.0
    )

@pytest.mark.asyncio
async def test_send_telegram_notification(mocker):
    mock_post = mocker.patch("httpx.post", new_callable=AsyncMock)
    mock_post.return_value.raise_for_status = mocker.Mock()

    chat_id = "123456789"
    token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    await send_telegram_notification(chat_id, token, "Hello Telegram")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    mock_post.assert_called_once_with(
        url,
        json={"chat_id": chat_id, "text": "Hello Telegram"},
        timeout=10.0
    )
