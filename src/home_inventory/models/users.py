"""Класс пользователя и функции авторизации."""


class User:
    """Пользователь системы учёта товаров."""

    def __init__(self, user_id: int, username: str, password: str) -> None:
        """Создать пользователя и сохранить его данные в атрибутах."""
        username = username.strip()
        if not username:
            raise ValueError("Имя пользователя не может быть пустым")

        self.id = user_id
        self.username = username
        self._password = password

    @property
    def password(self) -> str:
        """Пароль пользователя, доступный только для чтения."""
        return self._password

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из набора данных JSON."""
        return cls(
            user_id=int(data["id"]),
            username=data["username"],
            password=data["password"],
        )

    def check_password(self, password: str) -> bool:
        """Проверить пароль пользователя."""
        return self._password == password

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f"Пользователь #{self.id}: {self.username}"


def add_user(users: list[User], username: str, password: str) -> User:
    """Создать пользователя, добавить его в коллекцию и вернуть объект."""
    user_id = max((user.id for user in users), default=0) + 1
    user = User(user_id, username, password)
    users.append(user)
    return user


def find_user(users: list[User], username: str) -> User | None:
    """Найти пользователя по имени."""
    for user in users:
        if user.username == username:
            return user
    return None


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def authenticate(
    users: list[User],
    username: str,
    password: str,
) -> User | None:
    """Вернуть пользователя, если пара «имя — пароль» верна."""
    user = find_user(users, username)
    if user is not None and user.check_password(password):
        return user
    return None


def get_login_status(username: str, is_logged_in: bool) -> str:
    """Вернуть текстовый статус авторизации."""
    if is_logged_in:
        return f"Пользователь '{username}' успешно авторизован"
    return "Неверный пароль, авторизация не выполнена"
