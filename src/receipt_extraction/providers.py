"""Ollama-backed structured receipt provider."""

import json
import os
from abc import ABC, abstractmethod
from typing import Any
from urllib.request import Request, urlopen

from PIL import Image

from receipt_extraction.constants import (
    _DEFAULT_OLLAMA_BASE_URL,
    _DEFAULT_OLLAMA_MODEL,
)
from receipt_extraction.prompts import SYSTEM_PROMPT, USER_PROMPT
from receipt_extraction.utils import encode_image_to_base64


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def get_response(
        self,
        image: str | bytes | Image.Image,
        json_schema: dict,
        model: str,
        response_format_type: str | None = None,
    ) -> Any:
        """Get the response from the LLM provider."""
        ...


class OllamaProvider(LLMProvider):
    """Provider for Ollama's native HTTP API."""

    def __init__(self, base_url: str | None = None):
        """Initialize a provider for the configured local Ollama server."""
        self.base_url = (
            base_url or os.getenv("OLLAMA_BASE_URL") or _DEFAULT_OLLAMA_BASE_URL
        ).rstrip("/")
        if self.base_url.endswith("/v1"):
            self.base_url = self.base_url.removesuffix("/v1")

    def get_response(
        self,
        image: str | bytes | Image.Image,
        json_schema: dict,
        model: str | None = None,
        response_format_type: str | None = None,
    ) -> str:
        """Send a receipt image and extraction schema to the configured model."""
        response_format_type = response_format_type or "json_object"
        if response_format_type not in ["json_object", "json_schema", "text"]:
            raise ValueError(
                f"Invalid response_format_type: {response_format_type}. Supported: json_object, json_schema, text"
            )
        image_base64 = encode_image_to_base64(image)
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(
                    json_schema_content=json.dumps(json_schema, indent=2)
                ),
            },
            {
                "role": "user",
                "content": USER_PROMPT,
                "images": [image_base64],
            },
        ]
        payload = {
            "model": model or os.getenv("OLLAMA_MODEL", _DEFAULT_OLLAMA_MODEL),
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.2},
        }
        if response_format_type == "json_schema":
            payload["format"] = json_schema
        elif response_format_type == "json_object":
            payload["format"] = "json"

        request = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result["message"]["content"]
