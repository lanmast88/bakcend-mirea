"""Класс категории товаров и функции работы с их коллекцией."""


class Category:
    """Категория, к которой относится товар."""

    def __init__(self, category_id: int, name: str) -> None:
        """Создать категорию с идентификатором и названием."""
        name = name.strip()
        if not name:
            raise ValueError("Название категории не может быть пустым")

        self.id = category_id
        self.name = name

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """Создать категорию из набора данных JSON."""
        return cls(category_id=int(data["id"]), name=data["name"])

    def matches(self, name: str) -> bool:
        """Проверить совпадение названия без учёта регистра."""
        return self.name.lower() == name.strip().lower()

    def __str__(self) -> str:
        """Вернуть строковое представление категории."""
        return f"Категория #{self.id}: {self.name}"


def add_category(categories: list[Category], name: str) -> Category:
    """Создать категорию, добавить её в коллекцию и вернуть объект."""
    category_id = max((category.id for category in categories), default=0) + 1
    category = Category(category_id, name)
    categories.append(category)
    return category


def find_category(categories: list[Category], name: str) -> Category | None:
    """Найти категорию по названию."""
    for category in categories:
        if category.matches(name):
            return category
    return None


def find_category_by_id(
    categories: list[Category],
    category_id: int,
) -> Category | None:
    """Найти категорию по идентификатору."""
    for category in categories:
        if category.id == category_id:
            return category
    return None


def get_or_create_category(
    categories: list[Category],
    name: str,
) -> Category:
    """Вернуть категорию с таким названием, создав её при отсутствии."""
    category = find_category(categories, name)
    if category is None:
        category = add_category(categories, name)
    return category
