"""Coordinate model inference and parsing for receipt images."""

from typing import Any

from receipt_extraction.parsers import ReceiptParser
from receipt_extraction.providers import LLMProvider, OllamaProvider


class ReceiptProcessor:
    """Process a receipt image and return a structured JSON object."""

    def __init__(
        self,
        provider: LLMProvider | None = None,
        parser: ReceiptParser | None = None,
    ):
        """Initialize the receipt processor."""
        self.provider = provider or OllamaProvider()
        self.parser = parser or ReceiptParser()

    def process_receipt(
        self,
        image_path: str,
        json_schema: dict[str, Any],
        model: str | None = None,
        response_format_type: str | None = None,
    ) -> dict[str, Any]:
        """Process a receipt image and return a structured JSON object.

        Args:
            image_path: Path to the receipt image file.
            json_schema: JSON schema defining the expected output structure.
            model: Optional model name to use for the LLM.
            response_format_type: Optional response format type. Supported: "json_object", "json_schema", "text".

        Returns:
            Dict containing the parsed receipt data.
        """
        response = self.provider.get_response(
            image_path, json_schema, model, response_format_type
        )
        return self.parser.parse(response)
