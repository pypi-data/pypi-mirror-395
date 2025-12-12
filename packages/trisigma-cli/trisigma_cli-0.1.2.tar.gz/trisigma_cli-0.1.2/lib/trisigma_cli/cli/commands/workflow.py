"""Команды для управления рабочими процессами (Git workflow)."""

import time
import webbrowser
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich.table import Table

from ...core.config import config
from ...core.git_wrapper import GitWorkflow
from ...core.jwt_decoder import extract_user_info
from ...core.telemetry_global import track_event
from ...utils.exceptions import AuthenticationError, TrisigmaError
from ...utils.validation import validate_task_number

console = Console()
workflow_app = typer.Typer(add_completion=False)


@workflow_app.command("task")
def task_command(
    task_number: Optional[str] = typer.Argument(None, help="Номер задачи (например PROJECT-123)"),
    description: Optional[str] = typer.Argument(None, help="Краткое описание задачи"),
):
    """
    Создание или переключение на ветку задачи.

    Создает новую ветку в git от master и переключается на неё.
    Если ветка уже существует, переключается на неё.
    """
    start_time = time.time()
    branch_created = True  # Предполагаем что ветка будет создана

    try:
        # Проверяем конфигурацию
        config.validate_current_config()

        # Получаем параметры валидации из backend config
        cli_config = config.get_cli_config()
        task_required = True
        task_pattern = None
        task_example = "PROJECT-123"

        if cli_config and cli_config.ui:
            task_required = cli_config.ui.task_id_required
            task_pattern = cli_config.ui.task_id_regex
            task_example = cli_config.ui.task_format_example

        # Выводим информацию о задаче если указана
        if task_number:
            console.print(f"[bold blue]Работа с задачей: {task_number}[/bold blue]\n")
        else:
            console.print("[bold blue]Создание ветки[/bold blue]\n")

        # Валидируем номер задачи с учетом настроек из конфига
        validated_task = validate_task_number(
            task_number or "",
            required=task_required,
            pattern=task_pattern,
            example=task_example
        )

        # Инициализируем Git workflow
        git = GitWorkflow(config.repository_path)

        # Проверяем состояние репозитория
        check_git_status(git)

        # Создаем ветку
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Создание ветки задачи...", total=None)

            branch_name = git.create_task_branch(
                task_number=validated_task or None,
                description=description,
                task_required=task_required,
                task_pattern=task_pattern,
                task_example=task_example
            )

            progress.remove_task(task)

        console.print(f"[green]✓ Переключен на ветку:[/green] [cyan]{branch_name}[/cyan]")
        console.print("Теперь вы можете вносить изменения и сохранять их командой:")
        console.print('  [cyan]trisigma sl save -m "Описание изменений"[/cyan]')

        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.task",
            result="success",
            duration_ms=duration_ms,
            parameters={
                "task_number": validated_task,
                "branch_created": branch_created,
                "has_description": bool(description),
                "current_branch": branch_name,
            },
            repository_path=config.repository_path,
        )

    except AuthenticationError as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        console.print("[yellow]💡 Выполните 'trisigma login' для повторной авторизации[/yellow]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="git.status",
            result="error",
            duration_ms=duration_ms,
            error_type="AuthenticationError",
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)
    except TrisigmaError as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="git.status",
            result="error",
            duration_ms=duration_ms,
            error_type=type(e).__name__,
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Прервано пользователем[/yellow]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.task",
            result="cancelled",
            duration_ms=duration_ms,
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)


