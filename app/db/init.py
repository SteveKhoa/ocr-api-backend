"""Initialization script for database.

init.py NOT __init__.py
"""

from app.db.utils import connector

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

"""
Perhaps in the future implement some kind of ORM
"""

if __name__ == "__main__":
    cursor = connector.cursor()
    cursor.execute(DROP_TABLE_USER)
    cursor.execute(DROP_TABLE_APIKEY)
    cursor.execute(CREATE_USER_TABLE_QUERY)
    cursor.execute(CREATE_APIKEY_TABLE)
