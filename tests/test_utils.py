"""Тесты ввода данных с обработкой ошибок."""

from datetime import date

from home_inventory.utils import input_date, input_int, input_text


def answers(monkeypatch, *values: str) -> None:
    """Подменить input() последовательностью ответов пользователя."""
    queue = list(values)
    monkeypatch.setattr("builtins.input", lambda _: queue.pop(0))


def test_input_text_repeats_on_empty(monkeypatch):
    answers(monkeypatch, "  ", "Молоко")
    assert input_text("Название: ") == "Молоко"


def test_input_int_repeats_on_not_a_number(monkeypatch):
    answers(monkeypatch, "много", "7")
    assert input_int("Количество: ") == 7


def test_input_int_checks_min_value(monkeypatch):
    answers(monkeypatch, "0", "1")
    assert input_int("Количество: ", min_value=1) == 1


def test_input_date_parses_russian_format(monkeypatch):
    answers(monkeypatch, "08.09.2026")
    assert input_date("Дата: ") == date(2026, 9, 8)