@workflow_app.command("save")
def save_command(
    message: str = typer.Option(..., "--message", "-m", help="Сообщение коммита"),
    task_number: Optional[str] = typer.Option(
        None, "--task", "-t", help="Номер задачи (если не указан, определяется автоматически)"
    ),
):
    """
    Сохранение изменений в репозитории.

    Автоматически добавляет все файлы (кроме игнорируемых) и создает коммит
    с указанным сообщением и номером задачи.
    """
    start_time = time.time()
    files_changed = 0
    has_author_from_jwt = False

    try:
        # Проверяем конфигурацию
        config.validate_current_config()

        console.print("[bold blue]Сохранение изменений[/bold blue]\n")

        # Инициализируем Git workflow
        git = GitWorkflow(config.repository_path)

        # Проверяем есть ли что сохранять
        if not git.has_uncommitted_changes():
            console.print("[yellow]Нет изменений для сохранения[/yellow]")
            raise typer.Exit(0)

        # Показываем изменения
        show_changes(git)

        # Подсчитываем количество измененных файлов
        changes = git.get_changed_files()
        files_changed = sum(
            len(changes.get(key, []))
            for key in ["modified", "added", "deleted", "untracked"]
        )

        # Определяем номер задачи
        current_branch = git.get_current_branch()
        if task_number is None:
            # Пытаемся извлечь номер задачи из названия ветки
            task_number = extract_task_from_branch(current_branch)

        if task_number:
            try:
                task_number = validate_task_number(task_number)
            except Exception:
                console.print(
                    f"[yellow]Предупреждение: невалидный номер задачи '{task_number}'[/yellow]"
                )
                task_number = None

        # Извлекаем информацию об авторе из JWT токена
        author_name, author_email = None, None
        access_token = config.get("access_token")
        if access_token:
            author_name, author_email = extract_user_info(access_token)
            has_author_from_jwt = bool(author_name and author_email)

        # Создаем коммит
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Создание коммита...", total=None)

            commit_sha = git.commit_changes(message, task_number, author_name, author_email)

            progress.remove_task(task)

        console.print("[green]✓ Изменения сохранены[/green]")
        console.print(f"Коммит: [cyan]{commit_sha[:8]}[/cyan]")

        if task_number:
            console.print(f"Задача: [cyan]{task_number}[/cyan]")

        console.print("\nДля публикации изменений выполните:")
        console.print("  [cyan]trisigma sl publish[/cyan]")

        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.save",
            result="success",
            duration_ms=duration_ms,
            parameters={
                "files_changed": files_changed,
                "has_author_from_jwt": has_author_from_jwt,
                "has_task_number": bool(task_number),
                "current_branch": current_branch,
            },
            repository_path=config.repository_path,
        )

    except AuthenticationError as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        console.print("[yellow]💡 Выполните 'trisigma login' для повторной авторизации[/yellow]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.save",
            result="error",
            duration_ms=duration_ms,
            error_type="AuthenticationError",
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)
    except TrisigmaError as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.save",
            result="error",
            duration_ms=duration_ms,
            error_type=type(e).__name__,
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Прервано пользователем[/yellow]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.save",
            result="cancelled",
            duration_ms=duration_ms,
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)


