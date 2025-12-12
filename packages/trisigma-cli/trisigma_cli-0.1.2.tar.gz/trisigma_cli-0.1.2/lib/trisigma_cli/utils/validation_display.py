"""Утилиты для отображения результатов валидации."""

from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..core.api_client import ValidationResult
from ..core.dto import ProcessedValidationError


def display_validation_results(result: ValidationResult, console: Console = None):
    """
    Отображает результаты валидации.

    Args:
        result: Результат валидации
        console: Console для вывода (по умолчанию создается новый)
    """
    if console is None:
        console = Console()

    console.print("[bold]Результаты валидации:[/bold]\n")

    if result.is_valid():
        console.print("[green]✓ Все компоненты прошли валидацию успешно[/green]")
        display_component_summary(result, console)
    else:
        errors = result.get_all_errors()

        if not errors:
            console.print("[red]✗ Валидация не удалась (причина неизвестна)[/red]")
            return

        errors_by_component = {}
        for error in errors:
            component = error.component
            if component not in errors_by_component:
                errors_by_component[component] = []
            errors_by_component[component].append(error)

        display_component_summary(result, console)
        for component, component_errors in errors_by_component.items():
            display_component_errors(component, component_errors, console)


def display_component_summary(result: ValidationResult, console: Console = None):
    """
    Отображает сводку по компонентам при валидации.

    Args:
        result: Результат валидации
        console: Console для вывода (по умолчанию создается новый)
    """
    if console is None:
        console = Console()

    if not result.results:
        return

    table = Table(title="Компоненты репозитория")
    table.add_column("Компонент", style="cyan", no_wrap=True)
    table.add_column("Статус", style="green", justify="center")
    table.add_column("Детали", style="dim")

    single_components = [
        ("ab_schedules", result.results.ab_schedules),
        ("dimensions", result.results.dimensions),
        ("sources", result.results.sources),
    ]

    for component_name, component_data in single_components:
        if component_data is not None:
            status = "✓ OK" if component_data.success else "✗ Error"
            details = ""
            table.add_row(component_name, status, details)

    dict_components = [
        ("metrics", result.results.configs),
        ("cubes_configs", result.results.cubes_configs),
        ("m42_reports", result.results.m42_reports),
        ("enrichments", result.results.enrichments),
    ]

    for component_type, component_dict in dict_components:
        if component_dict is not None:
            failed_files = []
            all_success = True

            for component_name, component_data in component_dict.items():
                if not component_data.success:
                    all_success = False
                    failed_files.append(component_name)

            status = "✓ OK" if all_success else "✗ Error"
            details = ""
            if failed_files:
                details = f"Файлы с ошибками: {', '.join(failed_files)}"

            table.add_row(component_type, status, details)

    console.print(table)
    console.print()


def display_component_errors(
    component: str, errors: List[ProcessedValidationError], console: Console = None
):
    """
    Отображает ошибки для конкретного компонента.

    Args:
        component: Название компонента
        errors: Список ошибок компонента
        console: Console для вывода (по умолчанию создается новый)
    """
    if console is None:
        console = Console()

    header = f"[red]🚨 Ошибки в компоненте: {component}[/red]"
    style = "red"

    console.print(Panel(header, style=style))

    for i, error in enumerate(errors, 1):
        message = error.message

        prefix = f"[red]{i}. [ОШИБКА][/red]"

        console.print(f"{prefix} {message}")

        file_info = error.file
        line_info = error.line
        column_info = error.column

        details = []
        if file_info:
            details.append(f"файл: {file_info}")
        if line_info:
            details.append(f"строка: {line_info}")
        if column_info:
            details.append(f"колонка: {column_info}")

        if details:
            console.print(f"   [dim]({', '.join(details)})[/dim]")

        console.print()

    console.print()


def display_validation_error_summary(result: ValidationResult, pretty: bool = False) -> str:
    """
    Возвращает краткое описание ошибок валидации для встраивания в другие сообщения.

    Args:
        result: Результат валидации
        pretty: Если True, включает Rich разметку для форматирования

    Returns:
        Строка с описанием ошибок
    """
    if result.is_valid():
        return ""

    errors = result.get_all_errors()
    if not errors:
        return "Валидация не удалась (причина неизвестна)"

    total_errors = len(errors)

    if total_errors == 1:
        error = errors[0]
        if not pretty:
            return f"Ошибка валидации: {error.message}"
        else:
            return f"[red]Ошибка валидации:[/red] {error.message}"

    components = set(error.component for error in errors)
    component_count = len(components)

    if not pretty:
        return f"Найдено {total_errors} ошибок валидации в {component_count} компонентах. Выполните 'trisigma sl validate' для подробностей."
    else:
        return f"[red]Найдено {total_errors} ошибок валидации в {component_count} компонентах.[/red] Выполните 'trisigma sl validate' для подробностей."
