"""Тесты класса Category и функций работы с категориями."""

import pytest

from home_inventory.models import Category
from home_inventory.models.categories import (
    add_category,
    find_category,
    find_category_by_id,
    get_or_create_category,
)


def test_category_creation():
    category = Category(1, "Продукты")
    assert category.id == 1
    assert category.name == "Продукты"


def test_category_empty_name():
    with pytest.raises(ValueError):
        Category(1, "   ")


def test_category_str():
    assert str(Category(1, "Продукты")) == "Категория #1: Продукты"


def test_category_matches_ignores_case():
    category = Category(1, "Продукты")
    assert category.matches("продукты")
    assert not category.matches("Лекарства")


def test_category_from_data():
    category = Category.from_data({"id": "2", "name": "Лекарства"})
    assert category.id == 2
    assert category.name == "Лекарства"


def test_add_category_appends_object(categories):
    category = add_category(categories, "Лекарства")
    assert isinstance(category, Category)
    assert category.id == 3
    assert categories[-1] is category


def test_find_category(categories):
    assert find_category(categories, "Бытовая химия").id == 2
    assert find_category(categories, "Лекарства") is None


def test_find_category_by_id(categories):
    assert find_category_by_id(categories, 1).name == "Продукты"
    assert find_category_by_id(categories, 99) is None


def test_get_or_create_category(categories):
    existing = get_or_create_category(categories, "Продукты")
    assert existing is categories[0]

    created = get_or_create_category(categories, "Лекарства")
    assert created.name == "Лекарства"
    assert len(categories) == 3
