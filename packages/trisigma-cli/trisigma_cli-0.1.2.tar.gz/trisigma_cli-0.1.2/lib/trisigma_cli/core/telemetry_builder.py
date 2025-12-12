"""Утилита для построения параметров телеметрии."""

from typing import Any, Dict, List, Optional


class TelemetryBuilder:
    """Построитель параметров телеметрии для стандартизации сборки данных."""

    @staticmethod
    def build_compilation_params(
        is_metrics_mode: bool,
        granularity: str,
        source_name: Optional[str] = None,
        metrics_list: Optional[List[str]] = None,
        dimensions_list: Optional[List[str]] = None,
        columns_list: Optional[List[str]] = None,
        first_date: Optional[str] = None,
        last_date: Optional[str] = None,
        output_file: Optional[str] = None,
        pretty: bool = False,
        **extra_params: Any,
    ) -> Dict[str, Any]:
        """
        Собирает параметры для телеметрии компиляции.

        Args:
            is_metrics_mode: Режим компиляции метрик
            granularity: Гранулярность
            source_name: Название источника (для компиляции источников)
            metrics_list: Список метрик (для компиляции метрик)
            dimensions_list: Список дименшенов
            columns_list: Список колонок
            first_date: Начальная дата
            last_date: Конечная дата
            output_file: Файл для вывода
            pretty: Режим форматирования (pretty=True означает Rich форматирование)
            **extra_params: Дополнительные параметры

        Returns:
            Словарь с параметрами телеметрии
        """
        params: Dict[str, Any] = {
            "is_metrics_mode": is_metrics_mode,
            "granularity": granularity,
        }

        # Добавляем параметры в зависимости от режима
        if is_metrics_mode:
            if metrics_list:
                params["metrics"] = metrics_list
                params["metrics_count"] = len(metrics_list)
        else:
            if source_name:
                params["source_name"] = source_name

        # Добавляем dimensions если указаны
        if dimensions_list:
            params["dimensions_count"] = len(dimensions_list)
            params["dimensions"] = dimensions_list

        # Добавляем columns если указаны
        if columns_list:
            params["columns_count"] = len(columns_list)
            params["columns"] = columns_list

        # Добавляем даты если указаны
        if first_date:
            params["first_date"] = first_date
        if last_date:
            params["last_date"] = last_date

        # Добавляем информацию о выводе
        if output_file is not None:
            params["output_file"] = bool(output_file)

        params["pretty"] = pretty

        # Добавляем дополнительные параметры
        params.update(extra_params)

        return params

    @staticmethod
    def build_git_params(
        task_number: Optional[str] = None,
        has_author_from_jwt: bool = False,
        files_changed: int = 0,
        commit_sha: Optional[str] = None,
        pr_url_generated: bool = False,
        browser_opened: bool = False,
        current_branch: Optional[str] = None,
        **extra_params: Any,
    ) -> Dict[str, Any]:
        """
        Собирает параметры для телеметрии git операций.

        Args:
            task_number: Номер задачи
            has_author_from_jwt: Есть ли автор из JWT
            files_changed: Количество измененных файлов
            commit_sha: SHA коммита
            pr_url_generated: Сгенерирован ли URL PR
            browser_opened: Открыт ли браузер
            current_branch: Текущая git ветка
            **extra_params: Дополнительные параметры

        Returns:
            Словарь с параметрами телеметрии
        """
        params: Dict[str, Any] = {}

        if task_number:
            params["task_number"] = task_number
            params["has_task_number"] = True
        else:
            params["has_task_number"] = False

        params["has_author_from_jwt"] = has_author_from_jwt

        if files_changed > 0:
            params["files_changed"] = files_changed

        if commit_sha:
            params["commit_sha"] = commit_sha[:8]

        if pr_url_generated:
            params["pr_url_generated"] = pr_url_generated

        if browser_opened:
            params["browser_opened"] = browser_opened

        if current_branch:
            params["current_branch"] = current_branch

        # Добавляем дополнительные параметры
        params.update(extra_params)

        return params

    @staticmethod
    def build_watch_params(
        compilation_type: str,
        granularity: str,
        source_name: Optional[str] = None,
        metrics_list: Optional[List[str]] = None,
        dimensions_list: Optional[List[str]] = None,
        columns_list: Optional[List[str]] = None,
        first_date: Optional[str] = None,
        last_date: Optional[str] = None,
        has_output_file: bool = False,
        total_recompilations: Optional[int] = None,
        **extra_params: Any,
    ) -> Dict[str, Any]:
        """
        Собирает параметры для телеметрии watch режима.

        Args:
            compilation_type: Тип компиляции ("source" или "metrics")
            granularity: Гранулярность
            source_name: Название источника
            metrics_list: Список метрик
            dimensions_list: Список дименшенов
            columns_list: Список колонок
            first_date: Начальная дата
            last_date: Конечная дата
            has_output_file: Есть ли output файл
            total_recompilations: Общее количество перекомпиляций
            **extra_params: Дополнительные параметры

        Returns:
            Словарь с параметрами телеметрии
        """
        params: Dict[str, Any] = {
            "compilation_type": compilation_type,
            "granularity": granularity,
        }

        # Добавляем параметры в зависимости от типа компиляции
        if compilation_type == "metrics":
            if metrics_list:
                params["metrics_count"] = len(metrics_list)
                params["metrics"] = metrics_list
        else:
            if source_name:
                params["source_name"] = source_name

        # Добавляем dimensions если указаны
        if dimensions_list:
            params["dimensions_count"] = len(dimensions_list)
            params["dimensions"] = dimensions_list

        # Добавляем columns если указаны
        if columns_list:
            params["columns_count"] = len(columns_list)
            params["columns"] = columns_list

        # Добавляем даты если указаны
        if first_date:
            params["first_date"] = first_date
        if last_date:
            params["last_date"] = last_date

        # Добавляем информацию о файле
        if has_output_file:
            params["has_output_file"] = has_output_file

        # Добавляем статистику перекомпиляций
        if total_recompilations is not None:
            params["total_recompilations"] = total_recompilations

        # Добавляем дополнительные параметры
        params.update(extra_params)

        return params

    @staticmethod
    def build_ai_explain_params(
        errors_count: int,
        error_text: str,
        ai_response_size: int,
        **extra_params: Any,
    ) -> Dict[str, Any]:
        """
        Собирает параметры для телеметрии AI объяснений.

        Args:
            errors_count: Количество ошибок
            error_text: Текст ошибки(ок)
            ai_response_size: Размер ответа AI в символах
            **extra_params: Дополнительные параметры

        Returns:
            Словарь с параметрами телеметрии
        """
        params: Dict[str, Any] = {
            "errors_count": errors_count,
            "error_text": error_text[:5000],
            "ai_response_size": ai_response_size,
        }

        # Добавляем дополнительные параметры
        params.update(extra_params)

        return params

    @staticmethod
    def build_ai_feedback_params(
        error_description: str,
        full_ai_response: str,
        rating: str,
        user_comment: str,
        **extra_params: Any,
    ) -> Dict[str, Any]:
        """
        Собирает параметры для телеметрии фидбека AI объяснений.

        Args:
            error_description: Описание ошибки (первые 5000 символов)
            full_ai_response: Полный ответ AI
            rating: Оценка пользователя ("like" или "dislike")
            user_comment: Комментарий пользователя
            **extra_params: Дополнительные параметры

        Returns:
            Словарь с параметрами телеметрии
        """
        params: Dict[str, Any] = {
            "error_description": error_description[:5000],
            "full_ai_response": full_ai_response,
            "rating": rating,
            "user_comment": user_comment,
        }

        params.update(extra_params)

        return params
