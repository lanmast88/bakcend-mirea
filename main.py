"""Точка запуска приложения учёта товаров в доме.

Приложение оформлено пакетом ``src/home_inventory``. Если пакет ещё не
установлен в окружение (``uv sync`` или ``pip install -e .``), каталог
``src`` добавляется в путь импорта, чтобы работал запуск ``python main.py``.
"""

import sys
from pathlib import Path

try:
    from home_inventory.cli import run
except ModuleNotFoundError:  # pragma: no cover - запуск без установки пакета
    sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
    from home_inventory.cli import run

if __name__ == "__main__":
    run()
