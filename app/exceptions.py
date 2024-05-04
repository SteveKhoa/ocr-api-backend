from fastapi import HTTPException, status, Request
from app.idp.schemas.Client import Client
import app.responses
from typing import List


def reponse_http_exception(
    request: Request, exception: HTTPException
) -> app.responses.ErrorResponse:
    http_status = exception.status_code
    detail = exception.detail

    return app.responses.ErrorResponse(http_status, 0, detail)


class UnsupportedQueryParam(HTTPException):
    def __init__(self, *qparams: List[str]) -> None:
        http_status = status.HTTP_400_BAD_REQUEST
        detail = f"Unsupported query params: {qparams}."
        headers = None

        super().__init__(http_status, detail, headers)


class MissingBody(HTTPException):
    def __init__(self, *bodies: List[str]) -> None:
        http_status = status.HTTP_400_BAD_REQUEST
        detail = f"Missing request bodies: {bodies}."
        headers = None

        super().__init__(http_status, detail, headers)


class DuplicateDatabaseEntry(HTTPException):
    def __init__(self, *entries: List[str]) -> None:
        http_status = status.HTTP_400_BAD_REQUEST
        detail = f"Duplicate database entry: {entries}."
        headers = None

        super().__init__(http_status, detail, headers)


class DatabaseEntryNotExisted(HTTPException):
    def __init__(self, *entries: List[str]) -> None:
        http_status = status.HTTP_400_BAD_REQUEST
        detail = f"Requested data not existed or invalid: {entries}."
        headers = None

        super().__init__(http_status, detail, headers)


class InvalidJWTSignature(HTTPException):
    def __init__(self):
        http_status = status.HTTP_401_UNAUTHORIZED
        detail = f"JWT is invalid, or expired."
        headers = None

        super().__init__(http_status, detail, headers)


class UndefinedJWTError(HTTPException):
    def __init__(self, msg: str):
        http_status = status.HTTP_401_UNAUTHORIZED
        detail = f"{msg}"
        headers = None

        super().__init__(http_status, detail, headers)


class InvalidData(HTTPException):
    def __init__(self, details: str):
        http_status = status.HTTP_400_BAD_REQUEST
        detail = f"Invalid or unsupported data: {details}"
        headers = None

        super().__init__(http_status, detail, headers)


class InvalidAccount(HTTPException):
    def __init__(self, client: Client):
        http_status = status.HTTP_401_UNAUTHORIZED
        detail = f"Account is invalid or not exist: {client.username}"
        headers = None

        super().__init__(http_status, detail, headers)
