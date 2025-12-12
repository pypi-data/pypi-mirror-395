"""Команда инициализации и настройки CLI."""

import asyncio
import os
import subprocess
import time
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt

from ...core.api_client import TrisigmaAPIClient
from ...core.config import DEFAULT_BACKEND_URL, config
from ...core.oauth_service import OAuthResult, OAuthService, save_oauth_config
from ...core.repository import MetricsRepository, detect_repository
from ...core.telemetry_global import track_event
from ...utils.exceptions import APIError, InvalidRepositoryError, TrisigmaError
from ...utils.validation import validate_directory, validate_url

console = Console()
init_app = typer.Typer(add_completion=False)


async def run_initialization() -> None:
    """Запускает процесс инициализации CLI."""
    start_time = time.time()
    current_step = "start"

    console.print("[bold blue]Настройка Trisigma CLI[/bold blue]\n")

    track_event(
        event_type="cli.command",
        action="init.start",
        result="started",
    )

    try:
        current_step = "repository_setup"
        step_start = time.time()
        setup_repository()
        step_duration = int((time.time() - step_start) * 1000)
        track_event(
            event_type="cli.command",
            action="init.repository_setup",
            result="success",
            duration_ms=step_duration,
            repository_path=config.repository_path,
        )

        current_step = "oauth_setup"
        step_start = time.time()
        await setup_oauth_authentication()
        step_duration = int((time.time() - step_start) * 1000)
        track_event(
            event_type="cli.command",
            action="init.oauth_setup",
            result="success",
            duration_ms=step_duration,
        )

        current_step = "pypi_setup"
        step_start = time.time()
        setup_pypi_index()
        step_duration = int((time.time() - step_start) * 1000)
        track_event(
            event_type="cli.command",
            action="init.pypi_setup",
            result="success",
            duration_ms=step_duration,
        )

        current_step = "config_test"
        step_start = time.time()
        await test_configuration()
        step_duration = int((time.time() - step_start) * 1000)
        track_event(
            event_type="cli.command",
            action="init.config_test",
            result="success",
            duration_ms=step_duration,
        )

        console.print("\n[green]✓ CLI успешно настроен![/green]")
        console.print("Используйте команды:")
        console.print("  • [cyan]trisigma[/cyan] - интерактивный режим")
        console.print("  • [cyan]trisigma sl validate[/cyan] - валидация")
        console.print("  • [cyan]trisigma sl compile[/cyan] - SQL")

        total_duration = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="init.complete",
            result="success",
            duration_ms=total_duration,
            repository_path=config.repository_path,
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Прервано[/yellow]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="init.complete",
            result="cancelled",
            duration_ms=duration_ms,
            parameters={"interrupted_at_step": current_step},
        )
        raise typer.Exit(1)
    except TrisigmaError as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="init",
            result="error",
            duration_ms=duration_ms,
            error_type=type(e).__name__,
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="init",
            result="error",
            duration_ms=duration_ms,
            error_type=type(e).__name__,
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)


@init_app.callback(invoke_without_command=True)
def init_command(ctx: typer.Context):
    """
    Инициализация и настройка Trisigma CLI.

    Интерактивно настраивает подключение к репозиторию, API URL и токен.
    """
    if ctx.invoked_subcommand is not None:
        return

    asyncio.run(run_initialization())


def setup_repository():
    """Настраивает подключение к репозиторию метрик."""
    console.print("[bold]1. Настройка репозитория метрик[/bold]")

    current_repo = config.repository_path
    if current_repo:
        console.print(f"Текущий репозиторий: [cyan]{current_repo}[/cyan]")

        if Confirm.ask("Изменить путь к репозиторию?", default=False):
            repo_path = choose_repository_path()
        else:
            repo_path = current_repo
    else:
        repo_path = choose_repository_path()

    # Проверяем что путь указывает на валидный репозиторий
    try:
        repo = MetricsRepository(repo_path, require_api=False)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Проверка структуры репозитория...", total=None)
            repo.validate_structure()
            progress.remove_task(task)

        console.print("[green]✓ Валидный репозиторий метрик найден[/green]")

        # Показываем статистику
        stats = repo.get_statistics()
        if "sources_sql_files" in stats:
            console.print(f"  Источников: {stats.get('sources_sql_files', 0)}")
        if "dimensions_sql_files" in stats:
            console.print(f"  Дименшенов: {stats.get('dimensions_sql_files', 0)}")

    except InvalidRepositoryError as e:
        console.print(f"[red]✗ {e}[/red]")
        raise typer.Exit(1)

    # Сохраняем путь в конфигурации
    config.update(repository_path=repo_path)
    console.print(f"Репозиторий сохранен: [cyan]{repo_path}[/cyan]\n")


