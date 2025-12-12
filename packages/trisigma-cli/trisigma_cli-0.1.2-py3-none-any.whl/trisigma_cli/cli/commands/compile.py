"""Команда компиляции SQL источников."""

import asyncio
import signal
import time
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table

from ...core.api_client import SQLGenerationResult
from ...core.config import config
from ...core.dto import ErrorCode, RepoContentDict
from ...core.file_monitor import FileSystemMonitor
from ...core.repository import MetricsRepository
from ...core.services.compilation_service import CompilationService, ParameterValidator
from ...core.telemetry_builder import TelemetryBuilder
from ...core.telemetry_global import get_telemetry_client, track_event
from ...utils.console import create_console, create_error_console
from ...utils.exceptions import AuthenticationError, TrisigmaError
from ...utils.validation_display import display_validation_results

console = Console()
compile_app = typer.Typer(add_completion=False)


@compile_app.callback(invoke_without_command=True)
def compile_command(
    ctx: typer.Context,
    source_name: Optional[str] = typer.Option(
        None, "--source", "-s", help="Название источника для компиляции"
    ),
    metrics: Optional[str] = typer.Option(
        None, "--metrics", "-m", help="Метрики через запятую (metric1,metric2)"
    ),
    dimensions: Optional[str] = typer.Option(
        None, "--dimensions", "-d", help="Дименшены через запятую (dim1,dim2)"
    ),
    columns: Optional[str] = typer.Option(
        None, "--columns", "-c", help="Колонки через запятую (col1,col2)"
    ),
    first_date: Optional[str] = typer.Option(
        None, "--first-date", help="Начальная дата (YYYY-MM-DD)"
    ),
    last_date: Optional[str] = typer.Option(
        None, "--last-date", help="Конечная дата (YYYY-MM-DD)"
    ),
    granularity: str = typer.Option(
        "day", "--granularity", "-g", help="Гранулярность (day, week, month)"
    ),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o", help="Файл для сохранения сгенерированного SQL"
    ),
    watch: bool = typer.Option(
        False,
        "--watch",
        "-w",
        help="Режим мониторинга: автоматически перекомпилировать при изменениях",
    ),
    pretty: bool = typer.Option(
        False, "--pretty", help="Включить форматирование с подсветкой (по умолчанию plain режим)"
    ),
):
    """
    Компиляция SQL для источников или метрик.

    Генерирует SQL-запросы для указанного источника или метрик с учетом дименшенов, дат и гранулярности.
    Поддерживает два режима:
    - Компиляция источника: --source-name (без --metrics)
    - Компиляция метрик: --metrics с обязательным --source-name
    """
    if ctx.invoked_subcommand is not None:
        return

    # Валидация взаимоисключающих опций
    if not source_name and not metrics:
        console.print(
            "[red]Ошибка: Укажите либо --source-name для компиляции источника, либо --metrics для компиляции метрик[/red]"
        )
        raise typer.Exit(1)

    if metrics and source_name:
        console.print(
            "[red]Ошибка: При использовании --metrics указывать --source-name не тебуется[/red]"
        )
        raise typer.Exit(1)

    is_metrics_mode = bool(metrics)

    # Если включен режим мониторинга, запускаем watch_mode
    if watch:
        watch_mode(
            source_name=source_name,
            metrics=metrics,
            dimensions=dimensions,
            columns=columns,
            first_date=first_date,
            last_date=last_date,
            granularity=granularity,
            output_file=output_file,
            pretty=pretty,
            is_metrics_mode=is_metrics_mode,
        )
        return

    async def run_compilation():
        compile_console = create_console(plain=not pretty)
        error_console = create_error_console()

        start_time = time.time()

        try:
            # Проверяем конфигурацию
            config.validate_current_config()

            # Определяем заголовок в зависимости от режима
            if is_metrics_mode:
                metrics_list = validate_and_parse_metrics(metrics)
                base_msg = f"Компиляция метрик: {', '.join(metrics_list)}"
                if source_name:
                    base_msg += f" (источник: {source_name})"
                if not pretty:
                    compile_console.print(f"{base_msg}\n")
                else:
                    compile_console.print(f"[bold blue]{base_msg}[/bold blue]\n")
            else:
                if not pretty:
                    compile_console.print(f"Компиляция источника: {source_name}\n")
                else:
                    compile_console.print(
                        f"[bold blue]Компиляция источника: {source_name}[/bold blue]\n"
                    )

            # Валидируем параметры
            dimensions_list = validate_and_parse_dimensions(dimensions)
            columns_list = validate_and_parse_columns(columns)
            if is_metrics_mode:
                metrics_list = validate_and_parse_metrics(metrics)
                if not metrics_list:
                    error_console.print("Список метрик не может быть пустым")
                    raise typer.Exit(1)
            validate_dates(first_date, last_date)
            validate_granularity(granularity)

            # Инициализируем репозиторий
            repo = MetricsRepository(config.repository_path)

            # Обеспечиваем валидацию репозитория
            repo.ensure_validated()

            # Генерируем SQL с реал-тайм прогрессом
            # Бекенд сам проверит существование источника и вернёт ошибку если нужно
            if pretty:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                ) as progress:
                    task = progress.add_task("Собираем содержимое репозитория...", total=None)

                    def update_progress(message: str):
                        progress.update(task, description=message)

                    repo_content = repo.get_repository_content()

                    # Генерируем SQL через async API в зависимости от режима
                    if is_metrics_mode:
                        result = await generate_metric_sql_async(
                            repo_content=repo_content,
                            metric_names=metrics_list,
                            dimensions=dimensions_list,
                            columns=columns_list,
                            first_date=first_date,
                            last_date=last_date,
                            granularity=granularity,
                            progress_callback=update_progress,
                        )
                    else:
                        result = await generate_sql_async(
                            repo_content=repo_content,
                            source_name=source_name,
                            dimensions=dimensions_list,
                            columns=columns_list,
                            first_date=first_date,
                            last_date=last_date,
                            granularity=granularity,
                            progress_callback=update_progress,
                        )

                    progress.remove_task(task)
            else:
                # В plain режиме без прогресс-бара
                compile_console.print("Собираем содержимое репозитория...")
                repo_content = repo.get_repository_content()

                if is_metrics_mode:
                    compile_console.print("Генерируем SQL для метрик...")
                    result = await generate_metric_sql_async(
                        repo_content=repo_content,
                        metric_names=metrics_list,
                        dimensions=dimensions_list,
                        columns=columns_list,
                        first_date=first_date,
                        last_date=last_date,
                        granularity=granularity,
                        progress_callback=None,
                    )
                else:
                    compile_console.print("Генерируем SQL...")
                    result = await generate_sql_async(
                        repo_content=repo_content,
                        source_name=source_name,
                        dimensions=dimensions_list,
                        columns=columns_list,
                        first_date=first_date,
                        last_date=last_date,
                        granularity=granularity,
                        progress_callback=None,
                    )

            if is_metrics_mode:
                display_title = f"метрики: {', '.join(metrics_list)}"
            else:
                display_title = f"источника: {source_name}"
            display_generation_results(result, display_title, output_file, pretty=pretty)

            # Телеметрия: успешная или неуспешная компиляция
            # Собираем параметры для телеметрии при завершении
            duration_ms = int((time.time() - start_time) * 1000)
            action = "compile.metrics" if is_metrics_mode else "compile.source"

            compilation_params = TelemetryBuilder.build_compilation_params(
                is_metrics_mode=is_metrics_mode,
                granularity=granularity,
                source_name=source_name if not is_metrics_mode else None,
                metrics_list=metrics_list if is_metrics_mode else None,
                dimensions_list=dimensions_list,
                columns_list=columns_list,
                first_date=first_date,
                last_date=last_date,
                output_file=output_file,
                pretty=pretty,
            )

            if result.is_successful():
                track_event(
                    event_type="cli.command",
                    action=action,
                    result="success",
                    duration_ms=duration_ms,
                    parameters=compilation_params,
                    repository_path=config.repository_path,
                )
                raise typer.Exit(0)
            else:
                track_event(
                    event_type="cli.command",
                    action=action,
                    result="error",
                    duration_ms=duration_ms,
                    parameters=compilation_params,
                    error_type="generation_failed",
                    error_message=str(result.error) if result.error else None,
                    repository_path=config.repository_path,
                )
                raise typer.Exit(1)

        except AuthenticationError as e:
            error_console.print(f"Ошибка: {e}")
            error_console.print("💡 Выполните 'trisigma login' для повторной авторизации")
            raise typer.Exit(1)
        except TrisigmaError as e:
            error_console.print(f"Ошибка: {e}")
            raise typer.Exit(1)
        except KeyboardInterrupt:
            if not pretty:
                error_console.print("\nКомпиляция прервана пользователем")
            else:
                compile_console.print("\n[yellow]Компиляция прервана пользователем[/yellow]")
            raise typer.Exit(1)

    # Запускаем async функцию
    try:
        asyncio.run(run_compilation())
    except KeyboardInterrupt:
        if not pretty:
            error_console = create_error_console()
            error_console.print("\nКомпиляция прервана пользователем")
        else:
            console.print("\n[yellow]Компиляция прервана пользователем[/yellow]")
        raise typer.Exit(1)


