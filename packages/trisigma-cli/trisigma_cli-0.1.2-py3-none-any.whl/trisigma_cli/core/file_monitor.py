"""Мониторинг изменений файловой системы для управления кешем."""

import logging
import threading
from pathlib import Path
from typing import Callable, List, Optional, Set

from watchdog.events import (
    FileSystemEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer

logger = logging.getLogger(__name__)


class FileSystemMonitor:
    """Менеджер мониторинга файловой системы с callback-интерфейсом."""

    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        """
        Инициализирует монитор файловой системы.

        Args:
            callback: Callback-функция, вызываемая при изменении файлов
        """
        self.callback = callback
        self.observer: Optional[Observer] = None
        self.monitored_paths: Set[Path] = set()
        self._lock = threading.Lock()
        self.is_monitoring = False

    def start_monitoring(self, paths: List[Path]) -> None:
        """
        Начинает мониторинг указанных путей.

        Args:
            paths: Список путей для мониторинга
        """
        with self._lock:
            if self.is_monitoring:
                self.stop_monitoring()

            if not paths:
                logger.debug("Список путей для мониторинга пуст")
                return

            try:
                self.observer = Observer()
                event_handler = _RepositoryEventHandler(self.callback)

                for path in paths:
                    if path.exists() and path.is_dir():
                        self.observer.schedule(event_handler, str(path), recursive=True)
                        self.monitored_paths.add(path)
                        logger.debug(f"Добавлен в мониторинг: {path}")

                if self.monitored_paths:
                    self.observer.start()
                    self.is_monitoring = True
                    logger.info(f"Мониторинг запущен для {len(self.monitored_paths)} путей")
                else:
                    logger.warning("Нет доступных путей для мониторинга")

            except Exception as e:
                logger.error(f"Ошибка запуска мониторинга: {e}")
                self.observer = None

    def stop_monitoring(self) -> None:
        """Останавливает мониторинг."""
        with self._lock:
            if self.observer is not None and self.is_monitoring:
                try:
                    self.observer.stop()
                    self.observer.join(timeout=5.0)
                    logger.info("Мониторинг остановлен")
                except Exception as e:
                    logger.error(f"Ошибка остановки мониторинга: {e}")
                finally:
                    self.observer = None
                    self.is_monitoring = False
                    self.monitored_paths.clear()

    def is_active(self) -> bool:
        """
        Проверяет активность мониторинга.

        Returns:
            True если мониторинг активен
        """
        return self.is_monitoring and self.observer is not None

    def get_monitored_paths(self) -> List[Path]:
        """
        Возвращает список отслеживаемых путей.

        Returns:
            Список отслеживаемых путей
        """
        with self._lock:
            return list(self.monitored_paths)

    def __del__(self) -> None:
        """Деструктор - останавливает мониторинг при удалении объекта."""
        self.stop_monitoring()


class _RepositoryEventHandler(FileSystemEventHandler):
    """Обработчик событий файловой системы для репозитория метрик."""

    # Расширения файлов, которые влияют на кеш
    CACHE_RELEVANT_EXTENSIONS = {".sql", ".yaml", ".yml"}

    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        """
        Инициализирует обработчик событий.

        Args:
            callback: Callback-функция для обработки изменений
        """
        super().__init__()
        self.callback = callback

    def on_any_event(self, event: FileSystemEvent) -> None:
        """
        Обрабатывает все события файловой системы.

        Args:
            event: Событие файловой системы
        """
        # Игнорируем события директорий
        if event.is_directory:
            return

        # Проверяем расширение файла
        try:
            file_path = Path(event.src_path)
        except (OSError, ValueError) as e:
            logger.debug(f"Невозможно создать Path из {event.src_path}: {e}")
            return

        if file_path.suffix.lower() not in self.CACHE_RELEVANT_EXTENSIONS:
            return

        # Игнорируем временные файлы и файлы IDE
        if self._should_ignore_file(file_path):
            return

        logger.debug(f"Обнаружено изменение файла: {file_path} ({event.event_type})")

        if self.callback:
            try:
                self.callback(str(file_path))
            except Exception as e:
                logger.error(f"Ошибка в callback при обработке {file_path}: {e}")

    def _should_ignore_file(self, file_path: Path) -> bool:
        """
        Проверяет, нужно ли игнорировать файл.

        Args:
            file_path: Путь к файлу

        Returns:
            True если файл следует игнорировать
        """
        name = file_path.name

        # Временные файлы
        if name.startswith(".") or name.startswith("~") or name.endswith(".tmp"):
            return True

        # Файлы IDE и редакторов
        if any(pattern in name for pattern in ["__pycache__", ".pyc", ".swp", ".swo"]):
            return True

        return False
