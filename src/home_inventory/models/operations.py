"""Классы операций с запасом и функции работы с их журналом.

Операция связывает товар :class:`~home_inventory.models.items.Item` и
пользователя :class:`~home_inventory.models.users.User`: объект операции
хранит ссылки на оба объекта, а не только их идентификаторы.
"""

from datetime import date

from .items import Item
from .users import User


class StockOperation:
    """Операция изменения остатка товара, выполненная пользователем."""

    #: Код операции при хранении в JSON (атрибут класса).
    KIND = "operation"

    #: Название операции для вывода в журнале (атрибут класса).
    TITLE = "операция"

    def __init__(
        self,
        operation_id: int,
        item: Item,
        user: User,
        amount: int,
        operation_date: date | None = None,
    ) -> None:
        """Создать операцию, связав товар и пользователя."""
        if amount <= 0:
            raise ValueError("Количество в операции должно быть больше нуля")

        self.id = operation_id
        self.item = item
        self.user = user
        self.amount = amount
        self.date = operation_date or date.today()

    @classmethod
    def from_data(
        cls,
        data: dict,
        item: Item,
        user: User,
    ) -> "StockOperation":
        """Создать операцию из данных JSON и связанных объектов."""
        return cls(
            operation_id=int(data["id"]),
            item=item,
            user=user,
            amount=int(data["amount"]),
            operation_date=date.fromisoformat(data["date"]),
        )

    def apply(self) -> int:
        """Применить операцию к товару и вернуть новый остаток."""
        raise NotImplementedError(
            "Класс операции должен определить метод apply()"
        )

    def __str__(self) -> str:
        """Вернуть строковое представление операции."""
        return (
            f"#{self.id} {self.date}: {self.TITLE} "
            f"{self.amount} {self.item.unit} — товар '{self.item.name}', "
            f"пользователь '{self.user.username}'"
        )


class Consumption(StockOperation):
    """Списание расхода товара."""

    KIND = "consume"
    TITLE = "расход"

    def apply(self) -> int:
        """Списать расход товара и вернуть новый остаток."""
        return self.item.consume(self.amount)


class Restocking(StockOperation):
    """Пополнение запаса товара."""

    KIND = "restock"
    TITLE = "пополнение"

    def apply(self) -> int:
        """Пополнить запас товара и вернуть новый остаток."""
        return self.item.restock(self.amount)


#: Классы операций по коду, с которым операция хранится в JSON.
OPERATION_CLASSES: dict[str, type[StockOperation]] = {
    Consumption.KIND: Consumption,
    Restocking.KIND: Restocking,
}


def operation_class(kind: str) -> type[StockOperation]:
    """Вернуть класс операции по её коду."""
    if kind not in OPERATION_CLASSES:
        raise ValueError(f"Неизвестный тип операции: {kind}")
    return OPERATION_CLASSES[kind]


def next_operation_id(operations: list[StockOperation]) -> int:
    """Вернуть следующий идентификатор операции."""
    return max((operation.id for operation in operations), default=0) + 1


def find_operation_by_id(
    operations: list[StockOperation],
    operation_id: int,
) -> StockOperation | None:
    """Найти операцию по идентификатору."""
    for operation in operations:
        if operation.id == operation_id:
            return operation
    return None


def register_operation(
    operations: list[StockOperation],
    operation: StockOperation,
) -> StockOperation:
    """Применить операцию к товару и записать её в журнал."""
    operation.apply()
    operations.append(operation)
    return operation


def consume_item(
    operations: list[StockOperation],
    item: Item,
    user: User,
    amount: int,
    operation_date: date | None = None,
) -> StockOperation:
    """Списать расход товара и зарегистрировать операцию."""
    return register_operation(
        operations,
        Consumption(
            next_operation_id(operations),
            item,
            user,
            amount,
            operation_date,
        ),
    )


def restock_item(
    operations: list[StockOperation],
    item: Item,
    user: User,
    amount: int,
    operation_date: date | None = None,
) -> StockOperation:
    """Пополнить запас товара и зарегистрировать операцию."""
    return register_operation(
        operations,
        Restocking(
            next_operation_id(operations),
            item,
            user,
            amount,
            operation_date,
        ),
    )


def find_item_operations(
    operations: list[StockOperation],
    item: Item,
) -> list[StockOperation]:
    """Отобрать операции, выполненные с указанным товаром."""
    return [
        operation for operation in operations if operation.item is item
    ]
