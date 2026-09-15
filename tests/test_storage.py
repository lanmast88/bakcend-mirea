from datetime import date

import pytest

from items import add_item
from storage import load_items, save_items


def test_save_and_load_items(tmp_path):
    filename = str(tmp_path / "items.json")
    items = {}
    add_item(items, "Молоко", "Продукты", "л", 5, 2, date(2026, 9, 8))
    save_items(items, filename)
    assert load_items(filename) == items


def test_load_missing_file(tmp_path):
    assert load_items(str(tmp_path / "missing.json")) == {}


def test_load_broken_json(tmp_path):
    path = tmp_path / "items.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError):
        load_items(str(path))
