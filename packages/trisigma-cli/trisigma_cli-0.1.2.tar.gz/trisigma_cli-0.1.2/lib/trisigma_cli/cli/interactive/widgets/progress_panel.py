"""Панель прогресса для длительных операций."""

from typing import Any, Generator, Optional, Union

from textual.widgets import ProgressBar, Static


class ProgressPanel(Static):
    """Панель для отображения прогресса операций."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.border_title = "Выполнение"
        self._is_visible = False
        self._current_operation = ""
        self.display = False  # Скрыто по умолчанию

    def compose(self) -> Generator[Union[Static, ProgressBar], None, None]:
        """Создает интерфейс панели прогресса."""
        yield Static(id="operation-text")
        yield ProgressBar(id="progress-bar")

    async def show_progress(self, operation: str, progress: Optional[float] = None) -> None:
        """
        Показывает прогресс операции.

        Args:
            operation: Описание операции
            progress: Прогресс от 0 до 100 (None для неопределенного прогресса)
        """
        self._current_operation = operation
        self._is_visible = True
        self.display = True

        # Обновляем текст операции
        operation_text = self.query_one("#operation-text", Static)
        operation_text.update(f"🔄 {operation}")

        # Обновляем прогресс-бар
        progress_bar = self.query_one("#progress-bar", ProgressBar)
        if progress is not None:
            progress_bar.update(progress=progress)
        else:
            # Неопределенный прогресс
            progress_bar.update(progress=-1)

    async def hide_progress(self) -> None:
        """Скрывает панель прогресса."""
        self._is_visible = False
        self.display = False

    async def update_progress(self, progress: float, operation: Optional[str] = None) -> None:
        """
        Обновляет прогресс.

        Args:
            progress: Новое значение прогресса (0-100)
            operation: Новое описание операции (опционально)
        """
        if operation:
            self._current_operation = operation
            operation_text = self.query_one("#operation-text", Static)
            operation_text.update(f"🔄 {operation}")

        progress_bar = self.query_one("#progress-bar", ProgressBar)
        progress_bar.update(progress=progress)

    @property
    def is_visible(self) -> bool:
        """Возвращает True если панель видима."""
        return self._is_visible
