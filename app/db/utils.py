"""
Common utilities for Database operations
"""
import sqlite3
import hashlib
import base64

DB_PATH = "/workspaces/ocr-api-backend/app/db/database.db"

connector = sqlite3.connect(DB_PATH)


def hash_bytes(message: bytes) -> tuple[bytes, int]:
    """Hash a message into a raw bytes digest.

    ## Return
    `digest` where, `digest` is the hashed message (as bytes).
    """
    hash_obj = hashlib.md5(message)
    digest = hash_obj.digest()
    digest = base64.b64encode(digest)  # convert to byte-safe bytestring

    return digest