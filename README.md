# Receipt OCR

Receipt OCR provides two ways to extract text from receipt images:

- **Structured extraction** with the `receipt-ocr` Python package and a local
  Ollama vision model.
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

Keep Ollama running while processing receipts. To use another Ollama model, set
`OLLAMA_MODEL` or pass `--model` to the CLI. `OLLAMA_BASE_URL` can point to
another Ollama server.

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
from receipt_extraction.processors import ReceiptProcessor

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
uv run pytest tests/receipt_extraction
uv run pytest tests/tesseract_ocr
```

Run the Ollama end-to-end response-format checks with Ollama running and the
default vision model installed:

```bash
uv run python tests/e2e/run_ollama_response_formats.py
```

Run Ruff checks and formatting:

```bash
uvx ruff check .
uvx ruff format --check .
```
