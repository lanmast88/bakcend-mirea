"""View-функции приложения категорий товаров."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from home_inventory.models.categories import find_category_by_id
from home_inventory.models.items import filter_items_by_category
from home_inventory.storage import load_data


def categories(request: HttpRequest) -> HttpResponse:
    """Страница /categories/: список категорий с числом товаров."""
    categories_data, items_data, _, _ = load_data()

    context = {
        "category_rows": [
            {
                "category": category,
                "items_count": len(
                    filter_items_by_category(items_data, category.name)
                ),
            }
            for category in categories_data
        ],
    }

    return render(request, "categories/category_list.html", context)


def category_detail(
    request: HttpRequest,
    category_id: int,
) -> HttpResponse:
    """Страница /categories/<category_id>/: товары категории."""
    categories_data, items_data, _, _ = load_data()
    category = find_category_by_id(categories_data, category_id)

    if category is None:
        category_items = []
    else:
        category_items = filter_items_by_category(
            items_data,
            category.name,
        )

    context = {
        "category": category,
        "items": category_items,
    }

    return render(
        request,
        "categories/category_detail.html",
        context,
        status=404 if category is None else 200,
    )
