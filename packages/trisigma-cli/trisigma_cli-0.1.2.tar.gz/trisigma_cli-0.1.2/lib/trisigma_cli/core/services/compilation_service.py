"""Сервис для компиляции SQL источников и метрик."""

import asyncio
from typing import Callable, List, Optional

from ..api_client import SQLGenerationResult, TrisigmaAPIClient
from ..config import config
from ..constants import (
    ACTIVITY_MESSAGES_METRICS,
    ACTIVITY_MESSAGES_METRICS_EMOJI,
    ACTIVITY_MESSAGES_SOURCE,
    ACTIVITY_MESSAGES_SOURCE_EMOJI,
)
from ..dto import RepoContentDict


class CompilationService:
    """Сервис для компиляции SQL с поддержкой источников и метрик."""

    api_url: str
    access_token: str

    def __init__(
        self, api_url: Optional[str] = None, access_token: Optional[str] = None
    ):
        """
        Инициализирует сервис компиляции.

        Args:
            api_url: URL API (если не указан, берётся из config)
            access_token: Access token (если не указан, берётся из config)

        Raises:
            ValueError: Если API URL или access token не указаны
        """
        final_api_url = api_url if api_url is not None else config.api_url
        final_access_token = access_token if access_token is not None else config.access_token

        if not final_api_url or not final_access_token:
            raise ValueError("API URL и access token обязательны для CompilationService")

        self.api_url = final_api_url
        self.access_token = final_access_token

    async def compile_source(
        self,
        repo_content: RepoContentDict,
        source_name: str,
        dimensions: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
        first_date: Optional[str] = None,
        last_date: Optional[str] = None,
        granularity: str = "day",
        progress_callback: Optional[Callable[[str], None]] = None,
        use_emoji: bool = False,
    ) -> SQLGenerationResult:
        """
        Компилирует SQL для источника.

        Args:
            repo_content: Содержимое репозитория
            source_name: Название источника
            dimensions: Список дименшенов
            columns: Список колонок
            first_date: Начальная дата
            last_date: Конечная дата
            granularity: Гранулярность
            progress_callback: Callback для обновления прогресса
            use_emoji: Использовать эмодзи в сообщениях активности

        Returns:
            Результат компиляции
        """
        activity_messages = (
            ACTIVITY_MESSAGES_SOURCE_EMOJI if use_emoji else ACTIVITY_MESSAGES_SOURCE
        )

        return await self._compile(
            repo_content=repo_content,
            activity_messages=activity_messages,
            progress_callback=progress_callback,
            is_metrics=False,
            source_name=source_name,
            dimensions=dimensions,
            columns=columns,
            first_date=first_date,
            last_date=last_date,
            granularity=granularity,
        )

    async def compile_metrics(
        self,
        repo_content: RepoContentDict,
        metric_names: List[str],
        dimensions: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
        first_date: Optional[str] = None,
        last_date: Optional[str] = None,
        granularity: str = "day",
        progress_callback: Optional[Callable[[str], None]] = None,
        use_emoji: bool = False,
    ) -> SQLGenerationResult:
        """
        Компилирует SQL для метрик.

        Args:
            repo_content: Содержимое репозитория
            metric_names: Список имен метрик
            dimensions: Список дименшенов
            columns: Список колонок
            first_date: Начальная дата
            last_date: Конечная дата
            granularity: Гранулярность
            progress_callback: Callback для обновления прогресса
            use_emoji: Использовать эмодзи в сообщениях активности

        Returns:
            Результат компиляции
        """
        activity_messages = (
            ACTIVITY_MESSAGES_METRICS_EMOJI if use_emoji else ACTIVITY_MESSAGES_METRICS
        )

        return await self._compile(
            repo_content=repo_content,
            activity_messages=activity_messages,
            progress_callback=progress_callback,
            is_metrics=True,
            metric_names=metric_names,
            dimensions=dimensions,
            columns=columns,
            first_date=first_date,
            last_date=last_date,
            granularity=granularity,
        )

    async def _compile(
        self,
        repo_content: RepoContentDict,
        activity_messages: List[str],
        progress_callback: Optional[Callable[[str], None]],
        is_metrics: bool,
        source_name: Optional[str] = None,
        metric_names: Optional[List[str]] = None,
        dimensions: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
        first_date: Optional[str] = None,
        last_date: Optional[str] = None,
        granularity: str = "day",
    ) -> SQLGenerationResult:
        """
        Внутренний метод компиляции с циклическими сообщениями активности.

        Args:
            repo_content: Содержимое репозитория
            activity_messages: Список сообщений активности
            progress_callback: Callback для обновления прогресса
            is_metrics: Режим компиляции метрик
            source_name: Название источника
            metric_names: Список метрик
            dimensions: Список дименшенов
            columns: Список колонок
            first_date: Начальная дата
            last_date: Конечная дата
            granularity: Гранулярность

        Returns:
            Результат компиляции
        """
        current_message_idx = 0
        activity_task: Optional[asyncio.Task] = None
        compilation_completed = False

        async def cycle_activity_messages() -> None:
            """Циклически показывает сообщения активности компиляции."""
            nonlocal current_message_idx
            while not compilation_completed:
                if progress_callback:
                    progress_callback(activity_messages[current_message_idx])
                current_message_idx = (current_message_idx + 1) % len(activity_messages)
                await asyncio.sleep(1.2)

        # Прогресс callback для API сообщений (имеет приоритет)
        def api_progress_callback(message: str) -> None:
            if progress_callback:
                progress_callback(f"API: {message}")

        try:
            # Запускаем циклические сообщения в фоне
            if progress_callback:
                activity_task = asyncio.create_task(cycle_activity_messages())

            async with TrisigmaAPIClient(self.api_url, self.access_token) as api_client:
                if is_metrics:
                    api_response = await api_client.generate_metric_sql(
                        repo_content=repo_content,
                        metric_names=metric_names or [],
                        dimensions=dimensions,
                        columns=columns,
                        first_date=first_date,
                        last_date=last_date,
                        granularity=granularity,
                        progress_callback=api_progress_callback,
                    )
                else:
                    api_response = await api_client.generate_sql(
                        repo_content=repo_content,
                        source_name=source_name or "",
                        dimensions=dimensions,
                        columns=columns,
                        first_date=first_date,
                        last_date=last_date,
                        granularity=granularity,
                        progress_callback=api_progress_callback,
                    )

            return SQLGenerationResult(api_response)

        finally:
            # Останавливаем циклические сообщения
            compilation_completed = True
            if activity_task and not activity_task.done():
                activity_task.cancel()
                try:
                    await activity_task
                except asyncio.CancelledError:
                    pass


