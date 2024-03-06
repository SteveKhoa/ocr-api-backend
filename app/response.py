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
    
    def json(self):
        return {"status": self.status, "data": self.data}


class Text(Response):
    def __init__(self, text: str):
        super().__init__(status="success", data={"text": text})


class Message(Response):
    def __init__(self, text: str):
        super().__init__(status="success", data={"message": text})