"""Конфигурация приложения items."""

from django.apps import AppConfig


class ItemsConfig(AppConfig):
    """Приложение товаров."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "items"
