"""Диалог AI объяснения ошибок валидации."""

import asyncio
from typing import List

from rich.markdown import Markdown
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static, TextArea

from ....core.config import config
from ....core.dto import ProcessedValidationError
from ....core.backend_llm_client import BackendLLMClient
from ....core.llm_explain_service import LLMExplainService
from ....core.repository import MetricsRepository
from ....core.token_refresh_service import TokenRefreshService
from ....utils.thinking_messages import ThinkingMessagesGenerator


class AIExplainDialog(ModalScreen[None]):
    """Диалог для показа AI объяснения ошибок валидации."""

    BINDINGS = [
        Binding("escape", "dismiss", "Закрыть"),
        Binding("ctrl+c", "copy_content", "Копировать"),
    ]

    CSS = """
    AIExplainDialog {
        align: center middle;
    }

    .dialog-container {
        width: 90%;
        height: 85%;
        max-width: 120;
        max-height: 40;
        background: $surface;
        border: solid gray;
        padding: 1;
    }

    .dialog-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .content-container {
        height: 1fr;
        border: round gray;
        padding: 1;
        background: $surface-lighten-1;
    }

    .content-text {
        height: auto;
        min-height: 1fr;
    }

    .content-container.thinking {
        text-align: center;
        content-align: center middle;
        color: $primary;
        text-style: italic;
    }

    .status-area {
        height: auto;
        margin: 1 0;
        text-align: center;
    }

    .buttons {
        height: auto;
        margin-top: 1;
        layout: horizontal;
    }

    .loading {
        color: $primary;
        text-style: italic;
    }

    .error {
        color: $error;
        text-style: bold;
    }

    .feedback-container {
        height: auto;
        margin-top: 2;
        padding: 1;
        border: round $primary;
        background: $surface;
    }

    .feedback-container.hidden {
        display: none;
    }

    .feedback-title {
        text-style: bold;
        margin-bottom: 1;
        text-align: center;
    }

    .feedback-rating-buttons {
        height: auto;
        margin-bottom: 1;
        layout: horizontal;
    }

    .feedback-rating-buttons Button {
        width: 1fr;
    }

    .feedback-rating-buttons Button.selected {
        text-style: bold;
        border: heavy;
    }

    .feedback-comment-label {
        height: auto;
        margin-bottom: 1;
        color: $text-muted;
    }

    .feedback-comment {
        height: 5;
        margin-bottom: 1;
        border: round gray;
    }

    .feedback-validation {
        height: auto;
        margin-bottom: 1;
        text-align: center;
        color: $error;
    }

    #submit-feedback-btn {
        width: 100%;
    }
    """

    def __init__(
        self,
        validation_errors: List[ProcessedValidationError],
        repository: MetricsRepository,
    ):
        super().__init__()
        self.validation_errors = validation_errors
        self.repository = repository
        self._explanation_task = None
        self._current_content = ""
        self._error_text = ""
        self._feedback_rating = None
        self._feedback_shown = False

    def compose(self) -> ComposeResult:
        """Создает интерфейс диалога."""
        with Vertical(classes="dialog-container"):
            yield Label("🤖 Помощь с ошибками валидации от AI", classes="dialog-title")

            yield Static(
                f"📊 Анализирую {len(self.validation_errors)} ошибок...",
                id="status-message",
                classes="status-area loading",
            )

            with ScrollableContainer(classes="content-container"):
                yield Static("Получение AI анализа...", id="content", classes="content-text")

                with Vertical(id="feedback-container", classes="feedback-container hidden"):
                    yield Label("Был ли полезен этот ответ?", classes="feedback-title")
                    with Horizontal(classes="feedback-rating-buttons"):
                        yield Button("✓ Полезно", variant="success", id="feedback-like-btn")
                        yield Button("✗ Не полезно", variant="error", id="feedback-dislike-btn")
                    yield Label(
                        "Комментарий (обязателен для отрицательной оценки):",
                        classes="feedback-comment-label",
                    )
                    yield TextArea(
                        id="feedback-comment",
                        classes="feedback-comment",
                    )
                    yield Label("", id="feedback-validation-message", classes="feedback-validation")
                    yield Button("Отправить фидбек", variant="primary", id="submit-feedback-btn")

            with Horizontal(classes="buttons"):
                yield Button("📋 Копировать", variant="primary", id="copy-btn")
                yield Button("📊 Оценить ответ", variant="default", id="rate-btn")
                yield Button("Закрыть", variant="default", id="close-btn")

    async def on_mount(self) -> None:
        """Инициализация при монтировании."""
        # Запускаем асинхронное получение объяснения
        self._explanation_task = asyncio.create_task(self._get_ai_explanation())

    async def _get_ai_explanation(self) -> None:
        """Получает AI объяснение ошибок."""
        thinking_task = None
        import time
        start_time = time.time()
        
        try:
            content_widget = self.query_one("#content", Static)
            status_widget = self.query_one("#status-message", Static)

            # Создаем LLM клиент и сервис
            if not config.api_url or not config.access_token:
                raise ValueError("API URL и access token должны быть настроены")

            token_refresh_service = TokenRefreshService(config.api_url)
            llm_client = BackendLLMClient(
                config.api_url, config.access_token, token_refresh_service
            )
            service = LLMExplainService(llm_client)

            # Показываем статистику контекста
            stats, context = service.get_context_stats(self.validation_errors, self.repository)
            if "error" not in stats:
                status_text = (
                    f"📊 Анализирую {stats['errors_count']} ошибок, "
                    f"{stats['found_files_count']} файлов, "
                    f"размер контекста: {stats['context_utilization']}"
                )
                status_widget.update(status_text)

            # Запускаем фоновую задачу для обновления thinking-сообщений
            thinking_generator = ThinkingMessagesGenerator()

            async def update_thinking_messages():
                """Фоновая задача для обновления thinking-сообщений."""
                try:
                    while True:
                        await asyncio.sleep(5)
                        message = thinking_generator.get_next()
                        status_widget.update(message)
                except asyncio.CancelledError:
                    pass

            try:
                thinking_task = asyncio.create_task(update_thinking_messages())
                response = await service.explain_validation_errors(
                    self.validation_errors, self.repository, context=context
                )
            finally:
                if thinking_task and not thinking_task.done():
                    thinking_task.cancel()
                    try:
                        await thinking_task
                    except asyncio.CancelledError:
                        pass

            self._current_content = response
            
            # Измеряем время выполнения
            duration_ms = int((time.time() - start_time) * 1000)

            # Обновляем контент как Markdown
            try:
                markdown_content = Markdown(self._current_content)
                content_widget.update(markdown_content)
            except Exception:
                content_widget.update(self._current_content)

            status_widget.update("✅ AI анализ завершен")

            # Логируем событие в телеметрию
            from ....core.telemetry_global import track_event
            from ....core.telemetry_builder import TelemetryBuilder

            error_text = "\n".join([
                f"{e.file or 'unknown'}:{e.line or 0} - {e.message}"
                for e in self.validation_errors[:5]
            ])[:5000]

            self._error_text = error_text

            telemetry_params = TelemetryBuilder.build_ai_explain_params(
                errors_count=len(self.validation_errors),
                error_text=error_text,
                ai_response_size=len(response),
            )
            track_event(
                event_type="tui.ai_explain",
                action="validation_explain",
                result="success",
                duration_ms=duration_ms,
                parameters=telemetry_params,
            )

        except Exception as e:
            if thinking_task and not thinking_task.done():
                thinking_task.cancel()
                try:
                    await thinking_task
                except asyncio.CancelledError:
                    pass

            # Измеряем время даже в случае ошибки
            duration_ms = int((time.time() - start_time) * 1000)

            error_message = f"❌ Ошибка получения AI объяснения: {str(e)}"

            content_widget = self.query_one("#content", Static)
            status_widget = self.query_one("#status-message", Static)

            content_widget.update(error_message)
            content_widget.add_class("error")
            status_widget.update("❌ Ошибка AI анализа")
            status_widget.add_class("error")

            # Логируем ошибку в телеметрию
            from ....core.telemetry_global import track_event

            track_event(
                event_type="tui.ai_explain",
                action="validation_explain",
                result="error",
                duration_ms=duration_ms,
                error_type=type(e).__name__,
                error_message=str(e)[:500],
            )

    def _copy_content_to_clipboard(self) -> None:
        """Копирует AI ответ в буфер обмена и показывает уведомление."""
        try:
            import pyperclip

            pyperclip.copy(self._current_content)
            self.notify("Текст скопирован в буфер обмена", severity="information")

            from ....core.telemetry_global import track_event

            track_event(
                event_type="tui.action",
                action="copy_ai_explanation",
                result="success",
                parameters={
                    "content_length": len(self._current_content),
                    "errors_count": len(self.validation_errors),
                },
                repository_path=config.repository_path,
            )
        except ImportError as e:
            self.notify(
                "Не удалось скопировать: модуль pyperclip не установлен", severity="warning"
            )
            from ....core.telemetry_global import track_event

            track_event(
                event_type="tui.action",
                action="copy_ai_explanation",
                result="error",
                error_type=type(e).__name__,
                error_message=str(e)[:500],
                repository_path=config.repository_path,
            )
        except Exception as e:
            self.notify(f"Ошибка копирования: {e}", severity="error")
            from ....core.telemetry_global import track_event

            track_event(
                event_type="tui.action",
                action="copy_ai_explanation",
                result="error",
                error_type=type(e).__name__,
                error_message=str(e)[:500],
                repository_path=config.repository_path,
            )

    def action_copy_content(self) -> None:
        """Действие для копирования контента (Ctrl+C)."""
        self._copy_content_to_clipboard()

    def action_dismiss(self) -> None:
        """Действие для закрытия диалога (ESC)."""
        if self._explanation_task and not self._explanation_task.done():
            self._explanation_task.cancel()
        self.dismiss()

    async def on_button_pressed(self, event) -> None:
        """Обработка нажатий кнопок."""
        if event.button.id == "copy-btn":
            self._copy_content_to_clipboard()
        elif event.button.id == "close-btn":
            self.action_dismiss()
        elif event.button.id == "rate-btn":
            self._show_feedback_form()
        elif event.button.id == "feedback-like-btn":
            self._set_feedback_rating("like")
        elif event.button.id == "feedback-dislike-btn":
            self._set_feedback_rating("dislike")
        elif event.button.id == "submit-feedback-btn":
            await self._submit_feedback()

    def _show_feedback_form(self) -> None:
        """Показывает форму фидбека."""
        if self._feedback_shown:
            return

        feedback_container = self.query_one("#feedback-container")
        feedback_container.remove_class("hidden")

        rate_btn = self.query_one("#rate-btn", Button)
        rate_btn.disabled = True

        def scroll_to_feedback():
            scroll_container = self.query_one(ScrollableContainer)
            scroll_container.scroll_end(animate=True)

        self.call_after_refresh(scroll_to_feedback)

        self._feedback_shown = True

    def _set_feedback_rating(self, rating: str) -> None:
        """Устанавливает оценку фидбека."""
        from ....core.dto import FeedbackRating

        self._feedback_rating = rating

        like_btn = self.query_one("#feedback-like-btn", Button)
        dislike_btn = self.query_one("#feedback-dislike-btn", Button)
        validation_msg = self.query_one("#feedback-validation-message", Label)

        like_btn.remove_class("selected")
        dislike_btn.remove_class("selected")

        if rating == FeedbackRating.LIKE:
            like_btn.add_class("selected")
        elif rating == FeedbackRating.DISLIKE:
            dislike_btn.add_class("selected")

        validation_msg.update("")

    async def _submit_feedback(self) -> None:
        """Отправляет фидбек в телеметрию."""
        from ....core.dto import FeedbackRating
        from ....core.telemetry_global import track_event
        from ....core.telemetry_builder import TelemetryBuilder

        if not self._feedback_rating:
            validation_msg = self.query_one("#feedback-validation-message", Label)
            validation_msg.update("Пожалуйста, выберите оценку")
            return

        comment_area = self.query_one("#feedback-comment", TextArea)
        user_comment = comment_area.text.strip()

        if self._feedback_rating == FeedbackRating.DISLIKE and not user_comment:
            validation_msg = self.query_one("#feedback-validation-message", Label)
            validation_msg.update("Пожалуйста расскажи чего не хватило в ответе и что стоит улучшить")
            return

        try:
            telemetry_params = TelemetryBuilder.build_ai_feedback_params(
                error_description=self._error_text,
                full_ai_response=self._current_content,
                rating=self._feedback_rating,
                user_comment=user_comment,
            )

            track_event(
                event_type="tui.ai_feedback",
                action="validation_explain_feedback",
                result="success",
                parameters=telemetry_params,
            )

            self.notify("Спасибо за отзыв!", severity="information", timeout=3)

            feedback_container = self.query_one("#feedback-container")
            feedback_container.add_class("hidden")

            comment_area.clear()

            like_btn = self.query_one("#feedback-like-btn", Button)
            dislike_btn = self.query_one("#feedback-dislike-btn", Button)
            like_btn.remove_class("selected")
            dislike_btn.remove_class("selected")

            validation_msg = self.query_one("#feedback-validation-message", Label)
            validation_msg.update("")

            self._feedback_shown = False
            self._feedback_rating = None

            rate_btn = self.query_one("#rate-btn", Button)
            rate_btn.disabled = False

        except Exception as e:
            track_event(
                event_type="tui.ai_feedback",
                action="validation_explain_feedback",
                result="error",
                error_type=type(e).__name__,
                error_message=str(e)[:500],
            )

            self.notify(f"Ошибка отправки фидбека: {e}", severity="error")

    def on_unmount(self) -> None:
        """Очистка при размонтировании."""
        if self._explanation_task and not self._explanation_task.done():
            self._explanation_task.cancel()
