"""Команда авторизации CLI."""

import asyncio
import time
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...core.api_client import TrisigmaAPIClient
from ...core.config import config
from ...core.telemetry_global import track_event
from ...utils.exceptions import TrisigmaError

console = Console()
login_app = typer.Typer(add_completion=False)


async def run_login() -> None:
    """Запускает процесс повторной авторизации."""
    start_time = time.time()
    current_step = "start"

    console.print("[bold blue]Авторизация в Trisigma[/bold blue]\n")

    track_event(
        event_type="cli.command",
        action="login.start",
        result="started",
    )

    try:
        backend_url: Optional[str] = config.get("backend_url")

        if not backend_url:
            console.print(
                "[red]✗ Backend URL не настроен[/red]\n"
                "Выполните 'trisigma init' для первоначальной настройки."
            )
            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="cli.command",
                action="login",
                result="error",
                duration_ms=duration_ms,
                error_type="ConfigurationError",
                error_message="Backend URL not configured",
                repository_path=None,
            )
            raise typer.Exit(1)

        console.print(f"Backend URL: [cyan]{backend_url}[/cyan]\n")

        current_step = "oauth_flow"
        step_start = time.time()
        await perform_oauth_flow(backend_url)
        step_duration = int((time.time() - step_start) * 1000)
        track_event(
            event_type="cli.command",
            action="login.oauth_flow",
            result="success",
            duration_ms=step_duration,
        )

        current_step = "api_test"
        step_start = time.time()
        await test_api_connection()
        step_duration = int((time.time() - step_start) * 1000)
        track_event(
            event_type="cli.command",
            action="login.api_test",
            result="success",
            duration_ms=step_duration,
        )

        console.print("\n[green]✓ Авторизация успешно обновлена![/green]")
        console.print("Используйте команды CLI для работы с репозиторием.")

        total_duration = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="login.complete",
            result="success",
            duration_ms=total_duration,
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Прервано[/yellow]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="login.complete",
            result="cancelled",
            duration_ms=duration_ms,
            parameters={"interrupted_at_step": current_step},
        )
        raise typer.Exit(1)
    except TrisigmaError as e:
        console.print(f"\n[red]Ошибка:[/red] {e}")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="login",
            result="error",
            duration_ms=duration_ms,
            error_type=type(e).__name__,
            error_message=str(e)[:500],
            repository_path=None,
        )
        raise typer.Exit(1)


async def perform_oauth_flow(backend_url: str) -> None:
    """
    Выполняет OAuth авторизацию через браузер.

    Args:
        backend_url: URL бэкенда для авторизации
    """
    from ...core.oauth_service import OAuthResult, OAuthService, save_oauth_config

    console.print("[bold]1. OAuth авторизация[/bold]")

    with Progress(SpinnerColumn(), TextColumn("{task.description}")) as progress:
        task = progress.add_task("Загрузка конфигурации...", total=None)

        oauth_service = OAuthService()
        result: OAuthResult = await oauth_service.perform_oauth_flow(backend_url, timeout=60)

        progress.remove_task(task)

    console.print("[green]✓ Конфигурация получена[/green]")
    console.print(f"\n[cyan]Откроется браузер:[/cyan] {result.auth_url}\n")
    console.print("⏳ Ожидание авторизации...")
    console.print("[green]✓ Токены получены[/green]")

    save_oauth_config(result)
    console.print("[green]✓ Токены сохранены[/green]\n")


async def test_api_connection() -> None:
    """Тестирует подключение к API с новым токеном."""
    console.print("[bold]2. Проверка подключения[/bold]")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Проверка доступности API...", total=None)

            async with TrisigmaAPIClient(config.api_url, config.access_token) as api_client:
                is_available = await api_client.health_check()

            progress.remove_task(task)

        if is_available:
            console.print("[green]✓ API доступно и токен валиден[/green]")
        else:
            console.print("[red]✗ API недоступно или токен невалиден[/red]")
            raise TrisigmaError("API недоступно или токен невалиден")

    except Exception as e:
        if isinstance(e, TrisigmaError):
            raise

        console.print(f"[red]✗ Не удалось проверить API:[/red] {e}")
        raise TrisigmaError("Не удалось проверить API подключение")


@login_app.callback(invoke_without_command=True)
def login_command(ctx: typer.Context):
    """
    Обновление авторизации (токена) для Trisigma CLI.

    Использует уже настроенный backend URL и запрашивает новый токен
    через OAuth авторизацию в браузере.

    Требует предварительного выполнения 'trisigma init'.
    """
    if ctx.invoked_subcommand is not None:
        return

    asyncio.run(run_login())
