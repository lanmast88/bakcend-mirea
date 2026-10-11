"""Параметры приложения: пути к данным и константы форматов."""

import os
from pathlib import Path

#: Корень проекта: src/home_inventory/config.py -> src/home_inventory -> src.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

#: Каталог с JSON-файлами данных; переопределяется переменной окружения.
DATA_DIR = Path(
    os.environ.get("HOME_INVENTORY_DATA_DIR", PROJECT_ROOT / "data")
)

ITEMS_FILE = DATA_DIR / "items.json"
USERS_FILE = DATA_DIR / "users.json"

#: Формат даты при хранении в JSON (ISO 8601).
STORAGE_DATE_FORMAT = "%Y-%m-%d"

#: Формат даты при вводе пользователем.
INPUT_DATE_FORMAT = "%d.%m.%Y"

#: Количество попыток ввода пароля при авторизации.
LOGIN_ATTEMPTS = 3
