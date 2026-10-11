"""Пакет приложения учёта товаров в доме.

Логика приложения разделена по модулям:

* :mod:`home_inventory.config` — параметры приложения и пути к данным;
* :mod:`home_inventory.auth` — авторизация пользователя;
* :mod:`home_inventory.items` — работа с товарами;
* :mod:`home_inventory.stock` — изменение и контроль остатков;
* :mod:`home_inventory.storage` — чтение и запись JSON-файлов;
* :mod:`home_inventory.utils` — ввод данных с обработкой ошибок;
* :mod:`home_inventory.cli` — меню и точка запуска приложения.
"""

__all__ = ["__version__"]

__version__ = "0.2.0"
