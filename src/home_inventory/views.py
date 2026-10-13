"""Форматирование и вывод объектов предметной области в консоль."""

from collections.abc import Iterable

from home_inventory.models import Item, StockOperation

TABLE_HEADER = (
    f"{'ID':<4}{'Название':<20}{'Категория':<16}{'Остаток':<12}Дата"
)


def format_items_table(items: Iterable[Item]) -> str:
    """Собрать таблицу товаров из коллекции объектов Item."""
    lines = [TABLE_HEADER]
    for item in items:
        quantity = f"{item.quantity} {item.unit}"
        lines.append(
            f"{item.id:<4}{item.name:<20}{item.category.name:<16}"
            f"{quantity:<12}{item.date_added}"
        )
    return "\n".join(lines)


def print_items(items: Iterable[Item]) -> None:
    """Вывести товары в виде таблицы или сообщение о пустом результате."""
    items = list(items)
    if not items:
        print("Товары не найдены")
        return
    print(format_items_table(items))


def format_operations_log(operations: Iterable[StockOperation]) -> str:
    """Собрать журнал операций из строковых представлений объектов."""
    return "\n".join(str(operation) for operation in operations)


def print_operations(operations: Iterable[StockOperation]) -> None:
    """Вывести журнал операций или сообщение о его отсутствии."""
    operations = list(operations)
    if not operations:
        print("Операции не выполнялись")
        return
    print(format_operations_log(operations))


def print_menu(actions: dict[str, tuple[str, object]]) -> None:
    """Вывести меню приложения."""
    print("\n=== Система учёта товаров в доме ===")
    for key, (title, _) in actions.items():
        print(f"{key}. {title}")
    print("0. Выход")
