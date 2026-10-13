"""Классы предметной области приложения учёта товаров в доме.

Пакет собирает классы, которыми описываются сущности предметной
области, и функции работы с коллекциями этих объектов:

* :mod:`home_inventory.models.categories` — категория товаров;
* :mod:`home_inventory.models.items` — товар и его остаток;
* :mod:`home_inventory.models.users` — пользователь системы;
* :mod:`home_inventory.models.operations` — операции расхода и
  пополнения, связывающие товар и пользователя.
"""

from .categories import Category
from .items import Item
from .operations import Consumption, Restocking, StockOperation
from .users import User

__all__ = [
    "Category",
    "Consumption",
    "Item",
    "Restocking",
    "StockOperation",
    "User",
]
