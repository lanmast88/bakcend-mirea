"""Меню приложения и сценарии взаимодействия объектов."""

from collections.abc import Callable

from home_inventory.config import LOGIN_ATTEMPTS
from home_inventory.models import Category, Item, StockOperation, User
from home_inventory.models.categories import get_or_create_category
from home_inventory.models.items import (
    add_item,
    filter_items_by_category,
    find_items,
    get_add_confirmation,
    get_item,
    get_low_stock_items,
    sort_items_by_quantity,
)
from home_inventory.models.operations import consume_item, restock_item
from home_inventory.models.users import authenticate, get_login_status
from home_inventory.storage import (
    load_categories,
    load_items,
    load_operations,
    load_users,
    save_categories,
    save_items,
    save_operations,
)
from home_inventory.utils import input_date, input_int, input_text
from home_inventory.views import print_items, print_menu, print_operations


class AppContext:
    """Коллекции объектов приложения и авторизованный пользователь."""

    def __init__(
        self,
        categories: list[Category],
        items: list[Item],
        users: list[User],
        operations: list[StockOperation],
        current_user: User,
    ) -> None:
        """Сохранить коллекции объектов и текущего пользователя."""
        self.categories = categories
        self.items = items
        self.users = users
        self.operations = operations
        self.current_user = current_user


#: Действие меню получает состояние приложения и возвращает
#: признак изменения данных.
Action = Callable[[AppContext], bool]

#: Операция изменения остатка товара из модуля operations.
StockChange = Callable[
    [list[StockOperation], Item, User, int],
    StockOperation,
]


def show_items(context: AppContext) -> bool:
    """Вывести список товаров."""
    print_items(context.items)
    return False


def find_items_action(context: AppContext) -> bool:
    """Вывести товары, найденные по подстроке названия."""
    query = input_text("Название или его часть: ")
    print_items(find_items(context.items, query))
    return False


def show_category(context: AppContext) -> bool:
    """Вывести товары выбранной категории."""
    category = input_text("Категория: ")
    print_items(filter_items_by_category(context.items, category))
    return False


def show_sorted_items(context: AppContext) -> bool:
    """Вывести товары, упорядоченные по остатку."""
    print_items(sort_items_by_quantity(context.items))
    return False


def show_low_stock(context: AppContext) -> bool:
    """Вывести товары, остаток которых ниже порога."""
    low_stock = get_low_stock_items(context.items)
    if not low_stock:
        print("Все запасы в норме")
        return False
    print_items(low_stock)
    return False


def show_operations(context: AppContext) -> bool:
    """Вывести журнал операций расхода и пополнения."""
    print_operations(context.operations)
    return False


def add_item_action(context: AppContext) -> bool:
    """Добавить новый товар."""
    name = input_text("Название: ")
    category_name = input_text("Категория: ")
    unit = input_text("Единица измерения: ")
    quantity = input_int("Количество: ")
    min_threshold = input_int("Порог пополнения: ")
    date_added = input_date("Дата добавления (ДД.ММ.ГГГГ, Enter — сегодня): ")

    category = get_or_create_category(context.categories, category_name)
    item = add_item(
        context.items,
        name,
        category,
        unit,
        quantity,
        min_threshold,
        date_added,
    )
    print(get_add_confirmation(item))
    return True


def consume_item_action(context: AppContext) -> bool:
    """Списать расход товара."""
    return change_quantity(context, consume_item, "Расход: ")


def restock_item_action(context: AppContext) -> bool:
    """Пополнить запас товара."""
    return change_quantity(context, restock_item, "Пополнение: ")


def change_quantity(
    context: AppContext,
    operation: StockChange,
    prompt: str,
) -> bool:
    """Изменить остаток товара выбранной операцией."""
    item_id = input_int("Идентификатор товара: ", min_value=1)
    item = get_item(context.items, item_id)
    amount = input_int(prompt, min_value=1)

    operation(context.operations, item, context.current_user, amount)
    print(f"Остаток товара '{item.name}': {item.quantity} {item.unit}")
    print(item.stock_status())
    return True


def login(users: list[User]) -> User | None:
    """Авторизовать пользователя, давая LOGIN_ATTEMPTS попыток."""
    for _ in range(LOGIN_ATTEMPTS):
        username = input_text("Имя пользователя: ")
        password = input_text("Пароль: ")
        user = authenticate(users, username, password)
        print(get_login_status(username, user is not None))
        if user is not None:
            return user
    return None


ACTIONS: dict[str, tuple[str, Action]] = {
    "1": ("Показать товары", show_items),
    "2": ("Найти товар по названию", find_items_action),
    "3": ("Показать товары категории", show_category),
    "4": ("Показать товары по остатку", show_sorted_items),
    "5": ("Добавить товар", add_item_action),
    "6": ("Списать расход", consume_item_action),
    "7": ("Пополнить запас", restock_item_action),
    "8": ("Показать товары ниже порога", show_low_stock),
    "9": ("Показать журнал операций", show_operations),
}


def run_action(context: AppContext, choice: str) -> bool:
    """Выполнить пункт меню и вернуть признак изменения данных."""
    action = ACTIONS.get(choice)
    if action is None:
        print("Такого пункта меню нет")
        return False

    try:
        return action[1](context)
    except KeyError as error:
        print(f"Ошибка: {error.args[0]}")
    except ValueError as error:
        print(f"Ошибка: {error}")
    return False


def save_data(context: AppContext) -> None:
    """Сохранить коллекции объектов в JSON-файлы."""
    save_categories(context.categories)
    save_items(context.items)
    save_operations(context.operations)


def menu_loop(context: AppContext) -> None:
    """Выполнять пункты меню до выбора выхода, сохраняя изменения."""
    while True:
        print_menu(ACTIONS)
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            break

        if run_action(context, choice):
            save_data(context)


def main() -> None:
    """Загрузить объекты, авторизовать пользователя и выполнить меню."""
    try:
        categories = load_categories()
        users = load_users()
        items = load_items(categories)
        operations = load_operations(items, users)
    except (OSError, ValueError, KeyError) as error:
        print(f"Не удалось загрузить данные: {error}")
        return

    current_user = login(users)
    if current_user is None:
        return

    menu_loop(
        AppContext(categories, items, users, operations, current_user)
    )
    print("Работа завершена")


def run() -> None:
    """Запустить приложение, перехватывая прерывание ввода."""
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nРабота прервана")


if __name__ == "__main__":
    run()
