"""Диалог управления ветками."""

import time
from typing import Any

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static

from ....core.config import config
from ....core.telemetry_builder import TelemetryBuilder
from ....core.telemetry_global import track_event


class BranchDialog(ModalScreen[bool]):
    """Диалог для создания и переключения веток."""

    CSS = """
    BranchDialog {
        align: center middle;
    }

    .dialog-container {
        width: 60;
        height: auto;
        background: $surface;
        border: solid gray;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Создает интерфейс диалога."""
        # Получаем конфигурацию UI из backend
        cli_config = config.get_cli_config()

        # Определяем placeholder и label для task ID
        task_placeholder = "PROJECT-123"  # Дефолт
        task_label_text = "Номер задачи"
        task_required = True

        if cli_config and cli_config.ui:
            if cli_config.ui.task_format_example:
                task_placeholder = cli_config.ui.task_format_example
            if cli_config.ui.task_format_label:
                task_label_text = cli_config.ui.task_format_label
            task_required = cli_config.ui.task_id_required

        # Добавляем метку о необязательности если нужно
        if not task_required:
            task_label_text += " (необязательно)"

        with Vertical(classes="dialog-container"):
            yield Label("Создание ветки для задачи", classes="dialog-title")

            yield Label(f"{task_label_text}:")
            yield Input(placeholder=task_placeholder, id="task-input")

            yield Label("Краткое описание (необязательно):")
            yield Input(placeholder="fix-source-bug", id="description-input")

            yield Static(id="status-message")

            with Horizontal(classes="buttons"):
                yield Button("Создать", variant="primary", id="create-btn")
                yield Button("Отмена", variant="default", id="cancel-btn")

    async def on_button_pressed(self, event: Any) -> None:
        """Обработка нажатий кнопок."""
        if event.button.id == "cancel-btn":
            self.dismiss(False)

        elif event.button.id == "create-btn":
            await self._create_branch()

    async def _create_branch(self) -> None:
        """Создает новую ветку."""
        start_time = time.time()
        branch_created = False

        try:
            task_input = self.query_one("#task-input", Input)
            description_input = self.query_one("#description-input", Input)

            task_number = task_input.value.strip()
            description = description_input.value.strip() or None

            # Показываем статус
            await self._show_message("🔄 Обновление master из origin...")

            git_ui_service = getattr(self.app, "git_ui_service", None)
            if not git_ui_service:
                await self._show_error("Сервис git недоступен")

                duration_ms = int((time.time() - start_time) * 1000)
                track_event(
                    event_type="tui.action",
                    action="git.create_branch",
                    result="error",
                    duration_ms=duration_ms,
                    error_type="git_service_unavailable",
                    error_message="Git service not available",
                    repository_path=config.repository_path,
                    parameters=TelemetryBuilder.build_git_params(),
                )
                return

            # Обновляем статус во время операции
            await self._show_message("🔄 Создание ветки от обновленного master...")

            result = await git_ui_service.create_task_branch(task_number, description)

            if not result.success:
                await self._show_error(result.error_message)

                duration_ms = int((time.time() - start_time) * 1000)
                error_msg = (
                    str(result.error_message)[:500]
                    if result.error_message
                    else "Branch creation failed"
                )
                current_branch = None
                if git_ui_service and git_ui_service.is_available:
                    try:
                        status = git_ui_service.get_git_status_info()
                        current_branch = status.current_branch
                    except Exception:
                        pass

                track_event(
                    event_type="tui.action",
                    action="git.create_branch",
                    result="error",
                    duration_ms=duration_ms,
                    error_type="branch_creation_failed",
                    error_message=error_msg,
                    parameters=TelemetryBuilder.build_git_params(
                        task_number=task_number,
                        has_description=bool(description),
                        current_branch=current_branch,
                    ),
                    repository_path=config.repository_path,
                )
                return

            branch_created = True

            # Сохраняем ссылки до закрытия диалога
            update_interface = getattr(self.app, "_update_interface", None)
            show_content = getattr(self.app, "show_content", None)

            # Подготавливаем текст результата
            result_text = (
                f"[green]✓ Создана и активна ветка:[/green] [cyan]{result.branch_name}[/cyan]\n\n"
                "[blue]Ветка создана от актуального master.[/blue]\n"
                "Теперь вы можете вносить изменения и сохранять их."
            )

            duration_ms = int((time.time() - start_time) * 1000)
            track_event(
                event_type="tui.action",
                action="git.create_branch",
                result="success",
                duration_ms=duration_ms,
                parameters=TelemetryBuilder.build_git_params(
                    task_number=task_number,
                    has_description=bool(description),
                    current_branch=result.branch_name,
                    branch_name=result.branch_name,
                    branch_created=branch_created,
                ),
                repository_path=config.repository_path,
            )

            # Закрываем диалог ПЕРЕД обновлением интерфейса
            self.dismiss(True)

            # Используем call_later для обновления после закрытия диалога
            if hasattr(self.app, "call_later"):
                if update_interface:
                    self.app.call_later(update_interface)

                if show_content:
                    self.app.call_later(lambda: show_content(result_text))
            else:
                # Fallback для старых версий
                if update_interface:
                    await update_interface()

                if show_content:
                    await show_content(result_text)

        except Exception as e:
            await self._show_error(f"Ошибка: {e}")

            duration_ms = int((time.time() - start_time) * 1000)
            current_branch = None
            git_ui_service = getattr(self.app, "git_ui_service", None)
            if git_ui_service and git_ui_service.is_available:
                try:
                    status = git_ui_service.get_git_status_info()
                    current_branch = status.current_branch
                except Exception:
                    pass

            track_event(
                event_type="tui.action",
                action="git.create_branch",
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

    async def _show_message(self, message: str) -> None:
        """Показывает информационное сообщение."""
        status = self.query_one("#status-message", Static)
        status.update(message)
