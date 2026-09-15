"""Настройка путей импорта для запуска тестов из корня проекта."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
