from fastapi import APIRouter
from fastapi import File, Depends
from fastapi import HTTPException
from typing import Annotated
from .tesseract.engine import TesseractOCR
from .tesseract.lang import DefaultLangs
from .tesseract.preprocess import load
from app.auth.utils import verify_apikey
from io import BytesIO


ocr_router = APIRouter(prefix="/ocr", tags=["ocr"])


@ocr_router.get("/", summary="Greeting message of the module")
async def ocr_readme(apikey: Annotated[str, Depends(verify_apikey)]):
    """Greetings endpoint of the module."""

    return {"text": "Hello from /ocr module!"}


@ocr_router.post("/extraction", summary="Extract text from uploaded image")
async def extract(
    file: Annotated[bytes, File()], apikey: Annotated[str, Depends(verify_apikey)]
):
    """String extraction service.

    This endpoint only accepts `multipart/form-data` uploaded bytes
    """

    tess = TesseractOCR(DefaultLangs.eng_fast)

    image = load(BytesIO(file))
    text = tess.read(image)
    return {"text": text}
