"""Команды для отображения списков сущностей."""

import asyncio
from typing import Callable, List

import typer
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

from ...core.config import config
from ...core.repository import MetricsRepository
from ...utils.console import create_console, create_error_console, format_text
from ...utils.exceptions import AuthenticationError, TrisigmaError
from ...utils.validation import validate_repository_with_progress


def _display_entity_list(
    entity_type: str,
    get_entities_func: Callable[[MetricsRepository], List[str]],
    plural_name: str,
    plain: bool = False,
) -> None:
    """
    Обобщенная функция для отображения списка сущностей.

    Args:
        entity_type: Тип сущности для отображения в заголовке
        get_entities_func: Функция для получения списка из репозитория
        plural_name: Название сущности во множественном числе для сообщений об ошибках
        plain: Если True, отключает Rich форматирование для лучшего копирования
    """
    console = create_console(plain=plain)

    async def run_with_validation():
        config.validate_current_config()

        repo = MetricsRepository(config.repository_path)

        # Валидация репозитория с прогресс-баром для прогрева кеша
        if not plain:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                task = progress.add_task("Загружаем данные...", total=None)

                def update_progress(message: str):
                    progress.update(task, description=message)

                # Валидируем через API для прогрева кеша
                await validate_repository_with_progress(repo, update_progress)

                progress.remove_task(task)
        else:
            # В plain режиме валидируем без прогресс-бара
            await validate_repository_with_progress(repo, lambda msg: None)

        # Получение списка сущностей из кеша
        entities = get_entities_func(repo)

        if not entities:
            not_found_text = format_text(
                f"{plural_name.capitalize()} не найдены",
                "[yellow]" if not plain else "",
                plain=plain,
            )
            console.print(not_found_text)
            return

        # Отображение результатов
        header_text = format_text(
            f"Доступные {plural_name} ({len(entities)}):",
            "[bold blue]" if not plain else "",
            plain=plain,
        )
        console.print(f"{header_text}\n")

        for i, entity in enumerate(entities, 1):
            entity_text = format_text(entity, "[cyan]" if not plain else "", plain=plain)
            console.print(f"{i:3d}. {entity_text}")

    try:
        asyncio.run(run_with_validation())
    except AuthenticationError as e:
        error_console = create_error_console()
        error_console.print(f"Ошибка: {e}")
        error_console.print("💡 Выполните 'trisigma login' для повторной авторизации")
        raise typer.Exit(1)
    except TrisigmaError as e:
        error_console = create_error_console()
        error_console.print(f"Ошибка: {e}")
        raise typer.Exit(1)


def list_sources(
    plain: bool = typer.Option(
        False, "--plain", help="Отключить форматирование для лучшего копирования"
    ),
):
    """Показывает список доступных источников."""
    _display_entity_list(
        entity_type="источники",
        get_entities_func=lambda repo: repo.get_cached_sources(),
        plural_name="источники",
        plain=plain,
    )


def list_dimensions(
    plain: bool = typer.Option(
        False, "--plain", help="Отключить форматирование для лучшего копирования"
    ),
):
    """Показывает список доступных дименшенов."""
    _display_entity_list(
        entity_type="дименшены",
        get_entities_func=lambda repo: repo.get_cached_dimensions(),
        plural_name="дименшены",
        plain=plain,
    )


def list_metrics(
    plain: bool = typer.Option(
        False, "--plain", help="Отключить форматирование для лучшего копирования"
    ),
):
    """Показывает список доступных метрик."""
    _display_entity_list(
        entity_type="метрики",
        get_entities_func=lambda repo: repo.get_cached_metrics(),
        plural_name="метрики",
        plain=plain,
    )


def show_source(
    source_name: str = typer.Argument(..., help="Название источника"),
    plain: bool = typer.Option(
        False, "--plain", help="Отключить форматирование для лучшего копирования"
    ),
):
    """Показывает SQL код источника."""
    console = create_console(plain=plain)

    async def run_with_validation():
        config.validate_current_config()

        repo = MetricsRepository(config.repository_path)

        # Валидация репозитория для прогрева кеша
        if not plain:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                task = progress.add_task("Загружаем данные...", total=None)

                def update_progress(message: str):
                    progress.update(task, description=message)

                await validate_repository_with_progress(repo, update_progress)

                progress.remove_task(task)
        else:
            await validate_repository_with_progress(repo, lambda msg: None)

        # Проверяем что источник существует
        available_sources = repo.get_cached_sources()
        if source_name not in available_sources:
            error_console = create_error_console()
            error_console.print(f"Источник '{source_name}' не найден")
            raise typer.Exit(1)

        # Получаем SQL код из файловой системы
        sources_sql_path = repo.repo_path / "sources" / "sql" / f"{source_name}.sql"
        if not sources_sql_path.exists():
            error_console = create_error_console()
            error_console.print(f"SQL файл источника '{source_name}' не найден")
            raise typer.Exit(1)

        try:
            with open(sources_sql_path, "r", encoding="utf-8") as f:
                sql_code = f.read()
        except (OSError, UnicodeDecodeError) as e:
            error_console = create_error_console()
            error_console.print(f"Не удалось прочитать SQL файл: {e}")
            raise typer.Exit(1)

        # Отображаем SQL
        if plain:
            title_text = f"SQL источника: {source_name}"
            console.print(f"\n{title_text}")
            console.print("=" * len(title_text))
            console.print(sql_code)
        else:
            console.print(
                Panel(
                    Syntax(sql_code, "sql", theme="monokai", line_numbers=True),
                    title=f"[bold blue]SQL источника: {source_name}[/bold blue]",
                    border_style="blue",
                )
            )

    try:
        asyncio.run(run_with_validation())
    except AuthenticationError as e:
        error_console = create_error_console()
        error_console.print(f"Ошибка: {e}")
        error_console.print("💡 Выполните 'trisigma login' для повторной авторизации")
        raise typer.Exit(1)
    except TrisigmaError as e:
        error_console = create_error_console()
        error_console.print(f"Ошибка: {e}")
        raise typer.Exit(1)
