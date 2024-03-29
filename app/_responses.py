"""
Common JSON Response formats for OCR-API
"""

from typing import Any
from fastapi import status as http_status
import fastapi.responses


class Response:
    """Response JSON format, base class. Use this when any other formats
    are not sufficient to describe the intention.

    ## Schema
    ```json
    {
        "status": <HTTP STATUS>,
        "data": <RESPONSE DATA>
    }
    ```
    ## Params
    `status`: can take three possible values
        - `success`, all went well
        - `fail`, problem with data submitted, pre-condition not satisfied
        - `error`, error during request processing

    `data`: any dictionary

    The format is JSend-compliance.
    For more details, see https://github.com/omniti-labs/jsend
    """

    def __init__(self, status: int, data: dict):
        self.status = status
        self.data = data

    async def __call__(self, scope, receive, send) -> None:
        response = fastapi.responses.JSONResponse(self.to_json(), self.status)

        await response(scope, receive, send)

    def to_json(self) -> dict:
        return {"status": self.status, "data": self.data}

    def to_data(self):
        return self.data

    def get_key(self):
        return "response"


class Text(Response):
    """Plain text string, deliver no server's intention"""

    def __init__(self, text: str):
        super().__init__(status=http_status.HTTP_200_OK, data=text)

    def get_key(self):
        return "text"


class Message(Response):
    """A message, delivering an explicit server intention"""

    def __init__(self, message: str):
        super().__init__(status=http_status.HTTP_200_OK, data=message)

    def get_key(self):
        return "msg"


class Collection(Response):
    """A list of strings

    ## Schema
    ```json
    {
        "status": 200,
        "data": [
            <entry01>,
            <entry02>,
            <entry03>,
            ...
        ]
    }
    ```
    """

    def __init__(self, collection: list[str]):
        super().__init__(status=http_status.HTTP_200_OK, data=collection)

    def get_key(self):
        return "collection"


class AccessToken(Response):
    """String representing access token"""

    def __init__(self, token: str):
        super().__init__(status=http_status.HTTP_200_OK, data=token)

    def get_key(self):
        return "access_token"


class Composite(Response):
    """Composite of many `Response` formats.

    ## Example
    ```json
    {
        "status": 200,
        "data": {
            "access_token": "123456",
            "collection": [
                1,
                2,
                3
            ],
            "msg": "an example",
            ...
        }
    }
    ```
    """

    def __init__(self, *responses: Response):
        responses_data = [
            {response_data.get_key(): response_data.to_data()}
            for response_data in responses
        ]

        merged_dict = {}
        for data_dict in responses_data:
            merged_dict.update(data_dict)

        super().__init__(status=http_status.HTTP_200_OK, data=merged_dict)
