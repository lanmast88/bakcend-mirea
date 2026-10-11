"""Функции авторизации пользователя."""


def find_user(users: list[dict], username: str) -> dict | None:
    """Найти пользователя по имени."""
    for user in users:
        if user["username"] == username:
            return user
    return None


def authenticate(users: list[dict], username: str, password: str) -> bool:
    """Проверить пару «имя пользователя — пароль»."""
    user = find_user(users, username)
    return user is not None and user["password"] == password


def get_login_status(username: str, is_logged_in: bool) -> str:
    """Вернуть текстовый статус авторизации."""
    if is_logged_in:
        return f"Пользователь '{username}' успешно авторизован"
    return "Неверный пароль, авторизация не выполнена"
