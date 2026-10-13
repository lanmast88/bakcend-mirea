"""Тесты форматирования вывода объектов."""

from datetime import date

from home_inventory.models import Consumption
from home_inventory.views import format_items_table, format_operations_log


def test_format_items_table_contains_header(items):
    table = format_items_table(items)
    assert table.splitlines()[0].startswith("ID")


def test_format_items_table_row_per_item(items):
    table = format_items_table(items)
    assert len(table.splitlines()) == len(items) + 1


def test_format_items_table_shows_category_name(items):
    table = format_items_table(items)
    assert "Продукты" in table.splitlines()[1]


def test_format_operations_log(item, user):
    operations = [
        Consumption(1, item, user, 2, date(2026, 9, 12)),
        Consumption(2, item, user, 1, date(2026, 9, 13)),
    ]
    log = format_operations_log(operations)

    assert len(log.splitlines()) == 2
    assert "расход 2 л" in log
