from fastapi import HTTPException, status
import app._responses
from typing import List


def response_exception(exception: HTTPException):
    http_status = exception.status_code
    detail = exception.detail

    return app._responses.Response(http_status, detail)


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
        detail = f"Invalid entry, or entry does not exist: {entries}."
        headers = None

        super().__init__(http_status, detail, headers)
