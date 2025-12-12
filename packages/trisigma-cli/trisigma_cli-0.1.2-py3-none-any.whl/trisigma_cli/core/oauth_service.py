"""OAuth сервис для авторизации CLI."""

import webbrowser
from dataclasses import dataclass
from typing import Dict
from urllib.parse import urlencode

from .auth_server import LocalAuthServer
from .cli_config_client import CLIConfig, CLIConfigClient
from .config import config


@dataclass
class OAuthResult:
    """Результат OAuth авторизации."""

    access_token: str
    refresh_token: str
    backend_url: str
    auth_url: str
    cli_config: CLIConfig


class OAuthService:
    """Сервис для выполнения OAuth авторизации."""

    async def perform_oauth_flow(
        self,
        backend_url: str,
        timeout: int = 60,
        open_browser: bool = True,
    ) -> OAuthResult:
        """
        Выполняет OAuth flow и возвращает токены.

        Args:
            backend_url: URL бэкенда
            timeout: Таймаут ожидания в секундах
            open_browser: Открывать ли браузер автоматически

        Returns:
            OAuthResult с токенами и конфигурацией

        Raises:
            TrisigmaError: При ошибке авторизации
            TimeoutError: При таймауте ожидания
        """
        cli_config: CLIConfig = await CLIConfigClient().fetch_config(backend_url)

        auth_server: LocalAuthServer = LocalAuthServer()
        port: int = auth_server.port
        redirect_uri: str = f"http://localhost:{port}/callback"

        params: str = urlencode({"redirect_uri": redirect_uri})
        auth_url: str = f"{cli_config.auth_url}?{params}"

        if open_browser:
            webbrowser.open(auth_url)

        try:
            token_data: Dict[str, str] = auth_server.start_and_wait_for_callback(timeout=timeout)
        except TimeoutError as e:
            raise TimeoutError(f"Авторизация не завершена за {timeout} секунд") from e

        return OAuthResult(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            backend_url=backend_url,
            auth_url=auth_url,
            cli_config=cli_config,
        )


def save_oauth_config(result: OAuthResult) -> None:
    """
    Сохраняет OAuth результат в конфигурацию.

    Args:
        result: Результат OAuth авторизации
    """
    config.update(
        backend_url=result.backend_url,
        api_url=result.backend_url,
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )
    config.set_cli_config(result.cli_config)
