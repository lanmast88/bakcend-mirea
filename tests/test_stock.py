"""Тесты функций изменения и контроля остатков."""

import pytest

from home_inventory.stock import (
    consume_item,
    get_low_stock_items,
    get_stock_status,
    restock_item,
)


def test_consume_item(make_items):
    assert consume_item(make_items(), 1, 3) == 2


def test_consume_more_than_available(make_items):
    with pytest.raises(ValueError):
        consume_item(make_items(), 1, 10)


def test_restock_item(make_items):
    assert restock_item(make_items(), 1, 4) == 9


def test_get_low_stock_items(make_items):
    assert len(get_low_stock_items(make_items(quantity=1))) == 1


def test_get_stock_status():
    assert get_stock_status(0, 2) == "Товар закончился, необходимо купить"
    assert get_stock_status(5, 2) == "Запас товара в норме"
