import asyncio
import sys

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...core.config import config
from ...core.updater import InstallationMethod, UpdateChecker, UpdateError
from ...core.version import __version__

console = Console()
self_update_app = typer.Typer(add_completion=False)


async def check_and_update(check_only: bool = False) -> None:
    checker = UpdateChecker(config=config)

    if config.is_pypi_configured():
        configured_index = config.pypi_index
        if "pypi.org" in configured_index:
            console.print("[dim]Используется публичный PyPI[/dim]")
        else:
            console.print(f"[dim]Используется PyPI: {configured_index}[/dim]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Проверка обновлений...", total=None)
        latest_version = await checker.check_for_updates()
        progress.remove_task(task)

    console.print(f"Текущая версия: [cyan]{__version__}[/cyan]")

    if not latest_version:
        console.print("[yellow]⚠ Не удалось проверить обновления[/yellow]")
        console.print("Проверьте подключение к интернету или попробуйте позже")
        raise typer.Exit(1)

    if checker.is_update_available(latest_version):
        console.print(f"Доступна версия: [green]{latest_version}[/green]")

        source_url = checker.get_update_source()
        if source_url:
            source_name = "avito-pypi" if "avito" in source_url else "PyPI"
            console.print(f"Источник: [cyan]{source_name}[/cyan]")

        if check_only:
            console.print("\nИспользуйте [cyan]trisigma self-update[/cyan] для обновления")
            raise typer.Exit(0)

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                task = progress.add_task("Установка обновления...", total=None)
                checker.perform_update()
                progress.remove_task(task)

            console.print(f"[green]✓ Обновление до версии {latest_version} завершено[/green]")
            console.print("\n[yellow]Перезапустите CLI для применения изменений[/yellow]")

        except UpdateError as e:
            console.print(f"[red]✗ Ошибка обновления:[/red] {e}")
            if source_url:
                installation_method = checker.get_installation_method()
                console.print("\n[yellow]Попробуйте обновить вручную:[/yellow]")
                if installation_method == InstallationMethod.PIPX:
                    console.print(
                        f"  pipx upgrade trisigma-cli --pip-args='--index-url {source_url}' --force"
                    )
                else:
                    console.print(
                        f"  {sys.executable} -m pip install --upgrade --index-url {source_url} trisigma-cli"
                    )
            raise typer.Exit(1)
    else:
        console.print(f"Последняя версия: [cyan]{latest_version}[/cyan]")
        console.print("[green]✓ Используется актуальная версия[/green]")


@self_update_app.callback(invoke_without_command=True)
def self_update_command(
    ctx: typer.Context,
    check: bool = typer.Option(False, "--check", help="Только проверить обновления"),
):
    """
    Обновить trisigma CLI до последней версии.

    Проверяет доступность новой версии в PyPI и устанавливает её через pip.
    """
    if ctx.invoked_subcommand is not None:
        return

    try:
        asyncio.run(check_and_update(check_only=check))
    except KeyboardInterrupt:
        console.print("\n[yellow]Прервано[/yellow]")
        raise typer.Exit(1)
