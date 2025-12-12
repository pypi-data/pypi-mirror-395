"""Service for automatic token refresh."""

import asyncio
import logging
from typing import Optional

import aiohttp
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

from .config import config, VERIFY_SSL
from ..utils.exceptions import APIError, AuthenticationError, ConfigurationError
from ..utils.http import extract_error_message, is_server_error

logger = logging.getLogger(__name__)


class TokenRefreshService:
    """Handles automatic refresh of access tokens."""

    TOKEN_REFRESH_BUFFER_SECONDS = 300

    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize token refresh service.

        Args:
            api_url: API base URL (defaults to config.api_url)
        """
        self.api_url = api_url or config.api_url
        # Ленивая инициализация Lock - создаём только внутри async контекста
        # чтобы избежать ошибки "There is no current event loop" в Python 3.10+
        self._refresh_lock: Optional[asyncio.Lock] = None

    def _get_lock(self) -> asyncio.Lock:
        """
        Получает asyncio.Lock, создавая его лениво при первом использовании.

        Returns:
            asyncio.Lock для синхронизации refresh операций
        """
        if self._refresh_lock is None:
            self._refresh_lock = asyncio.Lock()
        return self._refresh_lock

    async def ensure_valid_token(self) -> str:
        """
        Ensure we have a valid access token, refreshing if necessary.

        Returns:
            Valid access token

        Raises:
            ConfigurationError: If no tokens are configured
            APIError: If token refresh fails
        """
        access_token = config.access_token

        if not access_token:
            raise ConfigurationError(
                "Токен доступа не настроен. Выполните 'trisigma login' для авторизации."
            )

        return access_token

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=(
            retry_if_exception_type(
                (asyncio.TimeoutError, aiohttp.ClientConnectionError, aiohttp.ClientError)
            )
            | retry_if_exception(is_server_error)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _refresh_tokens(self) -> None:
        """
        Refresh access token using refresh token.

        Backend всегда возвращает HTTP 200, даже для ошибок.
        Ошибки передаются через JSON: {"error": {"message": "..."}}.

        Raises:
            ConfigurationError: If refresh token is not configured
            AuthenticationError: If refresh token is invalid or expired
            APIError: If refresh request fails
        """
        refresh_token = config.refresh_token

        if not refresh_token:
            raise ConfigurationError(
                "Refresh токен не настроен. Выполните 'trisigma login' для повторной авторизации."
            )

        if not self.api_url:
            raise ConfigurationError("API URL не настроен. Выполните 'trisigma login' для настройки.")

        url = f"{self.api_url.rstrip('/')}/api/internal/refreshJwtAuthToken"

        try:
            connector = aiohttp.TCPConnector(ssl=VERIFY_SSL)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(
                    url,
                    json={"refresh_token": refresh_token},
                    headers={"Content-Type": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise APIError(
                            f"Failed to refresh token: HTTP {response.status} - {error_text}",
                            status_code=response.status,
                        )

                    data = await response.json()

                    if "error" in data:
                        error_message = extract_error_message(data["error"])
                        refresh_error_patterns = ["refresh token", "invalid", "expired"]
                        if any(
                            pattern in error_message.lower() for pattern in refresh_error_patterns
                        ):
                            raise AuthenticationError(
                                f"{error_message}. Выполните 'trisigma login' для повторной авторизации.",
                                status_code=response.status,
                            )
                        raise APIError(f"Token refresh failed: {error_message}")

                    result = data.get("result", data)

                    # Backend возвращает токены в camelCase
                    new_access_token = result.get("accessToken") or result.get("access_token")
                    new_refresh_token = result.get("refreshToken") or result.get("refresh_token")

                    if not new_access_token or not new_refresh_token:
                        raise APIError("Invalid refresh response: missing tokens")

                    config.update(
                        access_token=new_access_token,
                        refresh_token=new_refresh_token,
                    )

        except aiohttp.ClientError as e:
            raise APIError(f"Network error during token refresh: {e}")
        except asyncio.TimeoutError:
            raise APIError("Token refresh request timed out")