class CompilationWatcher:
    """
    Класс для управления режимом мониторинга файловых изменений и автоматической перекомпиляции.

    Инкапсулирует состояние мониторинга, управление потоками и логику компиляции.
    """

    def __init__(
        self,
        source_name: Optional[str] = None,
        metrics: Optional[str] = None,
        dimensions: Optional[str] = None,
        columns: Optional[str] = None,
        first_date: Optional[str] = None,
        last_date: Optional[str] = None,
        granularity: str = "day",
        output_file: Optional[str] = None,
        debounce_interval: float = 2.0,
        pretty: bool = False,
        is_metrics_mode: bool = False,
    ):
        """
        Инициализирует watcher с параметрами компиляции.

        Args:
            source_name: Название источника для компиляции (optional для metrics mode)
            metrics: Метрики через запятую
            dimensions: Дименшены через запятую
            columns: Колонки через запятую
            first_date: Начальная дата
            last_date: Конечная дата
            granularity: Гранулярность
            output_file: Файл для сохранения SQL
            debounce_interval: Секунды задержки между перекомпиляциями
            pretty: Если True, включает форматирование с подсветкой
            is_metrics_mode: Если True, генерируем SQL для метрик
        """
        self.source_name = source_name
        self.metrics = metrics
        self.dimensions = dimensions
        self.columns = columns
        self.first_date = first_date
        self.last_date = last_date
        self.granularity = granularity
        self.output_file = output_file
        self.debounce_interval = debounce_interval
        self.pretty = pretty
        self.is_metrics_mode = is_metrics_mode

        # Состояние мониторинга
        self.is_active = True
        self.compilation_in_progress = False
        self.last_compilation_time = 0.0
        self.recompilation_count = 0  # Счетчик перекомпиляций для телеметрии

        # Синхронизация (будет создан в async контексте)
        self._compilation_lock = None

        # Мониторинг файлов
        self.monitor = None
        
        # Event loop для запуска async tasks из синхронных callbacks
        self.loop = None
    
    @property
    def compilation_lock(self):
        """Ленивое создание asyncio.Lock для совместимости с Python 3.9."""
        if self._compilation_lock is None:
            self._compilation_lock = asyncio.Lock()
        return self._compilation_lock

    def _setup_signal_handlers(self):
        """Устанавливает обработчики системных сигналов."""

        def signal_handler(signum, frame):
            if not self.pretty:
                error_console = create_error_console()
                error_console.print("\nПолучен сигнал прерывания, останавливаем мониторинг...")
            else:
                console.print(
                    "\n[yellow]Получен сигнал прерывания, останавливаем мониторинг...[/yellow]"
                )
            self.stop()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    async def _perform_compilation(self, file_changed: Optional[str] = None):
        """
        Выполняет компиляцию с обработкой ошибок и debounce логикой.

        Args:
            file_changed: Имя измененного файла (для телеметрии перекомпиляции)
        """
        async with self.compilation_lock:
            if self.compilation_in_progress:
                return

            # Проверяем debounce
            current_time = time.time()
            if current_time - self.last_compilation_time < self.debounce_interval:
                return

            self.compilation_in_progress = True
            self.last_compilation_time = current_time

        compilation_start_time = time.time()
        is_recompilation = file_changed is not None

        try:
            display_console = create_console(plain=not self.pretty)
            error_console = create_error_console()

            # Отображаем сообщение в зависимости от режима
            if self.is_metrics_mode:
                metrics_list = validate_and_parse_metrics(self.metrics)
                metrics_display = ", ".join(metrics_list) if metrics_list else "неизвестно"
                if not self.pretty:
                    display_console.print(f"🔄 Компиляция метрик: {metrics_display}")
                else:
                    display_console.print(f"[cyan]🔄 Компиляция метрик: {metrics_display}[/cyan]")
            else:
                if not self.pretty:
                    display_console.print(f"🔄 Компиляция источника: {self.source_name}")
                else:
                    display_console.print(
                        f"[cyan]🔄 Компиляция источника: {self.source_name}[/cyan]"
                    )

            # Парсим и валидируем параметры
            dimensions_list = validate_and_parse_dimensions(self.dimensions)
            columns_list = validate_and_parse_columns(self.columns)
            validate_dates(self.first_date, self.last_date)
            validate_granularity(self.granularity)

            # Выполняем компиляцию
            try:
                config.validate_current_config()
                repo = MetricsRepository(config.repository_path)
                repo.ensure_validated()

                if self.is_metrics_mode:
                    # Режим компиляции метрик
                    metrics_list = validate_and_parse_metrics(self.metrics)
                    if not metrics_list:
                        error_console.print("❌ Список метрик не может быть пустым")
                        success = False
                    else:
                        # Генерируем SQL для метрик
                        repo_content = repo.get_repository_content()
                        result = await generate_metric_sql_async(
                            repo_content=repo_content,
                            metric_names=metrics_list,
                            dimensions=dimensions_list,
                            columns=columns_list,
                            first_date=self.first_date,
                            last_date=self.last_date,
                            granularity=self.granularity,
                            progress_callback=None,  # Отключаем прогресс в watch режиме
                        )
                        success = result.is_successful()

                        if success:
                            if not self.pretty:
                                display_console.print("✅ Компиляция успешна")
                            else:
                                display_console.print("[green]✅ Компиляция успешна[/green]")

                            # Сохраняем в файл если указан
                            if self.output_file:
                                sql = result.get_sql()
                                if sql:
                                    save_sql_to_file(sql, self.output_file)
                            else:
                                # Показываем краткую информацию о результате
                                sql = result.get_sql()
                                if sql:
                                    lines_count = len(sql.split("\n"))
                                    if not self.pretty:
                                        display_console.print(
                                            f"📄 Сгенерировано {lines_count} строк SQL"
                                        )
                                    else:
                                        display_console.print(
                                            f"[green]📄 Сгенерировано {lines_count} строк SQL[/green]"
                                        )
                        else:
                            error = result.error
                            if error:
                                error_console.print("❌ Ошибка генерации SQL:")
                                error_code = error.code
                                error_message = error.message

                                if error_code == ErrorCode.VALIDATION_ERROR:
                                    validation_result = result.to_validation_result()
                                    if validation_result:
                                        display_console.print(
                                            "\n[red]✗ Ошибки валидации препятствуют генерации SQL:[/red]"
                                        )
                                        display_validation_results(validation_result, display_console)
                                    else:
                                        if not self.pretty:
                                            error_console.print(
                                                "Ошибка валидации репозитория, выполните 'trisigma sl validate'"
                                            )
                                        else:
                                            display_console.print(
                                                Panel(
                                                    "[red]Ошибка валидации репозитория, выполните 'trisigma sl validate'[/red]",
                                                    title="[bold red]Ошибка валидации[/bold red]",
                                                    border_style="red",
                                                )
                                            )
                                else:
                                    if not self.pretty:
                                        error_console.print(f"Ошибка: {error_message}")
                                    else:
                                        display_console.print(
                                            Panel(
                                                f"{error_message}",
                                                title="[bold red]Ошибка[/bold red]",
                                                border_style="red",
                                            )
                                        )
                            else:
                                error_console.print("❌ Неизвестная ошибка компиляции")
                else:
                    # Режим компиляции источника
                    # Бекенд сам проверит существование источника
                    repo_content = repo.get_repository_content()
                    result = await generate_sql_async(
                        repo_content=repo_content,
                        source_name=self.source_name,
                        dimensions=dimensions_list,
                        columns=columns_list,
                        first_date=self.first_date,
                        last_date=self.last_date,
                        granularity=self.granularity,
                        progress_callback=None,  # Отключаем прогресс в watch режиме
                    )
                    success = result.is_successful()

                    if success:
                        if not self.pretty:
                            display_console.print("✅ Компиляция успешна")
                        else:
                            display_console.print("[green]✅ Компиляция успешна[/green]")

                        # Сохраняем в файл если указан
                        if self.output_file:
                            sql = result.get_sql()
                            if sql:
                                save_sql_to_file(sql, self.output_file)
                        else:
                            # Показываем краткую информацию о результате
                            sql = result.get_sql()
                            if sql:
                                lines_count = len(sql.split("\n"))
                                if not self.pretty:
                                    display_console.print(
                                        f"📄 Сгенерировано {lines_count} строк SQL"
                                    )
                                else:
                                    display_console.print(
                                        f"[green]📄 Сгенерировано {lines_count} строк SQL[/green]"
                                    )
                    else:
                        error = result.error
                        if error:
                            error_console.print("❌ Ошибка генерации SQL:")
                            error_code = error.code
                            error_message = error.message

                            if error_code == ErrorCode.VALIDATION_ERROR:
                                validation_result = result.to_validation_result()
                                if validation_result:
                                    display_console.print(
                                        "\n[red]✗ Ошибки валидации препятствуют генерации SQL:[/red]"
                                    )
                                    display_validation_results(validation_result, display_console)
                                else:
                                    if not self.pretty:
                                        error_console.print(
                                            "Ошибка валидации репозитория, выполните 'trisigma sl validate'"
                                        )
                                    else:
                                        display_console.print(
                                            Panel(
                                                "[red]Ошибка валидации репозитория, выполните 'trisigma sl validate'[/red]",
                                                title="[bold red]Ошибка валидации[/bold red]",
                                                border_style="red",
                                            )
                                        )
                            else:
                                if not self.pretty:
                                    error_console.print(f"Ошибка: {error_message}")
                                else:
                                    display_console.print(
                                        Panel(
                                            f"{error_message}",
                                            title="[bold red]Ошибка[/bold red]",
                                            border_style="red",
                                        )
                                    )
                        else:
                            error_console.print("❌ Неизвестная ошибка компиляции")

            except Exception as e:
                error_console.print(f"❌ Ошибка компиляции: {e}")
                success = False

            # Телеметрия: перекомпиляция в watch mode (только если это не первая компиляция)
            if is_recompilation:
                self.recompilation_count += 1
                compilation_duration_ms = int((time.time() - compilation_start_time) * 1000)

                track_event(
                    event_type="cli.command",
                    action="compile.watch_recompile",
                    result="success" if success else "error",
                    duration_ms=compilation_duration_ms,
                    parameters={
                        "file_changed": file_changed,
                        "compilation_type": "metrics" if self.is_metrics_mode else "source",
                        "recompilation_number": self.recompilation_count,
                    },
                    repository_path=config.repository_path,
                )

            if success:
                if not self.pretty:
                    display_console.print("Ожидание изменений...")
                else:
                    display_console.print("[dim]Ожидание изменений...[/dim]")

        except Exception as e:
            error_console.print(f"❌ Критическая ошибка: {e}")

            # Телеметрия: ошибка компиляции в watch mode
            if is_recompilation:
                self.recompilation_count += 1
                compilation_duration_ms = int((time.time() - compilation_start_time) * 1000)

                track_event(
                    event_type="cli.command",
                    action="compile.watch_recompile",
                    result="error",
                    duration_ms=compilation_duration_ms,
                    parameters={
                        "file_changed": file_changed,
                        "compilation_type": "metrics" if self.is_metrics_mode else "source",
                        "recompilation_number": self.recompilation_count,
                    },
                    error_type=type(e).__name__,
                    error_message=str(e)[:500],
                    repository_path=config.repository_path,
                )
        finally:
            self.compilation_in_progress = False

    def _on_file_change(self, file_path: str):
        """
        Callback при изменении файла.

        Args:
            file_path: Путь к измененному файлу
        """
        if not self.is_active:
            return

        file_name = Path(file_path).name
        display_console = create_console(plain=not self.pretty)

        if not self.pretty:
            display_console.print(f"📝 Изменен файл: {file_name}")
        else:
            display_console.print(f"[yellow]📝 Изменен файл: {file_name}[/yellow]")

        # Запускаем компиляцию как async task через сохраненный event loop
        if self.loop and not self.loop.is_closed():
            asyncio.run_coroutine_threadsafe(
                self._perform_compilation(file_name), self.loop
            )

    def _deduplicate_monitor_paths(self, paths: List[Path]) -> List[Path]:
        """
        Убирает дочерние пути если их родители уже мониторятся.

        Предотвращает дублирование событий файловой системы из-за
        перекрывающихся рекурсивных мониторов.

        Args:
            paths: Список путей для мониторинга

        Returns:
            Дедуплицированный список путей
        """
        if not paths:
            return []

        # Сортируем по глубине (кол-во частей пути)
        sorted_paths = sorted(paths, key=lambda p: len(p.parts))
        deduplicated = []

        for path in sorted_paths:
            # Проверяем, не является ли path дочерним для уже добавленных
            is_child = False
            for existing in deduplicated:
                try:
                    # is_relative_to доступен только в Python 3.9+
                    if hasattr(path, "is_relative_to"):
                        if path.is_relative_to(existing):
                            is_child = True
                            break
                    else:
                        # Fallback для более старых версий Python
                        try:
                            path.relative_to(existing)
                            is_child = True
                            break
                        except ValueError:
                            continue
                except (OSError, ValueError):
                    continue

            if not is_child:
                deduplicated.append(path)

        return deduplicated

    def _setup_file_monitoring(self):
        """Настраивает мониторинг файловой системы."""
        config.validate_current_config()
        repo = MetricsRepository(config.repository_path)

        # Определяем пути для мониторинга
        monitor_paths = []
        for _, path, is_dir, _ in repo.CONFIGS:
            full_path = repo.repo_path / path
            if is_dir and full_path.exists():
                monitor_paths.append(full_path)
            elif not is_dir and full_path.parent.exists():
                monitor_paths.append(full_path.parent)

        # Дедуплицируем пути чтобы избежать overlapping мониторинга
        monitor_paths = self._deduplicate_monitor_paths(monitor_paths)

        if not monitor_paths:
            error_console = create_error_console()
            error_console.print("❌ Нет путей для мониторинга")
            raise typer.Exit(1)

        # Запускаем мониторинг
        self.monitor = FileSystemMonitor(callback=self._on_file_change)
        self.monitor.start_monitoring(monitor_paths)

    def stop(self):
        """Останавливает мониторинг и очищает ресурсы."""
        if not self.is_active:
            return

        self.is_active = False
        if self.monitor:
            self.monitor.stop_monitoring()
            self.monitor = None

    async def run(self):
        """
        Запускает режим мониторинга.

        Raises:
            typer.Exit: При критических ошибках
        """
        display_console = create_console(plain=not self.pretty)

        if not self.pretty:
            display_console.print("\n🔍 Режим мониторинга активирован")
            display_console.print("Нажмите Ctrl+C для выхода\n")
        else:
            display_console.print("\n[bold blue]🔍 Режим мониторинга активирован[/bold blue]")
            display_console.print("[dim]Нажмите Ctrl+C для выхода[/dim]\n")

        # Сохраняем текущий event loop для использования в callbacks
        self.loop = asyncio.get_running_loop()

        # Запускаем телеметрию в текущем event loop
        telemetry_client = get_telemetry_client()
        if telemetry_client:
            await telemetry_client.start()

        # Телеметрия: старт watch mode
        metrics_list = None
        dimensions_list = None
        columns_list = None

        if self.is_metrics_mode and self.metrics:
            metrics_list = validate_and_parse_metrics(self.metrics)

        if self.dimensions:
            dimensions_list = validate_and_parse_dimensions(self.dimensions)

        if self.columns:
            columns_list = validate_and_parse_columns(self.columns)

        watch_params = TelemetryBuilder.build_watch_params(
            compilation_type="metrics" if self.is_metrics_mode else "source",
            granularity=self.granularity,
            source_name=self.source_name if not self.is_metrics_mode else None,
            metrics_list=metrics_list,
            dimensions_list=dimensions_list,
            columns_list=columns_list,
            first_date=self.first_date,
            last_date=self.last_date,
            has_output_file=bool(self.output_file),
        )

        track_event(
            event_type="cli.command",
            action="compile.watch_start",
            result="started",
            parameters=watch_params,
            repository_path=config.repository_path,
        )

        self._setup_signal_handlers()

        watch_start_time = time.time()

        try:
            # Выполняем первоначальную компиляцию
            await self._perform_compilation()

            # Настраиваем мониторинг файлов
            self._setup_file_monitoring()

            if not self.pretty:
                display_console.print("Нажмите Ctrl+C для завершения...")
            else:
                display_console.print("[dim]Нажмите Ctrl+C для завершения...[/dim]")

            # Основной цикл мониторинга
            # Используем короткие sleep чтобы event loop мог обрабатывать другие задачи
            # (включая _periodic_flush телеметрии)
            while self.is_active:
                # Короткий sleep позволяет event loop обработать другие задачи
                await asyncio.sleep(0.1)

        except KeyboardInterrupt:
            if not self.pretty:
                error_console = create_error_console()
                error_console.print("\nМониторинг прерван пользователем")
            else:
                display_console.print("\n[yellow]Мониторинг прерван пользователем[/yellow]")
        except TrisigmaError as e:
            error_console = create_error_console()
            error_console.print(f"Ошибка: {e}")
            raise typer.Exit(1)
        finally:
            self.stop()

            # Телеметрия: остановка watch mode
            watch_duration_ms = int((time.time() - watch_start_time) * 1000)

            # Собираем все параметры компиляции для телеметрии
            metrics_list = None
            dimensions_list = None
            columns_list = None

            if self.is_metrics_mode and self.metrics:
                metrics_list = validate_and_parse_metrics(self.metrics)

            if self.dimensions:
                dimensions_list = validate_and_parse_dimensions(self.dimensions)

            if self.columns:
                columns_list = validate_and_parse_columns(self.columns)

            watch_stop_params = TelemetryBuilder.build_watch_params(
                compilation_type="metrics" if self.is_metrics_mode else "source",
                granularity=self.granularity,
                source_name=self.source_name if not self.is_metrics_mode else None,
                metrics_list=metrics_list,
                dimensions_list=dimensions_list,
                columns_list=columns_list,
                first_date=self.first_date,
                last_date=self.last_date,
                has_output_file=bool(self.output_file),
                total_recompilations=self.recompilation_count,
            )

            track_event(
                event_type="cli.command",
                action="compile.watch_stop",
                result="stopped",
                duration_ms=watch_duration_ms,
                parameters=watch_stop_params,
                repository_path=config.repository_path,
            )

            # Корректно завершаем телеметрию и отправляем оставшиеся события
            telemetry_client = get_telemetry_client()
            if telemetry_client:
                try:
                    await telemetry_client.shutdown()
                except Exception:
                    # Игнорируем ошибки при shutdown телеметрии
                    pass

            if not self.pretty:
                display_console.print("🔚 Мониторинг завершен")
            else:
                display_console.print("[green]🔚 Мониторинг завершен[/green]")


