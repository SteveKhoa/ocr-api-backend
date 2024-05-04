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
        self.status = http_status.HTTP_200_OK
        self.data = {"text": text}


class Collection(SuccessResponse):
    """A list of Any"""

    def __init__(self, collection: list[Any]):
        self.status = http_status.HTTP_200_OK
        self.data = {"collection": [str(item) for item in collection]}


class AuthorizedTokens(SuccessResponse):
    """Dictionary containing necessary, for OAuth2 compliance.

    Typical AuthorizationCode format:
    {
        "grant_type": "authorization_code",
        "access_token": "SlAV32hkKG",
        "token_type": "Bearer",
        "refresh_token": "8xLOxBtZp8",
        "exp": 3600,
        "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjFlOWdkazcifQ.ewogImlzc
            yI6ICJodHRwOi8vc2VydmVyLmV4YW1wbGUuY29tIiwKICJzdWIiOiAiMjQ4Mjg5
            NzYxMDAxIiwKICJhdWQiOiAiczZCaGRSa3F0MyIsCiAibm9uY2UiOiAibi0wUzZ
            fV3pBMk1qIiwKICJleHAiOiAxMzExMjgxOTcwLAogImlhdCI6IDEzMTEyODA5Nz
            AKfQ.ggW8hZ1EuVLuxNuuIJKX_V8a_OMXzR0EHR9R6jgdqrOOF4daGU96Sr_P6q
            Jp6IcmD3HP99Obi1PRs-cwh3LO-p146waJ8IhehcwL7F09JdijmBqkvPeB2T9CJ
            NqeGpe-gccMg4vfKjkM8FcGvnzZUN4_KSP0aAp1tOJ1zZwgjxqGByKHiOtX7Tpd
            QyHE5lcMiKPXfEIQILVq0pc_E2DzL7emopWoaoZTF_m0_N0YzFC6g6EJbOEoRoS
            K5hoDalrcvRYLSrQAZZKflyuVCyixEoV9GfNQC3_osjzw2PAithfubEEBLuVVk4
            XUVrWOLrLl0nx7RkKU8NXNHq-rvKMzqg"
    }

    Since my usecase is not as complex, I only implement `access_token` and
    `token_type`.
    """

    def __init__(self, access_token: str, token_type: str = "bearer"):
        self.status = http_status.HTTP_200_OK
        self.data = {
            "grant_type": "",
            "access_token": access_token,
            "token_type": token_type,
            "refresh_token": "",
            "expires_in": 0,
            "id_token": "",
        }


class IDToken(SuccessResponse):
    def __init__(self, id_token: str):
        self.status = http_status.HTTP_200_OK
        self.data = id_token


class FailResponse(BaseResponse):
    def __init__(self, status: int, data: Any = None):
        self.status = str(status)
        self.data = {}


class ErrorResponse(BaseResponse):
    def __init__(self, status: int, code: int, message: str, data: Any = None):
        self.status = str(status)
        self.code = str(code)
        self.message = str(message)
