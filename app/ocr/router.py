from fastapi import APIRouter
from fastapi import File, Depends
from fastapi import HTTPException, status
from typing import Annotated
from fastapi import Query
from app.auth.utils.apikey import verify_apikey
import app.ocr.services

import app._responses
from app.main import app


ocr_router = APIRouter(prefix="/ocr", tags=["ocr"])
app.include_router(ocr_router)


@ocr_router.post(
    "",
    summary="Request Optical Character Recognition service.",
)
def read_post_image(
    apikey: Annotated[str, Depends(verify_apikey)],
    file: Annotated[bytes, File()],
    query: Annotated[list[str], Query()],
):
    match query:
        case "all":
            text_data = app.ocr.services.data_from(file)
            return app._responses.Response(status="success", data=text_data)
        case "tokens":
            tokens = app.ocr.services.tokens_from(file)
            return app._responses.Collection(tokens)
        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported query parameter query.",
            )
