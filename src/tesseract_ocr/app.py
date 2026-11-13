"""FastAPI endpoints for raw text extraction with Tesseract."""

import numpy as np
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse

from .utils import perform_ocr

app = FastAPI()


@app.get("/")
async def root():
    """Return a short description of the OCR service."""
    return {"message": "Welcome to the OCR API"}


@app.get("/health")
async def health_check():
    """Report that the API process is responsive."""
    return {"status": "ok"}


@app.post("/ocr/")
async def ocr_receipt(file: UploadFile):
    """Extract and return raw text from an uploaded receipt image."""
    # Check if the uploaded file is an image
    if file.content_type.startswith("image"):
        image_bytes = await file.read()
        img_array = np.frombuffer(image_bytes, np.uint8)

        ocr_text = perform_ocr(img_array)
        return JSONResponse(content={"result": ocr_text}, status_code=200)
    else:
        return {"error": "Uploaded file is not an image"}
