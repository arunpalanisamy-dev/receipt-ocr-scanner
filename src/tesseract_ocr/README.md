# Tesseract OCR Module

This folder hosts a script and a Docker-compose setup for performing **Optical Character Recognition (OCR)** on receipt images.

![image](https://github.com/bhimrazy/receipt-ocr/assets/46085301/305df68d-50d8-41d4-81d0-9324966fb6c9)

## Prerequisites

- Python 3.10 or later and `uv` for running locally
- The Tesseract OCR executable installed and available on `PATH`
- Docker Desktop with Compose, only for the containerized API

## Installation

Install Tesseract for your operating system using the [official installation guide](https://tesseract-ocr.github.io/tessdoc/Installation.html). From the repository root, install the Python environment and Tesseract module requirements:

```bash
uv sync --dev
uv pip install -r src/tesseract_ocr/requirements.txt
```

## Run locally

The CLI detects the receipt outline, corrects the perspective, then prints the text recognized by Tesseract. Run from the repository root:

```bash
uv run --no-sync python src/tesseract_ocr/main.py --image images/receipt.jpg
```

## Run the API in Docker

From the repository root, build and start the API:

```bash
docker compose -f src/tesseract_ocr/docker-compose.yml up --build
```

The API listens on port 8000. If the structured OCR API is running on the same port, stop it first. To process a receipt, open another terminal:

```powershell
curl.exe -X POST "http://localhost:8000/ocr/" -F "file=@images/receipt.jpg"
```

`GET /health` checks service availability. `POST /ocr/` accepts an image and returns raw OCR text; unlike the Ollama workflow, this does not produce structured receipt fields.

## License

This project is licensed under the terms of the MIT license.

## References

- [Automatically OCR’ing Receipts and Scans](https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/)
