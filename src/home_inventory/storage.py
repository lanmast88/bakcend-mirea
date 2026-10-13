"""Преобразование объектов предметной области в JSON и обратно.

JSON остаётся форматом хранения данных: в файлах сохраняются только
значения атрибутов и идентификаторы связанных объектов. При загрузке
данные превращаются в объекты классов ``Category``, ``Item``, ``User``
и ``StockOperation``, при сохранении — обратно в структуры JSON.
"""

import json
from pathlib import Path

from home_inventory.config import (
    CATEGORIES_FILE,
    ITEMS_FILE,
    OPERATIONS_FILE,
    STORAGE_DATE_FORMAT,
    USERS_FILE,
)
from home_inventory.models import Category, Item, StockOperation, User
from home_inventory.models.categories import find_category_by_id
from home_inventory.models.items import find_item_by_id
from home_inventory.models.operations import operation_class
from home_inventory.models.users import find_user_by_id


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


def load_categories(
    filename: Path | str = CATEGORIES_FILE,
) -> list[Category]:
    """Загрузить категории из JSON-файла в коллекцию объектов."""
    return [Category.from_data(record) for record in _read_json(filename)]


def save_categories(
    categories: list[Category],
    filename: Path | str = CATEGORIES_FILE,
) -> None:
    """Сохранить объекты категорий в JSON-файл."""
    records = [
        {"id": category.id, "name": category.name}
        for category in categories
    ]
    _write_json(filename, records)


def load_items(
    categories: list[Category],
    filename: Path | str = ITEMS_FILE,
) -> list[Item]:
    """Загрузить товары из JSON-файла, связав их с категориями."""
    items = []
    for record in _read_json(filename):
        category_id = int(record["category_id"])
        category = find_category_by_id(categories, category_id)
        if category is None:
            raise ValueError(
                f"Для товара {record['id']} не найдена "
                f"категория {category_id}"
            )
        items.append(Item.from_data(record, category))
    return items


def save_items(
    items: list[Item],
    filename: Path | str = ITEMS_FILE,
) -> None:
    """Сохранить объекты товаров в JSON-файл."""
    records = [
        {
            "id": item.id,
            "name": item.name,
            "category_id": item.category.id,
            "unit": item.unit,
            "quantity": item.quantity,
            "min_threshold": item.min_threshold,
            "date_added": item.date_added.strftime(STORAGE_DATE_FORMAT),
        }
        for item in items
    ]
    _write_json(filename, records)


def load_users(filename: Path | str = USERS_FILE) -> list[User]:
    """Загрузить пользователей из JSON-файла в коллекцию объектов."""
    return [User.from_data(record) for record in _read_json(filename)]


def save_users(
    users: list[User],
    filename: Path | str = USERS_FILE,
) -> None:
    """Сохранить объекты пользователей в JSON-файл."""
    records = [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password,
        }
        for user in users
    ]
    _write_json(filename, records)


def load_operations(
    items: list[Item],
    users: list[User],
    filename: Path | str = OPERATIONS_FILE,
) -> list[StockOperation]:
    """Загрузить журнал операций, восстановив связи с объектами."""
    operations = []
    for record in _read_json(filename):
        item = find_item_by_id(items, int(record["item_id"]))
        user = find_user_by_id(users, int(record["user_id"]))
        if item is None or user is None:
            raise ValueError(
                f"Для операции {record['id']} не найден "
                "связанный товар или пользователь"
            )
        operation_type = operation_class(record["kind"])
        operations.append(operation_type.from_data(record, item, user))
    return operations


def save_operations(
    operations: list[StockOperation],
    filename: Path | str = OPERATIONS_FILE,
) -> None:
    """Сохранить журнал операций в JSON-файл."""
    records = [
        {
            "id": operation.id,
            "kind": operation.KIND,
            "item_id": operation.item.id,
            "user_id": operation.user.id,
            "amount": operation.amount,
            "date": operation.date.strftime(STORAGE_DATE_FORMAT),
        }
        for operation in operations
    ]
    _write_json(filename, records)
