"""Функции сохранения и загрузки данных проекта в JSON-файлах."""

import json
from datetime import date
from pathlib import Path

from home_inventory.config import (
    ITEMS_FILE,
    STORAGE_DATE_FORMAT,
    USERS_FILE,
)


def _read_json(filename: Path | str) -> list:
    """Прочитать список записей из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Файл {filename} содержит некорректный JSON: {error}"
        ) from error

    if not isinstance(data, list):
        raise ValueError(f"Файл {filename} должен содержать список записей")
    return data


def _write_json(filename: Path | str, records: list) -> None:
    """Записать список записей в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


def load_items(filename: Path | str = ITEMS_FILE) -> dict[int, dict]:
    """Загрузить товары из JSON-файла в словарь."""
    items = {}
    for record in _read_json(filename):
        items[int(record["id"])] = {
            "name": record["name"],
            "category": record["category"],
            "unit": record["unit"],
            "quantity": int(record["quantity"]),
            "min_threshold": int(record["min_threshold"]),
            "date_added": date.fromisoformat(record["date_added"]),
        }
    return items


def save_items(
    items: dict[int, dict],
    filename: Path | str = ITEMS_FILE,
) -> None:
    """Сохранить товары в JSON-файл."""
    records = []
    for item_id, item in items.items():
        record = {"id": item_id, **item}
        record["date_added"] = item["date_added"].strftime(STORAGE_DATE_FORMAT)
        records.append(record)
    _write_json(filename, records)


def load_users(filename: Path | str = USERS_FILE) -> list[dict]:
    """Загрузить пользователей из JSON-файла."""
    return _read_json(filename)


def save_users(
    users: list[dict],
    filename: Path | str = USERS_FILE,
) -> None:
    """Сохранить пользователей в JSON-файл."""
    _write_json(filename, users)
