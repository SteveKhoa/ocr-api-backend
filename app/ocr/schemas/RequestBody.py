from pydantic import BaseModel
from typing import Tuple


class OCRContext(BaseModel):
    """Baseclass to clarify the dependency tree, for readability."""

    pass


class Image(OCRContext):
    base64: str
    region: Tuple[int, int, int, int] | None = None


class Target(OCRContext):
    pattern: str


class Pivot(OCRContext):
    pattern: str
    tightness: float


class OCRLineRequestBody(BaseModel):
    """
    Example:
    {
        "image": {
            "base64": "U3dhZ2dlciByb2Nrcw==",
            "region": "12 47 55 93"
        },
        "target": {
            "pattern": "(?: \+? \d{1,2} \s? )?"
        },
        "pivot": {
            "pattern": "\s?-\s?-\s?"
            "tightness": "0.92"
        }
    }
    """

    image: Image
    target: Target
    pivot: Pivot | None = None


class OCRParagraphRequestBody(BaseModel):
    """
    Example:
    {
        "image": {
            "base64": "U3dhZ2dlciByb2Nrcw==",
            "region": "12 47 55 93"
        },
        "target": {
            "pattern": "(?: \+? \d{1,2} \s? )?"
        }
    }
    """

    image: Image
    target: Target
