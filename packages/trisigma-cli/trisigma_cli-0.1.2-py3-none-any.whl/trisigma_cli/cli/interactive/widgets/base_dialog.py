"""Базовый класс для TUI диалогов с общими методами."""

from enum import Enum

from textual.screen import ModalScreen
from textual.widgets import Static

from ....utils.exception_handler import ExceptionHandler


class DialogState(Enum):
    """Общие состояния диалогов."""

    IDLE = "idle"
    LOADING = "loading"
    PROCESSING = "processing"
    SUCCESS = "success"
    ERROR = "error"


class BaseDialog(ModalScreen):
    """Базовый класс для диалогов с общими методами показа сообщений."""

    # Общие CSS стили для всех диалогов
    BASE_CSS = """
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

    def _sanitize_message(self, message: str) -> str:
        """
        Очищает сообщение от символов, ломающих Rich markup.

        Args:
            message: Сообщение для очистки

        Returns:
            Очищенное сообщение
        """
        return ExceptionHandler.sanitize_message(message)

    def _extract_root_exception(self, exc: BaseException) -> BaseException:
        """
        Извлекает корневую причину цепочки исключений.

        Args:
            exc: Исключение для анализа

        Returns:
            Корневое исключение
        """
        return ExceptionHandler.extract_root_exception(exc)

    def _format_exception_message(
        self, exc: BaseException, *, friendly_retry: bool = True
    ) -> str:
        """
        Форматирует исключение в человеко-понятное сообщение.

        Args:
            exc: Исключение для форматирования
            friendly_retry: Дружелюбное сообщение для RetryError

        Returns:
            Отформатированное сообщение
        """
        return ExceptionHandler.format_exception_message(exc, friendly_retry=friendly_retry)

    async def _show_error(self, message: str) -> None:
        """
        Показывает сообщение об ошибке.

        Args:
            message: Текст сообщения об ошибке
        """
        clean_message = self._sanitize_message(message)
        status = self.query_one("#status-message", Static)
        status.update(f"[red]⚠ {clean_message}[/red]")
        status.remove_class("loading-message")
        status.remove_class("success-message")
        status.remove_class("warning-message")
        status.add_class("error-message")

    def _show_error_sync(self, message: str) -> None:
        """
        Синхронная версия показа ошибки (для call_later).

        Args:
            message: Текст сообщения об ошибке
        """
        clean_message = self._sanitize_message(message)
        status = self.query_one("#status-message", Static)
        status.update(f"[red]⚠ {clean_message}[/red]")
        status.remove_class("loading-message")
        status.remove_class("success-message")
        status.remove_class("warning-message")
        status.add_class("error-message")

    async def _show_loading(self, message: str) -> None:
        """
        Показывает сообщение загрузки.

        Args:
            message: Текст сообщения загрузки
        """
        clean_message = self._sanitize_message(message)
        status = self.query_one("#status-message", Static)
        status.update(clean_message)
        status.remove_class("error-message")
        status.remove_class("success-message")
        status.remove_class("warning-message")
        status.add_class("loading-message")

    def _show_loading_sync(self, message: str) -> None:
        """
        Синхронная версия показа загрузки (для call_later).

        Args:
            message: Текст сообщения загрузки
        """
        clean_message = self._sanitize_message(message)
        status = self.query_one("#status-message", Static)
        status.update(clean_message)
        status.remove_class("error-message")
        status.remove_class("success-message")
        status.remove_class("warning-message")
        status.add_class("loading-message")

    async def _show_info(self, message: str) -> None:
        """
        Показывает информационное сообщение.

        Args:
            message: Текст информационного сообщения
        """
        clean_message = self._sanitize_message(message)
        status = self.query_one("#status-message", Static)
        status.update(f"ℹ {clean_message}")
        status.remove_class("error-message")
        status.remove_class("loading-message")
        status.remove_class("warning-message")
        status.remove_class("success-message")

    async def _show_success(self, message: str) -> None:
        """
        Показывает сообщение об успехе.

        Args:
            message: Текст сообщения об успехе
        """
        clean_message = self._sanitize_message(message)
        status = self.query_one("#status-message", Static)
        status.update(f"[green]✓ {clean_message}[/green]")
        status.remove_class("error-message")
        status.remove_class("loading-message")
        status.remove_class("warning-message")
        status.add_class("success-message")

    async def _show_warning(self, message: str) -> None:
        """
        Показывает предупреждение.

        Args:
            message: Текст предупреждения
        """
        clean_message = self._sanitize_message(message)
        status = self.query_one("#status-message", Static)
        status.update(f"[yellow]⚠ {clean_message}[/yellow]")
        status.remove_class("error-message")
        status.remove_class("loading-message")
        status.remove_class("success-message")
        status.add_class("warning-message")
