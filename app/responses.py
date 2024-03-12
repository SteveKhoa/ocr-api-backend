"""
Defines Response JSON format
"""

from typing import Literal


class Response:
    """Response JSON format, base class.

    This does not replace the usage of FastAPI's standard exceptions.

    ## Params
    `status`: can take three possible values
        - `success`, all went well
        - `fail`, problem with data submitted, pre-condition not satisfied
        - `error`, error during request processing

    `data`: any dictionary

    The format is JSend-compliance.
    For more details, see https://github.com/omniti-labs/jsend
    """

    def __init__(self, status: Literal["success", "fail", "error"], data: dict):
        self.status = status
        self.data = data

    def to_json(self) -> dict:
        return {"status": self.status, "data": self.data}

    def to_data(self):
        return self.data

    def get_key(self):
        return "response"


class Text(Response):
    def __init__(self, text: str):
        super().__init__(status="success", data=text)

    def get_key(self):
        return "text"


class Message(Response):
    def __init__(self, message: str):
        super().__init__(status="success", data=message)

    def get_key(self):
        return "text"


class Collection(Response):
    def __init__(self, collection: list[str]):
        super().__init__(status="success", data=collection)

    def get_key(self):
        return "list"


class Composite(Response):
    def __init__(self, *responses: Response):
        responses_data = [
            {response_data.get_key(): response_data.to_data()}
            for response_data in responses
        ]

        merged_dict = {}
        for data_dict in responses_data:
            merged_dict.update(data_dict)

        super().__init__(status="success", data=merged_dict)
