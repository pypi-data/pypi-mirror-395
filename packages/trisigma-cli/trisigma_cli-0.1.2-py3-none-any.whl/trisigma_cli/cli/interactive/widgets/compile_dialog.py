"""Диалог компиляции SQL источников."""

import asyncio
from enum import Enum
from typing import Optional

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Button, Label, Select, Static
from .base_dialog import BaseDialog
from .no_scroll import NoScrollInput as Input
from .dropdown_widgets import DropdownSelect, DropdownMultiSelect

from ....core.config import config
from ....core.services.compilation_service import CompilationService
from ....core.telemetry_builder import TelemetryBuilder
from ....core.telemetry_global import track_event
from ....utils.exceptions import APIError, AuthenticationError
from ....utils.validation import validate_repository_with_progress
from ....utils.validation_display import display_validation_error_summary


class CompilationState(Enum):
    """Состояния процесса компиляции."""

    IDLE = "idle"
    LOADING_REPO = "loading_repo"
    PREPARING = "preparing"
    COMPILING = "compiling"
    SUCCESS = "success"
    ERROR = "error"


class CompileDialog(BaseDialog):
    """Диалог для компиляции SQL источников."""

    AUTO_FOCUS = ""  # Отключаем автоматическую прокрутку к фокусированному элементу

    BINDINGS = [
        Binding("escape", "dismiss", "Закрыть"),
    ]

    CSS = """
    CompileDialog {
        align: center middle;
    }

    .dialog-container {
        width: 80;
        height: auto;
        max-height: 85vh;
        background: $surface;
        border: solid gray;
        padding: 1;
        layout: vertical;
    }

    .dialog-title {
        height: 1;
        margin: 0 0 1 0;
        text-align: center;
        text-style: bold;
    }

    .form-row {
        height: auto;
        min-height: 4;
        margin: 0 0 1 0;
        layout: vertical;
    }

    .form-row-horizontal {
        height: auto;
        min-height: 4;
        margin: 0 0 1 0;
        layout: horizontal;
    }

    .form-row > Label {
        height: 1;
        margin: 0 0 1 0;
    }

    .form-row > Input,
    .form-row > Select {
        height: 3;
        margin: 0;
    }

    .form-row > DropdownSelect,
    .form-row > DropdownMultiSelect {
        height: auto;
        margin: 0;
    }

    .form-column {
        width: 50%;
        height: auto;
        padding: 0 1 0 0;
        layout: vertical;
    }

    .form-column-right {
        width: 50%;
        height: auto;
        padding: 0 0 0 1;
        layout: vertical;
    }

    .buttons {
        height: 3;
        margin: 1 0 0 0;
        align: center middle;
        layout: horizontal;
    }

    .buttons > Button {
        margin: 0 1;
    }

    #status-message {
        height: auto;
        min-height: 1;
        margin: 1 0;
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

    .loading-message {
        color: $accent;
        text-style: italic;
    }

    .form-scroll {
        height: 1fr;
    }

    """

    def __init__(self):
        super().__init__()
        self._sources = []
        self._dimensions = []
        self._state = CompilationState.IDLE
        self._activity_task: Optional[asyncio.Task] = None
        self._compilation_task: Optional[asyncio.Task] = None

    def compose(self) -> ComposeResult:
        """Создает интерфейс диалога."""
        with Vertical(classes="dialog-container"):
            yield Label("Компиляция SQL источника", classes="dialog-title")
            yield Static("Инициализация...", id="status-message", classes="loading-message")

            # Область с формой (прокручивается)
            with ScrollableContainer(classes="form-scroll"):
                # Всегда создаем полную форму, но может быть скрыта/недоступна
                with Vertical(classes="form-row"):
                    yield Label("Источник:")
                    yield DropdownSelect(
                        placeholder="Выберите источник...",
                        prompt="Начните вводить для поиска",
                        id="source-select",
                    )

                with Vertical(classes="form-row"):
                    yield Label("Дименшены:")
                    yield DropdownMultiSelect(
                        placeholder="Выберите дименшены...", id="dimensions-select"
                    )

                with Horizontal(classes="form-row-horizontal"):
                    with Vertical(classes="form-column"):
                        yield Label("Начальная дата (необязательно):")
                        yield Input(placeholder="YYYY-MM-DD", id="first-date-input")

                    with Vertical(classes="form-column-right"):
                        yield Label("Конечная дата (необязательно):")
                        yield Input(placeholder="YYYY-MM-DD", id="last-date-input")

                with Vertical(classes="form-row"):
                    yield Label("Гранулярность:")
                    yield Select(
                        [("day", "day"), ("week", "week"), ("month", "month")],
                        value="day",
                        id="granularity-select",
                    )

            # Кнопки вне области скролла (фиксируются снизу диалога)
            with Horizontal(classes="buttons"):
                yield Button("Компилировать", variant="primary", id="compile-btn", disabled=True)
                yield Button("Отмена", variant="default", id="cancel-btn")

    async def on_mount(self):
        """Инициализация при показе диалога."""
        track_event(
            event_type="tui.action",
            action="compile_dialog_source_opened",
            result="success",
        )

        await self._set_state(CompilationState.LOADING_REPO)

        try:
            repo = self.app.repository

            # Проверяем нужно ли запускать валидацию
            if not repo.is_validation_cached():
                # Запускаем валидацию в background task
                self._compilation_task = asyncio.create_task(self._run_validation_in_background())
            else:
                # Данные уже кешированы - проверяем результат валидации
                validation_result = repo.get_cached_validation_result()
                if validation_result and validation_result.is_valid():
                    # Валидация прошла успешно - загружаем данные
                    await self._load_sources_and_dimensions()
                    await self._set_state(CompilationState.IDLE)
                else:
                    # Валидация не прошла
                    await self._set_state(CompilationState.ERROR)
                    await self._show_error("Сначала необходимо пройти валидацию")

        except Exception as e:
            await self._set_state(CompilationState.ERROR)
            await self._show_error(f"Ошибка инициализации: {e}")

    def on_unmount(self):
        """Вызывается при закрытии диалога."""
        track_event(
            event_type="tui.action",
            action="compile_dialog_source_closed",
            result="success",
        )

    async def _set_state(self, new_state: CompilationState):
        """Устанавливает новое состояние диалога."""
        self._state = new_state

        # Обновляем UI в зависимости от состояния
        compile_btn = self.query_one("#compile-btn", Button)

        if new_state == CompilationState.LOADING_REPO:
            compile_btn.disabled = True
            await self._show_loading("Подгружаем информацию о репозитории...")
        elif new_state == CompilationState.PREPARING:
            compile_btn.disabled = True
            await self._show_loading("Подготовка к компиляции...")
        elif new_state == CompilationState.COMPILING:
            compile_btn.disabled = True
            await self._show_loading("🔄 Подготовка к генерации SQL...")
        elif new_state == CompilationState.IDLE:
            compile_btn.disabled = False
            await self._show_info("Готов к компиляции")
        elif new_state == CompilationState.SUCCESS:
            compile_btn.disabled = False
            await self._show_info("Готов к компиляции для новой итерации")
        elif new_state == CompilationState.ERROR:
            compile_btn.disabled = False

    async def _run_validation_in_background(self):
        """Выполняет валидацию в фоновом режиме с realtime обновлениями."""
        try:
            # UI-safe progress callback для realtime обновлений
            def ui_safe_progress(message: str):
                if self._state == CompilationState.LOADING_REPO:
                    self.call_later(lambda: self._update_loading_message_sync(message))

            # Выполняем валидацию
            validation_result = await validate_repository_with_progress(
                self.app.repository, ui_safe_progress
            )

            # Проверяем результат валидации
            if validation_result and validation_result.is_valid():
                # После успешной валидации загружаем источники
                await self._load_sources_and_dimensions()
                await self._set_state(CompilationState.IDLE)
            else:
                # Валидация не прошла
                await self._set_state(CompilationState.ERROR)
                error_message = "Сначала необходимо пройти валидацию"
                self.call_later(lambda: self._show_error_sync(error_message))

        except Exception:
            await self._set_state(CompilationState.ERROR)
            error_message = (
                "Репозиторий содержит ошибки валидации. "
                "Данные для компиляции недоступны. "
                "Исправьте ошибки и попробуйте снова."
            )
            self.call_later(lambda: self._show_error_sync(error_message))

    async def _load_sources_and_dimensions(self):
        """Загружает источники и дименшены из кеша."""
        try:
            # Получаем списки источников и дименшенов из кеша
            self._sources = self.app.repository.get_cached_sources()
            self._dimensions = self.app.repository.get_cached_dimensions()

            # Обновляем селекторы
            source_selector = self.query_one("#source-select", DropdownSelect)
            dimensions_selector = self.query_one("#dimensions-select", DropdownMultiSelect)

            if self._sources:
                source_selector.set_options([(s, s) for s in self._sources])
            else:
                await self._show_warning("Источники не найдены")

            if self._dimensions:
                dimensions_selector.set_options(self._dimensions)

        except Exception as e:
            await self._set_state(CompilationState.ERROR)
            await self._show_error(f"Ошибка загрузки данных: {e}")

    def _update_loading_message_sync(self, message: str):
        """Синхронная версия для использования в call_later."""
        if self._state == CompilationState.LOADING_REPO:
            self._show_loading_sync(message)

    def action_dismiss(self) -> None:
        """Действие для закрытия диалога (ESC)."""
        if self._compilation_task and not self._compilation_task.done():
            self._compilation_task.cancel()
        self.dismiss(False)

    async def on_selection_list_selected_changed(self, event):
        """Обработка изменений в dropdown виджетах."""
        # Проверяем что событие от наших dropdown виджетов
        if event.selection_list.id == "item-list":
            # Получаем родительский виджет (DropdownSelect или DropdownMultiSelect)
            parent = event.selection_list.parent
            if parent and hasattr(parent, "id"):
                # Если это наши селекты источников или дименшенов
                if parent.id in ("source-select", "dimensions-select"):
                    # При изменении формы сбрасываем ERROR/SUCCESS в IDLE
                    if self._state in [CompilationState.ERROR, CompilationState.SUCCESS]:
                        await self._set_state(CompilationState.IDLE)

    async def on_button_pressed(self, event):
        """Обработка нажатий кнопок."""
        if event.button.id == "cancel-btn":
            self.action_dismiss()
        elif event.button.id == "compile-btn":
            # Предотвращаем повторные нажатия во время компиляции
            if self._state in [CompilationState.PREPARING, CompilationState.COMPILING]:
                return

            # Если была ошибка или успех, сбрасываем в IDLE перед новой компиляцией
            if self._state in [CompilationState.ERROR, CompilationState.SUCCESS]:
                await self._set_state(CompilationState.IDLE)

            self._compilation_task = asyncio.create_task(self._compile_sql())

    async def _compile_sql(self):
        """Выполняет компиляцию SQL с максимальной реактивностью и обработкой ошибок."""
        import time

        start_time = time.time()

        try:
            await self._set_state(CompilationState.PREPARING)

            # Валидируем форму
            source_selector = self.query_one("#source-select", DropdownSelect)
            dimensions_selector = self.query_one("#dimensions-select", DropdownMultiSelect)
            first_date_input = self.query_one("#first-date-input", Input)
            last_date_input = self.query_one("#last-date-input", Input)
            granularity_select = self.query_one("#granularity-select", Select)

            source_name = source_selector.value
            if not source_name:
                await self._set_state(CompilationState.ERROR)
                await self._show_error("Выберите источник")
                return

            # Получаем выбранные дименшены
            dimensions_list = (
                dimensions_selector.selected if dimensions_selector.selected else None
            )

            # Колонки не доступны в TUI (только в CLI для продвинутых пользователей)
            columns_list = []

            # Даты
            first_date = first_date_input.value.strip() or None
            last_date = last_date_input.value.strip() or None
            granularity = granularity_select.value

            await self._set_state(CompilationState.COMPILING)

            def progress_callback(message: str):
                if self._state == CompilationState.COMPILING:
                    self.call_later(lambda: self._show_loading_sync(message))

            repo_content = self.app.repository.get_repository_content()

            try:
                compilation_service = CompilationService()
                result = await compilation_service.compile_source(
                    repo_content=repo_content,
                    source_name=source_name,
                    dimensions=dimensions_list,
                    columns=columns_list,
                    first_date=first_date,
                    last_date=last_date,
                    granularity=granularity,
                    progress_callback=progress_callback,
                    use_emoji=True,
                )

                if result.is_successful():
                    duration_ms = int((time.time() - start_time) * 1000)
                    track_event(
                        event_type="tui.action",
                        action="compile",
                        result="success",
                        duration_ms=duration_ms,
                        parameters=TelemetryBuilder.build_compilation_params(
                            is_metrics_mode=False,
                            granularity=granularity,
                            source_name=source_name,
                            dimensions_list=dimensions_list,
                            columns_list=columns_list,
                            first_date=first_date,
                            last_date=last_date,
                        ),
                        repository_path=config.repository_path,
                    )
                    await self._set_state(CompilationState.SUCCESS)
                    sql = result.get_sql()
                    metadata = result.get_metadata()

                    # Показываем результат в главном окне
                    await self._show_sql_result(source_name, sql, metadata)
                    self.dismiss(True)
                else:
                    # Ошибка генерации SQL от бекенда
                    duration_ms = int((time.time() - start_time) * 1000)
                    await self._set_state(CompilationState.ERROR)
                    error = result.error
                    if error:
                        error_msg = error.message
                        track_event(
                            event_type="tui.action",
                            action="compile",
                            result="validation_errors",
                            duration_ms=duration_ms,
                            parameters=TelemetryBuilder.build_compilation_params(
                                is_metrics_mode=False,
                                granularity=granularity,
                                source_name=source_name,
                                dimensions_list=dimensions_list,
                                columns_list=columns_list,
                                first_date=first_date,
                                last_date=last_date,
                            ),
                            error_message=error_msg,
                            repository_path=config.repository_path,
                        )
                        await self._show_error(
                            f"Не удалось сгенерировать SQL по причине: {error_msg}"
                        )
                        # Если это ошибка валидации, выводим подробный отчет
                        if result.has_validation_errors():
                            validation_result = result.to_validation_result()
                            if validation_result:
                                summary = display_validation_error_summary(
                                    validation_result, pretty=False
                                )
                                if summary:
                                    await self._show_error(summary)
                    else:
                        track_event(
                            event_type="tui.action",
                            action="compile",
                            result="error",
                            duration_ms=duration_ms,
                            parameters=TelemetryBuilder.build_compilation_params(
                                is_metrics_mode=False,
                                granularity=granularity,
                                source_name=source_name,
                                dimensions_list=dimensions_list,
                                columns_list=columns_list,
                                first_date=first_date,
                                last_date=last_date,
                            ),
                            error_type="unknown",
                            repository_path=config.repository_path,
                        )
                        await self._show_error(
                            "Не удалось сгенерировать SQL по неизвестной причине"
                        )

            except AuthenticationError as e:
                duration_ms = int((time.time() - start_time) * 1000)
                track_event(
                    event_type="tui.action",
                    action="compile",
                    result="error",
                    duration_ms=duration_ms,
                    parameters=TelemetryBuilder.build_compilation_params(
                        is_metrics_mode=False,
                        granularity=granularity,
                        source_name=source_name,
                        dimensions_list=dimensions_list,
                        columns_list=columns_list,
                        first_date=first_date,
                        last_date=last_date,
                    ),
                    error_type="authentication_error",
                    repository_path=config.repository_path,
                )
                await self._set_state(CompilationState.ERROR)
                await self._show_error(
                    f"{e}\n\n💡 Откройте Настройки (F2) и выполните авторизацию заново"
                )

            except APIError as e:
                duration_ms = int((time.time() - start_time) * 1000)
                track_event(
                    event_type="tui.action",
                    action="compile",
                    result="error",
                    duration_ms=duration_ms,
                    parameters=TelemetryBuilder.build_compilation_params(
                        is_metrics_mode=False,
                        granularity=granularity,
                        source_name=source_name,
                        dimensions_list=dimensions_list,
                        columns_list=columns_list,
                        first_date=first_date,
                        last_date=last_date,
                    ),
                    error_type="api_error",
                    repository_path=config.repository_path,
                )
                await self._set_state(CompilationState.ERROR)
                if e.status_code == 404:
                    await self._show_error(
                        "Не удалось сгенерировать SQL по причине: API конечная точка не найдена"
                    )
                elif e.status_code == 429:
                    await self._show_error(
                        "Не удалось сгенерировать SQL по причине: "
                        "Превышен лимит запросов. Попробуйте позже"
                    )
                elif e.status_code and 500 <= e.status_code < 600:
                    await self._show_error(
                        f"Не удалось сгенерировать SQL по причине: "
                        f"Ошибка сервера ({e.status_code})"
                    )
                else:
                    await self._show_error(f"Не удалось сгенерировать SQL по причине: {e}")

            except asyncio.TimeoutError:
                duration_ms = int((time.time() - start_time) * 1000)
                track_event(
                    event_type="tui.action",
                    action="compile",
                    result="error",
                    duration_ms=duration_ms,
                    parameters=TelemetryBuilder.build_compilation_params(
                        is_metrics_mode=False,
                        granularity=granularity,
                        source_name=source_name,
                        dimensions_list=dimensions_list,
                        columns_list=columns_list,
                        first_date=first_date,
                        last_date=last_date,
                    ),
                    error_type="timeout",
                    repository_path=config.repository_path,
                )
                await self._set_state(CompilationState.ERROR)
                await self._show_error(
                    "Не удалось сгенерировать SQL по причине: "
                    "Превышено время ожидания ответа от сервера"
                )

            except asyncio.CancelledError:
                duration_ms = int((time.time() - start_time) * 1000)
                track_event(
                    event_type="tui.action",
                    action="compile",
                    result="cancelled",
                    duration_ms=duration_ms,
                    parameters=TelemetryBuilder.build_compilation_params(
                        is_metrics_mode=False,
                        granularity=granularity,
                        source_name=source_name,
                        dimensions_list=dimensions_list,
                        columns_list=columns_list,
                        first_date=first_date,
                        last_date=last_date,
                    ),
                    repository_path=config.repository_path,
                )
                await self._set_state(CompilationState.IDLE)
                await self._show_info("Компиляция отменена")

            except Exception as e:
                duration_ms = int((time.time() - start_time) * 1000)
                track_event(
                    event_type="tui.action",
                    action="compile",
                    result="error",
                    duration_ms=duration_ms,
                    parameters=TelemetryBuilder.build_compilation_params(
                        is_metrics_mode=False,
                        granularity=granularity,
                        source_name=source_name,
                        dimensions_list=dimensions_list,
                        columns_list=columns_list,
                        first_date=first_date,
                        last_date=last_date,
                    ),
                    error_type=type(e).__name__,
                    repository_path=config.repository_path,
                )
                await self._set_state(CompilationState.ERROR)
                friendly = self._format_exception_message(e)
                await self._show_error(f"Не удалось сгенерировать SQL по причине: {friendly}")

        except Exception as e:
            # Ошибки подготовки
            await self._set_state(CompilationState.ERROR)
            await self._show_error(f"Ошибка подготовки: {e}")

    async def _show_sql_result(self, source_name: str, sql: str, metadata: dict):
        """Показывает результат компиляции в главном окне."""
        # Используем новый метод для отображения SQL с кнопкой копирования
        await self.app.show_sql_with_copy_button(
            source_name, sql, metadata, compilation_type="source"
        )
