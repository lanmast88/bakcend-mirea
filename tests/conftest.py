"""Общие фикстуры тестов проекта."""

from collections.abc import Callable
from datetime import date

import pytest

from home_inventory.models import Category, Item, User
from home_inventory.models.items import add_item

TEST_DATE = date(2026, 9, 8)

ItemFactory = Callable[..., Item]


@pytest.fixture
def category() -> Category:
    """Категория «Продукты»."""
    return Category(1, "Продукты")


@pytest.fixture
def categories(category: Category) -> list[Category]:
    """Коллекция объектов Category из двух категорий."""
    return [category, Category(2, "Бытовая химия")]


@pytest.fixture
def user() -> User:
    """Пользователь, от имени которого выполняются операции."""
    return User(1, "ivan_petrov", "qwerty123")


@pytest.fixture
def users(user: User) -> list[User]:
    """Коллекция объектов User."""
    return [user]


@pytest.fixture
def make_item(category: Category) -> ItemFactory:
    """Вернуть фабрику товара «Молоко» с заданным остатком."""

    def factory(
        quantity: int = 5,
        min_threshold: int = 2,
    ) -> Item:
        return Item(
            1, "Молоко", category, "л", quantity, min_threshold, TEST_DATE,
        )

    return factory


@pytest.fixture
def item(make_item: ItemFactory) -> Item:
    """Товар «Молоко» с остатком 5 л."""
    return make_item()


@pytest.fixture
def items(make_item: ItemFactory, categories: list[Category]) -> list[Item]:
    """Коллекция объектов Item из двух разных категорий."""
    items = [make_item()]
    add_item(items, "Мыло", categories[1], "шт", 1, 1, TEST_DATE)
    return items
