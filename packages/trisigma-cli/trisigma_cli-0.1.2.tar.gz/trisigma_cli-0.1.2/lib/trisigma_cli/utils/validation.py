"""Утилиты для валидации."""

import asyncio
import random
import re
from pathlib import Path
from typing import Any, List, Union

from .exceptions import ValidationError


def validate_task_number(
    task: str,
    required: bool = True,
    pattern: Union[str, None] = None,
    example: str = "PROJECT-123"
) -> str:
    """
    Валидирует номер задачи.

    Args:
        task: Номер задачи для проверки
        required: Обязательно ли указание task ID (default: True)
        pattern: Regex паттерн для валидации (default: "^[A-Z]+-\d+$")
        example: Пример формата для сообщения об ошибке (default: "PROJECT-123")

    Returns:
        Валидный номер задачи (или пустая строка если not required)

    Raises:
        ValidationError: Если номер задачи невалиден
    """
    # Если task ID не обязателен и не указан - возвращаем пустую строку
    if not required and not task:
        return ""

    # Если task ID обязателен и не указан - ошибка
    if required and not task:
        raise ValidationError(
            f"Номер задачи обязателен. Ожидается формат {example}"
        )

    # Используем переданный паттерн или дефолтный
    validation_pattern = pattern if pattern else r"^[A-Z]+-\d+$"

    # Валидируем формат
    if not re.match(validation_pattern, task):
        raise ValidationError(
            f"Невалидный номер задачи '{task}'. Ожидается формат {example}"
        )

    return task


def validate_branch_name(branch: str) -> str:
    """
    Валидирует имя ветки.

    Args:
        branch: Имя ветки для проверки

    Returns:
        Валидное имя ветки

    Raises:
        ValidationError: Если имя ветки невалидно
    """
    if not branch:
        raise ValidationError("Имя ветки не может быть пустым")

    # Проверяем что имя ветки содержит только допустимые символы
    if not re.match(r"^[a-zA-Z0-9_-]+$", branch):
        raise ValidationError(
            f"Невалидное имя ветки '{branch}'. "
            f"Разрешены только буквы, цифры, дефис и подчеркивание"
        )

    return branch


def validate_path_exists(path: str) -> Path:
    """
    Проверяет существование пути.

    Args:
        path: Путь для проверки

    Returns:
        Path объект

    Raises:
        ValidationError: Если путь не существует
    """
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        raise ValidationError(f"Путь не существует: {path}")
    return path_obj


def validate_directory(path: str) -> Path:
    """
    Проверяет что путь является директорией.

    Args:
        path: Путь для проверки

    Returns:
        Path объект директории

    Raises:
        ValidationError: Если путь не является директорией
    """
    path_obj = validate_path_exists(path)
    if not path_obj.is_dir():
        raise ValidationError(f"Путь не является директорией: {path}")
    return path_obj


def validate_file(path: str) -> Path:
    """
    Проверяет что путь является файлом.

    Args:
        path: Путь для проверки

    Returns:
        Path объект файла

    Raises:
        ValidationError: Если путь не является файлом
    """
    path_obj = validate_path_exists(path)
    if not path_obj.is_file():
        raise ValidationError(f"Путь не является файлом: {path}")
    return path_obj


def validate_url(url: str) -> str:
    """
    Валидирует URL.

    Args:
        url: URL для проверки

    Returns:
        Валидный URL

    Raises:
        ValidationError: Если URL невалиден
    """
    if not url:
        raise ValidationError("URL не может быть пустым")

    # Простая проверка URL
    if not re.match(r"^https?://.+", url):
        raise ValidationError(
            f"Невалидный URL '{url}'. URL должен начинаться с http:// или https://"
        )

    return url.rstrip("/")


def validate_api_token(token: str) -> str:
    """
    Валидирует API токен.

    Args:
        token: Токен для проверки

    Returns:
        Валидный токен

    Raises:
        ValidationError: Если токен невалиден
    """
    if not token or not token.strip():
        raise ValidationError("API токен не может быть пустым")

    token = token.strip()
    if len(token) < 10:
        raise ValidationError("API токен слишком короткий")

    return token


def sanitize_commit_message(message: str) -> str:
    """
    Очищает сообщение коммита от потенциально опасных символов.

    Args:
        message: Сообщение коммита

    Returns:
        Очищенное сообщение
    """
    if not message or not message.strip():
        return "Автоматический коммит"

    # Удаляем переводы строк и опасные символы
    clean_message = re.sub(r"[\n\r\t]+", " ", message.strip())
    clean_message = re.sub(r"[`$\\;|&]+", "", clean_message)

    # Ограничиваем длину
    if len(clean_message) > 200:
        clean_message = clean_message[:197] + "..."

    return clean_message


