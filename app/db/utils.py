"""
Common utilities for Database operations
"""

import sqlite3
import hashlib
import base64

DB_PATH = "/workspaces/ocr-api-backend/app/db/database.db"

connector = sqlite3.connect(DB_PATH)

DROP_TABLE_USER = """
DROP TABLE IF EXISTS user"""

DROP_TABLE_APIKEY = """
DROP TABLE IF EXISTS apikey
"""

CREATE_USER_TABLE_QUERY = """
CREATE TABLE user(  
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT
)
"""

CREATE_APIKEY_TABLE = """
CREATE TABLE apikey(
    str char(16)
)
"""


def hash_bytes(message: bytes) -> tuple[bytes, int]:
    """Hash a message into a raw bytes digest.

    ## Return
    `digest` where, `digest` is the hashed message (as bytes).
    """
    hash_obj = hashlib.md5(message)
    digest = hash_obj.digest()
    digest = base64.b64encode(digest)  # convert to byte-safe bytestring

    return digest


def main():
    """Execute initial scripts for database initialization

    ## WARNING
    This will delete existsing database tables and re-initialize
    with a completely fresh database.
    """
    cursor = connector.cursor()
    cursor.execute(DROP_TABLE_USER)
    cursor.execute(DROP_TABLE_APIKEY)
    cursor.execute(CREATE_USER_TABLE_QUERY)
    cursor.execute(CREATE_APIKEY_TABLE)
    connector.commit()


if __name__ == "__main__":
    main()
