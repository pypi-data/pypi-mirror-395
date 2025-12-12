"""Диалог сохранения изменений для интерактивного режима."""

import asyncio
import time
from enum import Enum
from typing import Any, Optional

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static, TextArea

from ....core.config import config
from ....core.jwt_decoder import extract_user_info
from ....core.telemetry_builder import TelemetryBuilder
from ....core.telemetry_global import track_event


class SaveState(Enum):
    """Состояния процесса сохранения."""

    IDLE = "idle"
    ADDING_FILES = "adding_files"
    COMMITTING = "committing"
    SUCCESS = "success"
    ERROR = "error"


class SaveDialog(ModalScreen[bool]):
    """Диалог для сохранения изменений."""

    CSS = """
    SaveDialog {
        align: center middle;
    }

    .dialog-container {
        width: 70;
        height: auto;
        background: $surface;
        border: solid gray;
        padding: 1;
    }

    #status-message {
        height: auto;
        min-height: 1;
        margin: 1 0;
    }

    .loading-message {
        color: $accent;
        text-style: italic;
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

    def __init__(self):
        super().__init__()
        self._state = SaveState.IDLE
        self._save_task: Optional[asyncio.Task] = None

    def compose(self) -> ComposeResult:
        """Создает интерфейс диалога."""
        with Vertical(classes="dialog-container"):
            yield Label("Сохранение изменений", classes="dialog-title")

            yield Label("Сообщение коммита:")
            yield TextArea(id="message-input")

            yield Label("Номер задачи (определяется автоматически, можно изменить):")
            yield Input(id="task-input")

            yield Static(
                "[dim]ℹ Все SQL и YAML файлы будут автоматически добавлены в коммит[/dim]",
                id="info-message",
            )

            yield Static(id="status-message")

            with Horizontal(classes="buttons"):
                yield Button("Сохранить", variant="primary", id="save-btn")
                yield Button("Отмена", variant="default", id="cancel-btn")

    async def on_mount(self) -> None:
        """Инициализация при показе диалога."""
        try:
            # Пытаемся определить номер задачи из ветки
            git_ui_service = getattr(self.app, "git_ui_service", None)
            if git_ui_service:
                status = git_ui_service.get_git_status_info()
                task_number = git_ui_service.extract_task_from_branch(status.current_branch)

                if task_number:
                    task_input = self.query_one("#task-input", Input)
                    task_input.value = task_number

        except Exception:
            pass  # Игнорируем ошибки определения задачи

    async def _set_state(self, new_state: SaveState) -> None:
        """Устанавливает новое состояние диалога."""
        self._state = new_state

        save_btn = self.query_one("#save-btn", Button)
        cancel_btn = self.query_one("#cancel-btn", Button)

        if new_state == SaveState.IDLE:
            save_btn.disabled = False
            cancel_btn.disabled = False
        elif new_state in [SaveState.ADDING_FILES, SaveState.COMMITTING]:
            save_btn.disabled = True
            cancel_btn.disabled = False
        elif new_state in [SaveState.SUCCESS, SaveState.ERROR]:
            save_btn.disabled = False
            cancel_btn.disabled = False

    async def on_button_pressed(self, event: Any) -> None:
        """Обработка нажатий кнопок."""
        if event.button.id == "cancel-btn":
            if self._save_task and not self._save_task.done():
                self._save_task.cancel()
            self.dismiss(False)

        elif event.button.id == "save-btn":
            if self._state in [SaveState.ADDING_FILES, SaveState.COMMITTING]:
                return
            self._save_task = asyncio.create_task(self._save_changes())

    async def _save_changes(self) -> None:
        """Сохраняет изменения."""
        start_time = time.time()
        files_changed = 0
        has_author_from_jwt = False

        try:
            message_input = self.query_one("#message-input", TextArea)
            task_input = self.query_one("#task-input", Input)

            message = message_input.text.strip()
            task_number = task_input.value.strip() or None

            await self._set_state(SaveState.ADDING_FILES)
            await self._show_loading("🔄 Добавление SQL и YAML файлов...")
            await asyncio.sleep(0)

            try:
                git_workflow = getattr(self.app, "git_workflow", None)
                if git_workflow:
                    loop = asyncio.get_event_loop()
                    added_files = await loop.run_in_executor(None, git_workflow.add_metrics_files)
                    if added_files:
                        files_changed = len(added_files)
                        files_text = f"Добавлено {files_changed} файлов метрик"
                        await self._show_loading(f"✓ {files_text}")
                        await asyncio.sleep(0.5)
            except Exception as e:
                await self._show_warning(f"⚠ Предупреждение при добавлении файлов: {e}")
                await asyncio.sleep(1)

            await self._set_state(SaveState.COMMITTING)
            await self._show_loading("🔄 Создание коммита...")
            await asyncio.sleep(0)

            author_name, author_email = None, None
            access_token = config.get("access_token")
            if access_token:
                author_name, author_email = extract_user_info(access_token)
                has_author_from_jwt = bool(author_name and author_email)

            git_ui_service = getattr(self.app, "git_ui_service", None)
            if not git_ui_service:
                await self._set_state(SaveState.ERROR)
                await self._show_error("Сервис git недоступен")

                duration_ms = int((time.time() - start_time) * 1000)
                track_event(
                    event_type="tui.action",
                    action="git.save_changes",
                    result="error",
                    duration_ms=duration_ms,
                    error_type="git_service_unavailable",
                    error_message="Git service not available",
                    repository_path=config.repository_path,
                    parameters=TelemetryBuilder.build_git_params(),
                )
                return

            result = await git_ui_service.save_changes(
                message, task_number, author_name, author_email
            )

            if not result.success:
                await self._set_state(SaveState.ERROR)
                await self._show_error(result.error_message)

                current_branch = None
                if git_ui_service and git_ui_service.is_available:
                    try:
                        status = git_ui_service.get_git_status_info()
                        current_branch = status.current_branch
                    except Exception:
                        pass

                duration_ms = int((time.time() - start_time) * 1000)
                track_event(
                    event_type="tui.action",
                    action="git.save_changes",
                    result="error",
                    duration_ms=duration_ms,
                    parameters=TelemetryBuilder.build_git_params(
                        task_number=task_number,
                        has_author_from_jwt=has_author_from_jwt,
                        files_changed=files_changed,
                        current_branch=current_branch,
                    ),
                    error_type="save_failed",
                    error_message=result.error_message[:500],
                    repository_path=config.repository_path,
                )
                return

            await self._set_state(SaveState.SUCCESS)

            current_branch = None
            if git_ui_service and git_ui_service.is_available:
                try:
                    status = git_ui_service.get_git_status_info()
                    current_branch = status.current_branch
                except Exception:
                    pass

            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="tui.action",
                action="git.save_changes",
                result="success",
                duration_ms=duration_ms,
                parameters=TelemetryBuilder.build_git_params(
                    task_number=task_number,
                    has_author_from_jwt=has_author_from_jwt,
                    files_changed=files_changed,
                    commit_sha=result.commit_sha,
                    current_branch=current_branch,
                ),
                repository_path=config.repository_path,
            )

            update_interface = getattr(self.app, "_update_interface", None)
            show_content = getattr(self.app, "show_content", None)

            result_text = "[green]✓ Изменения сохранены[/green]\n"
            result_text += f"Коммит: [cyan]{result.commit_sha[:8]}[/cyan]\n"
            if result.task_number:
                result_text += f"Задача: [cyan]{result.task_number}[/cyan]\n"
            result_text += (
                "\n[dim]Все SQL и YAML файлы были автоматически добавлены в коммит[/dim]\n"
            )
            result_text += "\nДля публикации изменений используйте 'Опубликовать изменения'"

            self.dismiss(True)

            if hasattr(self.app, "call_later"):
                if update_interface:
                    self.app.call_later(update_interface)

                if show_content:
                    self.app.call_later(lambda: show_content(result_text))
            else:
                if update_interface:
                    await update_interface()

                if show_content:
                    await show_content(result_text)

        except asyncio.CancelledError:
            await self._set_state(SaveState.IDLE)
            await self._show_info("Операция отменена")

            current_branch = None
            git_ui_service = getattr(self.app, "git_ui_service", None)
            if git_ui_service and git_ui_service.is_available:
                try:
                    status = git_ui_service.get_git_status_info()
                    current_branch = status.current_branch
                except Exception:
                    pass

            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="tui.action",
                action="git.save_changes",
                result="cancelled",
                duration_ms=duration_ms,
                repository_path=config.repository_path,
                parameters=TelemetryBuilder.build_git_params(
                    current_branch=current_branch,
                ),
            )
        except Exception as e:
            await self._set_state(SaveState.ERROR)
            await self._show_error(f"Ошибка: {e}")

            current_branch = None
            git_ui_service = getattr(self.app, "git_ui_service", None)
            if git_ui_service and git_ui_service.is_available:
                try:
                    status = git_ui_service.get_git_status_info()
                    current_branch = status.current_branch
                except Exception:
                    pass

            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="tui.action",
                action="git.save_changes",
                result="error",
                duration_ms=duration_ms,
                error_type=type(e).__name__,
                error_message=str(e)[:500],
                repository_path=config.repository_path,
                parameters=TelemetryBuilder.build_git_params(
                    current_branch=current_branch,
                ),
            )

    async def _show_error(self, message: str) -> None:
        """Показывает сообщение об ошибке."""
        status = self.query_one("#status-message", Static)
        status.update(f"[red]Ошибка:[/red] {message}")
        status.remove_class("loading-message")
        status.remove_class("success-message")
        status.remove_class("warning-message")
        status.add_class("error-message")

    async def _show_loading(self, message: str) -> None:
        """Показывает сообщение загрузки."""
        status = self.query_one("#status-message", Static)
        status.update(message)
        status.remove_class("error-message")
        status.remove_class("success-message")
        status.remove_class("warning-message")
        status.add_class("loading-message")

    async def _show_warning(self, message: str) -> None:
        """Показывает предупреждение."""
        status = self.query_one("#status-message", Static)
        status.update(message)
        status.remove_class("error-message")
        status.remove_class("loading-message")
        status.remove_class("success-message")
        status.add_class("warning-message")

    async def _show_info(self, message: str) -> None:
        """Показывает информационное сообщение."""
        status = self.query_one("#status-message", Static)
        status.update(message)
        status.remove_class("error-message")
        status.remove_class("loading-message")
        status.remove_class("warning-message")
        status.remove_class("success-message")
