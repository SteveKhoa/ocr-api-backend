"""
Common JSON Response formats for OCR-API
"""

from typing import Any
from fastapi import status as http_status
import fastapi.responses


class Response:
    """Response JSON

    The format is JSend-compliance. See https://github.com/omniti-labs/jsend.

    ## Schema
    #### Success

    *Required keys*: status, data

    #### Fail

    *Required keys*: status, data

    #### Error

    *Required keys*: status, code, message, data
    """

    async def __call__(self, scope, receive, send) -> None:
        response = fastapi.responses.JSONResponse(
            self.to_json(), self.status
        )

        await response(scope, receive, send)

    def to_json(self):
        return {"status": http_status.HTTP_200_OK, "data": self.data}


class Text(Response):
    """Text response"""

    def __init__(self, text: str):
        self.data = {"text": text}


class Collection(Response):
    """A list of Any"""

    def __init__(self, collection: list[Any]):
        self.data = {"collection": [item for item in collection]}


class AccessToken(Response):
    """String representing access token"""

    def __init__(self, token: str):
        self.data = {"access_token": token}
