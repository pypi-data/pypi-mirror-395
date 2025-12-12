from __future__ import annotations

import os
from typing import List

import httpx

from ..models import ChatMessage


class OpenAIChatClient:
    """
    Minimal OpenAI-based implementation of ChatModelClient using raw HTTP.

    This avoids heavy dependencies and works cleanly with Python 3.12.
    It expects OPENAI_API_KEY to be set unless an explicit api_key is given.
    """

    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        api_key: str | None = None,
        base_url: str | None = None,
        timeout_seconds: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set and no api_key was provided."
            )

        self.model = model
        self.base_url = base_url or "https://api.openai.com/v1"
        self.timeout_seconds = timeout_seconds

    def complete(self, messages: List[ChatMessage]) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        with httpx.Client(base_url=self.base_url, timeout=self.timeout_seconds) as client:
            response = client.post("/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        choice = data["choices"][0]
        content = choice["message"]["content"]
        return content or ""
