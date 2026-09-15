from datetime import date

import pytest

from items import (
    add_item,
    filter_items_by_category,
    find_items,
    get_item,
    sort_items_by_quantity,
)


def test_add_item():
    items = {}
    add_item(items, "Молоко", "Продукты", "л", 5, 2, date(2026, 9, 8))
    assert len(items) == 1


def test_find_items():
    items = {}
    add_item(items, "Молоко", "Продукты", "л", 5, 2, date(2026, 9, 8))
    assert find_items(items, "моло")


def test_filter_items_by_category():
    items = {}
    add_item(items, "Молоко", "Продукты", "л", 5, 2, date(2026, 9, 8))
    add_item(items, "Мыло", "Бытовая химия", "шт", 3, 1, date(2026, 9, 8))
    assert len(filter_items_by_category(items, "Продукты")) == 1


def test_sort_items_by_quantity():
    items = {}
    add_item(items, "Молоко", "Продукты", "л", 5, 2, date(2026, 9, 8))
    add_item(items, "Мыло", "Бытовая химия", "шт", 1, 1, date(2026, 9, 8))
    sorted_items = sort_items_by_quantity(items)
    quantities = [item["quantity"] for _, item in sorted_items]
    assert quantities == [1, 5]


def test_get_item_unknown_id():
    with pytest.raises(KeyError):
        get_item({}, 1)
