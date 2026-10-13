"""View-функции приложения категорий товаров."""

from django.http import HttpRequest, HttpResponse

from home_inventory.models.categories import find_category_by_id
from home_inventory.models.items import filter_items_by_category
from home_inventory.storage import load_data
from homepage.views import page
from items.views import items_list


def categories(request: HttpRequest) -> HttpResponse:
    """Страница /categories/: список категорий с числом товаров."""
    categories_data, items_data, _, _ = load_data()
    rows = ""
    for category in categories_data:
        count = len(filter_items_by_category(items_data, category.name))
        rows += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/categories/{category.id}/">{category.name}</a>
            <span class="badge bg-primary rounded-pill">{count}</span>
        </li>
        """
    content = f"""
    <h1>Категории</h1>
    <p class="text-secondary">
        Всего категорий: {len(categories_data)}
    </p>
    <ul class="list-group">{rows}</ul>
    """
    return HttpResponse(page("Домашние запасы — категории", content))


def category_detail(
    request: HttpRequest,
    category_id: int,
) -> HttpResponse:
    """Страница /categories/<category_id>/: товары категории."""
    categories_data, items_data, _, _ = load_data()
    category = find_category_by_id(categories_data, category_id)

    if category is None:
        content = """
        <h1 class="text-danger">Категория не найдена</h1>
        <p>Категории с таким идентификатором нет в учёте.</p>
        <a href="/categories/" class="btn btn-outline-secondary">
            ← к списку категорий
        </a>
        """
        return HttpResponse(
            page("Категория не найдена", content),
            status=404,
        )

    category_items = filter_items_by_category(items_data, category.name)
    content = f"""
    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">{category.name}</h5>
            <p class="card-text">
                <strong>ID:</strong> {category.id}
            </p>
            <p class="card-text">
                <strong>Товаров в категории:</strong>
                {len(category_items)}
            </p>
            <a href="/categories/" class="btn btn-outline-secondary">
                ← к списку категорий
            </a>
        </div>
    </div>
    <h2 class="h5">Товары категории</h2>
    {items_list(category_items)}
    """
    return HttpResponse(page(category.name, content), status=200)
