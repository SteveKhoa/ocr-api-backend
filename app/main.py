from fastapi import FastAPI
from app.modules.ocr.tesseract.engine import OCREngine

app = FastAPI()


@app.get("/")
def read_root():
    ocr = OCREngine()
    text = ocr.read("hello")
    return text


@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id, "description": "A sample item from a dummy database"}