def choose_repository_path() -> str:
    """
    Интерактивный выбор пути к репозиторию.

    Returns:
        Путь к выбранному репозиторию
    """
    current_dir = os.getcwd()

    console.print("\nВыберите способ подключения к репозиторию:")
    console.print(f"1. Текущая директория ({current_dir})")
    console.print("2. Указать путь вручную")
    console.print("3. Клонировать репозиторий")

    choice = Prompt.ask("Ваш выбор", choices=["1", "2", "3"], default="1")

    if choice == "1":
        return use_current_directory()
    elif choice == "2":
        return specify_path_manually()
    else:
        return clone_repository()


def use_current_directory() -> str:
    """Использует текущую директорию как репозиторий."""
    current_dir = os.getcwd()
    console.print(f"Проверка текущей директории: [cyan]{current_dir}[/cyan]")

    try:
        # Пытаемся автоматически найти репозиторий
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Поиск репозитория метрик...", total=None)
            repo_path = detect_repository(current_dir)
            progress.remove_task(task)

        if repo_path != current_dir:
            console.print(f"[green]✓ Найден репозиторий в:[/green] [cyan]{repo_path}[/cyan]")
        else:
            console.print("[green]✓ Текущая директория является репозиторием метрик[/green]")

        return repo_path

    except InvalidRepositoryError:
        console.print("[red]✗ Репозиторий метрик не найден в текущей директории[/red]")
        console.print("Попробуйте другой способ подключения.")
        return choose_repository_path()


def specify_path_manually() -> str:
    """Позволяет пользователю указать путь вручную."""
    while True:
        repo_path = Prompt.ask("Введите полный путь к репозиторию метрик")

        if not repo_path.strip():
            console.print("[red]Путь не может быть пустым[/red]")
            continue

        try:
            # Проверяем что путь существует и является директорией
            path_obj = validate_directory(repo_path)
            return str(path_obj)
        except Exception as e:
            console.print(f"[red]Ошибка:[/red] {e}")

            if not Confirm.ask("Попробовать еще раз?", default=True):
                return choose_repository_path()


def extract_repo_name_from_url(url: str) -> str:
    """
    Извлекает название репозитория из git URL.

    Args:
        url: Git URL в формате git@..., https://... или http://...

    Returns:
        Название репозитория или fallback значение
    """
    try:
        url_clean = url.strip()

        if url_clean.endswith(".git"):
            url_clean = url_clean[:-4]

        if ":" in url_clean and "@" in url_clean:
            repo_name = url_clean.split(":")[-1].split("/")[-1]
        else:
            repo_name = url_clean.rstrip("/").split("/")[-1]

        if repo_name and repo_name not in ("", ".", ".."):
            return repo_name

    except Exception:
        pass

    return "trisigma-metrics"


def clone_repository() -> str:
    """Клонирует репозиторий с удаленного сервера."""
    console.print("\n[bold]Клонирование репозитория[/bold]")
    console.print("Для клонирования репозитория потребуется:")
    console.print("• URL удаленного репозитория")
    console.print("• Права доступа к репозиторию")
    console.print("• Установленный Git\n")

    # Получаем URL репозитория
    repo_url = Prompt.ask("Введите URL репозитория (git@... или https://...)")

    if not repo_url.strip():
        console.print("[red]URL не может быть пустым[/red]")
        return choose_repository_path()

    # Получаем целевую директорию
    repo_name = extract_repo_name_from_url(repo_url)
    default_dir = Path.home() / repo_name
    target_dir = Prompt.ask("Директория для клонирования", default=str(default_dir))

    try:
        target_path = Path(target_dir).resolve()

        # Проверяем не существует ли уже директория
        if target_path.exists():
            if not target_path.is_dir():
                raise ValueError(f"Путь существует и не является директорией: {target_path}")

            if list(target_path.iterdir()):  # Директория не пуста
                if not Confirm.ask(f"Директория {target_path} не пуста. Продолжить?"):
                    return choose_repository_path()

        # Клонируем репозиторий
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Клонирование репозитория...", total=None)

            subprocess.run(
                ["git", "clone", repo_url, str(target_path)],
                capture_output=True,
                text=True,
                check=True,
            )

            progress.remove_task(task)

        console.print(
            f"[green]✓ Репозиторий успешно склонирован в:[/green] [cyan]{target_path}[/cyan]"
        )
        return str(target_path)

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Ошибка клонирования:[/red] {e.stderr}")
        return choose_repository_path()
    except Exception as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        return choose_repository_path()


async def setup_oauth_authentication() -> None:
    """Настраивает OAuth авторизацию через браузер."""
    console.print("[bold]2. Авторизация[/bold]")

    backend_url: str = get_backend_url()

    with Progress(SpinnerColumn(), TextColumn("{task.description}")) as progress:
        task = progress.add_task("Загрузка конфигурации...", total=None)

        oauth_service = OAuthService()
        result: OAuthResult = await oauth_service.perform_oauth_flow(backend_url, timeout=60)

        progress.remove_task(task)

    console.print("[green]✓ Конфигурация получена[/green]")
    console.print(f"\n[cyan]Откроется браузер:[/cyan] {result.auth_url}\n")
    console.print("[green]✓ Успешно![/green]")

    save_oauth_config(result)
    console.print("[green]✓ Сохранено[/green]\n")


