"""Маршруты приложения главной страницы."""

from django.urls import path

from . import views

#: Пространство имён приложения: маршруты вида ``homepage:index``.
app_name = "homepage"

urlpatterns = [
    path("", views.index, name="index"),
]
