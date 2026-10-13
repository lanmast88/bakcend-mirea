"""Общий каркас HTML-страниц и view-функции главной страницы."""

from django.http import HttpRequest, HttpResponse

from home_inventory.models.items import get_low_stock_items
from home_inventory.storage import load_data

#: Адрес CSS-файла Bootstrap 5.3 на CDN.
BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)

#: Собственные стили проекта (CSS) поверх Bootstrap.
PAGE_STYLES = """
body { background-color: #f8f9fa; }
.navbar-brand { font-weight: 600; }
main.container { max-width: 960px; padding-bottom: 2rem; }
main.container h1 { margin: 1.5rem 0 1rem; }
"""

#: Ссылки навигации: адрес страницы и название раздела.
NAV_LINKS = (
    ("/", "Главная"),
    ("/items/", "Товары"),
    ("/categories/", "Категории"),
    ("/operations/", "Журнал операций"),
)


def page(title: str, content: str) -> str:
    """Собрать HTML-документ страницы из заголовка и содержимого."""
    links = "".join(
        f'<a class="nav-link" href="{url}">{name}</a>'
        for url, name in NAV_LINKS
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
    <style>{PAGE_STYLES}</style>
</head>
<body>
    <nav class="navbar navbar-expand bg-body-tertiary border-bottom">
        <div class="container">
            <span class="navbar-brand">Домашние запасы</span>
            <div class="nav">{links}</div>
        </div>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def summary_card(title: str, value: int, url: str) -> str:
    """Собрать карточку сводки для главной страницы."""
    return f"""
    <div class="col">
        <a href="{url}" class="text-decoration-none">
            <div class="card h-100">
                <div class="card-body">
                    <p class="card-text text-secondary mb-1">{title}</p>
                    <p class="h3 mb-0">{value}</p>
                </div>
            </div>
        </a>
    </div>
    """


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание приложения, сводка и навигация."""
    categories, items, _, operations = load_data()
    cards = (
        summary_card("Товаров", len(items), "/items/")
        + summary_card("Категорий", len(categories), "/categories/")
        + summary_card(
            "Ниже порога",
            len(get_low_stock_items(items)),
            "/items/low-stock/",
        )
        + summary_card("Операций", len(operations), "/operations/")
    )
    content = f"""
    <h1 class="display-6">Система учёта товаров в доме</h1>
    <p class="lead">
        Учёт продуктов, бытовой химии, лекарств и других товаров:
        какие товары есть в наличии, в каком количестве, к какой
        категории относятся и как изменялись их остатки.
    </p>
    <div class="row row-cols-2 row-cols-lg-4 g-3 mb-4">{cards}</div>
    <p>Основные разделы:</p>
    <a href="/items/" class="btn btn-primary me-2">Товары</a>
    <a href="/categories/" class="btn btn-secondary me-2">Категории</a>
    <a href="/operations/" class="btn btn-secondary">Журнал операций</a>
    """
    return HttpResponse(page("Домашние запасы", content))


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Собственная страница ошибки 404 для всего проекта."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес страницы или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
