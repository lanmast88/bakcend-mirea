#!/usr/bin/env python
"""Утилита управления Django-проектом homestock."""

import os
import sys


def main():
    """Выполнить административную команду Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homestock.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Проверьте, что он "
            "установлен и доступен в PYTHONPATH, а виртуальное "
            "окружение активировано."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
