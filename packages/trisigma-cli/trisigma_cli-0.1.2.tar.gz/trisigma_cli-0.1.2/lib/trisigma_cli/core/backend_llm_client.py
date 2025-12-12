"""Backend LLM клиент для вызова ChatCompletion API через ab-configurator."""

import asyncio
import logging

import aiohttp
from typing import Any, Dict, List, Optional, TypedDict

from pydantic import BaseModel
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

from ..utils.exceptions import AuthenticationError, ConfigurationError
from ..utils.http import is_auth_error, is_server_error
from .config import VERIFY_SSL
from .token_refresh_service import TokenRefreshService

logger = logging.getLogger(__name__)


class ModelInfo(TypedDict):
    id: str
    display_name: str
    aliases: List[str]
    token_limit: int


# Модели доступные через backend
HARD_CODED_MODELS: List[ModelInfo] = [
    {
        "id": "qwen3-32b",
        "display_name": "qwen3-32b",
        "aliases": ["fast", "qwen3"],
        "token_limit": 32768,
    },
]


class LLMMessage(BaseModel):
    role: str
    content: str


class BackendLLMClient:
    def __init__(
        self,
        backend_url: str,
        access_token: str,
        token_refresh_service: TokenRefreshService,
        timeout: int = 120,
    ):
        self.backend_url = backend_url.rstrip("/")
        self.access_token = access_token
        self.token_refresh_service = token_refresh_service
        self.timeout = timeout

    async def __aenter__(self) -> "BackendLLMClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

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
    async def _chat_completion_internal(
        self,
        messages: List[LLMMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        if not messages:
            raise ValueError("Messages list cannot be empty")

        prompt = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])

        url = f"{self.backend_url}/api/ChatCompletion"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {
            "prompt": prompt,
            "model": model or "qwen3-32b",
        }

        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["maxTokens"] = max_tokens

        connector = aiohttp.TCPConnector(ssl=VERIFY_SSL)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(
                url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as resp:
                if resp.status != 200:
                    error_text = await resp.text()

                    if is_auth_error(error_text, resp.status):
                        raise AuthenticationError(
                            f"Ошибка аутентификации: {error_text}. Выполните 'trisigma login' для повторной авторизации.",
                            status_code=resp.status,
                        )

                    raise RuntimeError(
                        f"ChatCompletion API failed with status {resp.status}: {error_text}"
                    )

                data = await resp.json()

                if "error" in data:
                    error_message = str(data["error"].get("message", data["error"]))
                    if is_auth_error(error_message, resp.status):
                        raise AuthenticationError(
                            f"{error_message}. Выполните 'trisigma login' для повторной авторизации.",
                            status_code=resp.status,
                        )
                    raise RuntimeError(f"ChatCompletion API error: {error_message}")

                result = data.get("result", data)

                content = result.get("content")
                if not content:
                    raise RuntimeError("Response does not contain 'content' field")

                return str(content)

    async def chat_completion(
        self,
        messages: List[LLMMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        _retry_count: int = 0,
    ) -> str:
        try:
            return await self._chat_completion_internal(messages, model, temperature, max_tokens)
        except AuthenticationError as e:
            if _retry_count == 0:
                try:
                    await self.token_refresh_service._refresh_tokens()

                    from .config import config

                    self.access_token = config.access_token

                    return await self.chat_completion(
                        messages, model, temperature, max_tokens, _retry_count=1
                    )
                except (AuthenticationError, ConfigurationError):
                    raise
                except Exception:
                    raise e
            raise

    async def health_check(self) -> bool:
        try:
            test_messages = [LLMMessage(role="user", content="Test")]
            response = await self.chat_completion(test_messages, max_tokens=1)
            return bool(response)
        except Exception:
            return False

    async def get_models(self) -> List[str]:
        """Возвращает список доступных моделей."""
        return [model["id"] for model in HARD_CODED_MODELS]

    def get_model_token_limit(self, model_name: Optional[str] = None) -> int:
        """
        Получает лимит токенов для указанной модели.

        Args:
            model_name: Название модели

        Returns:
            Лимит токенов для модели
        """
        if not model_name:
            # Используем первую доступную модель
            model_name = HARD_CODED_MODELS[0]["id"]

        # Ищем модель по ID или алиасам
        for model in HARD_CODED_MODELS:
            model_id = model["id"]
            aliases = model["aliases"]
            if model_id == model_name or model_name in aliases:
                return model["token_limit"]

        # Fallback на дефолтное значение
        return 32768
