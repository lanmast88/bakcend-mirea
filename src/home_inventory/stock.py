"""Функции для изменения и контроля остатков товаров."""

from home_inventory.items import get_item


def get_stock_status(quantity: int, min_threshold: int) -> str:
    """Вернуть текстовый статус запаса товара."""
    if quantity <= 0:
        return "Товар закончился, необходимо купить"
    elif quantity < min_threshold:
        return "Внимание: остаток товара ниже порога, пора пополнить запас"
    else:
        return "Запас товара в норме"


def consume_item(items: dict[int, dict], item_id: int, amount: int) -> int:
    """Списать расход товара и вернуть новый остаток."""
    if amount <= 0:
        raise ValueError("Расход должен быть больше нуля")

    item = get_item(items, item_id)
    if amount > item["quantity"]:
        raise ValueError(
            f"Нельзя списать {amount} {item['unit']}: "
            f"в наличии {item['quantity']} {item['unit']}"
        )

    item["quantity"] -= amount
    return item["quantity"]


def restock_item(items: dict[int, dict], item_id: int, amount: int) -> int:
    """Пополнить запас товара и вернуть новый остаток."""
    if amount <= 0:
        raise ValueError("Пополнение должно быть больше нуля")

    item = get_item(items, item_id)
    item["quantity"] += amount
    return item["quantity"]


def get_low_stock_items(items: dict[int, dict]) -> dict[int, dict]:
    """Отобрать товары, остаток которых ниже порога."""
    return {
        item_id: item
        for item_id, item in items.items()
        if item["quantity"] < item["min_threshold"]
    }
