"""Утилиты для работы с SSL сертификатами."""

import os
from pathlib import Path
from typing import Tuple, Union


def get_ssl_cert_paths() -> Union[Tuple[str, str], Tuple[None, None]]:
    """
    Получает пути к SSL сертификатам из домашней директории пользователя.

    Returns:
        Кортеж (cert_path, key_path) или (None, None) если сертификаты не найдены
    """
    try:
        # Получаем имя текущего пользователя
        username = os.environ.get("USER") or os.environ.get("USERNAME")

        if not username:
            # Fallback - попробуем получить из домашней директории
            home_dir = Path.home()
            username = home_dir.name

        # Формируем пути к сертификатам
        cert_path = f"/Users/{username}/.avito/certs/personal.crt"
        key_path = f"/Users/{username}/.avito/certs/personal.key"

        # Проверяем существование файлов
        if Path(cert_path).exists() and Path(key_path).exists():
            return cert_path, key_path

        # Если файлы не найдены, возвращаем None
        return None, None

    except Exception:
        return None, None
