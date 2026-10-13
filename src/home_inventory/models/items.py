"""Класс товара и функции работы с коллекцией товаров."""

from datetime import date

from .categories import Category


class Item:
    """Товар, хранящийся в доме."""

    def __init__(
        self,
        item_id: int,
        name: str,
        category: Category,
        unit: str,
        quantity: int,
        min_threshold: int,
        date_added: date,
    ) -> None:
        """Создать товар и сохранить переданные данные в атрибутах."""
        name = name.strip()
        if not name:
            raise ValueError("Название товара не может быть пустым")
        if not self.validate_quantity(quantity):
            raise ValueError("Количество не может быть отрицательным")
        if min_threshold < 0:
            raise ValueError("Порог запаса не может быть отрицательным")

        self.id = item_id
        self.name = name
        self.category = category
        self.unit = unit.strip()
        self.min_threshold = min_threshold
        self.date_added = date_added
        self._quantity = quantity

    @property
    def quantity(self) -> int:
        """Остаток товара; изменяется методами consume() и restock()."""
        return self._quantity

    @staticmethod
    def validate_quantity(quantity: int) -> bool:
        """Проверить корректность количества товара."""
        return quantity >= 0

    @classmethod
    def from_data(cls, data: dict, category: Category) -> "Item":
        """Создать товар из набора данных JSON и объекта категории."""
        return cls(
            item_id=int(data["id"]),
            name=data["name"],
            category=category,
            unit=data["unit"],
            quantity=int(data["quantity"]),
            min_threshold=int(data["min_threshold"]),
            date_added=date.fromisoformat(data["date_added"]),
        )

    def consume(self, amount: int) -> int:
        """Списать расход товара и вернуть новый остаток."""
        if amount <= 0:
            raise ValueError("Расход должен быть больше нуля")
        if amount > self._quantity:
            raise ValueError(
                f"Нельзя списать {amount} {self.unit}: "
                f"в наличии {self._quantity} {self.unit}"
            )

        self._quantity -= amount
        return self._quantity

    def restock(self, amount: int) -> int:
        """Пополнить запас товара и вернуть новый остаток."""
        if amount <= 0:
            raise ValueError("Пополнение должно быть больше нуля")

        self._quantity += amount
        return self._quantity

    def is_out_of_stock(self) -> bool:
        """Проверить, что товар закончился."""
        return self._quantity <= 0

    def is_low_stock(self) -> bool:
        """Проверить, что остаток опустился ниже порога пополнения."""
        return self._quantity < self.min_threshold

    def is_in_category(self, name: str) -> bool:
        """Проверить принадлежность товара категории с таким названием."""
        return self.category.matches(name)

    def matches(self, query: str) -> bool:
        """Проверить вхождение подстроки в название товара."""
        return query.strip().lower() in self.name.lower()

    def stock_status(self) -> str:
        """Вернуть текстовый статус запаса товара."""
        if self.is_out_of_stock():
            return "Товар закончился, необходимо купить"
        if self.is_low_stock():
            return "Внимание: остаток товара ниже порога, пора пополнить запас"
        return "Запас товара в норме"

    def __str__(self) -> str:
        """Вернуть строковое представление товара."""
        return (
            f"#{self.id} {self.name} ({self.category.name}): "
            f"{self._quantity} {self.unit}"
        )


def add_item(
    items: list[Item],
    name: str,
    category: Category,
    unit: str,
    quantity: int,
    min_threshold: int,
    date_added: date,
) -> Item:
    """Создать товар, добавить его в коллекцию и вернуть объект."""
    item_id = max((item.id for item in items), default=0) + 1
    item = Item(
        item_id, name, category, unit, quantity, min_threshold, date_added
    )
    items.append(item)
    return item


def get_item(items: list[Item], item_id: int) -> Item:
    """Вернуть товар по идентификатору."""
    item = find_item_by_id(items, item_id)
    if item is None:
        raise KeyError(f"Товар с идентификатором {item_id} не найден")
    return item


def find_item_by_id(items: list[Item], item_id: int) -> Item | None:
    """Найти товар по идентификатору."""
    for item in items:
        if item.id == item_id:
            return item
    return None


def find_items(items: list[Item], query: str) -> list[Item]:
    """Найти товары по подстроке названия."""
    return [item for item in items if item.matches(query)]


def filter_items_by_category(
    items: list[Item],
    category_name: str,
) -> list[Item]:
    """Отобрать товары выбранной категории."""
    return [item for item in items if item.is_in_category(category_name)]


def sort_items_by_quantity(
    items: list[Item],
    descending: bool = False,
) -> list[Item]:
    """Отсортировать товары по остатку."""
    return sorted(
        items,
        key=lambda item: item.quantity,
        reverse=descending,
    )


def get_low_stock_items(items: list[Item]) -> list[Item]:
    """Отобрать товары, остаток которых ниже порога."""
    return [item for item in items if item.is_low_stock()]


def get_add_confirmation(item: Item) -> str:
    """Вернуть текст подтверждения добавления товара."""
    if item.quantity > 0:
        return (
            f"Товар '{item.name}' добавлен в категорию "
            f"'{item.category.name}' в количестве "
            f"{item.quantity} {item.unit}"
        )
    return (
        f"Товар '{item.name}' не добавлен: "
        "количество должно быть больше нуля"
    )
