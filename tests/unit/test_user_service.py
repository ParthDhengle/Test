from src2.user.service import get_password_hash, verify_password
from unittest.mock import MagicMock
import pytest
from src2.user.service import login_user
from src2.user.models import UserModel


def test_get_password_hash():
    password="password123"

    hashed_password = get_password_hash(password)

    assert hashed_password != password
    assert isinstance(hashed_password, str)


def test_verify_password_with_correct_password():
    password = "password123"
    hashed_password = get_password_hash(password)

    result = verify_password(password, hashed_password)

    assert result is True

def test_verify_password_with_wrong_password():
    password = "password123"
    wrong_password = "wrongpassword"

    hashed_password = get_password_hash(password)

    result = verify_password(wrong_password, hashed_password)

    assert result is False

def test_login_user_success(monkeypatch):
    db=MagicMock()

    user = UserModel(
        id=1,
        username="parth",
        password="hashed_password"
    )

    db.query.return_value.filter.return_value.first.return_value = user

    monkeypatch.setattr(
        "src2.user.service.verify_password",
        lambda plain_password, hashed_password: True
    )

    result = login_user(
        body=MagicMock(username="parth", password="password123"),
        db=db
    )
    assert "token" in result
    assert isinstance(result["token"],str)

def test_login_user_user_not_found():
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    body = MagicMock(
        username="unknown",
        password="password123"
    )

    with pytest.raises(Exception) as exc_info:
        login_user(body, db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "User Not found"


def test_login_user_wrong_password(monkeypatch):
    db = MagicMock()

    user = UserModel(
        id=1,
        username="parth",
        password="hashed_password"
    )

    db.query.return_value.filter.return_value.first.return_value = user

    monkeypatch.setattr(
        "src2.user.service.verify_password",
        lambda plain_password, hashed_password: False
    )

    body = MagicMock(
        username="parth",
        password="wrongpassword"
    )

    with pytest.raises(Exception) as exc_info:
        login_user(body, db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Password didnt matched"