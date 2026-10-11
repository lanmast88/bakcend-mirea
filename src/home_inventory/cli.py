"""Меню приложения и точка запуска сценария взаимодействия."""

from collections.abc import Callable

from home_inventory.auth import authenticate, get_login_status
from home_inventory.config import LOGIN_ATTEMPTS
from home_inventory.items import (
    add_item,
    filter_items_by_category,
    find_items,
    get_add_confirmation,
    get_item,
    sort_items_by_quantity,
)
from home_inventory.stock import (
    consume_item,
    get_low_stock_items,
    get_stock_status,
    restock_item,
)
from home_inventory.storage import load_items, load_users, save_items
from home_inventory.utils import input_date, input_int, input_text
from home_inventory.views import print_items, print_menu

#: Действие меню получает товары и возвращает признак изменения данных.
Action = Callable[[dict[int, dict]], bool]


def show_items(items: dict[int, dict]) -> bool:
    """Вывести список товаров."""
    print_items(items.items())
    return False


def find_items_action(items: dict[int, dict]) -> bool:
    """Вывести товары, найденные по подстроке названия."""
    query = input_text("Название или его часть: ")
    print_items(find_items(items, query).items())
    return False


def show_category(items: dict[int, dict]) -> bool:
    """Вывести товары выбранной категории."""
    category = input_text("Категория: ")
    print_items(filter_items_by_category(items, category).items())
    return False


def show_sorted_items(items: dict[int, dict]) -> bool:
    """Вывести товары, упорядоченные по остатку."""
    print_items(sort_items_by_quantity(items))
    return False


def show_low_stock(items: dict[int, dict]) -> bool:
    """Вывести товары, остаток которых ниже порога."""
    low_stock = get_low_stock_items(items)
    if not low_stock:
        print("Все запасы в норме")
        return False
    print_items(low_stock.items())
    return False


def add_item_action(items: dict[int, dict]) -> bool:
    """Добавить новый товар."""
    name = input_text("Название: ")
    category = input_text("Категория: ")
    unit = input_text("Единица измерения: ")
    quantity = input_int("Количество: ")
    min_threshold = input_int("Порог пополнения: ")
    date_added = input_date("Дата добавления (ДД.ММ.ГГГГ, Enter — сегодня): ")

    add_item(
        items, name, category, unit, quantity, min_threshold, date_added
    )
    print(get_add_confirmation(name, category, quantity, unit))
    return True


def consume_item_action(items: dict[int, dict]) -> bool:
    """Списать расход товара."""
    return change_quantity(items, consume_item, "Расход: ")


def restock_item_action(items: dict[int, dict]) -> bool:
    """Пополнить запас товара."""
    return change_quantity(items, restock_item, "Пополнение: ")


def change_quantity(
    items: dict[int, dict],
    operation: Callable[[dict[int, dict], int, int], int],
    prompt: str,
) -> bool:
    """Изменить остаток товара выбранной операцией."""
    item_id = input_int("Идентификатор товара: ", min_value=1)
    item = get_item(items, item_id)
    amount = input_int(prompt, min_value=1)

    quantity = operation(items, item_id, amount)
    print(f"Остаток товара '{item['name']}': {quantity} {item['unit']}")
    print(get_stock_status(quantity, item["min_threshold"]))
    return True


def login(users: list[dict]) -> bool:
    """Авторизовать пользователя, давая LOGIN_ATTEMPTS попыток."""
    for _ in range(LOGIN_ATTEMPTS):
        username = input_text("Имя пользователя: ")
        password = input_text("Пароль: ")
        is_logged_in = authenticate(users, username, password)
        print(get_login_status(username, is_logged_in))
        if is_logged_in:
            return True
    return False


ACTIONS: dict[str, tuple[str, Action]] = {
    "1": ("Показать товары", show_items),
    "2": ("Найти товар по названию", find_items_action),
    "3": ("Показать товары категории", show_category),
    "4": ("Показать товары по остатку", show_sorted_items),
    "5": ("Добавить товар", add_item_action),
    "6": ("Списать расход", consume_item_action),
    "7": ("Пополнить запас", restock_item_action),
    "8": ("Показать товары ниже порога", show_low_stock),
}


def run_action(items: dict[int, dict], choice: str) -> bool:
    """Выполнить пункт меню и вернуть признак изменения данных."""
    action = ACTIONS.get(choice)
    if action is None:
        print("Такого пункта меню нет")
        return False

    try:
        return action[1](items)
    except KeyError as error:
        print(f"Ошибка: {error.args[0]}")
    except ValueError as error:
        print(f"Ошибка: {error}")
    return False


def menu_loop(items: dict[int, dict]) -> None:
    """Выполнять пункты меню до выбора выхода, сохраняя изменения."""
    while True:
        print_menu(ACTIONS)
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            break

        if run_action(items, choice):
            save_items(items)


def main() -> None:
    """Загрузить данные, авторизовать пользователя и выполнить меню."""
    try:
        users = load_users()
        items = load_items()
    except (OSError, ValueError, KeyError) as error:
        print(f"Не удалось загрузить данные: {error}")
        return

    if not login(users):
        return

    menu_loop(items)
    print("Работа завершена")


def run() -> None:
    """Запустить приложение, перехватывая прерывание ввода."""
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nРабота прервана")


if __name__ == "__main__":
    run()