def format_validation_errors(
    errors: Union[ValidationError, dict, list, Any], path: str = ""
) -> List[str]:
    """
    Преобразует ошибки любой структуры в читаемые строки с путями.

    Поддерживает:
    - ValidationError объекты
    - Словари с динамическими путями YAML
    - Списки ошибок любой вложенности
    - Любые другие типы данных

    Args:
        errors: Ошибки для форматирования
        path: Текущий путь в структуре данных (разделенный стрелками ->)

    Returns:
        Список форматированных строк с полными путями до ошибок
    """
    result = []

    if isinstance(errors, ValidationError):
        # Обработка стандартных ValidationError объектов
        error_path = f"{path} -> " if path else ""
        if hasattr(errors, "file"):
            message = getattr(errors, "message", str(errors))
            result.append(f"{error_path}{errors.file} - {message}")
        else:
            result.append(f"{error_path}{str(errors)}")

    elif isinstance(errors, dict):
        # Обработка словарей с динамическими путями
        if not errors:
            return result

        for key, value in errors.items():
            new_path = f"{path} -> {key}" if path else key
            result.extend(format_validation_errors(value, new_path))

    elif isinstance(errors, list):
        # Обработка списков
        if not errors:
            return result

        for i, item in enumerate(errors):
            # Для списков не добавляем индекс в путь, просто продолжаем с текущим путем
            result.extend(format_validation_errors(item, path))

    else:
        # Обработка любых других типов (строки, числа и т.д.)
        error_path = f"{path} -> " if path else ""
        result.append(f"{error_path}{str(errors)}")

    return result


async def validate_repository_with_progress(
    repo: Any, progress_callback: Any, config: Any = None, api_prefix: str = ""
) -> Any:
    """
    Асинхронно валидирует репозиторий с использованием API и realtime сообщениями.

    Args:
        repo: Репозиторий метрик (MetricsRepository)
        progress_callback: Callback для обновления прогресса (может быть async или sync)
        config: Конфигурация (по умолчанию берется из core.config)
        api_prefix: Префикс для API сообщений (например "API: ")

    Returns:
        ValidationResult: Результат валидации
    """
    import inspect

    from ..core.api_client import TrisigmaAPIClient, ValidationResult
    from ..core.config import config as default_config

    # Используем переданную конфигурацию или дефолтную
    cfg = config if config is not None else default_config

    # Определяем, является ли callback асинхронным
    is_async_callback = inspect.iscoroutinefunction(progress_callback)

    async def safe_progress_call(message: str) -> None:
        """Безопасный вызов progress callback (async или sync)."""
        try:
            if is_async_callback:
                await progress_callback(message)
            else:
                progress_callback(message)
        except Exception:
            # Игнорируем ошибки в progress callback
            pass

    # Сообщения для имитации активности
    activity_messages = [
        "🔍 Анализируем структуру проекта...",
        "🔄 Собираем данные из репозитория...",
        "📊 Проверяем конфигурации метрик...",
        "🔗 Анализируем связи между компонентами...",
        "⚡ Проверяем синтаксис конфигураций...",
        "🎯 Проверяем целостность дименшенов...",
        "🔧 Анализируем правила обогащения...",
        "📈 Валидируем источники данных...",
        "📋 Сканируем SQL запросы...",
        "📦 Анализируем зависимости...",
        "🔄 Финализируем результаты валидации...",
    ]

    current_message_idx = 0
    activity_task = None
    validation_completed = False
    api_active = False
    last_api_time = 0

    async def cycle_activity_messages() -> None:
        """Циклически показывает сообщения активности."""
        nonlocal current_message_idx
        while not validation_completed:
            current_time = asyncio.get_event_loop().time()

            # Показываем activity сообщения всегда, но с разной частотой
            if not api_active or (current_time - last_api_time > 3.0):
                # Показываем сообщение активности БЕЗ префикса
                await safe_progress_call(activity_messages[current_message_idx])
                current_message_idx = (current_message_idx + random.randint(1, 3)) % len(
                    activity_messages
                )

            await asyncio.sleep(2.0)  # Меняем сообщение каждые 2 секунды

    def api_progress_callback(message: str) -> None:
        """Callback для API сообщений (синхронный)."""
        nonlocal api_active, last_api_time
        api_active = True
        last_api_time = int(asyncio.get_event_loop().time())

        # Синхронно вызываем callback для API сообщений
        full_message = f"{api_prefix}{message}"
        try:
            if is_async_callback:
                # Создаем задачу для async callback, но не ждем её
                loop = asyncio.get_event_loop()
                loop.create_task(progress_callback(full_message))
            else:
                progress_callback(full_message)
        except Exception:
            # Игнорируем ошибки в callback
            pass

    try:
        # Запускаем циклические сообщения в фоне
        activity_task = asyncio.create_task(cycle_activity_messages())

        repo_content = repo.get_repository_content()

        async with TrisigmaAPIClient(str(cfg.api_url), str(cfg.access_token)) as api_client:
            api_response = await api_client.validate_repository(
                repo_content, progress_callback=api_progress_callback
            )

        validation_result = ValidationResult(
            api_response.results,
            success=api_response.success,
            source_names=api_response.source_names,
            dimension_names=api_response.dimension_names,
            metric_names=api_response.metric_names,
        )

        repo._cache_validation_result(validation_result)

        return validation_result

    finally:
        # Останавливаем циклические сообщения
        validation_completed = True
        if activity_task and not activity_task.done():
            activity_task.cancel()
            try:
                await activity_task
            except asyncio.CancelledError:
                pass
