"""Пакет приложения учёта товаров в доме.

Предметная область описана классами пакета
:mod:`home_inventory.models`, остальные модули отвечают за хранение
данных, ввод, вывод и взаимодействие с пользователем:

* :mod:`home_inventory.config` — параметры приложения и пути к данным;
* :mod:`home_inventory.models.categories` — класс ``Category``;
* :mod:`home_inventory.models.items` — класс ``Item``;
* :mod:`home_inventory.models.users` — класс ``User`` и авторизация;
* :mod:`home_inventory.models.operations` — классы операций с запасом;
* :mod:`home_inventory.storage` — преобразование объектов в JSON;
* :mod:`home_inventory.utils` — ввод данных с обработкой ошибок;
* :mod:`home_inventory.views` — вывод объектов в консоль;
* :mod:`home_inventory.cli` — меню и точка запуска приложения.
"""

__all__ = ["__version__"]

__version__ = "0.3.0"
