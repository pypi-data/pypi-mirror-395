"""Диалог для отображения SQL с полноценным скроллом."""

from typing import Literal, Optional

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static
from rich.syntax import Syntax
from rich.text import Text

from ....core.config import config
from ....core.telemetry_global import track_event


class SQLViewDialog(ModalScreen[bool]):
    """Диалог для отображения SQL с возможностью прокрутки."""

    AUTO_FOCUS = ""

    BINDINGS = [
        Binding("escape", "dismiss", "Закрыть"),
        Binding("ctrl+c", "copy_sql", "Копировать SQL"),
    ]

    CSS = """
    SQLViewDialog {
        align: center middle;
    }

    .dialog-container {
        width: 95%;
        height: 90%;
        background: $surface;
        border: solid gray;
        layout: vertical;
    }

    .dialog-header {
        height: auto;
        min-height: 3;
        padding: 1;
        background: $primary;
        text-align: center;
    }

    .dialog-content {
        height: 1fr;
        layout: vertical;
        padding: 1;
    }

    .metadata-section {
        height: auto;
        min-height: 1;
        max-height: 8;
        margin: 0 0 1 0;
        overflow-y: auto;
    }

    .sql-container {
        height: 1fr;
        border: solid gray;
        padding: 1;
        overflow-y: auto;
    }

    .sql-content {
        height: auto;
        min-height: 1fr;
    }

    .buttons {
        height: auto;
        min-height: 3;
        margin: 1 0 0 0;
        layout: horizontal;
        align: center middle;
    }

    .buttons > Button {
        margin: 0 1;
    }

    .title {
        color: white;
        text-style: bold;
    }

    .metadata-title {
        text-style: bold;
        color: $accent;
        margin: 0 0 1 0;
    }
    """

    def __init__(
        self,
        title: str,
        sql: str,
        metadata: Optional[dict] = None,
        compilation_type: Literal["source", "metrics"] = "source",
    ):
        super().__init__()
        self.title_text = title
        self.sql_content = sql
        self.metadata = metadata or {}
        self.compilation_type = compilation_type

    def compose(self) -> ComposeResult:
        """Создает интерфейс диалога."""
        with Vertical(classes="dialog-container"):
            # Заголовок
            with Static(classes="dialog-header"):
                yield Label(f"SQL для {self.title_text}", classes="title")

            # Основное содержимое
            with Vertical(classes="dialog-content"):
                # Метаданные (если есть)
                if self.metadata:
                    with ScrollableContainer(classes="metadata-section"):
                        yield Label("Метаданные генерации:", classes="metadata-title")

                        # Найденные столбцы
                        resolved_cols = self.metadata.get("resolved_columns", [])
                        if resolved_cols:
                            yield Static(f"Найденные столбцы: {', '.join(resolved_cols)}")

                        # Использованные обогащения
                        used_enrichments = self.metadata.get("used_enrichments", [])
                        if used_enrichments:
                            yield Static(
                                f"Использованные обогащения: {', '.join(used_enrichments)}"
                            )
                        else:
                            yield Static("Использованные обогащения: нет")

                        # Отсутствующие столбцы
                        missing_cols = self.metadata.get("missing_columns", [])
                        if missing_cols:
                            missing_text = Text(
                                f"Отсутствующие столбцы: {', '.join(missing_cols)}"
                            )
                            missing_text.stylize("yellow")
                            yield Static(missing_text)

                # SQL с прокруткой
                with ScrollableContainer(classes="sql-container"):
                    # Создаем объект Syntax для подсветки SQL
                    syntax_sql = Syntax(
                        self.sql_content, "sql", theme="monokai", line_numbers=True, word_wrap=True
                    )
                    yield Static(syntax_sql, classes="sql-content")

                # Кнопки
                with Horizontal(classes="buttons"):
                    yield Button("📋 Копировать", variant="primary", id="copy-btn")
                    yield Button("Закрыть", variant="default", id="close-btn")

    def action_dismiss(self) -> None:
        """Действие для закрытия диалога (ESC)."""
        self.dismiss(False)

    def action_copy_sql(self) -> None:
        """Копирует SQL в буфер обмена."""
        self._copy_sql_to_clipboard()

    def _copy_sql_to_clipboard(self) -> None:
        """Копирует SQL в буфер обмена и показывает уведомление."""
        try:
            import pyperclip

            pyperclip.copy(self.sql_content)
            self.notify("SQL скопирован в буфер обмена", severity="information")
            
            # Отправляем событие телеметрии
            track_event(
                event_type="tui.action",
                action=f"copy_sql.{self.compilation_type}",
                result="success",
                parameters={
                    "sql_length": len(self.sql_content),
                    "has_metadata": bool(self.metadata),
                },
                repository_path=config.repository_path,
            )
        except ImportError as e:
            self.notify(
                "Не удалось скопировать: модуль pyperclip не установлен", severity="warning"
            )
            # Телеметрия: ошибка - pyperclip не установлен
            track_event(
                event_type="tui.action",
                action=f"copy_sql.{self.compilation_type}",
                result="error",
                error_type=type(e).__name__,
                error_message=str(e)[:500],
                repository_path=config.repository_path,
            )
        except Exception as e:
            self.notify(f"Ошибка копирования: {e}", severity="error")
            # Телеметрия: ошибка копирования
            track_event(
                event_type="tui.action",
                action=f"copy_sql.{self.compilation_type}",
                result="error",
                error_type=type(e).__name__,
                error_message=str(e)[:500],
                repository_path=config.repository_path,
            )

    async def on_button_pressed(self, event) -> None:
        """Обработка нажатий кнопок."""
        if event.button.id == "copy-btn":
            self._copy_sql_to_clipboard()
        elif event.button.id == "close-btn":
            self.action_dismiss()
