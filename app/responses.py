"""
Common JSON Response format for OCR-API.
The format is JSend-compliance. See https://github.com/omniti-labs/jsend.

Success
    *Required keys*: status, data

Fail
    *Required keys*: status, data

Error
    *Required keys*: status, code, message, data

Notes:
    async def __call__ in BaseResponse formats its JSON
    using class's properties, not the 'self.data' we pass
    into `content` parameter. For example:
        - self.data, self.status will return:
        {
            status: 404,
            data: "",
        }
    This explains why some keys are missing in my initial
    wrong implementation.
"""

from typing import Any
from fastapi import status as http_status
import fastapi.responses


class BaseResponse:
    async def __call__(self, scope, receive, send) -> None:
        response = fastapi.responses.JSONResponse(self.data, self.status)

        await response(scope, receive, send)


class SuccessResponse(BaseResponse):
    def __init__(self, status: int = None, data: Any = None):
        # Define interface explicitly, even when these parameters are
        # not in use, to clearly declare what the response would contain
        # (to be JSend compliance)
        self.status = http_status.HTTP_200_OK


class Text(SuccessResponse):
    """Text response"""

    def __init__(self, text: str):
        self.data = {"text": text}


class Collection(SuccessResponse):
    """A list of Any"""

    def __init__(self, collection: list[Any]):
        self.data = {"collection": [str(item) for item in collection]}


class AccessToken(SuccessResponse):
    """String representing access token"""

    def __init__(self, token: str):
        self.data = {"access_token": token}


class FailResponse(BaseResponse):
    def __init__(self, status: int, data: Any = None):
        self.status = str(status)
        self.data = {}


class ErrorResponse(BaseResponse):
    def __init__(self, status: int, code: int, message: str, data: Any = None):
        self.status = str(status)
        self.code = str(code)
        self.message = str(message)
