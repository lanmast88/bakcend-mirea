"""Маршруты приложения журнала операций."""

from django.urls import path

from . import views

#: Пространство имён приложения: маршруты вида ``operations:detail``.
app_name = "operations"

urlpatterns = [
    path("", views.operations, name="list"),
    path("<int:operation_id>/", views.operation_detail, name="detail"),
]
