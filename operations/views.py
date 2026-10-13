"""View-функции приложения журнала операций с запасом."""

from django.http import HttpRequest, HttpResponse

from home_inventory.models import Consumption, StockOperation
from home_inventory.models.operations import find_operation_by_id
from home_inventory.storage import load_data
from homepage.views import page


def operation_badge(operation: StockOperation) -> str:
    """Вернуть бейдж Bootstrap с типом операции."""
    if isinstance(operation, Consumption):
        return (
            f'<span class="badge bg-warning text-dark">'
            f"{operation.TITLE}</span>"
        )
    return f'<span class="badge bg-success">{operation.TITLE}</span>'


def operations(request: HttpRequest) -> HttpResponse:
    """Страница /operations/: журнал расхода и пополнения."""
    _, _, _, operations_data = load_data()
    rows = ""
    for operation in operations_data:
        rows += f"""
        <li class="list-group-item d-flex justify-content-between">
            <span>
                <a href="/operations/{operation.id}/">
                    №{operation.id} — {operation.item.name}
                </a>
                <span class="text-secondary">
                    {operation.amount} {operation.item.unit},
                    {operation.date}
                </span>
            </span>
            {operation_badge(operation)}
        </li>
        """
    if not rows:
        body = '<p class="text-secondary">Операции не выполнялись</p>'
    else:
        body = f'<ul class="list-group">{rows}</ul>'
    content = f"""
    <h1>Журнал операций</h1>
    <p class="text-secondary">
        Всего операций: {len(operations_data)}
    </p>
    {body}
    """
    return HttpResponse(page("Домашние запасы — журнал", content))


def operation_detail(
    request: HttpRequest,
    operation_id: int,
) -> HttpResponse:
    """Страница /operations/<operation_id>/: карточка операции."""
    _, _, _, operations_data = load_data()
    operation = find_operation_by_id(operations_data, operation_id)

    if operation is None:
        content = """
        <h1 class="text-danger">Операция не найдена</h1>
        <p>Операции с таким идентификатором нет в журнале.</p>
        <a href="/operations/" class="btn btn-outline-secondary">
            ← к журналу операций
        </a>
        """
        return HttpResponse(
            page("Операция не найдена", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Операция №{operation.id}</h5>
            <p class="card-text">
                <strong>Тип:</strong> {operation_badge(operation)}
            </p>
            <p class="card-text">
                <strong>Количество:</strong>
                {operation.amount} {operation.item.unit}
            </p>
            <p class="card-text">
                <strong>Товар:</strong>
                <a href="/items/{operation.item.id}/">
                    {operation.item.name}
                </a>
                <span class="text-secondary">
                    ({operation.item.category.name})
                </span>
            </p>
            <p class="card-text">
                <strong>Пользователь:</strong>
                {operation.user.username}
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {operation.date}
            </p>
            <a href="/operations/" class="btn btn-outline-secondary">
                ← к журналу операций
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Операция №{operation.id}", content),
        status=200,
    )
