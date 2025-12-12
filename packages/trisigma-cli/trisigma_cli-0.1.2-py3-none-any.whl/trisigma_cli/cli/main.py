"""Основная точка входа для Trisigma CLI."""

import asyncio
import os
import sys

import typer
from rich.console import Console
from rich.traceback import install

from ..core.config import config
from ..core.telemetry_client import TelemetryClient
from ..core.telemetry_global import set_telemetry_client
from ..utils.exceptions import ConfigurationError, TrisigmaError
from ..utils.logging import get_logger
from .commands.compile import compile_command
from .commands.init import init_app
from .commands.listing import list_dimensions, list_metrics, list_sources, show_source
from .commands.login import login_app
from .commands.self_update import self_update_app
from .commands.validate import validate_command
from .commands.workflow import publish_command, save_command, status_command, task_command

# Устанавливаем красивые трассировки ошибок
install(show_locals=True)

# Создаем консоль для вывода
console = Console()

# Настраиваем логирование
logger = get_logger("trisigma.main")

# Основное приложение
app = typer.Typer(
    name="trisigma",
    help="Trisigma CLI - инструмент командной строки для работы с Репозиторием метрик",
    add_completion=False,
    rich_markup_mode="markdown",
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Добавляем подприложения
app.add_typer(init_app, name="init", help="Инициализация и настройка CLI")
app.add_typer(login_app, name="login", help="Обновление авторизации (токена)")
app.add_typer(self_update_app, name="self-update", help="Обновление trisigma CLI")

# Создаем группу 'sl' для основных команд
sl_app = typer.Typer(
    name="sl", help="Основные команды для работы с репозиторием метрик", add_completion=False
)

sl_app.command("validate", help="Валидация репозитория метрик")(validate_command)
sl_app.command("compile", help="Компиляция SQL источников")(compile_command)
sl_app.command("list-sources", help="Список доступных источников")(list_sources)
sl_app.command("list-dimensions", help="Список доступных дименшенов")(list_dimensions)
sl_app.command("list-metrics", help="Список доступных метрик")(list_metrics)
sl_app.command("show-source", help="Показать SQL код источника")(show_source)
sl_app.command("task", help="Создание ветки для задачи")(task_command)
sl_app.command("save", help="Сохранение изменений")(save_command)
sl_app.command("publish", help="Публикация изменений")(publish_command)
sl_app.command("status", help="Статус рабочего процесса")(status_command)

# Добавляем группу sl к основному приложению
app.add_typer(sl_app, name="sl")


def check_configuration() -> bool:
    """
    Проверяет настроен ли CLI.

    Returns:
        True если CLI настроен
    """
    try:
        config.validate_current_config()
        return True
    except ConfigurationError:
        return False


def detect_installation_method() -> str:
    executable = sys.executable

    if "pipx" in executable and "venvs" in executable:
        return "pipx"

    pipx_home = os.getenv("PIPX_HOME")
    if pipx_home and pipx_home in executable:
        return "pipx"

    return "pip"


async def initialize_telemetry():
    if not config.is_configured():
        return

    try:
        installation_method = detect_installation_method()
        telemetry_client = TelemetryClient(
            api_url=config.api_url,
            access_token=config.access_token,
            installation_method=installation_method,
        )
        set_telemetry_client(telemetry_client)
        # НЕ запускаем start() здесь - event loop сразу завершится
        # start() будет вызван в watch mode или TUI где event loop работает долго
    except Exception as e:
        logger.debug(f"Failed to initialize telemetry: {e}")


async def check_updates_background() -> None:
    """Фоновая проверка обновлений при запуске CLI."""
    try:
        from ..core.updater import UpdateChecker

        checker = UpdateChecker()

        if not checker.should_check_now():
            cached_version = checker.get_cached_latest_version()
            if cached_version and checker.is_update_available(cached_version):
                from ..core.version import __version__

                console.print(
                    f"\n[yellow]Доступно обновление:[/yellow] "
                    f"{__version__} → {cached_version}\n"
                    f"Выполните: [cyan]trisigma self-update[/cyan]\n"
                )
            return

        latest_version = await checker.check_for_updates()

        if latest_version and checker.is_update_available(latest_version):
            from ..core.version import __version__

            console.print(
                f"\n[yellow]Доступно обновление:[/yellow] "
                f"{__version__} → {latest_version}\n"
                f"Выполните: [cyan]trisigma self-update[/cyan]\n"
            )
    except Exception:
        pass


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context, version: bool = typer.Option(False, "--version", help="Показать версию")
):
    """
    Trisigma CLI - инструмент командной строки для работы с Репозиторием метрик.

    При запуске без аргументов запускается интерактивный режим.
    """
    try:
        asyncio.run(initialize_telemetry())
    except Exception:
        pass

    if version:
        from .. import __version__

        console.print(f"Trisigma CLI v{__version__}")
        raise typer.Exit(0)

    if ctx.invoked_subcommand not in [None, "init", "self-update", "login"]:
        try:
            asyncio.run(check_updates_background())
        except Exception:
            pass

    # Если нет команды, запускаем интерактивный режим
    if ctx.invoked_subcommand is None:
        try:
            # Проверяем конфигурацию
            if not check_configuration():
                console.print(
                    "[yellow]Внимание:[/yellow] CLI не настроен. "
                    "Выполните 'trisigma init' для настройки."
                )

                # Предлагаем запустить инициализацию
                should_init = typer.confirm("Запустить настройку сейчас?")
                if should_init:
                    from .commands.init import run_initialization

                    asyncio.run(run_initialization())
                    return
                else:
                    raise typer.Exit(1)

            # Запускаем интерактивный режим
            launch_interactive_mode()

        except KeyboardInterrupt:
            console.print("\n[yellow]Прервано пользователем[/yellow]")
            raise typer.Exit(1)
        except TrisigmaError as e:
            console.print(f"[red]Ошибка:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Неожиданная ошибка:[/red] {e}")
            raise typer.Exit(1)


