"""Корневая маршрутизация Django-проекта homestock.

Адреса распределены по приложениям: корневой файл подключает маршруты
приложений через ``include()``, конкретные адреса описаны в файлах
``urls.py`` самих приложений.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("items/", include("items.urls")),
    path("categories/", include("categories.urls")),
    path("operations/", include("operations.urls")),
]

#: Обработчик ошибки 404 для всего проекта; работает при DEBUG = False.
handler404 = "homepage.views.page_not_found"
