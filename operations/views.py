"""View-функции приложения журнала операций с запасом."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from home_inventory.models.operations import find_operation_by_id
from home_inventory.storage import load_data


def operations(request: HttpRequest) -> HttpResponse:
    """Страница /operations/: журнал расхода и пополнения."""
    _, _, _, operations_data = load_data()

    context = {
        "operations": operations_data,
    }

    return render(request, "operations/operation_list.html", context)


def operation_detail(
    request: HttpRequest,
    operation_id: int,
) -> HttpResponse:
    """Страница /operations/<operation_id>/: карточка операции."""
    _, _, _, operations_data = load_data()
    operation = find_operation_by_id(operations_data, operation_id)

    context = {
        "operation": operation,
    }

    return render(
        request,
        "operations/operation_detail.html",
        context,
        status=404 if operation is None else 200,
    )
