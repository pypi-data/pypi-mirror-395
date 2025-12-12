from typing import Any, Optional

import aiohttp


def is_server_error(exception: BaseException) -> bool:
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


def is_auth_error(error_message: str, status_code: Optional[int] = None) -> bool:
    """
    Проверяет, является ли ошибка ошибкой аутентификации.

    Проверяет HTTP статус коды 401/403 или наличие паттернов ошибок аутентификации
    в тексте сообщения об ошибке.

    Args:
        error_message: Текст сообщения об ошибке
        status_code: HTTP статус код (опционально)

    Returns:
        True если это ошибка аутентификации
    """
    if status_code is not None and status_code in (401, 403):
        return True

    auth_error_patterns = [
        "Valid Bearer token required in Authorization header",
        "Valid Bearer token required",
        "Token is invalid",
        "Token expired",
        "Invalid token",
        "Refresh token is invalid or expired",
    ]
    return any(pattern in error_message for pattern in auth_error_patterns)


def extract_error_message(error_data: Any) -> str:
    """
    Извлекает сообщение об ошибке из различных форматов ответа API.

    Поддерживает форматы:
    - {"message": "текст ошибки"}
    - {"dto": [{"msg": "текст ошибки"}]}
    - Другие словари и примитивные типы

    Args:
        error_data: Данные ошибки из JSON ответа API

    Returns:
        Сообщение об ошибке
    """
    if isinstance(error_data, dict):
        if "message" in error_data:
            return str(error_data["message"])
        elif "dto" in error_data and isinstance(error_data["dto"], list):
            dto_errors = error_data["dto"]
            if dto_errors and isinstance(dto_errors[0], dict) and "msg" in dto_errors[0]:
                return f"Ошибка: {dto_errors[0]['msg']}"
            else:
                error_msg = error_data.get("message", "Неизвестная ошибка валидации")
                return f"Ошибка API: {error_msg}"
        else:
            return str(error_data)
    return str(error_data)
