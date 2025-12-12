"""Система логирования для Trisigma CLI."""

import logging
import sys
from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.logging import RichHandler

from .exceptions import TrisigmaError


class TrisigmaLogger:
    """Настройщик логирования для Trisigma CLI."""

    def __init__(self) -> None:
        self.console = Console(file=sys.stderr)
        self._setup_done = False

    def setup_logging(self, level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
        """
        Настраивает систему логирования.

        Args:
            level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
            log_file: Путь к файлу логов (опционально)

        Returns:
            Настроенный logger
        """
        if self._setup_done:
            return logging.getLogger("trisigma")

        # Создаем основной logger
        logger = logging.getLogger("trisigma")
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        # Очищаем существующие handlers
        logger.handlers.clear()

        # Настраиваем форматтер
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="[%X]"
        )

        # Handler для консоли (Rich)
        rich_handler = RichHandler(
            console=self.console,
            show_time=True,
            show_level=True,
            show_path=False,
            markup=True,
            rich_tracebacks=True,
            tracebacks_show_locals=False,
        )
        rich_handler.setLevel(logging.WARNING)  # В консоль только важные сообщения
        logger.addHandler(rich_handler)

        # Handler для файла (если указан)
        if log_file:
            self._setup_file_logging(logger, log_file, formatter, level)

        # Настраиваем логирование для внешних библиотек
        self._setup_external_loggers()

        self._setup_done = True
        return logger

    def _setup_file_logging(
        self, logger: logging.Logger, log_file: str, formatter: logging.Formatter, level: str
    ) -> None:
        """Настраивает логирование в файл."""
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        except Exception as e:
            # Если не удалось настроить файловое логирование, продолжаем без него
            logger.warning(f"Не удалось настроить логирование в файл {log_file}: {e}")

    def _setup_external_loggers(self) -> None:
        """Настраивает логирование для внешних библиотек."""
        # Приглушаем логирование requests
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        # Приглушаем Git логирование
        logging.getLogger("git").setLevel(logging.WARNING)

        # Приглушаем Textual логирование
        logging.getLogger("textual").setLevel(logging.WARNING)


def get_logger(name: str = "trisigma") -> logging.Logger:
    """
    Получает logger для модуля.

    Args:
        name: Имя logger'а

    Returns:
        Logger объект
    """
    return logging.getLogger(name)


def log_exception(logger: logging.Logger, exception: Exception, context: str = "") -> None:
    """
    Логирует исключение с контекстом.

    Args:
        logger: Logger объект
        exception: Исключение для логирования
        context: Контекст, в котором произошло исключение
    """
    if isinstance(exception, TrisigmaError):
        # Для наших исключений используем уровень ERROR
        logger.error(f"{context}: {exception}", exc_info=False)
    else:
        # Для системных исключений используем уровень CRITICAL с traceback
        logger.critical(f"{context}: {exception}", exc_info=True)


def log_operation_start(logger: logging.Logger, operation: str, **kwargs: Any) -> None:
    """
    Логирует начало операции.

    Args:
        logger: Logger объект
        operation: Описание операции
        **kwargs: Дополнительные параметры операции
    """
    if kwargs:
        params_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        logger.info(f"Начало операции: {operation} ({params_str})")
    else:
        logger.info(f"Начало операции: {operation}")


def log_operation_end(
    logger: logging.Logger, operation: str, success: bool = True, **kwargs: Any
) -> None:
    """
    Логирует завершение операции.

    Args:
        logger: Logger объект
        operation: Описание операции
        success: Успешно ли завершена операция
        **kwargs: Дополнительные результаты операции
    """
    status = "успешно" if success else "с ошибкой"

    if kwargs:
        params_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        logger.info(f"Завершение операции: {operation} - {status} ({params_str})")
    else:
        logger.info(f"Завершение операции: {operation} - {status}")


class ContextualLogger:
    """Logger с контекстом для удобного использования в операциях."""

    def __init__(self, operation: str, logger: Optional[logging.Logger] = None) -> None:
        self.operation = operation
        self.logger = logger or get_logger()
        self._started = False

    def __enter__(self) -> "ContextualLogger":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type is None:
            self.success()
        else:
            self.error(exc_val)

    def start(self, **kwargs: Any) -> None:
        """Логирует начало операции."""
        if not self._started:
            log_operation_start(self.logger, self.operation, **kwargs)
            self._started = True

    def success(self, **kwargs: Any) -> None:
        """Логирует успешное завершение операции."""
        log_operation_end(self.logger, self.operation, success=True, **kwargs)

    def error(self, exception: Exception, **kwargs: Any) -> None:
        """Логирует завершение операции с ошибкой."""
        log_exception(self.logger, exception, f"Операция: {self.operation}")
        log_operation_end(self.logger, self.operation, success=False, **kwargs)

    def info(self, message: str) -> None:
        """Логирует информационное сообщение в контексте операции."""
        self.logger.info(f"[{self.operation}] {message}")

    def warning(self, message: str) -> None:
        """Логирует предупреждение в контексте операции."""
        self.logger.warning(f"[{self.operation}] {message}")

    def debug(self, message: str) -> None:
        """Логирует отладочное сообщение в контексте операции."""
        self.logger.debug(f"[{self.operation}] {message}")


# Глобальный экземпляр настройщика логирования
_logger_setup = TrisigmaLogger()


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Настраивает глобальное логирование."""
    return _logger_setup.setup_logging(level, log_file)
