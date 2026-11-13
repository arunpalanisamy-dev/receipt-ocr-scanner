"""Command-line entry point for structured receipt extraction."""

import argparse
import json
import os

from dotenv import load_dotenv

from receipt_ocr.constants import _DEFAULT_OLLAMA_MODEL
from receipt_ocr.processors import ReceiptProcessor
from receipt_ocr.providers import OpenAIProvider

load_dotenv()


def main():
    """Parse command-line options, process the receipt, and print JSON."""
    parser = argparse.ArgumentParser(
        description="Extract information from a receipt image."
    )
    parser.add_argument("image_path", type=str, help="The path to the receipt image.")
    parser.add_argument(
        "--schema_path", type=str, help="The path to a custom JSON schema file."
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("OLLAMA_MODEL", _DEFAULT_OLLAMA_MODEL),
        help="The Ollama model to use.",
    )
    args = parser.parse_args()

    # Load the JSON schema
    if args.schema_path:
        with open(args.schema_path, "r") as f:
            json_schema = json.load(f)
    else:
        json_schema = {
            "merchant_name": "string",
            "merchant_address": "string",
            "transaction_date": "string",
            "transaction_time": "string",
            "total_amount": "number",
            "line_items": [
                {
                    "item_name": "string",
                    "item_quantity": "number",
                    "item_price": "number",
                }
            ],
        }

    # Initialize the provider and parser
    provider = OpenAIProvider()

    # Initialize the processor
    processor = ReceiptProcessor(provider)

    # Process the receipt
    result = processor.process_receipt(args.image_path, json_schema, args.model)

    # Print the result
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
