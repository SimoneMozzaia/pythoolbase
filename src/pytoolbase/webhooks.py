from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class WebhookResponse:
    status_code: int
    text: str


def send_google_chat_message(webhook_url: str, text: str, *, timeout: int = 10) -> WebhookResponse:
    """Send a plain-text message to Google Chat via incoming webhook."""
    if not webhook_url.strip():
        raise ValueError("webhook_url must be non-empty")
    if not text.strip():
        raise ValueError("text must be non-empty")

    resp = requests.post(webhook_url, json={"text": text}, timeout=timeout)
    resp.raise_for_status()
    return WebhookResponse(status_code=resp.status_code, text=resp.text)


def send_teams_message(webhook_url: str, text: str, *, timeout: int = 10) -> WebhookResponse:
    """Send a plain-text message to Microsoft Teams via incoming webhook."""
    if not webhook_url.strip():
        raise ValueError("webhook_url must be non-empty")
    if not text.strip():
        raise ValueError("text must be non-empty")

    # Confirmed payload: {"text": "..."}
    resp = requests.post(webhook_url, json={"text": text}, timeout=timeout)
    resp.raise_for_status()
    return WebhookResponse(status_code=resp.status_code, text=resp.text)