@workflow_app.command("publish")
def publish_command():
    """
    Публикация изменений на сервер.

    Отправляет текущую ветку в удаленный репозиторий и генерирует
    ссылку для создания Pull Request.
    """
    start_time = time.time()
    pr_url_generated = False
    browser_opened = False

    try:
        # Проверяем конфигурацию
        config.validate_current_config()

        console.print("[bold blue]Публикация изменений[/bold blue]\n")

        # Инициализируем Git workflow
        git = GitWorkflow(config.repository_path)

        current_branch = git.get_current_branch()

        # Проверяем что не на master
        if current_branch in ["master", "main"]:
            console.print("[red]Нельзя публиковать напрямую в master/main ветку[/red]")
            console.print("Создайте ветку для задачи: [cyan]trisigma sl task PROJECT-123[/cyan]")
            raise typer.Exit(1)

        # Проверяем есть ли незакоммиченные изменения
        if git.has_uncommitted_changes():
            console.print("[red]Обнаружены незакоммиченные изменения[/red]")
            console.print(
                'Сохраните их перед публикацией: [cyan]trisigma sl save -m "сообщение"[/cyan]'
            )
            raise typer.Exit(1)

        # Показываем сводку изменений
        show_branch_summary(git, current_branch)

        # Подтверждение публикации
        if not Confirm.ask("Опубликовать изменения?", default=True):
            console.print("[yellow]Публикация отменена[/yellow]")
            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="cli.command",
                action="workflow.publish",
                result="cancelled",
                duration_ms=duration_ms,
                parameters={"cancelled_by_user": True},
                repository_path=config.repository_path,
            )
            raise typer.Exit(0)

        # Публикуем ветку
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Отправка в удаленный репозиторий...", total=None)

            git.push_branch(current_branch)

            progress.update(task, description="Генерация ссылки на PR...")

            # Генерируем ссылку на PR
            pr_url = git.generate_pull_request_url(current_branch)
            pr_url_generated = bool(pr_url)

            progress.remove_task(task)

        console.print(f"[green]✓ Ветка '{current_branch}' опубликована[/green]\n")

        # Показываем ссылку на PR
        console.print(
            Panel(
                f"[bold blue]{pr_url}[/bold blue]",
                title="[bold green]Ссылка для создания Pull Request[/bold green]",
                border_style="green",
            )
        )

        # Пытаемся открыть в браузере
        try:
            if Confirm.ask("Открыть ссылку в браузере?", default=True):
                webbrowser.open(pr_url)
                browser_opened = True
                console.print("[green]✓ Ссылка открыта в браузере[/green]")
        except Exception:
            console.print("[yellow]Не удалось открыть браузер[/yellow]")

        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.publish",
            result="success",
            duration_ms=duration_ms,
            parameters={
                "pr_url_generated": pr_url_generated,
                "browser_opened": browser_opened,
                "current_branch": current_branch,
            },
            repository_path=config.repository_path,
        )

    except AuthenticationError as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        console.print("[yellow]💡 Выполните 'trisigma login' для повторной авторизации[/yellow]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="git.publish",
            result="error",
            duration_ms=duration_ms,
            error_type="AuthenticationError",
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)
    except TrisigmaError as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="git.publish",
            result="error",
            duration_ms=duration_ms,
            error_type=type(e).__name__,
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Прервано пользователем[/yellow]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.publish",
            result="cancelled",
            duration_ms=duration_ms,
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)


@workflow_app.command("status")
def status_command():
    """
    Показывает статус текущего рабочего процесса.

    Отображает текущую ветку, изменения и историю коммитов.
    """
    start_time = time.time()
    has_changes = False
    commits_count = 0

    try:
        # Проверяем конфигурацию
        config.validate_current_config()

        console.print("[bold blue]Статус рабочего процесса[/bold blue]\n")

        # Инициализируем Git workflow
        git = GitWorkflow(config.repository_path)

        current_branch = git.get_current_branch()

        # Показываем текущую ветку
        console.print(f"[bold]Текущая ветка:[/bold] [cyan]{current_branch}[/cyan]")

        # Извлекаем номер задачи из ветки
        task_number = extract_task_from_branch(current_branch)
        if task_number:
            console.print(f"[bold]Задача:[/bold] [cyan]{task_number}[/cyan]")

        console.print()

        # Показываем изменения
        has_changes = git.has_uncommitted_changes()
        if has_changes:
            console.print("[bold yellow]Незакоммиченные изменения:[/bold yellow]")
            show_changes(git)
        else:
            console.print("[green]Нет незакоммиченных изменений[/green]")

        # Показываем историю коммитов для текущей ветки
        if current_branch not in ["master", "main"]:
            show_branch_history(git, current_branch)
            commits = git.get_commit_history()
            commits_count = len(commits)

        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.status",
            result="success",
            duration_ms=duration_ms,
            parameters={
                "has_changes": has_changes,
                "commits_count": commits_count,
                "is_feature_branch": current_branch not in ["master", "main"],
            },
            repository_path=config.repository_path,
        )

    except AuthenticationError as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        console.print("[yellow]💡 Выполните 'trisigma login' для повторной авторизации[/yellow]")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.status",
            result="error",
            duration_ms=duration_ms,
            error_type="AuthenticationError",
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)
    except TrisigmaError as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        duration_ms = int((time.time() - start_time) * 1000)
        track_event(
            event_type="cli.command",
            action="workflow.status",
            result="error",
            duration_ms=duration_ms,
            error_type=type(e).__name__,
            error_message=str(e)[:500],
            repository_path=config.repository_path,
        )
        raise typer.Exit(1)


