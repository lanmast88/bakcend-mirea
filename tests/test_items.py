"""Тесты класса Item и функций работы с товарами."""

from datetime import date

import pytest

from home_inventory.models import Item
from home_inventory.models.items import (
    add_item,
    filter_items_by_category,
    find_item_by_id,
    find_items,
    get_add_confirmation,
    get_item,
    get_low_stock_items,
    sort_items_by_quantity,
)

TEST_DATE = date(2026, 9, 8)


def test_item_creation(category):
    item = Item(1, "Молоко", category, "л", 5, 2, TEST_DATE)

    assert item.id == 1
    assert item.name == "Молоко"
    assert item.category is category
    assert item.unit == "л"
    assert item.quantity == 5
    assert item.min_threshold == 2
    assert item.date_added == TEST_DATE


def test_item_str(item):
    assert str(item) == "#1 Молоко (Продукты): 5 л"


def test_item_empty_name(category):
    with pytest.raises(ValueError):
        Item(1, "   ", category, "л", 5, 2, TEST_DATE)


def test_item_negative_quantity(category):
    with pytest.raises(ValueError):
        Item(1, "Молоко", category, "л", -1, 2, TEST_DATE)


def test_item_negative_threshold(category):
    with pytest.raises(ValueError):
        Item(1, "Молоко", category, "л", 5, -1, TEST_DATE)


def test_item_quantity_is_read_only(item):
    with pytest.raises(AttributeError):
        item.quantity = 100


def test_item_validate_quantity_is_static():
    assert Item.validate_quantity(0)
    assert not Item.validate_quantity(-1)


def test_item_from_data(category):
    item = Item.from_data(
        {
            "id": "7",
            "name": "Молоко",
            "unit": "л",
            "quantity": "5",
            "min_threshold": "2",
            "date_added": "2026-09-08",
        },
        category,
    )

    assert item.id == 7
    assert item.category is category
    assert item.quantity == 5
    assert item.date_added == TEST_DATE


def test_item_consume(item):
    assert item.consume(3) == 2
    assert item.quantity == 2


def test_item_consume_more_than_available(item):
    with pytest.raises(ValueError):
        item.consume(10)
    assert item.quantity == 5


def test_item_consume_not_positive(item):
    with pytest.raises(ValueError):
        item.consume(0)


def test_item_restock(item):
    assert item.restock(4) == 9
    assert item.quantity == 9


def test_item_restock_not_positive(item):
    with pytest.raises(ValueError):
        item.restock(0)


def test_item_is_low_stock(make_item):
    assert make_item(quantity=1).is_low_stock()
    assert not make_item(quantity=5).is_low_stock()


def test_item_is_out_of_stock(make_item):
    assert make_item(quantity=0).is_out_of_stock()
    assert not make_item(quantity=1).is_out_of_stock()


def test_item_stock_status(make_item):
    assert make_item(quantity=0).stock_status() == (
        "Товар закончился, необходимо купить"
    )
    assert make_item(quantity=1).stock_status() == (
        "Внимание: остаток товара ниже порога, пора пополнить запас"
    )
    assert make_item(quantity=5).stock_status() == "Запас товара в норме"


def test_item_is_in_category(item):
    assert item.is_in_category("продукты")
    assert not item.is_in_category("Лекарства")


def test_add_item_returns_object(category):
    items: list[Item] = []
    item = add_item(items, "Молоко", category, "л", 5, 2, TEST_DATE)

    assert isinstance(item, Item)
    assert item.id == 1
    assert items == [item]


def test_add_item_generates_next_id(items, categories):
    item = add_item(items, "Шампунь", categories[1], "шт", 2, 1, TEST_DATE)
    assert item.id == 3


def test_add_item_empty_name(category):
    with pytest.raises(ValueError):
        add_item([], "   ", category, "л", 5, 2, TEST_DATE)


def test_get_item(items):
    assert get_item(items, 2).name == "Мыло"


def test_get_item_unknown_id():
    with pytest.raises(KeyError):
        get_item([], 1)


def test_find_item_by_id(items):
    assert find_item_by_id(items, 1) is items[0]
    assert find_item_by_id(items, 99) is None


def test_find_items(items):
    found = find_items(items, "моло")
    assert [item.id for item in found] == [1]


def test_filter_items_by_category(items):
    found = filter_items_by_category(items, "Продукты")
    assert [item.name for item in found] == ["Молоко"]


def test_sort_items_by_quantity(items):
    quantities = [item.quantity for item in sort_items_by_quantity(items)]
    assert quantities == [1, 5]


def test_sort_items_by_quantity_descending(items):
    sorted_items = sort_items_by_quantity(items, descending=True)
    assert [item.quantity for item in sorted_items] == [5, 1]


def test_get_low_stock_items(make_item, categories):
    items = [make_item(quantity=1)]
    add_item(items, "Мыло", categories[1], "шт", 5, 1, TEST_DATE)
    low_stock = get_low_stock_items(items)

    assert [item.name for item in low_stock] == ["Молоко"]


def test_get_add_confirmation(item):
    assert "добавлен в категорию 'Продукты'" in get_add_confirmation(item)


def test_get_add_confirmation_zero_quantity(category):
    item = Item(1, "Молоко", category, "л", 0, 2, TEST_DATE)
    assert "не добавлен" in get_add_confirmation(item)