def watch_mode(
    source_name: Optional[str] = None,
    metrics: Optional[str] = None,
    dimensions: Optional[str] = None,
    columns: Optional[str] = None,
    first_date: Optional[str] = None,
    last_date: Optional[str] = None,
    granularity: str = "day",
    output_file: Optional[str] = None,
    pretty: bool = False,
    is_metrics_mode: bool = False,
) -> None:
    """
    Режим мониторинга: автоматически перекомпилирует при изменениях файлов.

    Args:
        source_name: Название источника для компиляции (optional для metrics mode)
        metrics: Метрики через запятую
        dimensions: Дименшены через запятую
        columns: Колонки через запятую
        first_date: Начальная дата
        last_date: Конечная дата
        granularity: Гранулярность
        output_file: Файл для сохранения SQL
        pretty: Если True, включает форматирование с подсветкой
        is_metrics_mode: Если True, генерируем SQL для метрик
    """
    watcher = CompilationWatcher(
        source_name=source_name,
        metrics=metrics,
        dimensions=dimensions,
        columns=columns,
        first_date=first_date,
        last_date=last_date,
        granularity=granularity,
        output_file=output_file,
        pretty=pretty,
        is_metrics_mode=is_metrics_mode,
    )
    asyncio.run(watcher.run())


def save_sql_to_file(sql_content: str, file_path: str) -> None:
    """
    Сохраняет SQL содержимое в файл.

    Args:
        sql_content: SQL код для сохранения
        file_path: Путь к файлу для сохранения

    Raises:
        typer.Exit: При ошибке сохранения файла
    """
    try:
        output_path = Path(file_path)

        # Создаем родительские директории если они не существуют
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Проверяем права на запись в директорию
        if not output_path.parent.is_dir():
            console.print(f"[red]Не удалось создать директорию: {output_path.parent}[/red]")
            raise typer.Exit(1)

        # Атомарная запись: сначала во временный файл, затем переименование
        temp_file = output_path.with_suffix(output_path.suffix + ".tmp")

        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(sql_content)
                f.flush()  # Принудительно сбрасываем буферы

            # Переименовываем временный файл в целевой
            temp_file.replace(output_path)

            console.print(f"[green]✓ SQL сохранен в файл: {output_path}[/green]")

        except Exception as e:
            # Убираем временный файл если что-то пошло не так
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass
            raise e

    except PermissionError:
        console.print(f"[red]Недостаточно прав для записи в файл: {file_path}[/red]")
        raise typer.Exit(1)
    except OSError as e:
        console.print(f"[red]Ошибка ввода-вывода при сохранении файла: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Неожиданная ошибка при сохранении файла: {e}[/red]")
        raise typer.Exit(1)


