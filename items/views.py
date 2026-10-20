"""View-функции приложения товаров."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from home_inventory.models.items import (
    find_item_by_id,
    get_low_stock_items,
    sort_items_by_quantity,
)
from home_inventory.models.operations import find_item_operations
from home_inventory.storage import load_data


def items(request: HttpRequest) -> HttpResponse:
    """Страница /items/: список товаров, упорядоченный по остатку."""
    _, items_data, _, _ = load_data()

    context = {
        "items": sort_items_by_quantity(items_data),
    }

    return render(request, "items/item_list.html", context)


def low_stock(request: HttpRequest) -> HttpResponse:
    """Страница /items/low-stock/: товары с остатком ниже порога."""
    _, items_data, _, _ = load_data()

    context = {
        "items": get_low_stock_items(items_data),
    }

    return render(request, "items/low_stock.html", context)


def item_detail(request: HttpRequest, item_id: int) -> HttpResponse:
    """Страница /items/<item_id>/: карточка товара и его операции."""
    _, items_data, _, operations_data = load_data()
    item = find_item_by_id(items_data, item_id)

    if item is None:
        item_operations = []
    else:
        item_operations = find_item_operations(operations_data, item)

    context = {
        "item": item,
        "operations": item_operations,
    }

    return render(
        request,
        "items/item_detail.html",
        context,
        status=404 if item is None else 200,
    )