def launch_interactive_mode():
    """Запускает интерактивный режим."""
    try:
        from .interactive.app import TrisigmaApp

        app_instance = TrisigmaApp()
        app_instance.run()

    except ImportError as e:
        console.print(
            f"[red]Ошибка:[/red] Не удалось загрузить интерактивный режим: {e}\n"
            f"Убедитесь что установлены зависимости: pip install textual"
        )
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Ошибка в интерактивном режиме:[/red] {e}")
        raise typer.Exit(1)


@app.command("config")
def config_command(
    show: bool = typer.Option(False, "--show", help="Показать текущую конфигурацию"),
    clear: bool = typer.Option(False, "--clear", help="Очистить конфигурацию"),
):
    """Управление конфигурацией CLI."""
    try:
        if clear:
            if typer.confirm("Вы уверены что хотите очистить всю конфигурацию?"):
                config.clear()
                console.print("[green]Конфигурация очищена[/green]")
            return

        if show:
            current_config = config.get_all()
            if not current_config:
                console.print("[yellow]Конфигурация пуста[/yellow]")
                return

            console.print("[bold]Текущая конфигурация:[/bold]")
            for key, value in current_config.items():
                if key == "access_token":
                    # Скрываем токен частично
                    masked_value = f"{value[:8]}..." if value else "не задан"
                    console.print(f"  {key}: {masked_value}")
                else:
                    console.print(f"  {key}: {value}")

            # Показываем статус конфигурации
            if config.is_configured():
                console.print("\n[green]✓ CLI настроен и готов к работе[/green]")
            else:
                missing = config.get_missing_config()
                console.print(f"\n[yellow]⚠ Не хватает настроек: {', '.join(missing)}[/yellow]")
                console.print("Выполните 'trisigma init' для завершения настройки.")
        else:
            console.print("Используйте --show для просмотра конфигурации или --clear для очистки")

    except TrisigmaError as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        raise typer.Exit(1)


def handle_error(error: Exception) -> None:
    """
    Централизованная обработка ошибок.

    Args:
        error: Исключение для обработки
    """
    if isinstance(error, ConfigurationError):
        console.print(f"[red]Ошибка конфигурации:[/red] {error}")
        console.print("Выполните 'trisigma init' для настройки CLI.")
    elif isinstance(error, TrisigmaError):
        console.print(f"[red]Ошибка:[/red] {error}")
    else:
        console.print(f"[red]Неожиданная ошибка:[/red] {error}")


# Глобальный обработчик исключений для typer
def exception_handler(exception: Exception):
    """Глобальный обработчик исключений."""
    handle_error(exception)
    sys.exit(1)


# Экспорт для setuptools entry point
def cli_main():
    """Entry point для setuptools."""
    try:
        app()
    except Exception as e:
        exception_handler(e)


if __name__ == "__main__":
    cli_main()
