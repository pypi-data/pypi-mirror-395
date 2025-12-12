"""Диалог публикации изменений для интерактивного режима."""

import asyncio
import time
from enum import Enum
from typing import Any, Optional

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static

from ....core.config import config
from ....core.telemetry_builder import TelemetryBuilder
from ....core.telemetry_global import track_event


class PublishState(Enum):
    """Состояния процесса публикации."""

    IDLE = "idle"
    PUSHING = "pushing"
    SUCCESS = "success"
    ERROR = "error"


class PublishDialog(ModalScreen[bool]):
    """Диалог для публикации изменений."""

    CSS = """
    PublishDialog {
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
        self._state = PublishState.IDLE
        self._publish_task: Optional[asyncio.Task] = None

    def compose(self) -> ComposeResult:
        """Создает интерфейс диалога."""
        with Vertical(classes="dialog-container"):
            yield Label("Публикация изменений", classes="dialog-title")

            yield Static(id="branch-info")
            yield Static(id="changes-summary")
            yield Static(id="status-message")

            with Horizontal(classes="buttons"):
                yield Button("Опубликовать", variant="primary", id="publish-btn")
                yield Button("Отмена", variant="default", id="cancel-btn")

    async def on_mount(self) -> None:
        """Инициализация при показе диалога."""
        try:
            # Получаем информацию через сервис
            git_ui_service = getattr(self.app, "git_ui_service", None)
            if git_ui_service:
                branch_info_text = git_ui_service.format_branch_info_for_publish()
                branch_info = self.query_one("#branch-info", Static)
                branch_info.update(branch_info_text)

                # Показываем сводку изменений
                status = git_ui_service.get_git_status_info()
                changes_summary = self.query_one("#changes-summary", Static)

                summary_text = "[bold]Сводка изменений:[/bold]\n"
                summary_text += f"Файлов изменено: {status.diff_summary.get('files_changed', 0)}\n"
                summary_text += f"Строк добавлено: +{status.diff_summary.get('insertions', 0)}\n"
                summary_text += f"Строк удалено: -{status.diff_summary.get('deletions', 0)}"

                changes_summary.update(summary_text)

        except Exception as e:
            await self._show_error(f"Ошибка инициализации: {e}")

    async def _set_state(self, new_state: PublishState) -> None:
        """Устанавливает новое состояние диалога."""
        self._state = new_state

        publish_btn = self.query_one("#publish-btn", Button)
        cancel_btn = self.query_one("#cancel-btn", Button)

        if new_state == PublishState.IDLE:
            publish_btn.disabled = False
            cancel_btn.disabled = False
        elif new_state == PublishState.PUSHING:
            publish_btn.disabled = True
            cancel_btn.disabled = False
        elif new_state in [PublishState.SUCCESS, PublishState.ERROR]:
            publish_btn.disabled = False
            cancel_btn.disabled = False

    async def on_button_pressed(self, event: Any) -> None:
        """Обработка нажатий кнопок."""
        if event.button.id == "cancel-btn":
            if self._publish_task and not self._publish_task.done():
                self._publish_task.cancel()
            self.dismiss(False)

        elif event.button.id == "publish-btn":
            if self._state == PublishState.PUSHING:
                return
            self._publish_task = asyncio.create_task(self._publish_changes())

    async def _publish_changes(self) -> None:
        """Публикует изменения."""
        start_time = time.time()
        pr_url_generated = False
        current_branch = None

        try:
            await self._set_state(PublishState.PUSHING)
            await self._show_loading("🔄 Отправка в удаленный репозиторий...")
            await asyncio.sleep(0)

            git_ui_service = getattr(self.app, "git_ui_service", None)
            if not git_ui_service:
                await self._set_state(PublishState.ERROR)
                await self._show_error("Сервис git недоступен")

                duration_ms = int((time.time() - start_time) * 1000)
                track_event(
                    event_type="tui.action",
                    action="git.publish_changes",
                    result="error",
                    duration_ms=duration_ms,
                    error_type="git_service_unavailable",
                    error_message="Git service not available",
                    repository_path=config.repository_path,
                    parameters=TelemetryBuilder.build_git_params(),
                )
                return

            result = await git_ui_service.publish_changes()

            if not result.success:
                await self._set_state(PublishState.ERROR)
                await self._show_error(result.error_message)

                current_branch = None
                if git_ui_service and git_ui_service.is_available:
                    try:
                        status = git_ui_service.get_git_status_info()
                        current_branch = status.current_branch
                    except Exception:
                        pass

                duration_ms = int((time.time() - start_time) * 1000)
                error_msg = (
                    str(result.error_message)[:500]
                    if result.error_message
                    else "Publish failed"
                )
                track_event(
                    event_type="tui.action",
                    action="git.publish_changes",
                    result="error",
                    duration_ms=duration_ms,
                    error_type="publish_failed",
                    error_message=error_msg,
                    repository_path=config.repository_path,
                    parameters=TelemetryBuilder.build_git_params(
                        current_branch=current_branch,
                    ),
                )
                return

            await self._set_state(PublishState.SUCCESS)

            status = git_ui_service.get_git_status_info()
            current_branch = status.current_branch
            pr_url_generated = bool(result.pull_request_url)

            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="tui.action",
                action="git.publish_changes",
                result="success",
                duration_ms=duration_ms,
                parameters=TelemetryBuilder.build_git_params(
                    pr_url_generated=pr_url_generated,
                    files_changed=status.diff_summary.get("files_changed", 0),
                    current_branch=current_branch,
                    insertions=status.diff_summary.get("insertions", 0),
                    deletions=status.diff_summary.get("deletions", 0),
                ),
                repository_path=config.repository_path,
            )

            result_text = f"[green]✓ Ветка '{current_branch}' опубликована[/green]\n\n"
            result_text += "Нажмите кнопку ниже для создания Pull Request в браузере."

            show_content = getattr(self.app, "show_content", None)
            update_interface = getattr(self.app, "_update_interface", None)
            show_pr_button = getattr(self.app, "show_pull_request_button", None)

            pr_url = result.pull_request_url

            self.dismiss(True)

            if hasattr(self.app, "call_later"):
                if update_interface:
                    self.app.call_later(update_interface)

                if show_content:
                    self.app.call_later(lambda: show_content(result_text))

                if show_pr_button:
                    self.app.call_later(lambda: show_pr_button(pr_url))
            else:
                if update_interface:
                    await update_interface()

                if show_content:
                    await show_content(result_text)

                if show_pr_button:
                    await show_pr_button(pr_url)

        except asyncio.CancelledError:
            await self._set_state(PublishState.IDLE)
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
                action="git.publish_changes",
                result="cancelled",
                duration_ms=duration_ms,
                repository_path=config.repository_path,
                parameters=TelemetryBuilder.build_git_params(
                    current_branch=current_branch,
                ),
            )
        except Exception as e:
            await self._set_state(PublishState.ERROR)
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
                action="git.publish_changes",
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

    async def _show_info(self, message: str) -> None:
        """Показывает информационное сообщение."""
        status = self.query_one("#status-message", Static)
        status.update(message)
        status.remove_class("error-message")
        status.remove_class("loading-message")
        status.remove_class("warning-message")
        status.remove_class("success-message")
