from io import BytesIO
import app.ocr.tesseract.preprocess
from typing import Annotated
from app.ocr.tesseract.engine import TesseractOCR
from app.ocr.tesseract.lang import DefaultLangs
from fastapi import File

import app.responses

eng_tess = TesseractOCR(DefaultLangs.eng_fast)


def tokens_from(file: Annotated[bytes, File()]):

    text_data = data_from(file)
    tokens_dict = text_data["text"]
    tokens = list(tokens_dict.values())

    return tokens


def data_from(file: Annotated[bytes, File()]):
    image = app.ocr.tesseract.preprocess.load(BytesIO(file))
    text_data = eng_tess.read(image)

    return text_data