class ParameterValidator:
    """Валидатор параметров компиляции."""

    @staticmethod
    def validate_and_parse_dimensions(dimensions: Optional[str]) -> Optional[List[str]]:
        """
        Валидирует и парсит строку дименшенов.

        Args:
            dimensions: Строка дименшенов через запятую

        Returns:
            Список дименшенов или None

        Raises:
            ValueError: При невалидных дименшенах
        """
        import re

        if not dimensions:
            return None

        dimensions_list = [d.strip() for d in dimensions.split(",") if d.strip()]

        if not dimensions_list:
            return None

        for dim in dimensions_list:
            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", dim):
                raise ValueError(
                    f"Невалидное имя дименшена: '{dim}'. "
                    f"Дименшены должны содержать только буквы, цифры и подчеркивания"
                )

        return dimensions_list

    @staticmethod
    def validate_and_parse_columns(columns: Optional[str]) -> Optional[List[str]]:
        """
        Валидирует и парсит строку колонок.

        Args:
            columns: Строка колонок через запятую

        Returns:
            Список колонок или None

        Raises:
            ValueError: При невалидных колонках
        """
        import re

        if not columns:
            return None

        columns_list = [c.strip() for c in columns.split(",") if c.strip()]

        if not columns_list:
            return None

        for col in columns_list:
            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", col):
                raise ValueError(
                    f"Невалидное имя колонки: '{col}'. "
                    f"Колонки должны содержать только буквы, цифры и подчеркивания"
                )

        return columns_list

    @staticmethod
    def validate_and_parse_metrics(metrics: Optional[str]) -> Optional[List[str]]:
        """
        Валидирует и парсит строку метрик.

        Args:
            metrics: Строка метрик через запятую

        Returns:
            Список метрик или None

        Raises:
            ValueError: При невалидных метриках
        """
        import re

        if not metrics:
            return None

        metrics_list = [m.strip() for m in metrics.split(",") if m.strip()]

        if not metrics_list:
            return None

        for metric in metrics_list:
            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", metric):
                raise ValueError(
                    f"Невалидное имя метрики: '{metric}'. "
                    f"Метрики должны содержать только буквы, цифры и подчеркивания"
                )

        return metrics_list

    @staticmethod
    def validate_dates(first_date: Optional[str], last_date: Optional[str]) -> None:
        """
        Валидирует даты.

        Args:
            first_date: Начальная дата
            last_date: Конечная дата

        Raises:
            ValueError: При невалидных датах
        """
        import re
        from datetime import datetime

        date_pattern = r"^\d{4}-\d{2}-\d{2}$"

        if first_date and not re.match(date_pattern, first_date):
            raise ValueError(
                f"Невалидная начальная дата: '{first_date}'. Используйте формат YYYY-MM-DD"
            )

        if last_date and not re.match(date_pattern, last_date):
            raise ValueError(
                f"Невалидная конечная дата: '{last_date}'. Используйте формат YYYY-MM-DD"
            )

        # Проверяем что начальная дата не больше конечной
        if first_date and last_date:
            try:
                start = datetime.strptime(first_date, "%Y-%m-%d")
                end = datetime.strptime(last_date, "%Y-%m-%d")

                if start > end:
                    raise ValueError("Начальная дата не может быть больше конечной")

            except ValueError as e:
                if "does not match format" in str(e):
                    raise ValueError(f"Ошибка в формате дат: {e}")
                raise

    @staticmethod
    def validate_granularity(granularity: str) -> None:
        """
        Валидирует гранулярность.

        Args:
            granularity: Гранулярность

        Raises:
            ValueError: При невалидной гранулярности
        """
        valid_granularities = ["day", "week", "month"]

        if granularity.lower() not in valid_granularities:
            raise ValueError(
                f"Невалидная гранулярность: '{granularity}'. "
                f"Поддерживаются: {', '.join(valid_granularities)}"
            )
