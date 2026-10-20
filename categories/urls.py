"""Маршруты приложения категорий."""

from django.urls import path

from . import views

#: Пространство имён приложения: маршруты вида ``categories:detail``.
app_name = "categories"

urlpatterns = [
    path("", views.categories, name="list"),
    path("<int:category_id>/", views.category_detail, name="detail"),
]
