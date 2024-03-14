"""
Black-box testing on app/auth/account.py
"""

import app.auth.account
from app.db.connectors import connector
import pytest
import app._exceptions


def test_success_registration():
    # Input
    username = "Mr_SHelby"
    password = "peaky123_birmingham"

    # Test execution
    token = app.auth.account.register_account(username, password)  # database modified

    ret_query = connector.execute(
        "SELECT * FROM user WHERE username=?",
        (username,),
    )
    retval = ret_query.fetchall()

    # Test clean-up
    connector.execute(
        "DELETE FROM user WHERE username=?",
        (username,),
    )
    connector.commit()

    # Comparing with expected
    assert len(retval) > 0


def test_duplicate_registration():
    # Input
    username = "Mr_SHelby"
    password = "peaky123_birmingham"

    # Test execution
    with pytest.raises(app._exceptions.DuplicateDatabaseEntry) as exc:
        token = app.auth.account.register_account(
            username, password
        )  # database modified
        token = app.auth.account.register_account(
            username, password
        )  # database modified

    # Test clean-up
    connector.execute(
        "DELETE FROM user WHERE username=?",
        (username,),
    )
    connector.commit()

    assert str(exc.value) == "400: Duplicate database entry: ('account',)."


def test_empty_username_registration():
    # Input
    username = ""
    password = "peaky123_birmingham"

    # Test execution
    with pytest.raises(app._exceptions.InvalidData) as exc:
        token = app.auth.account.register_account(
            username, password
        )  # database modified

    # Test clean-up
    connector.execute(
        "DELETE FROM user WHERE username=?",
        (username,),
    )
    connector.commit()

    assert str(exc.value) == None


def test_empty_password_registration():
    # Input
    username = "thomasShelby"
    password = ""

    # Execution
    with pytest.raises(app._exceptions.InvalidData) as exc:
        token = app.auth.account.register_account(
            username, password
        )  # database modified

    # Test clean-up
    connector.execute(
        "DELETE FROM user WHERE username=?",
        (username,),
    )
    connector.commit()

    assert str(exc.value) == None


def test_change_password():
    # Input
    username = "thomasShelby"
    password = "GhostOf_england123#"

    # Execution

    # Clean-up
    # Compare to expected


def test_delete_account():
    pass


def test_get_info():
    pass


def test_template():
    # Input
    # Execution
    # Clean-up
    # Compare to expected
    pass
