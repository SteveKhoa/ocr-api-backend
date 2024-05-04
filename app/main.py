from fastapi import FastAPI
from fastapi import HTTPException
from app.idp import router as idp_router
from app.ocr import router as ocr_router
import app.responses as Responses
from app.exceptions import reponse_http_exception
from app.config import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(idp_router.router)
app.include_router(ocr_router.router)
app.add_exception_handler(HTTPException, reponse_http_exception)


@app.get("/")
async def greetings():
    return Responses.Text("Hello world!")