def validate_and_parse_dimensions(dimensions: Optional[str]) -> Optional[List[str]]:
    """
    Валидирует и парсит строку дименшенов.

    Args:
        dimensions: Строка дименшенов через запятую

    Returns:
        Список дименшенов или None

    Raises:
        typer.Exit: При невалидных дименшенах
    """
    try:
        return ParameterValidator.validate_and_parse_dimensions(dimensions)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)


def validate_and_parse_columns(columns: Optional[str]) -> Optional[List[str]]:
    """
    Валидирует и парсит строку колонок.

    Args:
        columns: Строка колонок через запятую

    Returns:
        Список колонок или None

    Raises:
        typer.Exit: При невалидных колонках
    """
    try:
        return ParameterValidator.validate_and_parse_columns(columns)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)


def validate_and_parse_metrics(metrics: Optional[str]) -> Optional[List[str]]:
    """
    Валидирует и парсит строку метрик.

    Args:
        metrics: Строка метрик через запятую

    Returns:
        Список метрик или None

    Raises:
        typer.Exit: При невалидных метриках
    """
    try:
        return ParameterValidator.validate_and_parse_metrics(metrics)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)


def validate_dates(first_date: Optional[str], last_date: Optional[str]) -> None:
    """
    Валидирует даты.

    Args:
        first_date: Начальная дата
        last_date: Конечная дата

    Raises:
        typer.Exit: При невалидных датах
    """
    try:
        ParameterValidator.validate_dates(first_date, last_date)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)


