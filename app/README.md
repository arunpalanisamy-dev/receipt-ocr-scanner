# Receipt OCR API

A **FastAPI** service that extracts structured data from receipt images using a local Ollama vision model by default. OpenAI-compatible cloud services can also be configured.

## Features

- **Local model by default**: Uses Ollama and Qwen2.5-VL without a paid API key
- **Structured JSON output**: Returns merchant info, line items, totals, and dates
- **Custom schemas**: Support for custom JSON schemas
- **File validation**: Validates image files and sizes (max 5MB)
- **RESTful API**: Clean FastAPI endpoints with automatic documentation

## Get Started Quickly

### 1. Install Dependencies

```bash
# Install uv if it is not already installed
pip install uv

uv sync
```

Run these commands from the `app` directory. Python dependencies are downloaded during setup; receipt images are processed by Ollama on your machine.

### 2. Start a Local Model

Install [Ollama](https://ollama.com/download) and download the default vision model:

```bash
ollama pull qwen2.5vl:3b
```

Ollama must remain running while the API is in use. For direct local development, create a `.env` file from `.env.example`:

```bash
copy .env.example .env
```

### 3. Run the API locally

```bash
uv run fastapi run server.py --host 127.0.0.1 --port 8000
```

Or, from the repository root, run the API and Ollama in Docker:

```powershell
docker compose -f app\docker-compose.yml up --build -d
docker compose -f app\docker-compose.yml exec ollama ollama pull qwen2.5vl:3b
```

The Docker model is stored in a named volume and only needs to be pulled once.

To select another Ollama vision model, set `OPENAI_MODEL` in your environment. For a cloud provider, set `OPENAI_BASE_URL`, `OPENAI_API_KEY`, and `OPENAI_MODEL`.

### 4. Test the API

```powershell
# Health check
curl.exe -f http://localhost:8000/health

# Process a receipt (default schema)
curl.exe -X POST "http://localhost:8000/ocr/" -F "file=@..\images\receipt.jpg"

# Process with custom schema
curl.exe -X POST "http://localhost:8000/ocr/" `
  -F "file=@..\images\receipt.jpg" `
  -F 'json_schema={"merchant":"string","total":"number"}'
```

For requests made from the repository root, use `-F "file=@images/receipt.jpg"` instead. Open `http://localhost:8000/docs` for the interactive API reference. Stop the Docker services with `docker compose -f app\docker-compose.yml down`; do not use `-v` if you want to keep the downloaded model.

## API Endpoints

### `GET /`
Returns API information and available endpoints.

### `GET /health`
Health check endpoint.

### `POST /ocr/`
Extract structured data from a receipt image.

**Parameters:**
- `file` (required): Receipt image file (JPEG, PNG, etc., max 5MB)
- `json_schema` (optional): Custom JSON schema as dictionary

**Response:**
```json
{
  "merchant_name": "Store Name",
  "merchant_address": "123 Main St",
  "transaction_date": "2024-01-01",
  "total_amount": 25.99,
  "line_items": [
    {
      "item_name": "Product Name",
      "item_quantity": 1,
      "item_price": 25.99
    }
  ]
}
```

## Configuration

The API uses the following environment variables:

- `OPENAI_API_KEY`: API key for the configured provider; Ollama accepts the placeholder `ollama`
- `OPENAI_MODEL`: Model to use (default: `qwen2.5vl:3b`)
- `OPENAI_BASE_URL`: OpenAI-compatible API URL (default: `http://localhost:11434/v1`)

## Development

### API Documentation

When running, visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

### Project Structure

```
app/
├── server.py          # FastAPI routes and receipt processing setup
├── pyproject.toml     # API dependencies
├── docker-compose.yml # API plus local Ollama service
└── README.md          # API setup and usage
```

## License

MIT License
