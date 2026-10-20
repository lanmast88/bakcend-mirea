"""View-функции главной страницы и страницы ошибки 404.

HTML-разметка страниц находится в шаблонах Django: представление
загружает данные предметной области, готовит контекст и передаёт его
шаблону через ``render()``.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from home_inventory.models.items import get_low_stock_items
from home_inventory.storage import load_data


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание приложения и сводка по данным."""
    categories, items, _, operations = load_data()

    context = {
        "categories": categories,
        "items": items,
        "low_stock_items": get_low_stock_items(items),
        "operations": operations,
    }

    return render(request, "homepage/index.html", context)


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Собственная страница ошибки 404 для всего проекта."""
    return render(request, "homepage/not_found.html", status=404)
