from typing import Optional

"""Кастомные исключения для Trisigma CLI."""


class TrisigmaError(Exception):
    """Базовое исключение для Trisigma CLI."""

    pass


class ConfigurationError(TrisigmaError):
    """Ошибка в конфигурации CLI."""

    pass


class RepositoryError(TrisigmaError):
    """Ошибка при работе с репозиторием метрик."""

    pass


class InvalidRepositoryError(RepositoryError):
    """Репозиторий не является валидным репозиторием метрик."""

    pass


class APIError(TrisigmaError):
    """Ошибка при работе с API."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[dict] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(APIError):
    """Ошибка аутентификации - токен недействителен или истек."""

    def __init__(
        self,
        message: str = "Токен недействителен или истек. Выполните 'trisigma login' для повторной авторизации.",
        status_code: Optional[int] = None,
        response_data: Optional[dict] = None,
    ):
        super().__init__(message, status_code, response_data)


class GitError(TrisigmaError):
    """Ошибка при работе с Git."""

    pass


class ValidationError(TrisigmaError):
    """Ошибка валидации."""

    def __init__(self, message: str, errors: Optional[list] = None):
        super().__init__(message)
        self.errors = errors or []
