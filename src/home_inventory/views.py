"""Форматирование и вывод данных проекта в консоль."""

from collections.abc import Iterable

TABLE_HEADER = (
    f"{'ID':<4}{'Название':<20}{'Категория':<16}{'Остаток':<12}Дата"
)


def format_items_table(rows: Iterable[tuple[int, dict]]) -> str:
    """Собрать таблицу товаров из пар «идентификатор — товар»."""
    lines = [TABLE_HEADER]
    for item_id, item in rows:
        quantity = f"{item['quantity']} {item['unit']}"
        lines.append(
            f"{item_id:<4}{item['name']:<20}{item['category']:<16}"
            f"{quantity:<12}{item['date_added']}"
        )
    return "\n".join(lines)


def print_items(rows: Iterable[tuple[int, dict]]) -> None:
    """Вывести товары в виде таблицы или сообщение о пустом результате."""
    rows = list(rows)
    if not rows:
        print("Товары не найдены")
        return
    print(format_items_table(rows))


def print_menu(actions: dict[str, tuple[str, object]]) -> None:
    """Вывести меню приложения."""
    print("\n=== Система учёта товаров в доме ===")
    for key, (title, _) in actions.items():
        print(f"{key}. {title}")
    print("0. Выход")
