from fastapi import APIRouter
from app.ocr.schemas.RequestBody import OCRLineRequestBody, OCRParagraphRequestBody
import app.ocr.controller
from fastapi import Depends
from typing import Annotated
import app.responses
import app.exceptions
import os
from fastapi.security import OAuth2PasswordBearer
from app.ocr.schemas.ImageWrappers import ImageRegion, SourceImage
from app.idp.controller import decode_token
import jwt

router = APIRouter(prefix="/ocr", tags=["ocr"])
idtok_bearer = OAuth2PasswordBearer("/identity/me")
# Not quite right, why use ID Token?? Actually because I do not have time to
# implement this, will definitely do this soon.


@router.post("/line")
def read_ocr_line(
    req: OCRLineRequestBody, id_token: Annotated[str, Depends(idtok_bearer)]
):
    try:
        # Calling a controller from another module is NOT correct
        # However for simplicity I just put it here.
        # In practice I should make an API Call to an Identity Server
        # and get the decoded payload.
        # Will definitely do that soon.
        payload = decode_token(id_token)
    except jwt.exceptions.InvalidTokenError:
        raise app.exceptions.InvalidJWTSignature()

    ocr_lines = app.ocr.controller.query_lines(
        image=SourceImage(req.image.base64),
        pattern=req.target.pattern,
        pivot_pattern=req.pivot.pattern,
        tightness=req.pivot.tightness,
        region=(
            ImageRegion(tuple(req.image.region.split(" ")))
            if req.image.region is not None
            else None
        ),
    )
    text_lines = [ocr_line.text_line for ocr_line in ocr_lines]

    return app.responses.Collection(text_lines)


@router.post("/paragraph")
def read_ocr_paragraph(
    req: OCRParagraphRequestBody, id_token: Annotated[str, Depends(idtok_bearer)]
):
    try:
        payload = decode_token(id_token)
    except jwt.exceptions.InvalidTokenError:
        raise app.exceptions.InvalidJWTSignature()
    
    ocr_paragraphs = app.ocr.controller.query_paragraphs(
        image=SourceImage(req.image.base64),
        pattern=req.target.pattern,
        region=(
            ImageRegion(tuple(req.image.region.split(" ")))
            if req.image.region is not None
            else None
        ),
    )

    paragraphs = [ocr_paragraph.get_textlines() for ocr_paragraph in ocr_paragraphs]

    return app.responses.Collection(
        [[text_line for text_line in paragraph] for paragraph in paragraphs]
    )
