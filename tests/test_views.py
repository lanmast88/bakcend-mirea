"""Тесты форматирования вывода."""

from home_inventory.views import format_items_table


def test_format_items_table_contains_header(items):
    table = format_items_table(items.items())
    assert table.splitlines()[0].startswith("ID")


def test_format_items_table_row_per_item(items):
    table = format_items_table(items.items())
    assert len(table.splitlines()) == len(items) + 1
