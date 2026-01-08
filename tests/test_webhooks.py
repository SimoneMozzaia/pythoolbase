from __future__ import annotations

import types

import pytest

import pytoolbase.webhooks as wh


class _Resp:
    def __init__(self, status_code: int = 200, text: str = "ok"):
        self.status_code = status_code
        self.text = text

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError("http error")


def test_send_google_chat_message(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {}

    def fake_post(url, json=None, timeout=None):
        calls["url"] = url
        calls["json"] = json
        calls["timeout"] = timeout
        return _Resp()

    monkeypatch.setattr(wh.requests, "post", fake_post)

    resp = wh.send_google_chat_message("http://example", "hello", timeout=3)
    assert resp.status_code == 200
    assert calls["json"] == {"text": "hello"}
    assert calls["timeout"] == 3


def test_send_teams_message(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {}

    def fake_post(url, json=None, timeout=None):
        calls["url"] = url
        calls["json"] = json
        calls["timeout"] = timeout
        return _Resp()

    monkeypatch.setattr(wh.requests, "post", fake_post)

    resp = wh.send_teams_message("http://example", "hello", timeout=5)
    assert resp.status_code == 200
    assert calls["json"] == {"text": "hello"}
    assert calls["timeout"] == 5
