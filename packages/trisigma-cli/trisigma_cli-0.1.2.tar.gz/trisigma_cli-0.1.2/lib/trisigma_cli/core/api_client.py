"""Клиент для работы с Trisigma API."""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientTimeout
from pydantic import ValidationError as PydanticValidationError
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

from ..utils.exceptions import APIError, AuthenticationError, ConfigurationError
from ..utils.http import extract_error_message, is_auth_error, is_server_error
from ..utils.validation import format_validation_errors
from .config import VERIFY_SSL
from .token_refresh_service import TokenRefreshService
from .version import __version__


from .dto import (
    ComponentValidationResult,
    ErrorCode,
    EntityType,
    FastValidateRepoContentRequest,
    FastValidateRepoContentResponse,
    GenerateSqlFromRepoRequest,
    GenerateSqlFromRepoResponse,
    Granularity,
    ProcessedValidationError,
    RepoContentDict,
    SqlGenerationItem,
    SqlGenerationMetricItem,
    ValidationError,
    ValidationResults,
)

logger = logging.getLogger(__name__)


class TrisigmaAPIClient:
    """Клиент для взаимодействия с Trisigma API."""

    def __init__(
        self,
        base_url: str,
        api_token: Optional[str] = None,
        timeout: int = 60,
        use_token_refresh: bool = True,
    ):
        """
        Инициализирует API клиент.

        Args:
            base_url: Базовый URL API
            api_token: API токен для аутентификации (optional if using token refresh)
            timeout: Таймаут запросов в секундах
            use_token_refresh: Use automatic token refresh
        """
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout
        self.use_token_refresh = use_token_refresh
        self._session: Optional[aiohttp.ClientSession] = None
        self._token_refresh_service: Optional[TokenRefreshService] = None
        if use_token_refresh:
            self._token_refresh_service = TokenRefreshService(api_url=base_url)

    async def __aenter__(self) -> "TrisigmaAPIClient":
        """Async context manager entry."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def _ensure_session(self) -> None:
        """Ensures the aiohttp session is created with a valid token."""
        if self._session is None or self._session.closed:
            token = self.api_token

            timeout = ClientTimeout(total=self.timeout)
            headers = {
                "Content-Type": "application/json",
                "User-Agent": f"Trisigma-CLI/{__version__}",
                "Authorization": f"Bearer {token}",
            }
            connector = aiohttp.TCPConnector(ssl=VERIFY_SSL)
            self._session = aiohttp.ClientSession(
                timeout=timeout, headers=headers, connector=connector
            )

    async def close(self) -> None:
        """Closes the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def _make_request_with_retry(
        self,
        method: str,
        endpoint: str,
        progress_callback: Optional[Callable[[str], None]] = None,
        _retry_count: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Make request with automatic retry after token refresh.

        Backend возвращает HTTP 200 даже для auth ошибок.
        Ошибки auth передаются через JSON: {"error": {"message": "..."}}.

        Args:
            method: HTTP method
            endpoint: API endpoint
            progress_callback: Progress callback
            _retry_count: Internal retry counter
            **kwargs: Additional aiohttp arguments

        Returns:
            Parsed JSON response

        Raises:
            AuthenticationError: On authentication failure after refresh attempt
            APIError: On request failure
        """
        try:
            return await self._make_request_internal(method, endpoint, progress_callback, **kwargs)
        except (AuthenticationError, APIError) as e:
            if (
                self._should_retry_with_token_refresh(e)
                and _retry_count == 0
                and self.use_token_refresh
            ):
                if self._token_refresh_service:
                    try:
                        await self._token_refresh_service._refresh_tokens()

                        from .config import config

                        self.api_token = config.access_token

                        await self._session.close() if self._session else None
                        self._session = None

                        await self._ensure_session()

                        return await self._make_request_with_retry(
                            method, endpoint, progress_callback, _retry_count=1, **kwargs
                        )
                    except (AuthenticationError, ConfigurationError):
                        raise
                    except Exception:
                        raise e
            raise

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
    async def _make_request_internal(
        self,
        method: str,
        endpoint: str,
        progress_callback: Optional[Callable[[str], None]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Выполняет HTTP запрос к API с поддержкой повторных попыток.

        Args:
            method: HTTP метод
            endpoint: Конечная точка API
            progress_callback: Callback для обновления прогресса
            **kwargs: Дополнительные аргументы для aiohttp

        Returns:
            Parsed JSON response data

        Raises:
            APIError: При ошибке запроса
            AuthenticationError: При ошибке аутентификации
        """
        await self._ensure_session()
        url = urljoin(self.base_url, endpoint)

        if progress_callback:
            progress_callback("Отправка запроса...")

        timeout = aiohttp.ClientTimeout(total=300)

        try:
            await self._ensure_session()
            if self._session is None:
                raise RuntimeError("Failed to create session")

            async with self._session.request(method, url, timeout=timeout, **kwargs) as response:
                if progress_callback:
                    progress_callback("Обработка ответа...")

                response.raise_for_status()

                if progress_callback:
                    progress_callback("Получение данных ответа...")

                json_response = await response.json()

                if progress_callback:
                    progress_callback("Парсинг JSON ответа...")

                if "error" in json_response:
                    error_data = json_response["error"]
                    error_message = extract_error_message(error_data)

                    if is_auth_error(error_message):
                        raise AuthenticationError(
                            error_message,
                            status_code=response.status,
                            response_data=json_response,
                        )

                    raise APIError(
                        error_message,
                        status_code=response.status,
                        response_data=json_response,
                    )

                return json_response

        except aiohttp.ClientResponseError as e:
            if is_server_error(e):
                raise
            if e.status in (401, 403):
                raise AuthenticationError(
                    f"Ошибка HTTP {e.status}: {e.message}. Выполните 'trisigma login' для повторной авторизации.",
                    status_code=e.status,
                    response_data=None,
                )
            raise APIError(
                f"Ошибка HTTP {e.status}: {e.message}",
                status_code=e.status,
                response_data=None,
            )
        except (json.JSONDecodeError, ValueError) as e:
            raise APIError(f"Невалидный JSON ответ от API: {e}")
        except asyncio.TimeoutError:
            raise APIError("Превышено время ожидания ответа от API")
        except aiohttp.ClientError as e:
            raise APIError(f"Ошибка соединения с API: {e}")

    def _should_retry_with_token_refresh(self, error: Exception) -> bool:
        """
        Проверяет нужно ли попробовать refresh токена.

        Backend всегда возвращает HTTP 200, даже для auth ошибок.
        Ошибки передаются через JSON body с полем "error".

        Returns:
            True если нужно попробовать обновить токен:
            - AuthenticationError (может быть expired access token)
            - APIError с status 401 или 403 (для обратной совместимости)
        """
        if isinstance(error, AuthenticationError):
            return True
        if isinstance(error, APIError):
            return error.status_code in (401, 403)
        return False

    async def validate_repository(
        self,
        repo_content: RepoContentDict,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> FastValidateRepoContentResponse:
        """
        Валидирует репозиторий метрик через API.

        Args:
            repo_content: Типизированная модель с содержимым репозитория
            progress_callback: Callback для обновления прогресса

        Returns:
            Результат валидации

        Raises:
            APIError: При ошибке API
        """
        try:
            if progress_callback:
                progress_callback("Подготовка данных для валидации...")

            # Используем готовую типизированную модель
            request_model = FastValidateRepoContentRequest(repo_content=repo_content)

            if progress_callback:
                progress_callback("Отправка данных репозитория на сервер...")

            response_data = await self._make_request_with_retry(
                "POST",
                "/api/FastValidateRepoContent",
                progress_callback=progress_callback,
                json=request_model.model_dump(),
            )

            if progress_callback:
                progress_callback("Обработка результатов валидации...")

            result = response_data.get("result")

            if progress_callback:
                progress_callback("Завершение валидации...")

            return FastValidateRepoContentResponse(**(result or {}))

        except PydanticValidationError as e:
            raise APIError(f"Ошибка валидации данных запроса: {e}")
        except (json.JSONDecodeError, ValueError) as e:
            raise APIError(f"Невалидный JSON ответ от API: {e}")

    async def generate_sql(
        self,
        repo_content: RepoContentDict,
        source_name: str,
        dimensions: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
        first_date: Optional[str] = None,
        last_date: Optional[str] = None,
        granularity: str = "day",
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> GenerateSqlFromRepoResponse:
        """
        Генерирует SQL через API.

        Args:
            repo_content: Типизированная модель с содержимым репозитория
            source_name: Название источника
            dimensions: Список дименшенов
            columns: Список колонок
            first_date: Начальная дата (YYYY-MM-DD)
            last_date: Конечная дата (YYYY-MM-DD)
            granularity: Гранулярность (day, week, month)
            progress_callback: Callback для обновления прогресса

        Returns:
            Результат генерации SQL

        Raises:
            APIError: При ошибке API
        """
        try:
            if progress_callback:
                progress_callback("Подготовка данных для генерации SQL...")

            # Создаем элемент для генерации
            item = SqlGenerationItem(
                source_name=source_name,
                granularity=Granularity(granularity),
                dimensions=dimensions,
                columns=columns,
                first_date=first_date,
                last_date=last_date,
            )

            request_model = GenerateSqlFromRepoRequest(
                repo_content=repo_content,
                entity_type=EntityType.SOURCE,
                source_items=[item],
            )

            if progress_callback:
                progress_callback("Отправка запроса на генерацию SQL...")

            response_data = await self._make_request_with_retry(
                "POST",
                "/api/GenerateSqlFromRepo",
                progress_callback=progress_callback,
                json=request_model.model_dump(),
            )

            if progress_callback:
                progress_callback("Парсинг результатов генерации...")

            result = response_data.get("result")
            return GenerateSqlFromRepoResponse(**(result or {}))

        except PydanticValidationError as e:
            raise APIError(f"Ошибка валидации данных запроса: {e}")
        except (json.JSONDecodeError, ValueError) as e:
            raise APIError(f"Невалидный JSON ответ от API: {e}")

    async def generate_metric_sql(
        self,
        repo_content: RepoContentDict,
        metric_names: List[str],
        dimensions: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
        first_date: Optional[str] = None,
        last_date: Optional[str] = None,
        granularity: str = "day",
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> GenerateSqlFromRepoResponse:
        """
        Генерирует SQL для метрик через API.

        Args:
            repo_content: Типизированная модель с содержимым репозитория
            metric_names: Список имен метрик
            dimensions: Список дименшенов
            columns: Список колонок
            first_date: Начальная дата (YYYY-MM-DD)
            last_date: Конечная дата (YYYY-MM-DD)
            granularity: Гранулярность (day, week, month)
            progress_callback: Callback для обновления прогресса

        Returns:
            Результат генерации SQL

        Raises:
            APIError: При ошибке API
        """
        try:
            if progress_callback:
                progress_callback("Подготовка данных для генерации SQL метрик...")

            # Создаем элемент для генерации метрик
            item = SqlGenerationMetricItem(
                metric_names=metric_names,
                granularity=Granularity(granularity),
                dimensions=dimensions,
                columns=columns,
                first_date=first_date,
                last_date=last_date,
            )

            request_model = GenerateSqlFromRepoRequest(
                repo_content=repo_content,
                entity_type=EntityType.METRIC,  # Используем METRIC для метрик
                metric_items=[item],
            )

            if progress_callback:
                progress_callback("Отправка запроса на генерацию SQL метрик...")

            response_data = await self._make_request_with_retry(
                "POST",
                "/api/GenerateSqlFromRepo",
                progress_callback=progress_callback,
                json=request_model.model_dump(),
            )

            if progress_callback:
                progress_callback("Парсинг результатов генерации...")

            result = response_data.get("result")
            return GenerateSqlFromRepoResponse(**(result or {}))

        except PydanticValidationError as e:
            raise APIError(f"Ошибка валидации данных запроса: {e}")
        except (json.JSONDecodeError, ValueError) as e:
            raise APIError(f"Невалидный JSON ответ от API: {e}")

    async def health_check(self) -> bool:
        """
        Проверяет доступность API.

        Returns:
            True если API доступно
        """
        try:
            await self._ensure_session()
            if self._session is None:
                return False
            # Простой запрос для проверки доступности
            async with self._session.get(
                urljoin(self.base_url, "/_info"), timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                return response.status < 400
        except Exception:
            return False


class ValidationResult:
    """Результат валидации репозитория."""

    def __init__(
        self,
        results: ValidationResults,
        *,
        success: bool,
        source_names: Optional[List[str]] = None,
        dimension_names: Optional[List[str]] = None,
        metric_names: Optional[List[str]] = None,
    ) -> None:
        """
        Инициализирует результат валидации.

        Args:
            results: Результаты валидации по компонентам
            success: Общий флаг успеха
            source_names: Имена источников (опционально)
            dimension_names: Имена дименшенов (опционально)
            metric_names: Имена метрик (опционально)
        """
        self.results = results
        self.success = success
        self.source_names = source_names or []
        self.dimension_names = dimension_names or []
        self.metric_names = metric_names or []

    def is_valid(self) -> bool:
        """Проверяет прошла ли валидация успешно."""
        return self.success and not self.has_errors()

    def has_errors(self) -> bool:
        """Проверяет есть ли ошибки валидации."""
        if not self.results:
            return not self.success

        # Проверяем фатальные ошибки
        if self.results.fatal_errors:
            return True

        # Проверяем ошибки в отдельных компонентах (не dict)
        if self.results.ab_schedules and (
            not self.results.ab_schedules.success or self.results.ab_schedules.errors
        ):
            return True
        if self.results.dimensions and (
            not self.results.dimensions.success or self.results.dimensions.errors
        ):
            return True
        if self.results.sources and (
            not self.results.sources.success or self.results.sources.errors
        ):
            return True

        # Проверяем dict компоненты
        if self.results.configs:
            for component_result in self.results.configs.values():
                if not component_result.success or component_result.errors:
                    return True
        if self.results.cubes_configs:
            for component_result in self.results.cubes_configs.values():
                if not component_result.success or component_result.errors:
                    return True
        if self.results.m42_reports:
            for component_result in self.results.m42_reports.values():
                if not component_result.success or component_result.errors:
                    return True
        if self.results.enrichments:
            for component_result in self.results.enrichments.values():
                if not component_result.success or component_result.errors:
                    return True

        return False

    def get_all_errors(self) -> List[ProcessedValidationError]:
        """
        Получает все ошибки валидации.

        Returns:
            Список типизированных ошибок валидации
        """
        all_errors = []

        if not self.results and not self.success:
            all_errors.append(
                ProcessedValidationError(
                    component="general",
                    message="Валидация не удалась",
                )
            )
            return all_errors

        # Добавляем фатальные ошибки
        fatal_errors = self.results.fatal_errors or []
        for error in fatal_errors:
            all_errors.append(
                ProcessedValidationError(
                    component="general", message=str(error), details={"error": error}
                )
            )

        # Добавляем ошибки отдельных компонентов (не dict)
        if self.results.ab_schedules:
            self._add_component_errors(
                all_errors=all_errors,
                component_name="ab_schedules",
                file_name="ab/schedules.yaml",
                component_result=self.results.ab_schedules,
            )
        if self.results.dimensions:
            self._add_component_errors(
                all_errors=all_errors,
                component_name="dimensions",
                component_result=self.results.dimensions,
                file_name="dimensions/dimensions.yaml",
            )
        if self.results.sources:
            self._add_component_errors(
                all_errors=all_errors,
                component_name="sources",
                component_result=self.results.sources,
                file_name="sources/sources.yaml",
            )

        # Добавляем ошибки dict компонентов
        if self.results.configs:
            for name, result in self.results.configs.items():
                self._add_component_errors(
                    all_errors=all_errors,
                    component_name="metrics",
                    component_result=result,
                    file_name=f"metrics/{name}.yaml",
                )
        if self.results.cubes_configs:
            for name, result in self.results.cubes_configs.items():
                self._add_component_errors(
                    all_errors=all_errors,
                    component_name="cubes_configs",
                    component_result=result,
                    file_name=f"m42/cubes_configs/{name}.yaml",
                )
        if self.results.m42_reports:
            for name, result in self.results.m42_reports.items():
                self._add_component_errors(
                    all_errors=all_errors,
                    component_name="m42_reports",
                    component_result=result,
                    file_name=f"m42/reports/{name}.yaml",
                )
        if self.results.enrichments:
            for name, result in self.results.enrichments.items():
                self._add_component_errors(
                    all_errors=all_errors,
                    component_name="enrichments",
                    component_result=result,
                    file_name=f"enrichments/{name}.yaml",
                )

        return all_errors

    def _add_component_errors(
        self,
        *,
        all_errors: List[ProcessedValidationError],
        component_name: str,
        file_name: str,
        component_result: ComponentValidationResult,
    ) -> None:
        """Добавляет ошибки одного компонента в общий список."""
        for i, error in enumerate(component_result.errors):
            # Получаем соответствующий error_mark если есть
            error_mark = (
                component_result.error_marks[i] if i < len(component_result.error_marks) else None
            )

            if isinstance(error, ValidationError):
                # Это ValidationError объект
                all_errors.append(
                    ProcessedValidationError(
                        component=component_name,
                        message=error.message,
                        file=getattr(error, "file", file_name),
                        line=error_mark.line if error_mark else None,
                        column=error_mark.column if error_mark else None,
                        details=getattr(error, "details", None),
                    )
                )
            else:
                # Это dict с динамическим YAML путем
                formatted_errors = format_validation_errors(error, component_name)
                for formatted_error in formatted_errors:
                    all_errors.append(
                        ProcessedValidationError(
                            component=component_name,
                            message=formatted_error,
                            file=file_name,
                            line=error_mark.line if error_mark else None,
                            column=error_mark.column if error_mark else None,
                            details=error,
                        )
                    )


class SQLGenerationResult:
    """Результат генерации SQL."""

    def __init__(self, api_response: GenerateSqlFromRepoResponse) -> None:
        """
        Инициализирует результат генерации SQL.

        Args:
            api_response: Типизированный ответ от API генерации SQL
        """
        self.response = api_response
        self.results = api_response.results
        self.error = api_response.error
        self.validation_results = api_response.validation_results

    def is_successful(self) -> bool:
        """Проверяет успешно ли сгенерирован SQL."""
        return self.error is None and bool(self.results)

    def get_sql(self) -> Optional[str]:
        """
        Получает сгенерированный SQL.

        Returns:
            SQL код или None если генерация не удалась
        """
        if not self.results:
            return None

        # Берем первый результат
        first_result = self.results[0]
        return first_result.sql

    def get_metadata(self) -> Optional[Dict[str, Any]]:
        """
        Получает метаданные генерации.

        Returns:
            Метаданные или None
        """
        if not self.results:
            return None

        first_result = self.results[0]
        return first_result.meta.model_dump()

    def has_validation_errors(self) -> bool:
        """Проверяет, содержит ли ответ ошибки валидации."""
        if self.error is None:
            return False
        try:
            return (
                self.error.code == ErrorCode.VALIDATION_ERROR
                and self.validation_results is not None
            )
        except Exception:
            return False

    def to_validation_result(self) -> Optional["ValidationResult"]:
        """Преобразует результаты валидации генерации в ValidationResult."""
        if not self.validation_results:
            return None
        return ValidationResult(self.validation_results, success=False)

    def get_validation_errors(self) -> List[ProcessedValidationError]:
        """Возвращает список обработанных ошибок валидации, если они есть."""
        validation_result = self.to_validation_result()
        if not validation_result:
            return []
        return validation_result.get_all_errors()

    def format_validation_errors_summary(self, max_items: int = 10) -> str:
        """Формирует краткое текстовое описание ошибок валидации для отображения в TUI."""
        errors = self.get_validation_errors()
        if not errors:
            return ""
        parts: List[str] = []
        total = len(errors)
        parts.append(f"Обнаружены ошибки валидации ({total}):")
        for idx, err in enumerate(errors[:max_items]):
            location_parts: List[str] = []
            if err.file:
                location_parts.append(err.file)
            if err.line is not None:
                location_parts.append(f"строка {err.line}")
            if err.column is not None:
                location_parts.append(f"колонка {err.column}")
            location = f" ({', '.join(location_parts)})" if location_parts else ""
            parts.append(f"{idx + 1}. {err.component}: {err.message}{location}")
        if total > max_items:
            parts.append(f"… и ещё {total - max_items}")
        return "\n".join(parts)