async def generate_sql_async(
    repo_content: RepoContentDict,
    source_name: str,
    dimensions: Optional[List[str]] = None,
    columns: Optional[List[str]] = None,
    first_date: Optional[str] = None,
    last_date: Optional[str] = None,
    granularity: str = "day",
    progress_callback=None,
) -> SQLGenerationResult:
    """
    Асинхронно генерирует SQL для источника с использованием API.

    Args:
        repo_content: Содержимое репозитория
        source_name: Название источника
        dimensions: Список дименшенов
        columns: Список колонок
        first_date: Начальная дата
        last_date: Конечная дата
        granularity: Гранулярность
        progress_callback: Callback для обновления прогресса

    Returns:
        SQLGenerationResult: Результат генерации
    """
    compilation_service = CompilationService()
    return await compilation_service.compile_source(
        repo_content=repo_content,
        source_name=source_name,
        dimensions=dimensions,
        columns=columns,
        first_date=first_date,
        last_date=last_date,
        granularity=granularity,
        progress_callback=progress_callback,
        use_emoji=False,
    )


async def generate_metric_sql_async(
    repo_content: RepoContentDict,
    metric_names: List[str],
    dimensions: Optional[List[str]] = None,
    columns: Optional[List[str]] = None,
    first_date: Optional[str] = None,
    last_date: Optional[str] = None,
    granularity: str = "day",
    progress_callback=None,
) -> SQLGenerationResult:
    """
    Асинхронно генерирует SQL для метрик с использованием API.

    Args:
        repo_content: Содержимое репозитория
        metric_names: Список имен метрик
        dimensions: Список дименшенов
        columns: Список колонок
        first_date: Начальная дата
        last_date: Конечная дата
        granularity: Гранулярность
        progress_callback: Callback для обновления прогресса

    Returns:
        SQLGenerationResult: Результат генерации
    """
    compilation_service = CompilationService()
    return await compilation_service.compile_metrics(
        repo_content=repo_content,
        metric_names=metric_names,
        dimensions=dimensions,
        columns=columns,
        first_date=first_date,
        last_date=last_date,
        granularity=granularity,
        progress_callback=progress_callback,
        use_emoji=False,
    )


