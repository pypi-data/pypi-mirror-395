import asyncio
import logging
from typing import Dict, Optional

import aiohttp
from pydantic import BaseModel, ConfigDict, Field
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

from ..utils.exceptions import APIError
from .config import VERIFY_SSL

logger = logging.getLogger(__name__)


def _is_server_error(exception: BaseException) -> bool:
    """
    Проверяет, является ли исключение ошибкой сервера (5xx).

    Args:
        exception: Исключение для проверки

    Returns:
        True если это ClientResponseError с кодом 500-599
    """
    if isinstance(exception, aiohttp.ClientResponseError):
        return 500 <= exception.status < 600
    return False


class GitConfig(BaseModel):
    """Git configuration with PR URL template and default branch."""

    model_config = ConfigDict(populate_by_name=True)

    default_branch: Optional[str] = Field(default=None, alias="defaultBranch")
    pr_url_template: Optional[str] = Field(default=None, alias="prUrlTemplate")


class UIConfig(BaseModel):
    """UI/UX configuration for prompts and placeholders."""

    model_config = ConfigDict(populate_by_name=True)

    task_format_example: str = Field(default="PROJECT-123", alias="taskFormatExample")
    task_format_label: str = Field(default="Task tracking system", alias="taskFormatLabel")
    task_id_required: bool = Field(default=True, alias="taskIdRequired")
    task_id_regex: Optional[str] = Field(default=None, alias="taskIdRegex")


class SupportConfig(BaseModel):
    """Support and help configuration."""

    model_config = ConfigDict(populate_by_name=True)

    support_chat_url: Optional[str] = Field(default=None, alias="supportChatUrl")
    support_chat_text: Optional[str] = Field(default=None, alias="supportChatText")


class CLIConfig(BaseModel):
    """Extended CLI configuration from backend."""

    model_config = ConfigDict(populate_by_name=True)

    auth_url: str = Field(alias="authUrl")
    git: Optional[GitConfig] = None
    ui: Optional[UIConfig] = None
    support: Optional[SupportConfig] = None


class CLIConfigClient:
    """Client for fetching CLI configuration from backend."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=(
            retry_if_exception_type(
                (asyncio.TimeoutError, aiohttp.ClientConnectionError, aiohttp.ClientError)
            )
            | retry_if_exception(_is_server_error)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def fetch_config(self, backend_url: str) -> CLIConfig:
        """
        Fetch CLI configuration from backend.

        Args:
            backend_url: Backend server URL

        Returns:
            CLIConfig object with extended configuration
        """
        url: str = f"{backend_url.rstrip('/')}/api/internal/getCliConfig"

        headers: Dict[str, str] = {"Content-Type": "application/json"}
        connector = aiohttp.TCPConnector(ssl=VERIFY_SSL)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    if 500 <= resp.status < 600:
                        raise aiohttp.ClientResponseError(
                            request_info=resp.request_info,
                            history=resp.history,
                            status=resp.status,
                            message=f"Server error: HTTP {resp.status}",
                        )
                    raise APIError(f"Failed to fetch CLI config: HTTP {resp.status}")
                data: Dict[str, object] = await resp.json()
                result: Dict[str, object] = data.get("result", data)  # type: ignore
                return CLIConfig(**result)  # type: ignore