def setup_pypi_index() -> None:
    """Сохраняет PyPI index использованный при установке.
    
    Источники для определения PyPI index (в порядке приоритета):
    1. Environment variable TRISIGMA_PYPI_INDEX
    2. Временный файл /tmp/trisigma_pypi_index.txt (создается install.sh)
    3. Уже сохраненный pypi_index в конфиге
    """
    import os
    
    # Приоритет 1: Environment variable
    env_pypi_index = os.environ.get("TRISIGMA_PYPI_INDEX")
    if env_pypi_index:
        config.update(pypi_index=env_pypi_index)
        if "pypi.org" in env_pypi_index:
            console.print("[yellow]ℹ Используется публичный PyPI (из env)[/yellow]")
        else:
            console.print(
                f"[green]✓ PyPI index сохранен (из env):[/green] "
                f"[cyan]{env_pypi_index}[/cyan]"
            )
        return
    
    # Приоритет 2: Временный файл от install.sh
    pypi_index_file = Path("/tmp/trisigma_pypi_index.txt")
    if pypi_index_file.exists():
        try:
            with open(pypi_index_file, "r", encoding="utf-8") as f:
                pypi_index = f.read().strip()

            if pypi_index:
                config.update(pypi_index=pypi_index)

                if "pypi.org" in pypi_index:
                    console.print("[yellow]ℹ Используется публичный PyPI[/yellow]")
                else:
                    console.print(
                        f"[green]✓ PyPI index сохранен:[/green] [cyan]{pypi_index}[/cyan]"
                    )

            pypi_index_file.unlink()
            return
        except Exception as e:
            console.print(f"[yellow]⚠ Не удалось прочитать PyPI index из файла: {e}[/yellow]")
    
    # Приоритет 3: Уже сохраненный в конфиге
    if config.pypi_index:
        console.print(f"[dim]PyPI index уже настроен: {config.pypi_index}[/dim]")
        return
    
    # Если ничего не найдено, используем публичный PyPI как безопасный дефолт
    # (корпоративный может быть недоступен, а публичный всегда доступен)
    console.print("[dim]Источник установки не определен, будет использован автоопределение[/dim]")


def get_backend_url() -> str:
    """Получает и валидирует Backend URL."""
    import os

    default: str = os.environ.get("TRISIGMA_BACKEND_URL", DEFAULT_BACKEND_URL)
    current: Optional[str] = config.get("backend_url")

    if current:
        console.print(f"\nТекущий Backend URL: [cyan]{current}[/cyan]")
        change: bool = Confirm.ask("Изменить?", default=False)
        if not change:
            return current

    console.print("\n[bold]Backend URL[/bold] — адрес вашего Trisigma сервера")
    console.print(
        f"  • Нажмите [green]Enter[/green] для использования: [cyan]{default}[/cyan]\n"
    )

    while True:
        url: str = Prompt.ask("Backend URL", default=default)
        try:
            validated: str = validate_url(url)
            return validated
        except Exception as e:
            console.print(f"[red]{e}[/red]")
            retry: bool = Confirm.ask("Retry?", default=True)
            if not retry:
                raise typer.Exit(1)


async def test_configuration():
    """Тестирует конфигурацию."""
    console.print("[bold]3. Проверка конфигурации[/bold]")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Создание API клиента...", total=None)

            progress.update(task, description="Проверка доступности API...")

            async with TrisigmaAPIClient(config.api_url, config.access_token) as api_client:
                is_available = await api_client.health_check()

            progress.update(task, description="Завершение проверки...")
            progress.remove_task(task)

        if is_available:
            console.print("[green]✓ API доступно и токен валиден[/green]")
        else:
            console.print("[red]✗ API недоступно или токен невалиден[/red]")
            raise TrisigmaError("API недоступно или токен невалиден")

    except Exception as e:
        if isinstance(e, TrisigmaError):
            raise

        # Handle specific API errors with clearer messages
        if isinstance(e, APIError):
            if e.status_code == 401:
                console.print("[red]✗ Неверный API токен[/red]")
                raise TrisigmaError("API токен невалиден или просрочен")
            elif e.status_code == 403:
                console.print("[red]✗ Недостаточно прав доступа[/red]")
                raise TrisigmaError("API токен не имеет необходимых прав доступа")
            elif e.status_code == 404:
                console.print("[red]✗ API конечная точка не найдена[/red]")
                raise TrisigmaError("Указанный API URL неверен")
            else:
                console.print(f"[red]✗ Ошибка API:[/red] {e}")
                raise TrisigmaError(f"API ошибка: {e}")
        else:
            console.print(f"[red]✗ Не удалось проверить API:[/red] {e}")
            raise TrisigmaError("Не удалось проверить API настройки")
