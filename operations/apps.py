"""Конфигурация приложения operations."""

from django.apps import AppConfig


class OperationsConfig(AppConfig):
    """Приложение журнала операций."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "operations"
