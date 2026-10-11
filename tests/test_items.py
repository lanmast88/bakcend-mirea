"""Тесты функций работы с товарами."""

from datetime import date

import pytest

from home_inventory.items import (
    add_item,
    filter_items_by_category,
    find_items,
    get_add_confirmation,
    get_item,
    sort_items_by_quantity,
)

TEST_DATE = date(2026, 9, 8)


def test_add_item_returns_id():
    items: dict[int, dict] = {}
    item_id = add_item(
        items, "Молоко", "Продукты", "л", 5, 2, TEST_DATE
    )
    assert item_id == 1
    assert items[item_id]["name"] == "Молоко"


def test_add_item_empty_name():
    with pytest.raises(ValueError):
        add_item({}, "   ", "Продукты", "л", 5, 2, TEST_DATE)


def test_find_items(items):
    assert list(find_items(items, "моло")) == [1]


def test_filter_items_by_category(items):
    assert len(filter_items_by_category(items, "Продукты")) == 1


def test_sort_items_by_quantity(items):
    pairs = sort_items_by_quantity(items)
    quantities = [item["quantity"] for _, item in pairs]
    assert quantities == [1, 5]


def test_get_item_unknown_id():
    with pytest.raises(KeyError):
        get_item({}, 1)


def test_get_add_confirmation_zero_quantity():
    assert "не добавлен" in get_add_confirmation("Молоко", "Продукты", 0, "л")
