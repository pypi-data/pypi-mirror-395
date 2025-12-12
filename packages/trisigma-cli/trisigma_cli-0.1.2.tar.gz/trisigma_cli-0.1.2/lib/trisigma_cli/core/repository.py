"""Работа с репозиторием метрик."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from ..utils.exceptions import InvalidRepositoryError, RepositoryError
from .api_client import TrisigmaAPIClient, ValidationResult
from .config import config
from .dto import RepoContentDict
from .file_monitor import FileSystemMonitor

# Import GitWorkflow with fallback for CI environments
try:
    from .git_wrapper import GitWorkflow

    GIT_WRAPPER_AVAILABLE = True
except (ImportError, OSError):
    # Git is not available (e.g., in CI environment without git executable)
    GIT_WRAPPER_AVAILABLE = False
    GitWorkflow = None  # type: ignore


class MetricsRepository:
    """Менеджер репозитория метрик (тонкий клиент для API)."""

    # Конфигурация структуры репозитория из validate.py
    # Формат: (имя_поля, путь_к_файлу/директории, является_ли_директорией, опциональный)
    # Опциональные компоненты не блокируют валидацию и возвращают пустой контент если отсутствуют
    CONFIGS = [
        ("sources", "sources/sources.yaml", False, False),
        ("sources_sql", "sources/sql", True, False),
        ("dimensions", "dimensions/dimensions.yaml", False, False),
        ("dimensions_sql", "dimensions/sql", True, False),
        ("enrichments", "enrichments", True, True),  # Опциональная папка
        ("configs", "metrics", True, False),
        ("cubes_configs", "m42/cubes_configs", True, True),  # Опциональная папка
        ("m42_reports", "m42/reports", True, True),  # Опциональная папка
        ("ab_schedules", "ab/schedules.yaml", False, False),
    ]

    def __init__(
        self,
        repo_path: str,
        api_client: Optional[TrisigmaAPIClient] = None,
        require_api: bool = True,
    ):
        """
        Инициализирует репозиторий метрик.

        Args:
            repo_path: Путь к корню репозитория
            api_client: Клиент API (если не указан - создается автоматически)
            require_api: Требовать ли настроенное API для инициализации

        Raises:
            RepositoryError: Если путь невалиден
        """
        # Инициализируем базовые атрибуты в начале для безопасности
        self._file_monitor: Optional[FileSystemMonitor] = None
        self._monitoring_enabled = False
        self._cached_validation_result: Optional[ValidationResult] = None
        self._cached_branch: Optional[str] = None
        self._logger = logging.getLogger(__name__)

        self.repo_path = Path(repo_path).resolve()
        if not self.repo_path.exists():
            raise RepositoryError(f"Путь не существует: {repo_path}")
        if not self.repo_path.is_dir():
            raise RepositoryError(f"Путь не является директорией: {repo_path}")

        # Инициализируем Git wrapper
        self.git: Optional[GitWorkflow] = None
        if GIT_WRAPPER_AVAILABLE:
            try:
                self.git = GitWorkflow(str(self.repo_path))
            except Exception:
                self.git = None  # Не критично если нет Git

        # Инициализируем API клиент
        self.api_client: Optional[TrisigmaAPIClient] = None
        if api_client is not None:
            self.api_client = api_client
        elif require_api:
            if not config.is_configured():
                raise RepositoryError("API не настроено. Выполните 'trisigma init' для настройки.")

            if not config.api_url or not config.access_token:
                raise RepositoryError(
                    "API URL или токен не настроены. Выполните 'trisigma init' для настройки."
                )

            self.api_client = TrisigmaAPIClient(
                base_url=config.api_url, api_token=config.access_token
            )

    def is_valid_repository(self) -> bool:
        """
        Проверяет является ли директория валидным репозиторием метрик.

        Returns:
            True если репозиторий валиден
        """
        try:
            self.validate_structure()
            return True
        except InvalidRepositoryError:
            return False

    def validate_structure(self) -> None:
        """
        Валидирует структуру репозитория метрик.

        Raises:
            InvalidRepositoryError: Если структура репозитория невалидна
        """
        missing_components = []

        for field_name, relative_path, is_directory, is_optional in self.CONFIGS:
            full_path = self.repo_path / relative_path

            if not full_path.exists():
                # Пропускаем опциональные компоненты
                if not is_optional:
                    missing_components.append(relative_path)
                continue

            if is_directory and not full_path.is_dir():
                missing_components.append(f"{relative_path} (должна быть директорией)")
            elif not is_directory and not full_path.is_file():
                missing_components.append(f"{relative_path} (должен быть файлом)")

        if missing_components:
            raise InvalidRepositoryError(
                f"Директория не является валидным репозиторием метрик. "
                f"Отсутствуют компоненты: {', '.join(missing_components)}"
            )

    def get_repository_content(self) -> RepoContentDict:
        """
        Собирает содержимое репозитория для отправки в API.

        Returns:
            Типизированная модель с содержимым репозитория в формате для API

        Raises:
            RepositoryError: Если не удалось прочитать файлы
        """
        self.validate_structure()

        # Собираем данные для всех компонентов
        content_data: Dict[str, Union[Dict[str, Tuple[str, bool]], Tuple[str, bool]]] = {}

        for field_name, relative_path, is_directory, is_optional in self.CONFIGS:
            full_path = self.repo_path / relative_path

            # Для отсутствующих опциональных компонентов возвращаем пустой контент
            if not full_path.exists() and is_optional:
                if is_directory:
                    content_data[field_name] = {}
                else:
                    content_data[field_name] = ("", False)
                continue

            if is_directory:
                # Для директорий возвращаем Dict[str, Tuple[str, bool]]
                content_data[field_name] = self._read_directory_content(full_path, relative_path)
            else:
                # Для одиночных файлов возвращаем Tuple[str, bool] напрямую
                content_data[field_name] = self._read_file_content(full_path, relative_path)

        # Создаем типизированную модель
        return RepoContentDict(
            sources=cast(Tuple[str, bool], content_data.get("sources", ("", False))),
            sources_sql=cast(Dict[str, Tuple[str, bool]], content_data.get("sources_sql", {})),
            dimensions=cast(Tuple[str, bool], content_data.get("dimensions", ("", False))),
            dimensions_sql=cast(
                Dict[str, Tuple[str, bool]], content_data.get("dimensions_sql", {})
            ),
            enrichments=cast(Dict[str, Tuple[str, bool]], content_data.get("enrichments", {})),
            configs=cast(Dict[str, Tuple[str, bool]], content_data.get("configs", {})),
            cubes_configs=cast(Dict[str, Tuple[str, bool]], content_data.get("cubes_configs", {})),
            m42_reports=cast(Dict[str, Tuple[str, bool]], content_data.get("m42_reports", {})),
            ab_schedules=cast(Tuple[str, bool], content_data.get("ab_schedules", ("", False))),
        )

    def read_file_safe(self, file_path: Union[str, Path]) -> Optional[str]:
        """
        Безопасно читает содержимое файла.

        Args:
            file_path: Путь к файлу (абсолютный или относительный от корня репозитория)

        Returns:
            Содержимое файла как строку, если файл существует и доступен.
            None, если файла нет или есть ошибки доступа.
        """
        try:
            path = Path(file_path)

            # Если путь не абсолютный, разрешаем его относительно корня репозитория
            if not path.is_absolute():
                path = self.repo_path / path

            if not path.exists() or not path.is_file():
                return None

            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except (OSError, UnicodeDecodeError, PermissionError):
            return None

    def _read_file_content(self, file_path: Path, relative_path: str) -> Tuple[str, bool]:
        """
        Читает содержимое файла.

        Args:
            file_path: Полный путь к файлу
            relative_path: Относительный путь для ключа

        Returns:
            Кортеж (content, contains_changes)

        Raises:
            RepositoryError: Если не удалось прочитать файл
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return (content, False)  # content, contains_changes
        except (OSError, UnicodeDecodeError) as e:
            raise RepositoryError(f"Не удалось прочитать файл {file_path}: {e}")

    def _read_directory_content(
        self, dir_path: Path, base_relative_path: str
    ) -> Dict[str, Tuple[str, bool]]:
        """
        Читает содержимое директории рекурсивно.

        Args:
            dir_path: Путь к директории
            base_relative_path: Базовый относительный путь

        Returns:
            Словарь с содержимым файлов в директории

        Raises:
            RepositoryError: Если не удалось прочитать файлы
        """
        content = {}

        try:
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    # Проверяем расширение файла
                    if file_path.suffix.lower() not in {".yaml", ".yml", ".sql"}:
                        continue

                    # Вычисляем относительный путь от корня репозитория
                    rel_path = file_path.relative_to(self.repo_path)

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_content = f.read()
                        # content, contains_changes
                        file_name_without_ext = rel_path.stem
                        content[file_name_without_ext] = (file_content, False)
                    except (OSError, UnicodeDecodeError):
                        # Пропускаем бинарные файлы или файлы с ошибками кодировки
                        continue
        except OSError as e:
            raise RepositoryError(f"Не удалось прочитать директорию {dir_path}: {e}")

        return content

    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику репозитория.

        Returns:
            Словарь со статистикой репозитория
        """
        if not self.is_valid_repository():
            return {"valid": False}

        stats: Dict[str, Union[bool, int]] = {"valid": True}

        try:
            for field_name, relative_path, is_directory, is_optional in self.CONFIGS:
                full_path = self.repo_path / relative_path

                if is_directory:
                    # Считаем файлы в директории (0 если опциональная и не существует)
                    if full_path.exists():
                        file_count = sum(1 for f in full_path.rglob("*") if f.is_file())
                    else:
                        file_count = 0
                    stats[f"{field_name}_files"] = file_count
                else:
                    # Проверяем размер файла
                    if full_path.exists():
                        stats[f"{field_name}_size"] = full_path.stat().st_size
                    else:
                        stats[f"{field_name}_size"] = 0
        except OSError:
            # Игнорируем ошибки статистики
            pass

        return stats

    def _cache_validation_result(self, validation_result: ValidationResult) -> None:
        """
        Кеширует результат валидации.

        Args:
            validation_result: Результат валидации для кеширования
        """
        self._cached_validation_result = validation_result
        if self.git:
            try:
                self._cached_branch = self.git.get_current_branch()
            except Exception:
                self._cached_branch = None

    def is_validation_cached(self) -> bool:
        """
        Проверяет есть ли кешированный результат валидации.

        Returns:
            True если результат валидации закеширован
        """
        return self._cached_validation_result is not None

    def get_cached_validation_result(self) -> Optional['ValidationResult']:
        """
        Получает закешированный результат валидации.

        Returns:
            ValidationResult или None если валидация еще не выполнялась
        """
        return self._cached_validation_result

    def get_cached_sources(self) -> List[str]:
        """
        Получает список источников из кеша валидации.

        Returns:
            Список названий источников

        Raises:
            RepositoryError: Если кеш недоступен
        """
        if self._cached_validation_result:
            return self._cached_validation_result.source_names

        raise RepositoryError(
            "Список источников недоступен. Выполните валидацию репозитория."
        )

    def get_cached_dimensions(self) -> List[str]:
        """
        Получает список dimensions из кеша валидации.

        Returns:
            Список названий dimensions

        Raises:
            RepositoryError: Если кеш недоступен
        """
        if self._cached_validation_result:
            return self._cached_validation_result.dimension_names

        raise RepositoryError(
            "Список дименшенов недоступен. Выполните валидацию репозитория."
        )

    def get_cached_metrics(self) -> List[str]:
        """
        Получает список метрик из кеша валидации.

        Returns:
            Список названий метрик

        Raises:
            RepositoryError: Если кеш недоступен
        """
        if self._cached_validation_result:
            return self._cached_validation_result.metric_names

        raise RepositoryError(
            "Список метрик недоступен. Выполните валидацию репозитория."
        )

    def is_cache_valid(self) -> bool:
        """
        Проверяет валидность кеша для текущей ветки.

        Returns:
            True если кеш валиден
        """
        try:
            current_branch = self.git.get_current_branch() if self.git else "unknown"
            return (
                self._cached_validation_result is not None
                and self._cached_branch == current_branch
                and self._cached_validation_result.is_valid()
            )
        except Exception:
            return False

    def clear_cache(self) -> None:
        """
        Очищает весь кеш валидации.
        """
        self._logger.debug("Очистка кеша валидации")
        self._cached_validation_result = None
        self._cached_branch = None

    def _invalidate_cache(self, file_path: str) -> None:
        """
        Инвалидирует кеш при изменении файла.

        Args:
            file_path: Путь к изменившемуся файлу
        """
        self._logger.info(f"Инвалидация кеша из-за изменения файла: {file_path}")
        self.clear_cache()

    def start_file_monitoring(self) -> None:
        """
        Запускает мониторинг файловой системы для автоматической инвалидации кеша.
        """
        if self._monitoring_enabled:
            # Останавливаем существующий мониторинг перед запуском нового
            self.stop_file_monitoring()

        try:
            self._file_monitor = FileSystemMonitor(callback=self._invalidate_cache)

            # Определяем пути для мониторинга на основе конфигурации
            monitor_paths = []
            for _, path, is_dir, _ in self.CONFIGS:
                full_path = self.repo_path / path
                if is_dir and full_path.exists():
                    monitor_paths.append(full_path)
                elif not is_dir and full_path.parent.exists():
                    monitor_paths.append(full_path.parent)

            if monitor_paths:
                self._file_monitor.start_monitoring(monitor_paths)
                self._monitoring_enabled = True
                self._logger.info(
                    f"Мониторинг файловой системы запущен для {len(monitor_paths)} путей"
                )
            else:
                self._logger.warning("Нет доступных путей для мониторинга")

        except Exception as e:
            self._logger.error(f"Ошибка запуска мониторинга файловой системы: {e}")
            self._file_monitor = None

    def stop_file_monitoring(self) -> None:
        """
        Останавливает мониторинг файловой системы.
        """
        if self._file_monitor and self._monitoring_enabled:
            try:
                self._file_monitor.stop_monitoring()
                self._logger.info("Мониторинг файловой системы остановлен")
            except Exception as e:
                self._logger.error(f"Ошибка остановки мониторинга: {e}")
            finally:
                self._file_monitor = None
                self._monitoring_enabled = False

    def is_monitoring_active(self) -> bool:
        """
        Проверяет активность мониторинга файловой системы.

        Returns:
            True если мониторинг активен
        """
        return (
            self._monitoring_enabled
            and self._file_monitor is not None
            and self._file_monitor.is_active()
        )

    def get_monitored_paths(self) -> List[Path]:
        """
        Возвращает список отслеживаемых путей.

        Returns:
            Список отслеживаемых путей
        """
        if self._file_monitor:
            return self._file_monitor.get_monitored_paths()
        return []

    def __del__(self) -> None:
        """
        Деструктор - останавливает мониторинг при удалении объекта.
        """
        try:
            if hasattr(self, "_file_monitor") and hasattr(self, "_monitoring_enabled"):
                self.stop_file_monitoring()
        except Exception:
            pass  # Игнорируем ошибки в деструкторе

    def ensure_validated(self) -> None:
        """
        Проверяет что репозиторий готов к работе.

        Raises:
            RepositoryError: Если валидация показала ошибки
        """
        # Если есть закешированный результат валидации и он невалиден - ошибка
        if self._cached_validation_result and not self._cached_validation_result.is_valid():
            raise RepositoryError(
                "Репозиторий не прошел валидацию. Исправьте ошибки и повторите попытку."
            )

        # Если нет кеша валидации - предупреждаем, но не блокируем работу
        # (данные могут быть получены напрямую из файловой системы)


def detect_repository(start_path: Optional[str] = None) -> str:
    """
    Автоматически обнаруживает репозиторий метрик.

    Args:
        start_path: Путь для начала поиска (по умолчанию текущая директория)

    Returns:
        Путь к найденному репозиторию

    Raises:
        InvalidRepositoryError: Если репозиторий не найден
    """
    if start_path is None:
        start_path = os.getcwd()

    current_path = Path(start_path).resolve()

    # Ищем репозиторий, поднимаясь вверх по дереву директорий
    while current_path != current_path.parent:
        try:
            repo = MetricsRepository(str(current_path), require_api=False)
            if repo.is_valid_repository():
                return str(current_path)
        except RepositoryError:
            pass

        current_path = current_path.parent

    # Проверяем корневую директорию
    try:
        repo = MetricsRepository(str(current_path), require_api=False)
        if repo.is_valid_repository():
            return str(current_path)
    except RepositoryError:
        pass

    raise InvalidRepositoryError(
        f"Репозиторий метрик не найден в '{start_path}' или родительских директориях"
    )
