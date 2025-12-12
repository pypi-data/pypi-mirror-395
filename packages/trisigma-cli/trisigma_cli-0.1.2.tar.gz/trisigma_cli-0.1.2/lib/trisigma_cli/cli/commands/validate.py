"""Команда валидации репозитория метрик."""

import asyncio

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...core.api_client import ValidationResult
from ...core.config import config
from ...core.repository import MetricsRepository
from ...core.telemetry_decorator import track_command
from ...utils.exceptions import AuthenticationError, TrisigmaError
from ...utils.validation import validate_repository_with_progress
from ...utils.validation_display import display_validation_results

console = Console()
validate_app = typer.Typer(add_completion=False)


@validate_app.callback(invoke_without_command=True)
def validate_command(
    ctx: typer.Context,
    ai_explain: bool = typer.Option(
        False, "-ai", "--ai-explain", help="Включить AI объяснение ошибок валидации"
    ),
):
    """
    Валидация репозитория метрик.

    Проверяет структуру и содержимое файлов репозитория на соответствие правилам.
    """
    if ctx.invoked_subcommand is not None:
        return

    @track_command(event_type="cli.command", action="validate")
    async def run_validation():
        try:
            # Проверяем конфигурацию
            config.validate_current_config()

            console.print("[bold blue]Валидация репозитория метрик...[/bold blue]")

            # Инициализируем репозиторий
            repo = MetricsRepository(config.repository_path)

            # Валидируем репозиторий с реал-тайм прогрессом
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                task = progress.add_task("Собираем конфиги...", total=None)

                def update_progress(message: str):
                    progress.update(task, description=message)

                # Валидируем через общую async функцию
                validation_result = await validate_repository_with_progress(
                    repo, update_progress, api_prefix="API: "
                )

                progress.remove_task(task)

            display_validation_results(validation_result, console)

            # Показываем AI объяснение ошибок если запрошено
            if ai_explain and not validation_result.is_valid():
                await show_ai_explanation(validation_result)

            # Определяем код выхода
            if validation_result.is_valid():
                console.print("\n[green]✓ Валидация успешна! Репозиторий готов к работе.[/green]")
                raise typer.Exit(0)
            else:
                console.print("\n[red]✗ Валидация не прошла. Найдены ошибки.[/red]")
                raise typer.Exit(1)

        except AuthenticationError as e:
            console.print(f"[red]Ошибка:[/red] {e}")
            console.print(
                "[yellow]💡 Выполните 'trisigma login' для повторной авторизации[/yellow]"
            )
            raise typer.Exit(1)
        except TrisigmaError as e:
            console.print(f"[red]Ошибка:[/red] {e}")
            raise typer.Exit(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]Валидация прервана пользователем[/yellow]")
            raise typer.Exit(1)

    # Запускаем async функцию
    try:
        asyncio.run(run_validation())
    except KeyboardInterrupt:
        console.print("\n[yellow]Валидация прервана пользователем[/yellow]")
        raise typer.Exit(1)


async def show_ai_explanation(result: ValidationResult):
    """
    Показывает AI объяснение ошибок валидации.

    Args:
        result: Результат валидации с ошибками
    """
    from ...core.config import config
    from ...core.llm_explain_service import LLMExplainService
    from ...core.backend_llm_client import BackendLLMClient
    from ...core.repository import MetricsRepository
    from ...core.token_refresh_service import TokenRefreshService
    from ...utils.thinking_messages import ThinkingMessagesGenerator

    # Проверяем настроен ли LLM
    if not config.is_llm_configured():
        console.print(
            "[yellow]💡 LLM не настроен. Используйте 'trisigma init' для настройки AI функций.[/yellow]"
        )
        return

    errors = result.get_all_errors()
    if not errors:
        return

    console.print("\n[bold blue]🤖 Вот что считает AI:[/bold blue]")
    console.print()

    try:
        if not config.api_url or not config.access_token or not config.repository_path:
            console.print("[red]Не заданы необходимые параметры конфигурации[/red]")
            return

        # Создаем LLM клиент и сервис
        token_refresh_service = TokenRefreshService(config.api_url)
        llm_client = BackendLLMClient(config.api_url, config.access_token, token_refresh_service)
        service = LLMExplainService(llm_client)
        repo = MetricsRepository(config.repository_path)

        # Показываем статистику контекста для информации
        stats, context = service.get_context_stats(errors, repo)
        if "error" not in stats:
            console.print(
                f"[dim]📊 Анализирую {stats['errors_count']} ошибок, "
                f"{stats['found_files_count']} файлов, "
                f"размер контекста: {stats['context_utilization']}[/dim]"
            )
            console.print()

        # Запускаем thinking-сообщения и получаем AI объяснение
        thinking_generator = ThinkingMessagesGenerator()
        thinking_task = None
        
        import time
        start_time = time.time()

        async def update_thinking_messages():
            """Фоновая задача для обновления thinking-сообщений."""
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                task = progress.add_task(thinking_generator.get_next(), total=None)
                try:
                    while True:
                        await asyncio.sleep(5)
                        progress.update(task, description=thinking_generator.get_next())
                except asyncio.CancelledError:
                    pass

        try:
            thinking_task = asyncio.create_task(update_thinking_messages())
            response = await service.explain_validation_errors(errors, repo, context=context)
        finally:
            if thinking_task and not thinking_task.done():
                thinking_task.cancel()
                try:
                    await thinking_task
                except asyncio.CancelledError:
                    pass
        
        duration_ms = int((time.time() - start_time) * 1000)

        console.print("[dim]✅ Анализ завершен[/dim]\n")
        console.print(response, highlight=False)

        console.print("\n")

        # Логируем событие в телеметрию
        from ...core.telemetry_global import track_event
        from ...core.telemetry_builder import TelemetryBuilder

        error_text = "\n".join([f"{e.file or 'unknown'}:{e.line or 0} - {e.message}" for e in errors[:5]])
        telemetry_params = TelemetryBuilder.build_ai_explain_params(
            errors_count=len(errors),
            error_text=error_text,
            ai_response_size=len(response),
        )
        track_event(
            event_type="cli.ai_explain",
            action="validation_explain",
            result="success",
            duration_ms=duration_ms,
            parameters=telemetry_params,
        )

    except Exception as e:
        # Измеряем время даже в случае ошибки
        duration_ms = int((time.time() - start_time) * 1000)
        
        console.print(f"[red]❌ Ошибка AI анализа:[/red] {e}")
        console.print("[dim]Попробуйте проверить настройки LLM через 'trisigma init'[/dim]")

        # Логируем ошибку в телеметрию
        from ...core.telemetry_global import track_event

        track_event(
            event_type="cli.ai_explain",
            action="validation_explain",
            result="error",
            duration_ms=duration_ms,
            error_type=type(e).__name__,
            error_message=str(e)[:500],
        )
