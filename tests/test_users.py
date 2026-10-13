"""Тесты класса User и функций авторизации."""

import pytest

from home_inventory.models import User
from home_inventory.models.users import (
    add_user,
    authenticate,
    find_user,
    find_user_by_id,
    get_login_status,
)


def test_user_creation():
    user = User(1, "ivan_petrov", "qwerty123")
    assert user.id == 1
    assert user.username == "ivan_petrov"


def test_user_empty_username():
    with pytest.raises(ValueError):
        User(1, "   ", "qwerty123")


def test_user_str():
    assert str(User(1, "ivan_petrov", "x")) == (
        "Пользователь #1: ivan_petrov"
    )


def test_user_check_password(user):
    assert user.check_password("qwerty123")
    assert not user.check_password("12345")


def test_user_password_is_read_only(user):
    with pytest.raises(AttributeError):
        user.password = "new"


def test_user_from_data():
    user = User.from_data(
        {"id": "2", "username": "anna", "password": "secret"}
    )
    assert user.id == 2
    assert user.username == "anna"
    assert user.check_password("secret")


def test_add_user_appends_object(users):
    user = add_user(users, "anna", "secret")
    assert user.id == 2
    assert users[-1] is user


def test_find_user(users):
    assert find_user(users, "ivan_petrov") is users[0]


def test_find_unknown_user(users):
    assert find_user(users, "unknown") is None


def test_find_user_by_id(users):
    assert find_user_by_id(users, 1) is users[0]
    assert find_user_by_id(users, 99) is None


def test_authenticate_valid_password(users):
    assert authenticate(users, "ivan_petrov", "qwerty123") is users[0]


def test_authenticate_wrong_password(users):
    assert authenticate(users, "ivan_petrov", "12345") is None


def test_authenticate_unknown_user(users):
    assert authenticate(users, "unknown", "qwerty123") is None


def test_get_login_status():
    assert get_login_status("ivan_petrov", False) == (
        "Неверный пароль, авторизация не выполнена"
    )
    assert "успешно авторизован" in get_login_status("ivan_petrov", True)
