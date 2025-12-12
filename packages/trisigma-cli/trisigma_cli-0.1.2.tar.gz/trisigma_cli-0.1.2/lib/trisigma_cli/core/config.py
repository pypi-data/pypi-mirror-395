"""Управление конфигурацией Trisigma CLI."""

import json
import os
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils.exceptions import ConfigurationError
from ..utils.validation import (
    validate_api_token,
    validate_directory,
    validate_url,
)

if TYPE_CHECKING:
    from .cli_config_client import CLIConfig

VERIFY_SSL = False
DEFAULT_BACKEND_URL = "https://ab.avito.ru"


class Config:
    """Менеджер конфигурации CLI."""

    def __init__(self) -> None:
        """Инициализирует менеджер конфигурации."""
        self.config_dir = Path.home() / ".trisigma"
        self.config_file = self.config_dir / "config.json"
        self._config_data: Optional[Dict[str, Any]] = None
        self._lock = threading.Lock()

    def _ensure_config_dir(self) -> None:
        """Создает директорию конфигурации если она не существует."""
        try:
            self.config_dir.mkdir(exist_ok=True, mode=0o700)
        except OSError as e:
            raise ConfigurationError(f"Не удалось создать директорию конфигурации: {e}")

    def _ensure_config_loaded(self) -> None:
        """
        Гарантирует, что конфигурация загружена в _config_data.

        При первом вызове загружает конфигурацию из файла.
        Последующие вызовы используют кэшированные данные.

        Если файл конфигурации поврежден, создается backup и инициализируется пустая конфигурация.
        """
        if self._config_data is not None:
            return

        if not self.config_file.exists():
            self._config_data = {}
            return

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self._config_data = json.load(f)
        except json.JSONDecodeError as e:
            import time

            backup_file = self.config_file.with_suffix(f".corrupted.{int(time.time())}")
            try:
                self.config_file.rename(backup_file)
            except OSError:
                pass

            self._config_data = {}
            raise ConfigurationError(
                f"Файл конфигурации поврежден. Создан backup: {backup_file}. Ошибка: {e}"
            )
        except OSError as e:
            raise ConfigurationError(f"Не удалось загрузить конфигурацию: {e}")

    def _save_config(self) -> None:
        """
        Сохраняет конфигурацию в файл атомарно.

        Использует временный файл и атомарное переименование для предотвращения
        потери данных при прерывании записи.
        """
        if self._config_data is None:
            return

        self._ensure_config_dir()

        temp_file = self.config_file.with_suffix(".json.tmp")

        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self._config_data, f, indent=2, ensure_ascii=False)

            os.chmod(temp_file, 0o600)

            os.replace(temp_file, self.config_file)

        except OSError as e:
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass
            raise ConfigurationError(f"Не удалось сохранить конфигурацию: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Получает значение из конфигурации.

        Args:
            key: Ключ конфигурации
            default: Значение по умолчанию

        Returns:
            Значение из конфигурации или default
        """
        self._ensure_config_loaded()
        return self._config_data.get(key, default)

    def _validate_updates(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Валидирует обновления конфигурации.

        Args:
            updates: Словарь с обновлениями для валидации

        Returns:
            Словарь с валидированными значениями

        Raises:
            ConfigurationError: Если валидация не прошла
        """
        validated = {}

        for key, value in updates.items():
            try:
                if key == "repository_path":
                    if value is not None:
                        validated_path = validate_directory(value)
                        validated[key] = str(validated_path)
                    else:
                        validated[key] = None
                elif key == "api_url" or key == "backend_url":
                    if value is not None:
                        validated[key] = validate_url(value)
                    else:
                        validated[key] = None
                elif key == "access_token":
                    if value is not None:
                        validated[key] = validate_api_token(value)
                    else:
                        validated[key] = None
                elif key == "refresh_token":
                    validated[key] = value
                else:
                    validated[key] = value
            except Exception as e:
                raise ConfigurationError(f"Невалидное значение для '{key}': {e}")

        return validated

    def update(self, **kwargs) -> None:
        """
        Атомарно обновляет конфигурацию.

        Args:
            **kwargs: Ключи и значения для обновления

        Raises:
            ConfigurationError: Если валидация не прошла или произошла ошибка сохранения
        """
        if not kwargs:
            return

        with self._lock:
            self._config_data = None
            self._ensure_config_loaded()

            validated = self._validate_updates(kwargs)

            self._config_data.update(validated)
            self._save_config()

    def get_all(self) -> Dict[str, Any]:
        """
        Получает всю конфигурацию.

        Returns:
            Копия словаря с полной конфигурацией
        """
        self._ensure_config_loaded()
        return self._config_data.copy()

    def clear(self) -> None:
        """Очищает всю конфигурацию."""
        with self._lock:
            self._config_data = {}
            self._save_config()

    def delete(self, key: str) -> None:
        """
        Удаляет ключ из конфигурации.

        Args:
            key: Ключ для удаления
        """
        with self._lock:
            self._ensure_config_loaded()
            if key in self._config_data:
                del self._config_data[key]
                self._save_config()

    # Специфичные методы для Trisigma

    @property
    def repository_path(self) -> Optional[str]:
        """Путь к репозиторию метрик."""
        return self.get("repository_path")

    @property
    def api_url(self) -> Optional[str]:
        """URL API Trisigma."""
        return self.get("api_url")

    @property
    def access_token(self) -> Optional[str]:
        """Access token for API requests."""
        return self.get("access_token")

    @property
    def refresh_token(self) -> Optional[str]:
        """Refresh token for token renewal."""
        return self.get("refresh_token")

    @property
    def pypi_index(self) -> Optional[str]:
        """PyPI index URL."""
        return self.get("pypi_index")

    def get_pypi_index(self) -> Optional[str]:
        """
        Получает PyPI index URL.

        Returns:
            Сохраненный pypi_index или None если не настроен.
            Если pypi_index не сохранен, updater сам определит доступный источник.
        """
        return self.pypi_index

    def is_pypi_configured(self) -> bool:
        """
        Проверяет настроен ли PyPI index.

        Returns:
            True если pypi_index сохранен в конфигурации
        """
        return self.pypi_index is not None

    def is_configured(self) -> bool:
        """
        Проверяет настроен ли CLI.

        Returns:
            True если все обязательные параметры настроены
        """
        return (
            self.repository_path is not None
            and self.api_url is not None
            and self.access_token is not None
        )

    def is_llm_configured(self) -> bool:
        """
        Проверяет настроены ли LLM параметры.

        Returns:
            True если API настроен (LLM доступен через backend)
        """
        return self.access_token is not None

    def get_missing_config(self) -> List[str]:
        """
        Получает список отсутствующих параметров конфигурации.

        Returns:
            Список названий отсутствующих параметров
        """
        missing = []
        if not self.repository_path:
            missing.append("repository_path")
        if not self.api_url:
            missing.append("api_url")
        if not self.access_token:
            missing.append("access_token")
        return missing

    def validate_current_config(self) -> None:
        """
        Валидирует текущую конфигурацию.

        Raises:
            ConfigurationError: Если конфигурация невалидна
        """
        missing = self.get_missing_config()
        if missing:
            raise ConfigurationError(
                f"Отсутствуют обязательные параметры конфигурации: {', '.join(missing)}. "
                f"Выполните 'trisigma init' для настройки."
            )

        # Дополнительная валидация существующих значений
        if self.repository_path:
            try:
                validate_directory(self.repository_path)
            except Exception as e:
                raise ConfigurationError(f"Путь к репозиторию невалиден: {e}")

        if self.api_url:
            try:
                validate_url(self.api_url)
            except Exception as e:
                raise ConfigurationError(f"API URL невалиден: {e}")

        if self.access_token:
            try:
                validate_api_token(self.access_token)
            except Exception as e:
                raise ConfigurationError(f"Access токен невалиден: {e}")

    def get_cli_config(self) -> Optional["CLIConfig"]:
        """
        Получает расширенную CLI конфигурацию из backend.

        Returns:
            CLIConfig или None если не загружена
        """
        cli_config_dict = self.get("cli_config")
        if cli_config_dict is None:
            return None

        from .cli_config_client import CLIConfig

        try:
            return CLIConfig(**cli_config_dict)
        except Exception:
            return None

    def set_cli_config(self, cli_config: "CLIConfig") -> None:
        """
        Сохраняет CLI конфигурацию полученную от backend.

        Args:
            cli_config: Конфигурация от backend
        """
        self.update(cli_config=cli_config.model_dump())


# Глобальный экземпляр конфигурации
config: Config = Config()
