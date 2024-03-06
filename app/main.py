from fastapi import FastAPI
from .auth import router as auth_router
from .ocr import router as ocr_router
from app.response import Message

app = FastAPI()

app.include_router(auth_router.auth_router)
app.include_router(ocr_router.ocr_router)


@app.get("/")
async def greetings():
    return Message("Greetings! Thanks for using OCR-API.")
