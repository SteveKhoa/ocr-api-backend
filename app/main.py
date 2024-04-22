from fastapi import FastAPI
from fastapi import HTTPException
from app.auth import router as auth_router
from app.ocr import router as ocr_router
from app._responses import Message
from app._exceptions import reponse_http_exception
from app._config import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router.auth_router)
app.include_router(ocr_router.ocr_router)
app.add_exception_handler(HTTPException, reponse_http_exception)


@app.get("/")
async def greetings():
    return Message("Greetings! Thanks for using OCR-API.")
