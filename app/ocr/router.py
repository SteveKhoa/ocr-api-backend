from fastapi import APIRouter
from app.ocr.schemas.RequestBody import OCRLineRequestBody, OCRParagraphRequestBody
import app.ocr.controller
import app.responses
from app.ocr.schemas.ImageWrappers import ImageRegion, SourceImage

router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.post("/line")
def read_ocr_line(req: OCRLineRequestBody):
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
def read_ocr_paragraph(req: OCRParagraphRequestBody):
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
