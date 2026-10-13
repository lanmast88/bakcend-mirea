"""Маршруты приложения товаров."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.items, name="items"),
    path("low-stock/", views.low_stock, name="low_stock"),
    path("<int:item_id>/", views.item_detail, name="item_detail"),
]
