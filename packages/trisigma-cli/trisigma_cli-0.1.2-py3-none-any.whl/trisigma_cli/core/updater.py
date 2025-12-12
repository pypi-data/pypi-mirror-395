import asyncio
import json
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import List, Optional

import aiohttp
from packaging import version

from trisigma_cli.core.config import VERIFY_SSL, Config
from trisigma_cli.core.version import __version__
from trisigma_cli.utils.exceptions import TrisigmaError

logger = logging.getLogger(__name__)


class UpdateError(TrisigmaError):
    pass


class InstallationMethod(Enum):
    PIPX = "pipx"
    PIP = "pip"
    UNKNOWN = "unknown"


class UpdateChecker:
    PACKAGE_NAME = "trisigma-cli"

    # Корпоративный PyPI имеет приоритет, публичный используется как fallback
    SOURCES = [
        {
            "name": "avito-pypi",
            "url": "https://pypi.k.avito.ru/pypi/trisigma-cli/json",
            "index_url": "https://pypi.k.avito.ru/simple/",
            "timeout": 10,
        },
        {
            "name": "pypi-public",
            "url": "https://pypi.org/pypi/trisigma-cli/json",
            "index_url": "https://pypi.org/simple/",
            "timeout": 10,
        },
    ]

    def __init__(self, config: Optional[Config] = None, config_dir: Optional[Path] = None) -> None:
        self.config = config
        self.config_dir = config_dir or Path.home() / ".trisigma"
        self.cache_file = self.config_dir / "last_update_check"
        self.current_version = __version__
        self._update_source_url: Optional[str] = None
        self._latest_version: Optional[str] = None

    def _build_json_api_url(self, index_url: str) -> str:
        """
        Преобразует PyPI index URL в URL для JSON API.
        
        Обрабатывает разные форматы:
        - https://pypi.org/simple/ -> https://pypi.org/pypi/PACKAGE/json
        - https://pypi.org/pypi/ -> https://pypi.org/pypi/PACKAGE/json
        - https://pypi.k.avito.ru/pypi/ -> https://pypi.k.avito.ru/pypi/PACKAGE/json
        
        Args:
            index_url: URL PyPI index (может заканчиваться на /simple/ или /pypi/)
            
        Returns:
            URL для запроса JSON API с информацией о пакете
        """
        url = index_url.rstrip('/')
        
        # Заменяем /simple на /pypi для публичного PyPI
        if url.endswith('/simple'):
            url = url[:-7] + '/pypi'
        
        # Если URL не заканчивается на /pypi, добавляем
        if not url.endswith('/pypi'):
            # Предполагаем что это base URL, добавляем /pypi
            url = url + '/pypi'
        
        return f"{url}/{self.PACKAGE_NAME}/json"

    def _normalize_index_url(self, index_url: str) -> str:
        """
        Нормализует PyPI index URL для использования в pip install.
        
        pip требует PEP 503 Simple API формат (/simple/).
        Преобразует /pypi/ в /simple/ для совместимости.
        
        Args:
            index_url: URL PyPI index
            
        Returns:
            Нормализованный URL (всегда с /simple/ для pip)
        """
        url = index_url.rstrip('/')
        
        # Заменяем /pypi на /simple для pip совместимости
        if url.endswith('/pypi'):
            url = url[:-5] + '/simple'
        
        # Если URL не заканчивается на /simple, добавляем
        if not url.endswith('/simple'):
            url = url + '/simple'
        
        return url + '/'

    def should_check_now(self, check_interval: int = 3600) -> bool:
        if os.getenv("CI"):
            return False

        if not self.cache_file.exists():
            return True

        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
                last_check = datetime.fromisoformat(data["last_check"])
                return datetime.now() - last_check > timedelta(seconds=check_interval)
        except (json.JSONDecodeError, KeyError, ValueError):
            return True

    def update_last_check_time(self, latest_version: Optional[str] = None) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "last_check": datetime.now().isoformat(),
            "latest_version": latest_version,
            "current_version": self.current_version,
            "source_url": self._update_source_url,
        }
        with open(self.cache_file, "w") as f:
            json.dump(data, f)

    async def check_for_updates(self) -> Optional[str]:
        """
        Проверяет наличие обновлений в доступных источниках.
        
        Приоритет источников:
        1. Сохраненный в конфиге pypi_index (если есть)
        2. Корпоративный avito-pypi (если доступен)
        3. Публичный pypi.org (fallback)
        
        Returns:
            Версия последнего доступного обновления или None
        """
        sources_to_check = []

        # Если pypi_index сохранен в конфиге - проверяем его первым
        if self.config and self.config.is_pypi_configured():
            pypi_index = self.config.pypi_index
            
            # Строим корректный URL для JSON API (обрабатывает /simple/ -> /pypi/)
            json_api_url = self._build_json_api_url(pypi_index)
            # Нормализуем index_url для pip install
            normalized_index = self._normalize_index_url(pypi_index)

            configured_source = {
                "name": "configured-pypi",
                "url": json_api_url,
                "index_url": normalized_index,
                "timeout": 10,
            }
            sources_to_check.append(configured_source)
            logger.debug(f"Using configured PyPI index: {pypi_index} -> {json_api_url}")

        # Добавляем стандартные источники как fallback
        sources_to_check.extend(self.SOURCES)

        for source in sources_to_check:
            try:
                latest = await self._check_source(source)
                if latest:
                    logger.debug(f"Found version {latest} from {source['name']}")
                    # Используем явный index_url если указан, иначе извлекаем из url
                    if "index_url" in source:
                        self._update_source_url = source["index_url"]
                    else:
                        url_parts = source["url"].rstrip("/").split("/")
                        self._update_source_url = "/".join(url_parts[:-2]) + "/"
                    self._latest_version = latest
                    self.update_last_check_time(latest)
                    return latest
            except Exception as e:
                logger.debug(f"Source {source['name']} failed: {e}")
                continue

        self.update_last_check_time()
        return None

    async def _check_source(self, source: dict) -> Optional[str]:
        try:
            timeout = aiohttp.ClientTimeout(total=source["timeout"])
            connector = aiohttp.TCPConnector(ssl=VERIFY_SSL)
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                async with session.get(source["url"]) as resp:
                    if resp.status == 404:
                        logger.debug(f"Package not found in {source['name']}")
                        return None

                    resp.raise_for_status()
                    data = await resp.json()
                    return data["info"]["version"]

        except asyncio.TimeoutError:
            logger.debug(f"Timeout checking {source['name']}")
            return None
        except aiohttp.ClientError as e:
            logger.debug(f"Network error checking {source['name']}: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            logger.debug(f"Invalid response from {source['name']}: {e}")
            return None

    def is_update_available(self, latest_version: Optional[str]) -> bool:
        if not latest_version:
            return False

        try:
            current = version.parse(self.current_version)
            latest = version.parse(latest_version)
            return latest > current
        except version.InvalidVersion:
            return False

    def _perform_pip_update(self) -> bool:
        if not self._update_source_url:
            raise UpdateError("Update source URL not available. Run check_for_updates() first.")

        if not self._latest_version:
            raise UpdateError("Target version not available. Run check_for_updates() first.")

        logger.info(f"Updating from PyPI index: {self._update_source_url}")
        package_spec = f"{self.PACKAGE_NAME}=={self._latest_version}"

        cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "--index-url",
            self._update_source_url,
            package_spec,
        ]

        try:
            logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.stdout:
                logger.info(f"pip stdout: {result.stdout}")
            if result.stderr:
                logger.warning(f"pip stderr: {result.stderr}")

            if result.returncode != 0:
                raise UpdateError(
                    f"pip install failed with exit code {result.returncode}\n"
                    f"stdout: {result.stdout}\n"
                    f"stderr: {result.stderr}"
                )

            return True
        except subprocess.TimeoutExpired:
            raise UpdateError("Update operation timed out after 120 seconds")
        except subprocess.SubprocessError as e:
            raise UpdateError(f"Failed to execute pip install: {e}")

    def perform_update(self) -> bool:
        method = self.detect_installation_method()

        if method == InstallationMethod.PIPX:
            logger.info("Detected pipx installation, using pipx upgrade")
            return self._perform_pipx_update()
        else:
            logger.info("Detected pip installation, using pip install")
            return self._perform_pip_update()

    def get_cached_latest_version(self) -> Optional[str]:
        if not self.cache_file.exists():
            return None

        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
                latest_version = data.get("latest_version")
                if latest_version and "source_url" in data:
                    self._update_source_url = data["source_url"]
                    self._latest_version = latest_version
                return latest_version
        except (json.JSONDecodeError, KeyError):
            return None

    def get_update_source(self) -> Optional[str]:
        return self._update_source_url

    def get_installation_method(self) -> InstallationMethod:
        return self.detect_installation_method()

    def detect_installation_method(self) -> InstallationMethod:
        executable = sys.executable

        if "pipx" in executable and "venvs" in executable:
            return InstallationMethod.PIPX

        pipx_home = os.getenv("PIPX_HOME")
        if pipx_home and pipx_home in executable:
            return InstallationMethod.PIPX

        return InstallationMethod.PIP

    def _find_pipx_command(self) -> Optional[List[str]]:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pipx", "--version"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                return [sys.executable, "-m", "pipx"]
        except Exception:
            pass

        python_dir = Path(sys.executable).parent
        pipx_path = python_dir / "pipx"
        if pipx_path.exists() and pipx_path.is_file():
            return [str(pipx_path)]

        pipx_which = shutil.which("pipx")
        if pipx_which:
            return [pipx_which]

        return None

    def _perform_pipx_update(self) -> bool:
        if not self._update_source_url:
            raise UpdateError("Update source URL not available. Run check_for_updates() first.")

        if not self._latest_version:
            raise UpdateError("Target version not available. Run check_for_updates() first.")

        logger.info(f"Updating from PyPI index: {self._update_source_url}")
        pipx_cmd = self._find_pipx_command()
        if not pipx_cmd:
            raise UpdateError("pipx command not found. Cannot update pipx installation.")

        # Указываем точную версию для установки через pipx
        version_spec = f"{self.PACKAGE_NAME}=={self._latest_version}"
        cmd = pipx_cmd + [
            "upgrade",
            self.PACKAGE_NAME,
            "--pip-args",
            f"--index-url {self._update_source_url} {version_spec}",
            "--force",
        ]

        try:
            logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.stdout:
                logger.info(f"pipx stdout: {result.stdout}")
            if result.stderr:
                logger.warning(f"pipx stderr: {result.stderr}")

            if result.returncode != 0:
                raise UpdateError(
                    f"pipx upgrade failed with exit code {result.returncode}\n"
                    f"stdout: {result.stdout}\n"
                    f"stderr: {result.stderr}"
                )

            return True
        except subprocess.TimeoutExpired:
            raise UpdateError("Update operation timed out after 120 seconds")
        except subprocess.SubprocessError as e:
            raise UpdateError(f"Failed to execute pipx upgrade: {e}")