def validate_granularity(granularity: str) -> None:
    """
    Валидирует гранулярность.

    Args:
        granularity: Гранулярность

    Raises:
        typer.Exit: При невалидной гранулярности
    """
    try:
        ParameterValidator.validate_granularity(granularity)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)


def display_generation_results(
    result: SQLGenerationResult,
    title: str,
    output_file: Optional[str] = None,
    pretty: bool = False,
):
    """
    Отображает результаты генерации SQL.

    Args:
        result: Результат генерации SQL
        title: Заголовок (например, "источника: events" или "метрики: revenue (источник: events)")
        output_file: Путь к файлу для сохранения SQL (опционально)
        pretty: Если True, включает форматирование с подсветкой
    """
    display_console = create_console(plain=not pretty)
    error_console = create_error_console()

    if result.is_successful():
        # Успешная генерация
        sql = result.get_sql()
        metadata = result.get_metadata()

        if sql:
            # Сохраняем в файл если указан output_file
            if output_file:
                save_sql_to_file(sql, output_file)

            # Отображаем сгенерированный SQL
            if not pretty:
                title_text = f"SQL для {title}"
                display_console.print(f"\n{title_text}")
                display_console.print("=" * len(title_text))
                display_console.print(sql)
            else:
                display_console.print(
                    Panel(
                        Syntax(sql, "sql", theme="monokai", line_numbers=True),
                        title=f"[bold green]SQL для {title}[/bold green]",
                        border_style="green",
                    )
                )

            # Показываем метаданные если есть
            if metadata:
                display_metadata(metadata, pretty=pretty)
        else:
            error_console.print("✗ SQL не был сгенерирован (пустой результат)")

    else:
        # Ошибка генерации
        error = result.error
        if error:
            error_console.print("✗ Ошибка генерации SQL:")

            error_code = error.code
            error_message = error.message

            if error_code == ErrorCode.VALIDATION_ERROR:
                # Отображаем подробный отчет об ошибках валидации
                validation_result = result.to_validation_result()
                if validation_result:
                    display_console.print(
                        "\n[red]✗ Ошибки валидации препятствуют генерации SQL:[/red]"
                    )
                    display_validation_results(validation_result, display_console)
                else:
                    # Fallback если не удалось получить детали валидации
                    if not pretty:
                        error_console.print(
                            "Ошибка валидации репозитория, выполните 'trisigma sl validate'"
                        )
                    else:
                        display_console.print(
                            Panel(
                                "[red]Ошибка валидации репозитория, выполните 'trisigma sl validate'[/red]",
                                title="[bold red]Ошибка валидации[/bold red]",
                                border_style="red",
                            )
                        )
            else:
                # Другие ошибки API
                if not pretty:
                    error_console.print(f"Ошибка: {error_message}")
                else:
                    display_console.print(
                        Panel(
                            f"{error_message}",
                            title="[bold red]Ошибка[/bold red]",
                            border_style="red",
                        )
                    )
        else:
            error_console.print("✗ Генерация SQL не удалась (причина неизвестна)")


