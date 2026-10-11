"""Вспомогательные функции ввода данных с обработкой ошибок."""

from datetime import date, datetime

from home_inventory.config import INPUT_DATE_FORMAT


def input_text(prompt: str) -> str:
    """Запросить непустую строку, повторяя запрос при пустом вводе."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значение не может быть пустым, повторите ввод")


def input_int(prompt: str, min_value: int = 0) -> int:
    """Запросить целое число не меньше min_value."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Нужно ввести целое число, повторите ввод")
            continue
        if value < min_value:
            print(f"Число должно быть не меньше {min_value}")
            continue
        return value


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ; пустой ввод — сегодня."""
    while True:
        value = input(prompt).strip()
        if not value:
            return date.today()
        try:
            return datetime.strptime(value, INPUT_DATE_FORMAT).date()
        except ValueError:
            print("Дата должна быть в формате ДД.ММ.ГГГГ, повторите ввод")
