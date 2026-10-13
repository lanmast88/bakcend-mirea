"""Тесты преобразования объектов в JSON и обратно."""

import pytest

from home_inventory.models import Consumption, Restocking, StockOperation
from home_inventory.storage import (
    load_categories,
    load_items,
    load_operations,
    load_users,
    save_categories,
    save_items,
    save_operations,
    save_users,
)


def test_save_and_load_categories(tmp_path, categories):
    filename = tmp_path / "categories.json"
    save_categories(categories, filename)
    loaded = load_categories(filename)

    assert [category.id for category in loaded] == [1, 2]
    assert [category.name for category in loaded] == [
        "Продукты",
        "Бытовая химия",
    ]


def test_save_and_load_items(tmp_path, items, categories):
    filename = tmp_path / "items.json"
    save_items(items, filename)
    loaded = load_items(categories, filename)

    assert len(loaded) == len(items)
    for restored, original in zip(loaded, items):
        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.unit == original.unit
        assert restored.quantity == original.quantity
        assert restored.min_threshold == original.min_threshold
        assert restored.date_added == original.date_added


def test_loaded_item_refers_to_category_object(tmp_path, items, categories):
    filename = tmp_path / "items.json"
    save_items(items, filename)
    loaded = load_items(categories, filename)

    assert loaded[0].category is categories[0]
    assert loaded[1].category is categories[1]


def test_load_items_with_unknown_category(tmp_path, items):
    filename = tmp_path / "items.json"
    save_items(items, filename)

    with pytest.raises(ValueError):
        load_items([], filename)


def test_load_missing_file(tmp_path):
    assert load_items([], tmp_path / "missing.json") == []


def test_load_broken_json(tmp_path):
    path = tmp_path / "items.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(ValueError):
        load_items([], path)


def test_save_and_load_users(tmp_path, users):
    filename = tmp_path / "users.json"
    save_users(users, filename)
    loaded = load_users(filename)

    assert loaded[0].id == users[0].id
    assert loaded[0].username == users[0].username
    assert loaded[0].check_password("qwerty123")


def test_save_and_load_operations(tmp_path, items, users):
    filename = tmp_path / "operations.json"
    operations: list[StockOperation] = [
        Consumption(1, items[0], users[0], 2),
        Restocking(2, items[1], users[0], 3),
    ]
    save_operations(operations, filename)
    loaded = load_operations(items, users, filename)

    assert isinstance(loaded[0], Consumption)
    assert isinstance(loaded[1], Restocking)
    assert [operation.amount for operation in loaded] == [2, 3]


def test_loaded_operation_refers_to_objects(tmp_path, items, users):
    filename = tmp_path / "operations.json"
    save_operations([Consumption(1, items[0], users[0], 2)], filename)
    loaded = load_operations(items, users, filename)

    assert loaded[0].item is items[0]
    assert loaded[0].user is users[0]
    assert loaded[0].item.category is items[0].category


def test_load_operations_does_not_change_stock(tmp_path, items, users):
    filename = tmp_path / "operations.json"
    save_operations([Consumption(1, items[0], users[0], 2)], filename)
    quantity = items[0].quantity
    load_operations(items, users, filename)

    assert items[0].quantity == quantity


def test_load_operations_with_unknown_links(tmp_path, items, users):
    filename = tmp_path / "operations.json"
    save_operations([Consumption(1, items[0], users[0], 2)], filename)

    with pytest.raises(ValueError):
        load_operations([], users, filename)