def display_metadata(metadata: dict, pretty: bool = False):
    """
    Отображает метаданные генерации.

    Args:
        metadata: Метаданные от API
        pretty: Если True, включает форматирование с подсветкой
    """
    display_console = create_console(plain=not pretty)

    if not pretty:
        display_console.print("\nМетаданные генерации:")

        # Найденные столбцы
        resolved_cols = metadata.get("resolved_columns", [])
        if resolved_cols:
            display_console.print(f"Найденные столбцы: {', '.join(resolved_cols)}")

        # Использованные обогащения
        used_enrichments = metadata.get("used_enrichments", [])
        if used_enrichments:
            display_console.print(f"Использованные обогащения: {', '.join(used_enrichments)}")
        else:
            display_console.print("Использованные обогащения: нет")

        # Отсутствующие столбцы
        missing_cols = metadata.get("missing_columns", [])
        if missing_cols:
            display_console.print(f"Отсутствующие столбцы: {', '.join(missing_cols)}")
    else:
        display_console.print("\n[bold]Метаданные генерации:[/bold]")

        table = Table()
        table.add_column("Параметр", style="cyan", no_wrap=True)
        table.add_column("Значение", style="green")

        # Найденные столбцы
        resolved_cols = metadata.get("resolved_columns", [])
        if resolved_cols:
            table.add_row("Найденные столбцы", ", ".join(resolved_cols))

        # Использованные обогащения
        used_enrichments = metadata.get("used_enrichments", [])
        if used_enrichments:
            table.add_row("Использованные обогащения", ", ".join(used_enrichments))
        else:
            table.add_row("Использованные обогащения", "[dim]нет[/dim]")

        # Отсутствующие столбцы
        missing_cols = metadata.get("missing_columns", [])
        if missing_cols:
            table.add_row("Отсутствующие столбцы", f"[yellow]{', '.join(missing_cols)}[/yellow]")

        display_console.print(table)
