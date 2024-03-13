from fastapi import FastAPI
from fastapi import HTTPException
from .auth import router as auth_router
from .ocr import router as ocr_router
from app._responses import Message
from app._exceptions import response_exception

app = FastAPI()

app.include_router(auth_router.auth_router)
app.include_router(ocr_router.ocr_router)

app.add_exception_handler(HTTPException, response_exception)


@app.get("/")
async def greetings():
    return Message("Greetings! Thanks for using OCR-API.")
