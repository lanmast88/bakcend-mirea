"""Конфигурация приложения categories."""

from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    """Приложение категорий."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "categories"
