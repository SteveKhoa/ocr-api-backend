"""
Common JSON Response format for OCR-API.

The format is JSend-compliance. See https://github.com/omniti-labs/jsend.

Success
    *Required keys*: status, data

Fail
    *Required keys*: status, data

Error
    *Required keys*: status, code, message, data
"""

from typing import Any
from fastapi import status as http_status
import fastapi.responses


class BaseResponse:
    async def __call__(self, scope, receive, send) -> None:
        response = fastapi.responses.JSONResponse(self.to_json(), self.status)

        await response(scope, receive, send)


class SuccessResponse(BaseResponse):
    def __init__(self, status: int = None, data: Any = None):
        # Define interface explicitly, even when these parameters are
        # not in use, to clearly declare what the response would contain
        # (to be JSend compliance)
        pass

    def to_json(self):
        return {"status": http_status.HTTP_200_OK, "data": self.data}


class Text(SuccessResponse):
    """Text response"""

    def __init__(self, text: str):
        self.data = {"text": text}


class Collection(SuccessResponse):
    """A list of Any"""

    def __init__(self, collection: list[Any]):
        self.data = {"collection": [item for item in collection]}


class AccessToken(SuccessResponse):
    """String representing access token"""

    def __init__(self, token: str):
        self.data = {"access_token": token}


class FailResponse(BaseResponse):
    def __init__(self, status: int, data: Any = None):
        self.status = status

    def to_json(self):
        return {"status": self.status, "data": self.data}


class ErrorResponse(BaseResponse):
    def __init__(self, code: int, message: int, data: Any = None):
        self.status = code
        self.message = message

    def to_json(self):
        return {
            "status": self.status,
            "code": "",  # omit for now
            "message": self.message,
            "data": "",  # omit for now
        }
