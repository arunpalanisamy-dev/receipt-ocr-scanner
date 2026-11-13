# Receipt OCR

Receipt OCR provides two ways to extract text from receipt images:

- **Structured extraction** with the `receipt-ocr` Python package and an
  OpenAI-compatible vision model. Ollama with `qwen2.5vl:3b` is the default.
- **Raw text extraction** with the Tesseract-based command-line tool.

## Structured extraction

### Install

Requires Python 3.10 or later and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --dev
```

### Configure a model

The default provider uses a local Ollama server. Install
[Ollama](https://ollama.com/) and pull the default vision model:

```bash
ollama pull qwen2.5vl:3b
```

Keep Ollama running while processing receipts. To use another OpenAI-compatible
provider, set `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `OPENAI_MODEL` for that
provider.

### Run the CLI

```bash
uv run receipt-ocr images/receipt.jpg
```

To supply a custom JSON schema, save it in a JSON file and pass its path:

```bash
uv run receipt-ocr images/receipt.jpg --schema_path schema.json
```

The CLI prints extracted receipt data as JSON. The package can also be used from
Python:

```python
from receipt_ocr.processors import ReceiptProcessor

processor = ReceiptProcessor()
schema = {
    "merchant_name": "string",
    "total_amount": "number",
}
result = processor.process_receipt("images/receipt.jpg", schema)
print(result)
```

## Tesseract text extraction

The Tesseract tool requires the Tesseract executable installed and available on
`PATH`. Install its Python dependencies and run it from the repository root:

```bash
uv pip install -r src/tesseract_ocr/requirements.txt
uv run --no-sync python src/tesseract_ocr/main.py --image images/receipt.jpg
```

This tool detects and rectifies the receipt outline before printing raw OCR
text. See [the Tesseract module README](src/tesseract_ocr/README.md) for its
Docker API instructions.

## API services

The repository also includes a FastAPI service for structured extraction and a
Docker-based Tesseract API. See [the structured API README](app/README.md) and
[the Tesseract module README](src/tesseract_ocr/README.md) for setup and usage.

## Development

Run the test suites from the repository root:

```bash
uv run pytest tests/receipt_ocr
uv run pytest tests/tesseract_ocr
```

Run Ruff checks and formatting:

```bash
uvx ruff check .
uvx ruff format --check .
```
