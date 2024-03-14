"""
Common utilities for Database operations
"""

import hashlib
import base64
from app.db.connectors import connector
import os


CREATE_USER_TABLE_QUERY = """
CREATE TABLE user(  
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT
)
"""

DROP_TABLE_USER = """DROP TABLE IF EXISTS user"""


CREATE_APIKEY_TABLE = """
CREATE TABLE apikey(
    str char(16)
)
"""

GET_TABLE_NAME = """
SELECT name FROM sqlite_master WHERE type='table' AND name=?
"""

DROP_TABLE_APIKEY = """DROP TABLE IF EXISTS apikey"""


def initialize_database():
    cursor = connector.cursor()

    query = connector.execute(GET_TABLE_NAME, ("user",))
    tbl_user_exist = bool(query.fetchall())
    query = connector.execute(GET_TABLE_NAME, ("apikey",))
    tbl_apikey_exist = bool(query.fetchall())

    if not tbl_user_exist:
        cursor.execute(CREATE_USER_TABLE_QUERY)

    if not tbl_apikey_exist:
        cursor.execute(CREATE_APIKEY_TABLE)

    connector.commit()

    print("Database initialized.")


def delete_database():
    """
    WARNING: this will delete all tables and there will be no
    look-back on this one.
    """
    cursor = connector.cursor()
    cursor.execute(DROP_TABLE_USER)
    cursor.execute(DROP_TABLE_APIKEY)


if __name__ == "__main__":
    delete_database()
