from auth import authenticate, get_login_status

USERS = [{"username": "ivan_petrov", "password": "qwerty123"}]


def test_authenticate_valid_password():
    assert authenticate(USERS, "ivan_petrov", "qwerty123")


def test_authenticate_wrong_password():
    assert not authenticate(USERS, "ivan_petrov", "12345")


def test_get_login_status():
    assert get_login_status("ivan_petrov", False) == (
        "Неверный пароль, авторизация не выполнена"
    )
