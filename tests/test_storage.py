"""Тесты сохранения и загрузки данных в JSON-файлах."""

import pytest

from home_inventory.storage import load_items, save_items


def test_save_and_load_items(tmp_path, items):
    filename = tmp_path / "items.json"
    save_items(items, filename)
    assert load_items(filename) == items


def test_load_missing_file(tmp_path):
    assert load_items(tmp_path / "missing.json") == {}


def test_load_broken_json(tmp_path):
    path = tmp_path / "items.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError):
        load_items(path)
