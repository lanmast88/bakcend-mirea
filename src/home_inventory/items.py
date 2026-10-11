"""Функции для работы с товарами."""

from datetime import date


def add_item(
    items: dict[int, dict],
    name: str,
    category: str,
    unit: str,
    quantity: int,
    min_threshold: int,
    date_added: date,
) -> int:
    """Добавить товар в словарь items и вернуть его идентификатор."""
    if not name.strip():
        raise ValueError("Название товара не может быть пустым")
    if quantity < 0:
        raise ValueError("Количество не может быть отрицательным")
    if min_threshold < 0:
        raise ValueError("Порог запаса не может быть отрицательным")

    item_id = max(items, default=0) + 1
    items[item_id] = {
        "name": name.strip(),
        "category": category.strip(),
        "unit": unit.strip(),
        "quantity": quantity,
        "min_threshold": min_threshold,
        "date_added": date_added,
    }
    return item_id


def get_item(items: dict[int, dict], item_id: int) -> dict:
    """Вернуть товар по идентификатору."""
    if item_id not in items:
        raise KeyError(f"Товар с идентификатором {item_id} не найден")
    return items[item_id]


def find_items(items: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти товары по подстроке названия."""
    query = query.strip().lower()
    return {
        item_id: item
        for item_id, item in items.items()
        if query in item["name"].lower()
    }


def filter_items_by_category(
    items: dict[int, dict],
    category: str,
) -> dict[int, dict]:
    """Отобрать товары выбранной категории."""
    category = category.strip().lower()
    return {
        item_id: item
        for item_id, item in items.items()
        if item["category"].lower() == category
    }


def sort_items_by_quantity(
    items: dict[int, dict],
    descending: bool = False,
) -> list[tuple[int, dict]]:
    """Отсортировать товары по остатку."""
    return sorted(
        items.items(),
        key=lambda pair: pair[1]["quantity"],
        reverse=descending,
    )


def get_add_confirmation(
    item_name: str,
    category: str,
    quantity: int,
    unit: str,
) -> str:
    """Вернуть текст подтверждения добавления товара."""
    if quantity > 0:
        return (
            f"Товар '{item_name}' добавлен в категорию '{category}' "
            f"в количестве {quantity} {unit}"
        )
    return (
        f"Товар '{item_name}' не добавлен: "
        "количество должно быть больше нуля"
    )
