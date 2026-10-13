"""Тесты классов операций с запасом и журнала операций."""

from datetime import date

import pytest

from home_inventory.models import Consumption, Restocking, StockOperation
from home_inventory.models.operations import (
    consume_item,
    next_operation_id,
    operation_class,
    register_operation,
    restock_item,
)

TEST_DATE = date(2026, 9, 12)


def test_operation_links_item_and_user(item, user):
    operation = Consumption(1, item, user, 2, TEST_DATE)

    assert operation.id == 1
    assert operation.item is item
    assert operation.user is user
    assert operation.amount == 2
    assert operation.date == TEST_DATE


def test_operation_reaches_related_objects(item, user):
    operation = Consumption(1, item, user, 2, TEST_DATE)

    assert operation.item.name == "Молоко"
    assert operation.item.category.name == "Продукты"
    assert operation.user.username == "ivan_petrov"


def test_operation_not_positive_amount(item, user):
    with pytest.raises(ValueError):
        Consumption(1, item, user, 0, TEST_DATE)


def test_operation_date_defaults_to_today(item, user):
    assert Consumption(1, item, user, 1).date == date.today()


def test_base_operation_apply_not_implemented(item, user):
    operation = StockOperation(1, item, user, 1, TEST_DATE)
    with pytest.raises(NotImplementedError):
        operation.apply()


def test_consumption_apply(item, user):
    assert Consumption(1, item, user, 3, TEST_DATE).apply() == 2
    assert item.quantity == 2


def test_restocking_apply(item, user):
    assert Restocking(1, item, user, 4, TEST_DATE).apply() == 9
    assert item.quantity == 9


def test_operations_are_polymorphic(make_item, user):
    results = []
    for operation_type in (Consumption, Restocking):
        operation = operation_type(1, make_item(), user, 1, TEST_DATE)
        results.append(operation.apply())

    assert results == [4, 6]


def test_operation_kind_and_title():
    assert Consumption.KIND == "consume"
    assert Restocking.KIND == "restock"
    assert Consumption.TITLE == "расход"


def test_operation_str(item, user):
    text = str(Consumption(1, item, user, 2, TEST_DATE))

    assert text.startswith("#1 2026-09-12: расход 2 л")
    assert "товар 'Молоко'" in text
    assert "пользователь 'ivan_petrov'" in text


def test_operation_from_data(item, user):
    operation = Consumption.from_data(
        {"id": "5", "amount": "2", "date": "2026-09-12"},
        item,
        user,
    )

    assert isinstance(operation, Consumption)
    assert operation.id == 5
    assert operation.item is item
    assert operation.date == TEST_DATE


def test_operation_class_by_kind():
    assert operation_class("consume") is Consumption
    assert operation_class("restock") is Restocking


def test_operation_class_unknown_kind():
    with pytest.raises(ValueError):
        operation_class("unknown")


def test_next_operation_id(item, user):
    assert next_operation_id([]) == 1
    assert next_operation_id([Consumption(4, item, user, 1, TEST_DATE)]) == 5


def test_register_operation_applies_and_appends(item, user):
    operations: list[StockOperation] = []
    operation = register_operation(
        operations, Restocking(1, item, user, 2, TEST_DATE)
    )

    assert operations == [operation]
    assert item.quantity == 7


def test_consume_item_registers_operation(item, user):
    operations: list[StockOperation] = []
    operation = consume_item(operations, item, user, 3, TEST_DATE)

    assert isinstance(operation, Consumption)
    assert operations == [operation]
    assert item.quantity == 2


def test_consume_more_than_available(item, user):
    operations: list[StockOperation] = []
    with pytest.raises(ValueError):
        consume_item(operations, item, user, 10, TEST_DATE)

    assert operations == []
    assert item.quantity == 5


def test_restock_item_registers_operation(item, user):
    operations: list[StockOperation] = []
    operation = restock_item(operations, item, user, 4, TEST_DATE)

    assert isinstance(operation, Restocking)
    assert operation.id == 1
    assert item.quantity == 9


def test_operations_share_journal(items, user):
    operations: list[StockOperation] = []
    consume_item(operations, items[0], user, 1, TEST_DATE)
    restock_item(operations, items[1], user, 2, TEST_DATE)

    assert [operation.id for operation in operations] == [1, 2]
    assert items[0].quantity == 4
    assert items[1].quantity == 3
