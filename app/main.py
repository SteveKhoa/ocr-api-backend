from fastapi import FastAPI
from app._responses import Message

app = FastAPI()


@app.get("/")
async def greetings():
    return Message("Greetings! Thanks for using OCR-API.")
