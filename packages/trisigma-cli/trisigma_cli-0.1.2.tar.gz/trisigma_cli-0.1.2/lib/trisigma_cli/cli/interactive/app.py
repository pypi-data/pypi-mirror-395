"""Основное приложение интерактивного режима."""

import os
import sys
import webbrowser
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer, Header, Static

from ...core.config import config
from ...core.git_wrapper import GitWorkflow
from ...core.repository import MetricsRepository
from ...core.services import GitUIService
from ...core.telemetry_global import get_telemetry_client, track_event
from ...utils.exceptions import AuthenticationError, TrisigmaError
from ...utils.validation import validate_repository_with_progress
from .widgets.main_menu import MainMenu
from .widgets.status_panel import StatusPanel
from .widgets.update_banner import UpdateBanner


class TrisigmaApp(App[None]):
    """Главное приложение Trisigma CLI в интерактивном режиме."""

    CSS = """
    .container {
        width: 100%;
        height: 100%;
    }

    #update-banner {
        width: 100%;
        height: auto;
        padding: 0 1;
        background: $warning;
        color: black;
        text-align: center;
        display: none;
    }

    #update-banner.visible {
        display: block;
    }

    .main-content {
        width: 100%;
        height: 1fr;
        layout: horizontal;
    }

    .sidebar {
        width: 30%;
        min-width: 25;
        max-width: 40;
        height: 100%;
        background: $surface;
        border-right: solid gray;
        layout: vertical;
    }

    #main-menu {
        height: 1fr;
        min-height: 15;
    }

    #status-panel {
        height: auto;
        min-height: 8;
        max-height: 12;
        padding: 1;
        margin: 1 0;
        border: round gray;
        background: $surface;
    }

    .content-area {
        width: 1fr;
        height: 100%;
        padding: 1;
        overflow-y: auto;
    }

    .simple-layout .main-content {
        layout: vertical;
    }

    .simple-layout .sidebar {
        width: 100%;
        height: auto;
        max-height: 15;
        border-right: none;
        border-bottom: solid gray;
    }

    .simple-layout .content-area {
        width: 100%;
        height: 1fr;
    }

    .current-branch {
        color: $accent;
        text-style: bold;
    }

    .repository-path {
        color: $text-muted;
    }

    .error-message {
        color: $error;
        text-style: bold;
    }

    .success-message {
        color: $success;
        text-style: bold;
    }

    .warning-message {
        color: $warning;
        text-style: bold;
    }
    """

    TITLE = "Trisigma CLI"
    SUB_TITLE = "Инструмент командной строки для работы с Репозиторием метрик"

    BINDINGS = [
        Binding("ctrl+c", "quit", "Выход"),
        Binding("ctrl+r", "refresh", "Обновить"),
        Binding("f1", "help", "Справка"),
        Binding("escape", "focus_menu", "Фокус на меню"),
    ]

    def __init__(self):
        super().__init__()
        self._current_branch = "неизвестно"
        self._repository_path = ""
        self._git_workflow = None
        self._git_ui_service = None
        self._repository = None
        self._validation_errors = None
        self._status_refresh_timer = None
        self._pull_request_url = None
        self._latest_version = None
        self._check_terminal_compatibility()

    def _get_welcome_text(self) -> str:
        """Возвращает приветственный текст с кликабельными ссылками."""
        return (
            "[bold cyan]Добро пожаловать в Trisigma CLI![/bold cyan]\n\n"
            "[bold]Начните работу с создания ветки под задачу:[/bold]\n"
            "• Используйте [@click=app.show_branches][cyan]🌿 Создать ветку под задачу[/cyan][/] для начала работы\n\n"
            "[bold]Основные возможности:[/bold]\n"
            "• [@click=app.validate][cyan]🔍 Валидация репозитория[/cyan][/] — проверка структуры и корректности метрик\n"
            "• [@click=app.compile_source][cyan]📄 Компиляция SQL источников[/cyan][/] — генерация SQL для источников\n"
            "• [@click=app.compile_metrics][cyan]📊 Компиляция SQL метрик[/cyan][/] — генерация SQL для метрик\n"
            "• [@click=app.show_git_status][cyan]📝 Статус изменений[/cyan][/] — просмотр текущего состояния репозитория\n"
            "• [@click=app.save_changes][cyan]💾 Сохранить изменения[/cyan][/] — коммит изменений в Git\n"
            "• [@click=app.publish_changes][cyan]🚀 Опубликовать изменения[/cyan][/] — push ветки и создание PR\n"
            "• [@click=app.show_settings][cyan]⚙️  Настройки[/cyan][/] — конфигурация CLI и LLM\n\n"
            "[dim]💡 Совет: Расширьте окно терминала для удобной работы с Trisigma CLI[/dim]"
        )

    def compose(self) -> ComposeResult:
        """Создает интерфейс приложения."""
        with Container(classes="container"):
            yield Header()
            yield UpdateBanner(id="update-banner")

            # Стандартный горизонтальный layout со статусом
            with Horizontal(classes="main-content"):
                with Vertical(classes="sidebar"):
                    yield MainMenu(id="main-menu")
                    yield StatusPanel(id="status-panel")

                with Container(classes="content-area"):
                    with Vertical(id="content"):
                        yield Static(
                            self._get_welcome_text(),
                            id="content-text",
                        )

            yield Footer()

    async def on_mount(self) -> None:
        """Инициализация при запуске."""
        try:
            await self._initialize_app()
        except Exception as e:
            self.log.error(f"Ошибка инициализации: {e}")
            self.notify(f"Ошибка инициализации: {e}", severity="error")

    async def _initialize_app(self) -> None:
        """Инициализирует приложение."""
        try:
            # Проверяем конфигурацию
            config.validate_current_config()

            # Инициализируем репозиторий
            if not config.repository_path:
                raise TrisigmaError("Путь к репозиторию не настроен")
            self._repository = MetricsRepository(config.repository_path)
            self._repository_path = config.repository_path

            # Запускаем мониторинг файловой системы
            self._repository.start_file_monitoring()

            # Инициализируем Git workflow и сервис
            try:
                self._git_workflow = GitWorkflow(config.repository_path)
                self._git_ui_service = GitUIService(self._git_workflow)
                self._current_branch = self._git_workflow.get_current_branch()
            except Exception as e:
                self.log.warning(f"Не удалось инициализировать Git: {e}")
                self._current_branch = "Git недоступен"
                self._git_ui_service = GitUIService(None)  # Создаем сервис без Git

            # Обновляем интерфейс
            await self._update_interface()

            # Запускаем периодическое обновление статуса
            self._start_status_refresh_timer()

            # Запускаем периодическую отправку телеметрии
            telemetry_client = get_telemetry_client()
            if telemetry_client:
                await telemetry_client.start()

            # Отправляем событие запуска TUI
            track_event(
                event_type="tui.lifecycle",
                action="app.start",
                result="success",
                parameters={
                    "repository_configured": bool(config.repository_path),
                    "api_configured": bool(config.api_url and config.access_token),
                    "llm_configured": config.is_llm_configured(),
                },
                repository_path=config.repository_path,
            )

            # Проверяем обновления в фоне
            await self._check_for_updates_background()

        except AuthenticationError as e:
            self.notify(
                f"{e}\n\n💡 Откройте Настройки (F2) и выполните авторизацию заново",
                severity="error",
                timeout=10,
            )
            raise
        except TrisigmaError as e:
            self.notify(str(e), severity="error")
            raise

    async def _update_interface(self) -> None:
        """Обновляет интерфейс с текущей информацией."""
        try:
            # Сначала обновляем информацию о текущей ветке
            await self._refresh_git_info()

            # Обновляем статусную панель
            status_panel = self.query_one("#status-panel", StatusPanel)

            # Проверяем изменения через Git UI сервис
            has_changes = False
            if self._git_ui_service and self._git_ui_service.is_available:
                try:
                    status = self._git_ui_service.get_git_status_info()
                    has_changes = status.has_uncommitted_changes
                except Exception as e:
                    self.log.warning(f"Не удалось проверить изменения Git: {e}")

            # Получаем информацию о мониторинге
            monitoring_active = (
                self._repository.is_monitoring_active() if self._repository else False
            )
            monitored_paths = self._repository.get_monitored_paths() if self._repository else []

            await status_panel.update_status(
                branch=self._current_branch,
                repository=self._repository_path,
                has_changes=has_changes,
                monitoring_active=monitoring_active,
                monitored_paths_count=len(monitored_paths),
            )

            # Обновляем главное меню
            main_menu = self.query_one("#main-menu", MainMenu)
            await main_menu.update_menu()

        except Exception as e:
            self.log.error(f"Ошибка обновления интерфейса: {str(e)}")

    async def _refresh_git_info(self) -> None:
        """Обновляет информацию о Git (текущая ветка и статус)."""
        try:
            if self._git_ui_service and self._git_ui_service.is_available:
                status = self._git_ui_service.get_git_status_info()
                self._current_branch = status.current_branch
                self.log.debug(f"Git info refreshed: branch={self._current_branch}")
        except Exception as e:
            self.log.warning(f"Не удалось обновить информацию Git: {e}")
            self._current_branch = "Git недоступен"

    def action_refresh(self) -> None:
        """Обновляет интерфейс."""
        try:
            # Принудительно обновляем интерфейс (включая Git info)
            self.call_later(self._update_interface)

            # Принудительная перерисовка для PyCharm терминала
            self.call_after_refresh(lambda: self.refresh())

        except Exception as e:
            self.log.error(f"Ошибка обновления: {str(e)}")

    def _check_terminal_compatibility(self):
        """Проверяет совместимость с терминалом."""
        try:
            # Проверяем является ли stdin TTY
            is_tty = sys.stdin.isatty()
            if not is_tty:
                self.log.warning(
                    "Terminal input не является TTY - возможны проблемы с управлением"
                )

            # Настройки для лучшей совместимости с терминалами
            os.environ.setdefault("FORCE_COLOR", "1")
            os.environ.setdefault("TERM", "xterm-256color")

        except Exception as e:
            self.log.error(f"Ошибка проверки совместимости терминала: {str(e)}")

    def _start_status_refresh_timer(self) -> None:
        """Запускает таймер для периодического обновления статуса."""
        # Обновляем статус каждые 10 секунд
        self._status_refresh_timer = self.set_interval(10.0, self._periodic_status_refresh)
        self.log.debug("Запущен таймер периодического обновления статуса")

    def _stop_status_refresh_timer(self) -> None:
        """Останавливает таймер обновления статуса."""
        if self._status_refresh_timer:
            self._status_refresh_timer.stop()
            self._status_refresh_timer = None
            self.log.debug("Остановлен таймер периодического обновления статуса")

    async def _periodic_status_refresh(self) -> None:
        """Периодическое обновление статуса."""
        try:
            # Обновляем только Git информацию и статус изменений
            await self._refresh_git_info()

            # Обновляем статусную панель
            status_panel = self.query_one("#status-panel", StatusPanel)

            # Проверяем изменения
            has_changes = False
            if self._git_ui_service and self._git_ui_service.is_available:
                try:
                    status = self._git_ui_service.get_git_status_info()
                    has_changes = status.has_uncommitted_changes
                except Exception as e:
                    self.log.debug(f"Ошибка проверки изменений при периодическом обновлении: {e}")

            # Обновляем только изменяющуюся информацию
            await status_panel.update_status(
                branch=self._current_branch,
                has_changes=has_changes,
            )

        except Exception as e:
            self.log.debug(f"Ошибка периодического обновления: {e}")

    async def _check_for_updates_background(self) -> None:
        try:
            from ...core.updater import UpdateChecker
            from ...core.version import __version__

            checker = UpdateChecker()

            latest_version = None
            if checker.should_check_now():
                latest_version = await checker.check_for_updates()
            else:
                latest_version = checker.get_cached_latest_version()

            if latest_version and checker.is_update_available(latest_version):
                self._latest_version = latest_version
                update_banner = self.query_one("#update-banner", UpdateBanner)
                update_banner.update_version(
                    current_version=__version__,
                    latest_version=latest_version,
                    is_visible=True,
                )
                self.log.info(f"Update available: {__version__} -> {latest_version}")
        except Exception as e:
            self.log.warning(f"Ошибка проверки обновлений: {e}")

    async def on_unmount(self) -> None:
        """Вызывается при размонтировании приложения."""
        self._stop_status_refresh_timer()

        telemetry_client = get_telemetry_client()
        if telemetry_client:
            await telemetry_client.shutdown()

    def action_focus_menu(self) -> None:
        """Устанавливает фокус на главное меню."""
        main_menu = self.query_one("#main-menu")

        # Сбрасываем меню к главному состоянию
        self.call_later(main_menu.reset_to_main_menu)

        main_menu.focus()

    async def action_help(self) -> None:
        """Показывает справку."""
        help_text = """
        [bold]Горячие клавиши:[/bold]

        • [cyan]Ctrl+C[/cyan] - Выход из приложения
        • [cyan]Ctrl+R[/cyan] - Обновить интерфейс
        • [cyan]F1[/cyan] - Показать справку
        • [cyan]Esc[/cyan] - Фокус на меню
        • [cyan]↑↓[/cyan] - Навигация по меню
        • [cyan]Enter[/cyan] - Выбрать пункт меню

        [bold]Возможности:[/bold]

        • Валидация репозитория метрик
        • Компиляция SQL источников
        • Управление задачами и ветками
        • Сохранение и публикация изменений
        """

        await self.show_content(help_text, clear_buttons=True)

    # Свойства для доступа к данным

    @property
    def current_branch(self) -> str:
        """Текущая Git ветка."""
        return self._current_branch

    @property
    def repository_path(self) -> str:
        """Путь к репозиторию."""
        return self._repository_path

    @property
    def git_workflow(self) -> GitWorkflow:
        """Git workflow объект."""
        return self._git_workflow

    @property
    def git_ui_service(self) -> Optional[GitUIService]:
        """Git UI сервис."""
        return self._git_ui_service

    @property
    def repository(self) -> MetricsRepository:
        """Репозиторий метрик."""
        return self._repository

    async def show_content(self, content, clear_buttons: bool = False) -> None:
        """Показывает контент в основной области.

        Args:
            content: Текст или разметка для отображения
            clear_buttons: Если True, удаляет все динамические элементы (кнопки) перед обновлением
        """
        try:
            container = self.query_one("#content")

            # Удаляем динамические кнопки если требуется
            if clear_buttons:
                await self._remove_dynamic_buttons()

            # Пытаемся обновить существующий текстовый виджет
            try:
                text_widget = self.query_one("#content-text")
                text_widget.update(content)
            except Exception:
                # Если нет #content-text, очищаем контейнер и создаем новый
                from textual.widgets import Static

                await container.remove_children()
                await container.mount(Static(content, id="content-text"))
        except Exception as e:
            # Если не удается найти #content (например, из-за модального диалога),
            # логируем ошибку и попробуем позже
            self.log.warning(f"Не удалось обновить контент: {e}")
            # Пытаемся обновить контент после небольшой задержки
            self.call_later(lambda: self._delayed_show_content(content))

    async def _remove_dynamic_buttons(self) -> None:
        """Удаляет все динамические кнопки из контейнера контента."""
        button_ids = ["ai-explain-btn", "create-pr-btn"]
        for button_id in button_ids:
            try:
                button = self.query_one(f"#{button_id}")
                await button.remove()
            except Exception:
                pass

    def _delayed_show_content(self, content) -> None:
        """Отложенный показ контента."""
        try:
            content_widget = self.query_one("#content")
            content_widget.update(content)
        except Exception as e:
            self.log.error(f"Повторная попытка обновления контента не удалась: {e}")

    def on_button_pressed(self, event) -> None:
        """Обработка нажатия кнопок."""
        try:
            self.log.debug(f"Кнопка нажата: {event.button}")
            if event.button.id == "ai-explain-btn":
                self.log.debug("Кнопка AI объяснения нажата")
                self.action_ai_explain()
            elif event.button.id == "create-pr-btn":
                self.log.debug("Кнопка создания PR нажата")
                self.action_open_pull_request()
        except Exception as e:
            self.log.error(f"Ошибка обработки нажатия кнопки: {e}")

    async def show_sql_with_copy_button(
        self, source_name: str, sql: str, metadata: dict, compilation_type: str = "source"
    ) -> None:
        """Показывает SQL в модальном диалоге с прокруткой."""
        from .widgets.sql_view_dialog import SQLViewDialog

        # Показываем SQL в модальном диалоге с прокруткой
        dialog = SQLViewDialog(
            title=source_name, sql=sql, metadata=metadata, compilation_type=compilation_type
        )
        self.push_screen(dialog)

    async def show_validation_results(self) -> None:
        """Показывает результаты валидации."""
        import time

        start_time = time.time()

        try:
            # Обновляем статусную панель
            status_panel = self.query_one("#status-panel", StatusPanel)
            await status_panel.update_status(loading_status="🔄 Валидация...")

            # Показываем прогресс и очищаем старые кнопки
            await self.show_content("🔄 Валидация репозитория...", clear_buttons=True)

            # Callback для обновления прогресса
            async def update_progress(message: str):
                # Проверяем, начинается ли сообщение с API префикса
                if message.startswith("🌐 "):
                    # Это API сообщение, показываем как есть
                    await self.show_content(message)
                    await status_panel.update_status(loading_status=message)
                else:
                    # Это обычное activity сообщение, не добавляем глобус
                    await self.show_content(message)
                    await status_panel.update_status(loading_status=message)

            # Валидируем через общую функцию
            result = await validate_repository_with_progress(
                self._repository, update_progress, api_prefix="🌐 "
            )

            # Очищаем статус загрузки
            await status_panel.update_status(loading_status="")

            duration_ms = int((time.time() - start_time) * 1000)

            if result.is_valid():
                self._validation_errors = None
                track_event(
                    event_type="tui.action",
                    action="validate",
                    result="success",
                    duration_ms=duration_ms,
                    repository_path=config.repository_path,
                )
                await self.show_content(
                    "[green]✓ Валидация успешна![/green]\n\n"
                    "Репозиторий соответствует всем требованиям."
                )
            else:
                errors = result.get_all_errors()
                self._validation_errors = errors
                track_event(
                    event_type="tui.action",
                    action="validate",
                    result="validation_errors",
                    duration_ms=duration_ms,
                    parameters={"error_count": len(errors)},
                    repository_path=config.repository_path,
                )
                error_text = "[red]✗ Найдены ошибки валидации:[/red]\n\n"

                for error in errors[:10]:  # Показываем первые 10 ошибок
                    component = error.component
                    message = error.message
                    error_text += f"• [{component}] {message}\n"

                if len(errors) > 10:
                    error_text += f"\n... и еще {len(errors) - 10} ошибок"

                # Обновляем текстовую часть контента
                await self.show_content(error_text)

                # Добавляем кнопку отдельно, если LLM настроен (не затирая текст)
                if config.is_llm_configured():
                    from textual.widgets import Button

                    # Удаляем все динамические кнопки перед добавлением новой
                    await self._remove_dynamic_buttons()

                    container = self.query_one("#content")
                    await container.mount(
                        Button("🤖 Помощь AI", id="ai-explain-btn", variant="primary")
                    )

        except AuthenticationError as e:
            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="tui.action",
                action="validate",
                result="error",
                duration_ms=duration_ms,
                error_type="authentication_error",
                repository_path=config.repository_path,
            )
            # Ошибка аутентификации - токен недействителен или истек
            status_panel = self.query_one("#status-panel", StatusPanel)
            await status_panel.update_status(loading_status="")
            self.notify(
                f"{e}\n\n💡 Откройте Настройки (F2) и выполните авторизацию заново",
                severity="error",
                timeout=10,
            )
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="tui.action",
                action="validate",
                result="error",
                duration_ms=duration_ms,
                error_type=type(e).__name__,
                repository_path=config.repository_path,
            )
            # Очищаем статус загрузки при ошибке
            status_panel = self.query_one("#status-panel", StatusPanel)
            await status_panel.update_status(loading_status="")
            self.notify(f"Ошибка валидации: {e}", severity="error")

    async def show_sources_list(self) -> None:
        """Показывает список источников."""
        try:
            if not self._repository.is_validation_cached():
                # Обновляем статусную панель
                status_panel = self.query_one("#status-panel", StatusPanel)
                await status_panel.update_status(loading_status="🔄 Загрузка источников...")

                await self.show_content("🔄 Подготовка данных...", clear_buttons=True)

                async def update_progress(message: str):
                    # Проверяем, начинается ли сообщение с API префикса
                    if message.startswith("🌐 "):
                        # Это API сообщение, показываем как есть
                        await self.show_content(message)
                        await status_panel.update_status(loading_status=message)
                    else:
                        # Это обычное activity сообщение, не добавляем глобус
                        await self.show_content(message)
                        await status_panel.update_status(loading_status=message)

                await self._ensure_repository_validated(update_progress)

                # Очищаем статус загрузки
                await status_panel.update_status(loading_status="")
            else:
                await self._ensure_repository_validated()

            sources = self._repository.get_cached_sources()

            if not sources:
                await self.show_content("[yellow]Источники не найдены[/yellow]")
                return

            content = f"[bold blue]Доступные источники ({len(sources)}):[/bold blue]\n\n"

            # Показываем первые 20
            for i, source in enumerate(sources[:20], 1):
                content += f"{i:2d}. [cyan]{source}[/cyan]\n"

            if len(sources) > 20:
                content += f"\n... и еще {len(sources) - 20}"

            await self.show_content(content)

        except AuthenticationError as e:
            # Ошибка аутентификации - токен недействителен или истек
            status_panel = self.query_one("#status-panel", StatusPanel)
            await status_panel.update_status(loading_status="")
            self.notify(
                f"{e}\n\n💡 Откройте Настройки (F2) и выполните авторизацию заново",
                severity="error",
                timeout=10,
            )
        except Exception as e:
            # Очищаем статус загрузки при ошибке
            status_panel = self.query_one("#status-panel", StatusPanel)
            await status_panel.update_status(loading_status="")
            self.notify(f"Ошибка получения источников: {e}", severity="error")

    async def _ensure_repository_validated(self, progress_callback=None):
        """Обеспечивает валидацию репозитория через async API."""
        if not self._repository.is_validation_cached():
            if progress_callback:
                await validate_repository_with_progress(self._repository, progress_callback)
            else:
                # Простой callback, не показываем прогресс для фоновой валидации
                def silent_progress(message: str):
                    pass

                await validate_repository_with_progress(self._repository, silent_progress)

    async def show_git_status(self) -> None:
        """Показывает статус Git."""
        import time

        start_time = time.time()
        has_changes = False
        current_branch = None

        try:
            # Получаем статус для телеметрии
            if self._git_ui_service:
                status_info = self._git_ui_service.get_git_status_info()
                has_changes = status_info.has_uncommitted_changes
                current_branch = status_info.current_branch

            content = self._git_ui_service.format_git_status_content()
            await self.show_content(content, clear_buttons=True)

            # Телеметрия: успешный просмотр статуса
            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="tui.action",
                action="git.show_status",
                result="success",
                duration_ms=duration_ms,
                parameters={
                    "has_changes": has_changes,
                    "current_branch": current_branch,
                },
                repository_path=config.repository_path,
            )
        except Exception as e:
            self.notify(f"Ошибка получения статуса Git: {e}", severity="error")

            # Телеметрия: ошибка
            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="tui.action",
                action="git.show_status",
                result="error",
                duration_ms=duration_ms,
                error_type=type(e).__name__,
                error_message=str(e)[:500],
                repository_path=config.repository_path,
            )

    async def show_getting_started(self) -> None:
        """Показывает приветственный текст (онбординг)."""
        await self.show_content(self._get_welcome_text(), clear_buttons=True)

    def action_ai_explain(self) -> None:
        """Показывает AI объяснение ошибок валидации."""
        if not self._validation_errors:
            self.notify("Нет ошибок валидации для объяснения", severity="warning")
            return

        if not config.is_llm_configured():
            self.notify(
                "LLM не настроен. Используйте 'trisigma init' для настройки AI функций.",
                severity="warning",
            )
            return

        # Показываем AI объяснение через модальный диалог
        from .widgets.ai_explain_dialog import AIExplainDialog

        dialog = AIExplainDialog(
            validation_errors=self._validation_errors, repository=self._repository
        )
        self.push_screen(dialog)

    def action_open_pull_request(self) -> None:
        """Открывает ссылку на создание Pull Request в браузере."""
        if not self._pull_request_url:
            self.notify("Ссылка на Pull Request недоступна", severity="warning")
            return

        try:
            webbrowser.open(self._pull_request_url)
            self.notify("Pull Request открыт в браузере", severity="information")
        except Exception as e:
            self.log.error(f"Ошибка открытия браузера: {e}")
            self.notify(f"Не удалось открыть браузер: {e}", severity="error")

    def action_show_branches(self) -> None:
        """Открывает диалог создания ветки."""
        try:
            from .widgets.branch_dialog import BranchDialog

            dialog = BranchDialog()
            self.push_screen(dialog)
        except Exception as e:
            self.log.error(f"Ошибка открытия диалога веток: {e}")
            self.notify(f"Ошибка: {e}", severity="error")

    def action_validate(self) -> None:
        """Запускает валидацию репозитория."""
        try:
            self.call_later(self.show_validation_results)
        except Exception as e:
            self.log.error(f"Ошибка запуска валидации: {e}")
            self.notify(f"Ошибка: {e}", severity="error")

    def action_compile_source(self) -> None:
        """Открывает диалог компиляции источников."""
        try:
            from .widgets.compile_dialog import CompileDialog

            dialog = CompileDialog()
            self.push_screen(dialog)
        except Exception as e:
            self.log.error(f"Ошибка открытия диалога компиляции: {e}")
            self.notify(f"Ошибка: {e}", severity="error")

    def action_compile_metrics(self) -> None:
        """Открывает диалог компиляции метрик."""
        try:
            from .widgets.metrics_compile_dialog import MetricsCompileDialog

            dialog = MetricsCompileDialog()
            self.push_screen(dialog)
        except Exception as e:
            self.log.error(f"Ошибка открытия диалога компиляции метрик: {e}")
            self.notify(f"Ошибка: {e}", severity="error")

    def action_show_git_status(self) -> None:
        """Показывает статус изменений Git."""
        try:
            self.call_later(self.show_git_status)
        except Exception as e:
            self.log.error(f"Ошибка показа статуса Git: {e}")
            self.notify(f"Ошибка: {e}", severity="error")

    def action_save_changes(self) -> None:
        """Открывает диалог сохранения изменений."""
        try:
            from .widgets.save_dialog import SaveDialog

            if self._git_ui_service:
                validation = self._git_ui_service.validate_save_operation()
                if not validation.is_valid:
                    if validation.error_message:
                        self.call_later(
                            lambda: self.show_content(
                                f"[red]Ошибка:[/red] {validation.error_message}",
                                clear_buttons=True,
                            )
                        )
                    elif validation.warning_message:
                        self.call_later(
                            lambda: self.show_content(
                                f"[yellow]{validation.warning_message}[/yellow]", clear_buttons=True
                            )
                        )
                    return

            dialog = SaveDialog()
            self.push_screen(dialog)
        except Exception as e:
            self.log.error(f"Ошибка открытия диалога сохранения: {e}")
            self.notify(f"Ошибка: {e}", severity="error")

    def action_publish_changes(self) -> None:
        """Открывает диалог публикации изменений."""
        try:
            from .widgets.publish_dialog import PublishDialog

            if self._git_ui_service:
                validation = self._git_ui_service.validate_publish_operation()
                if not validation.is_valid:
                    if validation.error_message:
                        self.call_later(
                            lambda: self.show_content(
                                f"[red]Ошибка:[/red] {validation.error_message}",
                                clear_buttons=True,
                            )
                        )
                    elif validation.warning_message:
                        self.call_later(
                            lambda: self.show_content(
                                f"[yellow]{validation.warning_message}[/yellow]", clear_buttons=True
                            )
                        )
                    return

            dialog = PublishDialog()
            self.push_screen(dialog)
        except Exception as e:
            self.log.error(f"Ошибка открытия диалога публикации: {e}")
            self.notify(f"Ошибка: {e}", severity="error")

    def action_show_settings(self) -> None:
        """Открывает диалог настроек."""
        try:
            from .widgets.settings_dialog import SettingsDialog

            dialog = SettingsDialog()
            self.push_screen(dialog)
        except Exception as e:
            self.log.error(f"Ошибка открытия настроек: {e}")
            self.notify(f"Ошибка: {e}", severity="error")

    def action_show_getting_started(self) -> None:
        """Показывает приветственный текст (онбординг)."""
        try:
            self.call_later(self.show_getting_started)
        except Exception as e:
            self.log.error(f"Ошибка показа онбординга: {e}")
            self.notify(f"Ошибка: {e}", severity="error")

    async def show_pull_request_button(self, pr_url: str) -> None:
        """Показывает кнопку для создания Pull Request."""
        try:
            self._pull_request_url = pr_url

            from textual.widgets import Button

            # Удаляем все динамические кнопки перед добавлением новой
            await self._remove_dynamic_buttons()

            container = self.query_one("#content")
            await container.mount(
                Button("🔗 Создать Pull Request", id="create-pr-btn", variant="success")
            )

        except Exception as e:
            self.log.error(f"Ошибка добавления кнопки PR: {e}")
            self.notify(f"Ошибка добавления кнопки: {e}", severity="error")


if __name__ == "__main__":
    app = TrisigmaApp()
    app.run()
