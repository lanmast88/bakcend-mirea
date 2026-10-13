"""View-функции приложения товаров."""

from django.http import HttpRequest, HttpResponse

from home_inventory.models import Item
from home_inventory.models.items import (
    find_item_by_id,
    get_low_stock_items,
    sort_items_by_quantity,
)
from home_inventory.models.operations import find_item_operations
from home_inventory.storage import load_data
from homepage.views import page


def stock_badge(item: Item) -> str:
    """Вернуть бейдж Bootstrap со статусом запаса товара."""
    if item.is_out_of_stock():
        return '<span class="badge bg-danger">закончился</span>'
    if item.is_low_stock():
        return (
            '<span class="badge bg-warning text-dark">ниже порога</span>'
        )
    return '<span class="badge bg-success">в норме</span>'


def item_row(item: Item) -> str:
    """Собрать элемент списка товаров со ссылкой на страницу товара."""
    return f"""
    <li class="list-group-item d-flex justify-content-between">
        <span>
            <a href="/items/{item.id}/">{item.name}</a>
            <span class="text-secondary">— {item.category.name}</span>
        </span>
        <span>
            {item.quantity} {item.unit} {stock_badge(item)}
        </span>
    </li>
    """


def items_list(items: list[Item]) -> str:
    """Собрать список товаров или сообщение о пустом результате."""
    if not items:
        return '<p class="text-secondary">Товары не найдены</p>'
    rows = "".join(item_row(item) for item in items)
    return f'<ul class="list-group mb-3">{rows}</ul>'


def items(request: HttpRequest) -> HttpResponse:
    """Страница /items/: список товаров, упорядоченный по остатку."""
    _, items_data, _, _ = load_data()
    content = f"""
    <h1>Товары</h1>
    <p class="text-secondary">Всего товаров: {len(items_data)}</p>
    {items_list(sort_items_by_quantity(items_data))}
    <a href="/items/low-stock/" class="btn btn-outline-danger">
        Товары ниже порога
    </a>
    """
    return HttpResponse(page("Домашние запасы — товары", content))


def low_stock(request: HttpRequest) -> HttpResponse:
    """Страница /items/low-stock/: товары с остатком ниже порога."""
    _, items_data, _, _ = load_data()
    low_stock_items = get_low_stock_items(items_data)
    if low_stock_items:
        body = items_list(low_stock_items)
    else:
        body = '<p class="text-success">Все запасы в норме</p>'
    content = f"""
    <h1>Товары ниже порога</h1>
    {body}
    <a href="/items/" class="btn btn-outline-secondary">
        ← ко всем товарам
    </a>
    """
    return HttpResponse(page("Домашние запасы — ниже порога", content))


def item_detail(request: HttpRequest, item_id: int) -> HttpResponse:
    """Страница /items/<item_id>/: карточка товара и его операции."""
    _, items_data, _, operations = load_data()
    item = find_item_by_id(items_data, item_id)

    if item is None:
        content = """
        <h1 class="text-danger">Товар не найден</h1>
        <p>Товара с таким идентификатором нет в учёте.</p>
        <a href="/items/" class="btn btn-outline-secondary">
            ← к списку товаров
        </a>
        """
        return HttpResponse(
            page("Товар не найден", content),
            status=404,
        )

    item_operations = find_item_operations(operations, item)
    if item_operations:
        rows = "".join(
            f'<li class="list-group-item">{operation}</li>'
            for operation in item_operations
        )
        history = f'<ul class="list-group">{rows}</ul>'
    else:
        history = (
            '<p class="text-secondary">Операций по товару не было</p>'
        )

    content = f"""
    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">{item.name}</h5>
            <p class="card-text">
                <strong>ID:</strong> {item.id}
            </p>
            <p class="card-text">
                <strong>Категория:</strong>
                <a href="/categories/{item.category.id}/">
                    {item.category.name}
                </a>
            </p>
            <p class="card-text">
                <strong>Остаток:</strong>
                {item.quantity} {item.unit} {stock_badge(item)}
            </p>
            <p class="card-text">
                <strong>Порог пополнения:</strong>
                {item.min_threshold} {item.unit}
            </p>
            <p class="card-text">
                <strong>Дата добавления:</strong> {item.date_added}
            </p>
            <p class="card-text">{item.stock_status()}</p>
            <a href="/items/" class="btn btn-outline-secondary">
                ← к списку товаров
            </a>
        </div>
    </div>
    <h2 class="h5">Операции по товару</h2>
    {history}
    """
    return HttpResponse(page(item.name, content), status=200)
