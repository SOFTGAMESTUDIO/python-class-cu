from __future__ import annotations

import json
from typing import Any

import requests


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def analyze(self, report: dict[str, Any]) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": "qwen",
                    "prompt": f"Provide a concise system diagnostic summary: {json.dumps(report, indent=2)}",
                    "stream": False,
                },
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "No AI output returned.")
        except requests.RequestException:
            return "Ollama is not running or is unavailable. Using local safe fallback analysis instead."
