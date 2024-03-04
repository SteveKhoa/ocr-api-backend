"""Utilities to interact with api-keys on the database
"""

from sqlite3 import Connection
from fastapi import HTTPException, status

def check_duplicate(db_connection: Connection, apikey: str) -> None:
    """Check duplication of apikey on the database.
    
    If duplication found, raise HTTPException 400
    """

    QUERY_APIKEY = """SELECT * FROM apikey WHERE str=?"""

    query_retval = db_connection.execute(QUERY_APIKEY, (apikey,))
    retvals = query_retval.fetchall()

    if len(retvals) > 0:  # duplicate apikey found
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="API-Key duplicated.")
    
    return  # pass the check


def create(db_connection: Connection, apikey: str) -> None:
    """Create a database entry for apikey"""

    CREATE_APIKEY = """INSERT INTO apikey VALUES (?)"""

    # Note: raw apikey is stored to the database, no
    # hash is performed.
    db_connection.execute(CREATE_APIKEY, (apikey,))

    return  # done procedure


def check_exist(db_connection: Connection, apikey: str):
    """Check if apikey exists on the database"""

    QUERY_APIKEY = """SELECT * FROM apikey WHERE str=?"""

    query_retval = db_connection.execute(QUERY_APIKEY, (apikey,))
    retvals = query_retval.fetchall()

    if len(retvals) <= 0:  # apikey not existed
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="API-Key Invalid")
    
    return  # pass the check