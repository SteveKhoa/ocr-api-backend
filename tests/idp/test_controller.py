import app.idp.controller
import sqlite3
import os
import pytest
from app.idp.schemas.Client import Client
import database.Clients

mockdb_url = "./database/mock_idp.db"
sqlite3.connect(mockdb_url)


@pytest.fixture(autouse=True)
def before_after_test():
    yield
    os.remove(mockdb_url)


def test_read_account():
    mockdb = database.Clients.ClientsDB(mockdb_url)
    mockdb.init()

    username = "steve123"
    password = "123456"
    client = Client(db_src=mockdb_url, username=username, password=password)
    client.create()  # assumes client.create() works sucessfully

    jwt = app.idp.controller.read_account(client)

    mockdb.destruct()
    assert jwt is not None


def test_create_account():
    mockdb = database.Clients.ClientsDB(mockdb_url)
    mockdb.init()

    username = "steve123"
    password = "123456"

    client = Client(db_src=mockdb_url, username=username, password=password)
    new_client = app.idp.controller.create_account(mockdb_url, username, password)

    mockdb.destruct()
    assert client.__dict__ == new_client.__dict__