def check_git_status(git: GitWorkflow):
    """
    Проверяет состояние Git репозитория перед операцией.

    Args:
        git: Git workflow объект

    Raises:
        typer.Exit: При наличии незакоммиченных изменений в feature ветке
    """
    if git.has_uncommitted_changes():
        current_branch = git.get_current_branch()
        protected_branches = ["master", "main"]

        # Если в master/main - показываем предупреждение, но разрешаем создание ветки
        if current_branch in protected_branches:
            console.print("[yellow]⚠ Обнаружены незакоммиченные изменения в master[/yellow]")
            console.print("[blue]Изменения будут сохранены и перенесены в новую ветку[/blue]")
            show_changes(git)
            console.print()
            return

        # Если в другой ветке - блокируем
        console.print("[red]Обнаружены незакоммиченные изменения[/red]")
        show_changes(git)

        console.print("Сохраните изменения перед созданием новой ветки:")
        console.print('  [cyan]trisigma sl save -m "Описание изменений"[/cyan]')
        raise typer.Exit(1)


def show_changes(git: GitWorkflow):
    """
    Показывает изменения в репозитории.

    Args:
        git: Git workflow объект
    """
    changes = git.get_changed_files()

    # Создаем таблицу изменений
    table = Table(title="Изменения")
    table.add_column("Статус", style="cyan", width=12)
    table.add_column("Файл", style="white")

    # Добавляем измененные файлы
    for file in changes.get("modified", []):
        table.add_row("[yellow]Изменен[/yellow]", file)

    for file in changes.get("added", []):
        table.add_row("[green]Добавлен[/green]", file)

    for file in changes.get("deleted", []):
        table.add_row("[red]Удален[/red]", file)

    for file in changes.get("untracked", []):
        table.add_row("[blue]Новый[/blue]", file)

    if table.row_count > 0:
        console.print(table)
    else:
        console.print("[dim]Нет изменений[/dim]")

    console.print()


def show_branch_summary(git: GitWorkflow, branch_name: str):
    """
    Показывает сводку по ветке перед публикацией.

    Args:
        git: Git workflow объект
        branch_name: Название ветки
    """
    console.print(f"[bold]Сводка по ветке: {branch_name}[/bold]\n")

    # Статистика изменений
    diff_stats = git.get_diff_summary()

    table = Table()
    table.add_column("Параметр", style="cyan")
    table.add_column("Значение", style="green", justify="right")

    table.add_row("Измененных файлов", str(diff_stats.get("files_changed", 0)))
    table.add_row("Добавлено строк", f"+{diff_stats.get('insertions', 0)}")
    table.add_row("Удалено строк", f"-{diff_stats.get('deletions', 0)}")

    console.print(table)

    # История коммитов
    show_branch_history(git, branch_name)


def show_branch_history(git: GitWorkflow, branch_name: str):
    """
    Показывает историю коммитов для ветки.

    Args:
        git: Git workflow объект
        branch_name: Название ветки
    """
    commits = git.get_commit_history()

    if not commits:
        console.print("\n[dim]Нет коммитов в текущей ветке[/dim]")
        return

    console.print(f"\n[bold]История коммитов ({len(commits)}):[/bold]")

    for commit in commits[-5:]:  # Показываем последние 5
        console.print(f"  [cyan]{commit['sha']}[/cyan] {commit['message']}")
        console.print(f"    [dim]{commit['author']} • {commit['date']}[/dim]")

    if len(commits) > 5:
        console.print(f"  [dim]... и еще {len(commits) - 5} коммитов[/dim]")

    console.print()


def extract_task_from_branch(branch_name: str) -> Optional[str]:
    """
    Извлекает номер задачи из названия ветки.

    Args:
        branch_name: Название ветки

    Returns:
        Номер задачи или None
    """
    import re

    # Ищем паттерн AB-1000 в названии ветки
    match = re.search(r"([A-Z]+-\d+)", branch_name.upper())
    return match.group(1) if match else None
