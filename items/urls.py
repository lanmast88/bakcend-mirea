"""Маршруты приложения товаров."""

from django.urls import path

from . import views

#: Пространство имён приложения: маршруты вида ``items:detail``.
app_name = "items"

urlpatterns = [
    path("", views.items, name="list"),
    path("low-stock/", views.low_stock, name="low_stock"),
    path("<int:item_id>/", views.item_detail, name="detail"),
]
