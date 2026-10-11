"""Общие фикстуры тестов проекта."""

from collections.abc import Callable
from datetime import date

import pytest

from home_inventory.items import add_item

TEST_DATE = date(2026, 9, 8)

ItemsFactory = Callable[..., dict[int, dict]]


@pytest.fixture
def make_items() -> ItemsFactory:
    """Вернуть фабрику словаря товаров с одним товаром «Молоко»."""

    def factory(
        quantity: int = 5,
        min_threshold: int = 2,
    ) -> dict[int, dict]:
        items: dict[int, dict] = {}
        add_item(
            items, "Молоко", "Продукты", "л",
            quantity, min_threshold, TEST_DATE,
        )
        return items

    return factory


@pytest.fixture
def items(make_items: ItemsFactory) -> dict[int, dict]:
    """Словарь с двумя товарами из разных категорий."""
    items = make_items()
    add_item(items, "Мыло", "Бытовая химия", "шт", 1, 1, TEST_DATE)
    return items
