"""Диалог настроек."""

import asyncio

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static

from ....core.api_client import TrisigmaAPIClient
from ....core.config import DEFAULT_BACKEND_URL, config
from ....core.oauth_service import OAuthResult, OAuthService


class SettingsDialog(ModalScreen[bool]):
    """Диалог настроек CLI."""

    BINDINGS = [
        Binding("escape", "dismiss", "Закрыть"),
    ]

    def __init__(self):
        super().__init__()
        self._auth_task = None

    CSS = """
    SettingsDialog {
        align: center middle;
    }

    .dialog-container {
        width: 80;
        height: 85vh;
        background: $surface;
        border: solid gray;
        padding: 1;
        layout: vertical;
    }

    .form-scroll {
        height: 1fr;
        overflow-y: auto;
    }

    .section-divider {
        margin: 1 0;
        padding: 0;
        color: $accent;
        text-style: bold;
    }

    .buttons-container {
        height: auto;
        margin: 1 0 0 0;
        layout: vertical;
    }

    .button-row {
        height: 3;
        align: center middle;
        layout: horizontal;
    }

    .button-row-actions {
        height: 3;
        align: center middle;
        layout: horizontal;
        margin-top: 1;
    }

    .button-row > Button {
        margin: 0 1;
    }

    .button-row-actions > Button {
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Создает интерфейс диалога."""
        with Vertical(classes="dialog-container"):
            yield Label("Настройки Trisigma CLI", classes="dialog-title")

            # Область с формой (прокручивается)
            with Vertical(classes="form-scroll"):
                yield Label("Путь к репозиторию:")
                yield Input(id="repository-input")

                yield Label("Backend URL:")
                yield Input(id="backend-url-input", placeholder=DEFAULT_BACKEND_URL)

                yield Static(id="current-config")
                yield Static(id="status-message")

            # Кнопки вне области скролла (фиксируются снизу диалога)
            with Vertical(classes="buttons-container"):
                with Horizontal(classes="button-row"):
                    yield Button("Авторизация", variant="success", id="auth-btn")
                    yield Button("Тест API", variant="default", id="test-btn")
                with Horizontal(classes="button-row-actions"):
                    yield Button("Сохранить", variant="primary", id="save-btn")
                    yield Button("Отмена", variant="default", id="cancel-btn")

    async def on_mount(self):
        """Инициализация при показе диалога."""
        try:
            # Заполняем текущие настройки
            repository_input = self.query_one("#repository-input", Input)
            backend_url_input = self.query_one("#backend-url-input", Input)

            if config.repository_path:
                repository_input.value = config.repository_path

            backend_url = config.get("backend_url")
            if backend_url:
                backend_url_input.value = backend_url

            # Показываем текущую конфигурацию
            await self._show_current_config()

        except Exception as e:
            await self._show_error(f"Ошибка инициализации: {e}")

    def action_dismiss(self):
        """Действие для закрытия диалога (ESC)."""
        self._cancel_auth_task()
        self.dismiss(False)

    def _cancel_auth_task(self):
        """Отменяет фоновую задачу авторизации."""
        if self._auth_task and not self._auth_task.done():
            self._auth_task.cancel()

    async def on_button_pressed(self, event):
        """Обработка нажатий кнопок."""
        if event.button.id == "cancel-btn":
            self._cancel_auth_task()
            self.dismiss(False)

        elif event.button.id == "save-btn":
            await self._save_settings()

        elif event.button.id == "auth-btn":
            if self._auth_task and not self._auth_task.done():
                await self._show_message("⚠️ Авторизация уже выполняется...")
                return
            self._auth_task = asyncio.create_task(self._start_oauth_flow())

        elif event.button.id == "test-btn":
            await self._test_api_connection()

    async def _save_settings(self):
        """Сохраняет настройки."""
        try:
            repository_input = self.query_one("#repository-input", Input)
            backend_url_input = self.query_one("#backend-url-input", Input)

            repository_path = repository_input.value.strip()
            backend_url = backend_url_input.value.strip()

            updates = {}
            if repository_path:
                updates["repository_path"] = repository_path
            if backend_url:
                updates["backend_url"] = backend_url

            if updates:
                config.update(**updates)

            await self._show_message("[green]✓ Настройки сохранены[/green]")
            await self._show_current_config()

            # Обновляем интерфейс приложения
            await self.app._initialize_app()

        except Exception as e:
            await self._show_error(f"Ошибка сохранения: {e}")

    async def _start_oauth_flow(self):
        """Запускает OAuth авторизацию через браузер."""
        try:
            repository_input = self.query_one("#repository-input", Input)
            backend_url_input = self.query_one("#backend-url-input", Input)

            repository_path = repository_input.value.strip()
            backend_url = backend_url_input.value.strip()

            if not backend_url:
                await self._show_error("Введите Backend URL")
                return

            await self._show_message("🔄 Загрузка конфигурации...")

            oauth_service = OAuthService()
            result: OAuthResult = await oauth_service.perform_oauth_flow(
                backend_url, timeout=300, open_browser=True
            )

            await self._show_message("✓ Конфигурация получена")
            await self._show_message(f"🌐 Браузер открыт: {result.auth_url}")
            await self._show_message("✓ Токены получены")

            updates = {
                "backend_url": result.backend_url,
                "api_url": result.backend_url,
                "access_token": result.access_token,
                "refresh_token": result.refresh_token,
            }

            if repository_path:
                updates["repository_path"] = repository_path

            config.update(**updates)

            await self._show_message("[green]✓ Авторизация успешна![/green]")
            await self._show_current_config()

            await self.app._initialize_app()

        except asyncio.CancelledError:
            await self._show_message("⚠️ Авторизация отменена")
        except TimeoutError as e:
            await self._show_error(f"Timeout: {e}")
        except Exception as e:
            await self._show_error(f"Ошибка авторизации: {e}")

    async def _test_api_connection(self):
        """Тестирует подключение к API."""
        try:
            if not config.api_url or not config.access_token:
                await self._show_error("Настройте API URL и токен")
                return

            await self._show_message("🔄 Проверка подключения к API...")

            async with TrisigmaAPIClient(config.api_url, config.access_token) as api_client:
                is_available = await api_client.health_check()

            if is_available:
                await self._show_message("[green]✓ API доступно и токен валиден[/green]")
            else:
                await self._show_error("API недоступно или токен невалиден")

        except Exception as e:
            await self._show_error(f"Ошибка подключения: {e}")

    async def _show_current_config(self):
        """Показывает текущую конфигурацию."""
        current_config = self.query_one("#current-config", Static)

        config_text = "[bold]Текущие настройки:[/bold]\n"
        config_text += f"Репозиторий: {config.repository_path or '[не настроен]'}\n"

        backend_url = config.get("backend_url")
        config_text += f"Backend URL: {backend_url or '[не настроен]'}\n"

        config_text += f"API URL: {config.api_url or '[не настроен]'}\n"
        config_text += (
            f"Access token: {'[настроен]' if config.access_token else '[не настроен]'}\n"
        )

        # Статус конфигурации
        if config.is_configured():
            config_text += "\n[green]✓ Конфигурация готова[/green]"
            if config.is_llm_configured():
                config_text += "\n[green]✓ LLM доступен через backend[/green]"
        else:
            missing = config.get_missing_config()
            missing_settings = ", ".join(missing)
            config_text += f"\n[yellow]⚠ Не хватает настроек: {missing_settings}[/yellow]"

        current_config.update(config_text)

    async def _show_error(self, message: str):
        """Показывает сообщение об ошибке."""
        status = self.query_one("#status-message", Static)
        error_msg = f"[red]Ошибка:[/red] {message}"
        status.update(error_msg)

    async def _show_message(self, message: str):
        """Показывает информационное сообщение."""
        status = self.query_one("#status-message", Static)
        status.update(message)

    def on_unmount(self):
        """Очистка при размонтировании."""
        self._cancel_auth_task()
