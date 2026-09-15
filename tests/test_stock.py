from datetime import date

import pytest

from items import add_item
from stock import (
    consume_item,
    get_low_stock_items,
    get_stock_status,
    restock_item,
)


def make_items(quantity: int = 5, min_threshold: int = 2) -> dict[int, dict]:
    items = {}
    add_item(
        items, "Молоко", "Продукты", "л",
        quantity, min_threshold, date(2026, 9, 8),
    )
    return items


def test_consume_item():
    items = make_items()
    assert consume_item(items, 1, 3) == 2


def test_consume_more_than_available():
    items = make_items()
    with pytest.raises(ValueError):
        consume_item(items, 1, 10)


def test_restock_item():
    items = make_items()
    assert restock_item(items, 1, 4) == 9


def test_get_low_stock_items():
    items = make_items(quantity=1)
    assert len(get_low_stock_items(items)) == 1


def test_get_stock_status():
    assert get_stock_status(0, 2) == "Товар закончился, необходимо купить"
    assert get_stock_status(5, 2) == "Запас товара в норме"
