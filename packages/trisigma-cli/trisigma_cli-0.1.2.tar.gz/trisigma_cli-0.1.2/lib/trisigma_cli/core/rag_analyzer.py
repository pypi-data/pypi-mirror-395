"""RAG анализатор для определения релевантных файлов для ошибок валидации."""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from .dto import ProcessedValidationError
from .repository import MetricsRepository


class RAGContext:
    """Контекст для LLM запроса с релевантными файлами и ошибками."""

    def __init__(self, max_total_size: int):
        """
        Инициализирует контекст RAG.

        Args:
            max_total_size: Максимальный размер контекста в символах (если не указан, используется дефолт)
        """
        self.max_total_size = max_total_size
        self.current_size = 0
        self.found_files: Dict[str, str] = {}
        self.missing_files: List[str] = []
        self.errors: List[ProcessedValidationError] = []
        # Хранение partial файлов: {virtual_path: (content, display_label)}
        self.partial_files: Dict[str, Tuple[str, str]] = {}

    def add_error(self, error: ProcessedValidationError) -> None:
        """Добавляет ошибку в контекст."""
        self.errors.append(error)

    def add_file_content(
        self, path: str, content: str, error: Optional[ProcessedValidationError] = None
    ) -> bool:
        """
        Добавляет содержимое файла в контекст.

        Args:
            path: Путь к файлу
            content: Содержимое файла
            error: Ошибка связанная с файлом (для умной обрезки)

        Returns:
            True если файл добавлен, False если не хватило места
        """
        if path in self.found_files:
            return True  # Файл уже добавлен

        # Проверяем доступное место
        remaining_space = self.max_total_size - self.current_size
        if remaining_space < len(content):  # Нет места для этого контента
            return False

        # Умная обрезка под доступное место
        if len(content) > remaining_space:
            content = self._smart_truncate(content, remaining_space, error, path)

        self.found_files[path] = content
        self.current_size += len(content)
        return True

    def add_missing_file(self, path: str) -> None:
        """Добавляет отсутствующий файл в список."""
        if path not in self.missing_files:
            self.missing_files.append(path)

    def has_space_for_more(self) -> bool:
        """Проверяет есть ли место для добавления новых файлов."""
        return (self.max_total_size - self.current_size) > 3000

    def _smart_truncate(
        self,
        content: str,
        max_size: int,
        error: Optional[ProcessedValidationError],
        file_path: str,
    ) -> str:
        """
        Умная обрезка контента с учетом контекста ошибки.

        Args:
            content: Содержимое для обрезки
            max_size: Максимальный размер
            error: Ошибка для контекста
            file_path: Путь к файлу

        Returns:
            Обрезанное содержимое
        """
        if error and error.line:
            # Берем окрестности строки с ошибкой
            return self._extract_lines_around_error(content, error.line, max_size)
        elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
            # Для YAML файлов ищем релевантные секции
            return self._extract_yaml_sections(content, error, max_size)
        elif file_path.endswith(".sql"):
            # Для SQL файлов ищем релевантные блоки
            return self._extract_sql_blocks(content, error, max_size)
        else:
            # Обычная обрезка: начало + конец
            chunk_size = max_size // 2
            return f"{content[:chunk_size]}\n\n... [TRUNCATED] ...\n\n{content[-chunk_size:]}"

    def _extract_lines_around_error(self, content: str, error_line: int, max_size: int) -> str:
        """Извлекает строки вокруг ошибки."""
        lines = content.split("\n")

        # Вычисляем сколько строк поместится
        avg_line_length = max(len(content) // len(lines), 50)
        max_lines = max_size // avg_line_length
        context_lines = max_lines // 2

        start_line = max(0, error_line - context_lines - 1)
        end_line = min(len(lines), error_line + context_lines)

        extracted_lines = lines[start_line:end_line]

        # Добавляем номера строк для контекста
        numbered_lines = []
        for i, line in enumerate(extracted_lines, start=start_line + 1):
            prefix = ">>> " if i == error_line else "    "
            numbered_lines.append(f"{prefix}{i:4}: {line}")

        result = "\n".join(numbered_lines)

        if len(result) > max_size:
            return result[: max_size - 100] + "\n... [TRUNCATED]"

        return result

    def _extract_yaml_sections(
        self, content: str, error: Optional[ProcessedValidationError], max_size: int
    ) -> str:
        """Извлекает релевантные секции из YAML файла."""
        if not error:
            return content[:max_size]

        # Ищем ключевые слова в сообщении ошибки
        keywords = self._extract_keywords_from_message(error.message)

        try:
            # Пытаемся найти релевантные секции
            lines = content.split("\n")
            relevant_sections = []
            current_section = []
            in_relevant_section = False

            for line in lines:
                # Проверяем начало новой секции (ключ на верхнем уровне)
                if line.strip() and not line.startswith(" ") and ":" in line:
                    # Сохраняем предыдущую секцию если она релевантна
                    if in_relevant_section and current_section:
                        relevant_sections.extend(current_section)
                        relevant_sections.append("")  # Пустая строка между секциями

                    # Начинаем новую секцию
                    current_section = [line]
                    section_key = line.split(":")[0].strip()
                    in_relevant_section = any(
                        keyword.lower() in section_key.lower() for keyword in keywords
                    )
                else:
                    current_section.append(line)

            # Добавляем последнюю секцию
            if in_relevant_section and current_section:
                relevant_sections.extend(current_section)

            if relevant_sections:
                result = "\n".join(relevant_sections)
                if len(result) <= max_size:
                    return result

        except Exception:
            # Если парсинг не удался, возвращаем начало файла
            pass

        # Fallback: начало + конец
        chunk_size = max_size // 2
        return f"{content[:chunk_size]}\n\n... [TRUNCATED] ...\n\n{content[-chunk_size:]}"

    def _extract_sql_blocks(
        self, content: str, error: Optional[ProcessedValidationError], max_size: int
    ) -> str:
        """Извлекает релевантные блоки из SQL файла."""
        if not error:
            return content[:max_size]

        keywords = self._extract_keywords_from_message(error.message)

        # Ищем CREATE TABLE, VIEW, FUNCTION и т.д. с релевантными именами
        relevant_blocks = []
        lines = content.split("\n")
        current_block = []
        in_relevant_block = False

        for line in lines:
            line_upper = line.strip().upper()

            # Проверяем начало нового блока
            if any(
                line_upper.startswith(keyword) for keyword in ["CREATE", "ALTER", "DROP", "WITH"]
            ):
                # Сохраняем предыдущий блок если он релевантен
                if in_relevant_block and current_block:
                    relevant_blocks.extend(current_block)
                    relevant_blocks.append("")

                # Начинаем новый блок
                current_block = [line]
                in_relevant_block = any(keyword.lower() in line.lower() for keyword in keywords)
            else:
                current_block.append(line)

                # Проверяем конец блока (пустая строка или ';')
                if line.strip().endswith(";") or not line.strip():
                    if in_relevant_block and current_block:
                        relevant_blocks.extend(current_block)
                        relevant_blocks.append("")
                    current_block = []
                    in_relevant_block = False

        # Добавляем последний блок
        if in_relevant_block and current_block:
            relevant_blocks.extend(current_block)

        if relevant_blocks:
            result = "\n".join(relevant_blocks)
            if len(result) <= max_size:
                return result

        # Fallback
        chunk_size = max_size // 2
        return f"{content[:chunk_size]}\n\n... [TRUNCATED] ...\n\n{content[-chunk_size:]}"

    def _extract_keywords_from_message(self, message: str) -> List[str]:
        """Извлекает ключевые слова из сообщения ошибки."""
        # Паттерны для поиска имен в кавычках, SQL идентификаторах и т.д.
        patterns = [
            r"['\"]([^'\"]+)['\"]",  # В кавычках
            r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b",  # SQL идентификаторы
            r"table\s+([a-zA-Z_][a-zA-Z0-9_]*)",  # table name
            r"column\s+([a-zA-Z_][a-zA-Z0-9_]*)",  # column name
        ]

        keywords = []
        for pattern in patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            keywords.extend(matches)

        # Фильтруем слишком короткие и общие слова
        filtered_keywords = [
            kw
            for kw in keywords
            if len(kw) > 2
            and kw.lower() not in ["the", "and", "for", "with", "from", "table", "column"]
        ]

        return list(set(filtered_keywords))  # Убираем дубликаты

    def to_llm_prompt(self, base_prompt: str) -> str:
        """
        Формирует финальный prompt для LLM.

        Args:
            base_prompt: Базовый prompt

        Returns:
            Полный prompt с контекстом
        """
        context_parts = [base_prompt]

        # Добавляем информацию об ошибках
        if self.errors:
            context_parts.append("\n## Контекст ошибок:")
            for i, error in enumerate(self.errors, 1):
                context_parts.append(f"\n**Ошибка {i}:**")
                context_parts.append(f"- Компонент: {error.component}")
                if error.file:
                    context_parts.append(f"- Файл: {error.file}")
                if error.line:
                    context_parts.append(f"- Строка: {error.line}")
                if error.column:
                    context_parts.append(f"- Колонка: {error.column}")
                context_parts.append(f"- Сообщение: {error.message}")

        # Добавляем доступные файлы (regular + partial)
        if self.found_files or self.partial_files:
            context_parts.append("\n## Доступные файлы:")

            # Обычные файлы
            for file_path, content in self.found_files.items():
                context_parts.append(f"\n### Файл: {file_path}")
                context_parts.append(f"```\n{content}\n```")

            # Partial файлы с метками
            for virtual_path, (content, label) in self.partial_files.items():
                context_parts.append(f"\n### Файл: {label}")
                context_parts.append(f"```\n{content}\n```")

        # Добавляем информацию об отсутствующих файлах
        if self.missing_files:
            context_parts.append("\n## ⚠️ Отсутствующие файлы:")
            context_parts.append("Следующие файлы не найдены в репозитории:")
            for file_path in self.missing_files:
                context_parts.append(f"- {file_path}")
            context_parts.append(
                "\nВозможно, файлы размещены некорректно или имеют другие имена. "
                "Think harder about possible locations and alternative naming."
            )

        return "\n".join(context_parts)


class RAGAnalyzer:
    """Анализатор для определения релевантных файлов по ошибкам валидации."""

    def __init__(self, max_context_size: int):
        """
        Инициализирует анализатор RAG.

        Args:
            max_context_size: Максимальный размер контекста в символах
        """
        self.max_context_size = max_context_size

    def _truncate_yaml_content(self, content: str, max_size: int) -> str:
        """
        Обрезает YAML контент, сохраняя структуру.

        Args:
            content: YAML контент
            max_size: Максимальный размер

        Returns:
            Обрезанный контент
        """
        try:
            data = yaml.safe_load(content)
            if data:
                # Считаем количество источников
                sources_count = 0
                if isinstance(data, dict) and "sources" in data:
                    sources = data["sources"]
                    if isinstance(sources, dict):
                        sources_count = len(sources)

                # Создаем краткую версию
                if sources_count > 0:
                    summary = f"Структура YAML с {sources_count} источниками (обрезана до {max_size} символов)"
                else:
                    summary = f"YAML структура (обрезана до {max_size} символов)"

                # Обрезаем оригинальный контент
                if len(content) > max_size:
                    chunk_size = max_size // 2
                    return f"{content[:chunk_size]}\n\n... [TRUNCATED] ...\n\n{summary}"
                return content
        except Exception:
            # В случае ошибки парсинга YAML - обычная обрезка
            pass

        # Обычная обрезка: начало + конец
        chunk_size = max_size // 2
        truncated = f"{content[:chunk_size]}\n\n... [TRUNCATED] ...\n\n{content[-chunk_size:]}"
        return truncated[:max_size]  # Убедимся, что размер точно max_size

    def _truncate_sql_content(self, content: str, max_size: int) -> str:
        """
        Обрезает SQL контент, сохраняя структуру.

        Args:
            content: SQL контент
            max_size: Максимальный размер

        Returns:
            Обрезанный контент
        """
        if len(content) <= max_size:
            return content

        # Ищем SQL блоки (SELECT, INSERT, UPDATE, DELETE, CREATE, etc.)
        sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"]

        lines = content.split("\n")
        result_lines = []

        current_block = []
        in_block = False

        for line in lines:
            line_stripped = line.strip()

            # Начинаем новый блок
            if any(keyword in line_stripped.upper() for keyword in sql_keywords):
                if in_block and current_block:
                    # Завершаем предыдущий блок
                    result_lines.extend(current_block)
                current_block = [line]
                in_block = True
            elif in_block:
                current_block.append(line)

                # Проверяем размер
                block_text = "\n".join(current_block)
                if len(block_text) > max_size // 2:
                    # Обрезаем блок
                    result_lines.append(f"{block_text[: max_size // 2]}\n... [TRUNCATED] ...")
                    break

        # Добавляем остаток
        remaining_size = max_size - len("\n".join(result_lines))
        if remaining_size > 0 and len(content) > len("\n".join(result_lines)):
            remaining_text = content[-remaining_size:]
            result_lines.append(f"... [TRUNCATED] ...\n{remaining_text}")

        result = "\n".join(result_lines)
        return result[:max_size]  # Убедимся, что размер точно max_size

    def _truncate_generic_content(self, content: str, max_size: int) -> str:
        """
        Обрезает обычный контент.

        Args:
            content: Контент для обрезки
            max_size: Максимальный размер

        Returns:
            Обрезанный контент
        """
        if len(content) <= max_size:
            return content

        # Обычная обрезка: начало + конец
        chunk_size = max_size // 2
        truncated = f"{content[:chunk_size]}\n\n... [TRUNCATED] ...\n\n{content[-chunk_size:]}"
        return truncated[:max_size]  # Убедимся, что размер точно max_size

    def _extract_source_names(self, error: ProcessedValidationError) -> List[str]:
        """
        Извлекает имя источника из ошибки.

        Args:
            error: Ошибка валидации

        Returns:
            Имя источника или None
        """
        # Сначала пытаемся извлечь имя из сообщения ошибки
        if error.details:
            return list(error.details.keys())

        return []

    def analyze_errors(
        self, errors: List[ProcessedValidationError], repository: MetricsRepository
    ) -> RAGContext:
        """
        Анализирует ошибки и собирает релевантный контекст.

        Args:
            errors: Список ошибок валидации
            repository: Репозиторий метрик

        Returns:
            Контекст с релевантными файлами
        """
        context = RAGContext(self.max_context_size)

        # Добавляем все ошибки в контекст
        for error in errors:
            context.add_error(error)

        # Собираем все файлы с приоритизацией
        all_files = []
        for error in errors:
            files = self._collect_files_for_error(error, repository)
            prioritized = self._prioritize_files(files, error)
            all_files.extend(prioritized)

        # Дедупликация с сохранением порядка приоритета
        unique_files = list(dict.fromkeys(all_files))

        # Добавляем файлы пока есть место
        for file_path in unique_files:
            if not context.has_space_for_more():
                break

            # Проверяем является ли это partial файлом (формат: path#section)
            if "#" in file_path:
                base_path, section_name = file_path.split("#", 1)
                full_content = repository.read_file_safe(base_path)

                if full_content is not None:
                    # Извлекаем секцию из файла
                    section_content = self._extract_source_yaml_section(section_name, full_content)
                    if section_content:
                        # Добавляем как partial файл с красивой меткой
                        label = f"{base_path} (source: {section_name})"
                        if len(section_content) <= context.max_total_size - context.current_size:
                            context.partial_files[file_path] = (section_content, label)
                            context.current_size += len(section_content)
                    else:
                        context.add_missing_file(file_path)
                else:
                    context.add_missing_file(file_path)
            else:
                # Обычный файл
                content = repository.read_file_safe(file_path)
                if content is not None:
                    related_error = self._find_related_error(file_path, errors)
                    context.add_file_content(file_path, content, related_error)
                else:
                    context.add_missing_file(file_path)

        return context

    def _collect_files_for_error(
        self, error: ProcessedValidationError, repository: MetricsRepository
    ) -> Set[str]:
        """Собирает все релевантные файлы для ошибки."""
        files = set()

        # 1. Основной файл из ошибки
        if error.file:
            files.add(error.file)

        # 2. Связанные файлы по логике компонентов
        related_files = self._get_related_files(error, repository)
        files.update(set(related_files))

        # 3. Файлы извлеченные из сообщения ошибки
        extracted_files = self._extract_files_from_message(
            error.message, error.component, repository
        )
        files.update(set(extracted_files))

        return files

    def _get_related_files(
        self, error: ProcessedValidationError, repository: MetricsRepository
    ) -> List[str]:
        """Определяет связанные файлы по логике компонентов."""
        related = []

        # README для всех компонентов
        readme_file = self._find_readme_file(repository)
        if readme_file:
            related.append(readme_file)

        # Диспетчеризация по типу компонента
        component_handlers = {
            "sources": self._get_files_for_sources,
            "dimensions": self._get_files_for_dimensions,
            "metrics": self._get_files_for_metrics,
            "cubes_configs": self._get_files_for_cubes_configs,
            "enrichments": self._get_files_for_enrichments,
        }

        handler = component_handlers.get(error.component)
        if handler:
            related.extend(handler(error, repository))

        return related

    def _get_files_for_sources(
        self, error: ProcessedValidationError, repository: MetricsRepository
    ) -> List[str]:
        """Возвращает файлы для ошибок источников."""
        files = ["sources/sources.yaml"]

        source_names = self._extract_source_names(error)
        if source_names:
            files.extend(f"sources/sql/{name}.sql" for name in source_names)

        return files

    def _get_files_for_dimensions(
        self, error: ProcessedValidationError, repository: MetricsRepository
    ) -> List[str]:
        """Возвращает файлы для ошибок дименшенов."""
        files = ["dimensions/dimensions.yaml"]

        dim_name = self._extract_dimension_name(error)
        if dim_name:
            files.append(f"dimensions/sql/{dim_name}.sql")

            # Добавляем parent dimensions для полного понимания иерархии
            # Например, для city (parent: region) включим и region.sql
            # Это помогает LLM понять связи: city -> region -> country
            hierarchy = self._parse_dimensions_hierarchy(repository)
            parent_dimensions = self._get_parent_dimensions(dim_name, hierarchy)

            # Добавляем SQL файлы всех родителей
            # Пример: для param2 добавим param1.sql, subcategory.sql, category.sql
            for parent_dim in parent_dimensions:
                files.append(f"dimensions/sql/{parent_dim}.sql")

        return files

    def _get_files_for_metrics(
        self, error: ProcessedValidationError, repository: MetricsRepository
    ) -> List[str]:
        """Возвращает файлы для ошибок метрик с умным RAG."""
        files = []

        metric_name = self._extract_metric_name_from_path(error.file)
        if metric_name:
            sources_yaml_content = repository.read_file_safe("sources/sources.yaml")
            if sources_yaml_content:
                parsed_sources = self._parse_sources_yaml(sources_yaml_content)  # todo reuse
                source_names = self._find_sources_for_metric(metric_name, parsed_sources)

                for source_name in source_names:
                    # Partial source section
                    files.append(f"sources/sources.yaml#{source_name}")
                    # SQL file
                    sql_file = parsed_sources[source_name].get("sql_file", "")
                    if sql_file:
                        files.append(f"sources/sql/{sql_file}.sql")

        columns = self._extract_column_names_from_error(error)
        if columns:
            enrichments_catalog = self._parse_enrichments_catalog(repository)
            enrichment_files = self._find_enrichments_for_columns(columns, enrichments_catalog)
            files.extend(enrichment_files)

        files.append("dimensions/dimensions.yaml")
        return files

    def _get_files_for_cubes_configs(
        self, error: ProcessedValidationError, repository: MetricsRepository
    ) -> List[str]:
        """Возвращает файлы для ошибок кубов."""
        return ["dimensions/dimensions.yaml"]

    def _get_files_for_enrichments(
        self, error: ProcessedValidationError, repository: MetricsRepository
    ) -> List[str]:
        """Возвращает файлы для ошибок обогащений."""
        files = ["dimensions/dimensions.yaml"]

        if error.file:
            enrichment_name = Path(error.file).stem
            files.insert(0, error.file)

            enrichments_catalog = self._parse_enrichments_catalog(repository)
            enrichment_info = enrichments_catalog.get(enrichment_name, {})
            sql_file = enrichment_info.get("sql", "")
            if sql_file:
                files.append(f"enrichments/sql/{sql_file}.sql")

        return files

    def _extract_files_from_message(
        self, message: str, component: str, repository: MetricsRepository
    ) -> List[str]:
        """Извлекает имена файлов из сообщения ошибки."""
        files = []

        # Ищем упоминания файлов в сообщении
        file_patterns = [
            r"([a-zA-Z_][a-zA-Z0-9_]*\.(?:yaml|yml|sql))",  # file.yaml или file.sql
            r"(?:file|файл|файле)\s+['\"]?([^'\"\\s]+)['\"]?",  # "file filename"
        ]

        for pattern in file_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            files.extend(matches)

        return files

    def _extract_dimension_name(self, error: ProcessedValidationError) -> Optional[str]:
        """Извлекает имя дименшена из ошибки."""
        message = error.message
        file_path = error.file or ""

        patterns = [
            r"dimension[s]?\s+['\"]([^'\"]+)['\"]",
            r"дименш[а-я]*\s+['\"]?([a-zA-Z_][a-zA-Z0-9_]*)['\"]?",
            r"dimensions/sql/([^/]+)\.sql",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1)

            match = re.search(pattern, file_path, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def _find_sources_in_dict(self, data: Dict, path: str = "") -> List[str]:
        """Рекурсивно ищет ссылки на источники в словаре."""
        sources = []

        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key

            # Ищем ключи которые могут содержать имена источников
            if key.lower() in ["source", "from", "table", "source_name"]:
                if isinstance(value, str):
                    sources.append(value)

            # Рекурсивно обходим вложенные структуры
            if isinstance(value, dict):
                sources.extend(self._find_sources_in_dict(value, current_path))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        sources.extend(self._find_sources_in_dict(item, current_path))

        return sources

    def _prioritize_files(
        self, file_list: List[str], error: ProcessedValidationError
    ) -> List[str]:  # todo readme first
        """Сортирует файлы по важности для анализа ошибки."""
        priority_order = []

        # 1. Файл из ошибки (высший приоритет)
        if error.file and error.file in file_list:
            priority_order.append(error.file)

        # 2. Основные конфигурационные файлы
        config_files = ["sources/sources.yaml", "dimensions/dimensions.yaml"]
        for config_file in config_files:
            if config_file in file_list and config_file not in priority_order:
                priority_order.append(config_file)

        # 3. README файлы (инструкции по настройке репозитория)
        readme_files = [
            f for f in file_list if f.lower().startswith("readme.") and f not in priority_order
        ]
        priority_order.extend(readme_files)

        # 4. SQL файлы (средний приоритет)
        sql_files = [f for f in file_list if f.endswith(".sql") and f not in priority_order]
        priority_order.extend(sql_files)

        # 5. Остальные файлы
        remaining_files = [f for f in file_list if f not in priority_order]
        priority_order.extend(remaining_files)

        return priority_order

    def _find_related_error(
        self, file_path: str, errors: List[ProcessedValidationError]
    ) -> Optional[ProcessedValidationError]:
        """Находит ошибку связанную с конкретным файлом."""
        # Сначала ищем точное совпадение по файлу
        for error in errors:
            if error.file == file_path:
                return error

        # Затем ищем по компоненту
        component_mapping = {
            "sources/sources.yaml": "sources",
            "dimensions/dimensions.yaml": "dimensions",
        }

        if file_path in component_mapping:
            target_component = component_mapping[file_path]
            for error in errors:
                if error.component == target_component:
                    return error

        # Для SQL файлов ищем по имени
        if file_path.endswith(".sql"):
            file_name = Path(file_path).stem
            for error in errors:
                if file_name.lower() in error.message.lower():
                    return error

        return None

    def _parse_sources_yaml(self, sources_yaml_content: str) -> Dict[str, Dict]:
        """
        Парсит sources.yaml и извлекает информацию о каждом источнике.

        Args:
            sources_yaml_content: Содержимое sources.yaml

        Returns:
            Dict с информацией о источниках: {source_name: {sql_file, metric_configs, metrics}}
        """
        try:
            sources_data = yaml.safe_load(sources_yaml_content)
            if not isinstance(sources_data, dict):
                return {}

            parsed_sources = {}
            for source_name, source_config in sources_data.items():
                if not isinstance(source_config, dict):
                    continue

                parsed_sources[source_name] = {
                    "sql_file": source_config.get("sql", ""),
                    "metric_configs": source_config.get("metric_configs", []),
                    "metrics": source_config.get("metrics", []),
                }

            return parsed_sources
        except Exception:
            return {}

    def _extract_source_yaml_section(
        self, source_name: str, sources_yaml_content: str
    ) -> Optional[str]:
        """
        Извлекает секцию конкретного источника из sources.yaml.

        Args:
            source_name: Имя источника
            sources_yaml_content: Содержимое sources.yaml

        Returns:
            YAML секция источника или None если не найдена
        """
        lines = sources_yaml_content.split("\n")
        section_lines = []
        in_section = False

        for i, line in enumerate(lines):
            # Начало секции источника (без отступа)
            if line.strip() and not line.startswith(" ") and line.startswith(f"{source_name}:"):
                in_section = True
                section_lines.append(line)
                continue

            if in_section:
                # Проверяем конец секции (новая секция без отступа)
                if line.strip() and not line.startswith(" ") and ":" in line:
                    break

                # Добавляем строку к секции
                section_lines.append(line)

        return "\n".join(section_lines) if section_lines else None

    def _find_sources_for_metric(
        self, metric_name: str, parsed_sources: Dict[str, Dict]
    ) -> List[str]:
        """
        Находит все источники связанные с метрикой.

        Args:
            metric_name: Имя метрики (без расширения файла)
            parsed_sources: Распарсенные источники из _parse_sources_yaml

        Returns:
            Список имен источников
        """
        sources = []
        for source_name, source_info in parsed_sources.items():
            # Способ 1: через metric_configs (список имен файлов конфигов)
            if metric_name in source_info.get("metric_configs", []):
                sources.append(source_name)
                continue

            # Способ 2: через metrics (явное перечисление метрик)
            if metric_name in source_info.get("metrics", []):
                sources.append(source_name)

        return sources

    def _extract_metric_name_from_path(self, file_path: str) -> Optional[str]:
        """
        Извлекает имя метрики из пути файла.

        Args:
            file_path: Путь к файлу метрики (например, "metrics/billing.yaml")

        Returns:
            Имя метрики без расширения или None
        """
        if not file_path:
            return None

        # Убираем путь и расширение
        file_name = Path(file_path).stem
        return file_name if file_name else None

    def _parse_enrichments_catalog(self, repository: MetricsRepository) -> Dict[str, Dict]:
        """
        Парсит все enrichments файлы для построения каталога.

        Args:
            repository: Репозиторий метрик

        Returns:
            Dict с информацией об enrichments: {enrichment_name: {sql, join_key, calculated_fields}}
        """
        enrichments_catalog = {}

        enrichments_path = repository.repo_path / "enrichments"
        if not enrichments_path.exists():
            return {}

        for enrichment_file in enrichments_path.glob("*.yaml"):
            enrichment_name = enrichment_file.stem
            content = repository.read_file_safe(f"enrichments/{enrichment_file.name}")

            if content:
                try:
                    enrichment_data = yaml.safe_load(content)
                    if isinstance(enrichment_data, dict):
                        enrichments_catalog[enrichment_name] = {
                            "sql": enrichment_data.get("sql", ""),
                            "join_key": enrichment_data.get("join_key", []),
                            "calculated_fields": enrichment_data.get("calculated_fields", {}),
                        }
                except Exception:
                    pass

        return enrichments_catalog

    def _extract_column_names_from_error(self, error: ProcessedValidationError) -> List[str]:
        """
        Извлекает названия колонок из сообщения ошибки.

        Args:
            error: Ошибка валидации

        Returns:
            Список названий колонок
        """
        patterns = [
            r"column[s]?\s+['\"]([^'\"]+)['\"]",
            r"field[s]?\s+['\"]([^'\"]+)['\"]",
            r"колонк[аи]\s+['\"]?([a-zA-Z_][a-zA-Z0-9_]*)['\"]?",
        ]

        columns = []
        for pattern in patterns:
            matches = re.findall(pattern, error.message, re.IGNORECASE)
            columns.extend(matches)

        return list(set(columns))

    def _find_enrichments_for_columns(
        self, columns: List[str], enrichments_catalog: Dict[str, Dict]
    ) -> List[str]:
        """
        Находит enrichments которые содержат указанные колонки.

        Args:
            columns: Список названий колонок
            enrichments_catalog: Каталог enrichments из _parse_enrichments_catalog

        Returns:
            Список имен enrichments файлов
        """
        enrichment_files = []

        for column in columns:
            for enrichment_name, enrichment_info in enrichments_catalog.items():
                calculated_fields = enrichment_info.get("calculated_fields", {})
                if isinstance(calculated_fields, dict) and column in calculated_fields:
                    enrichment_files.append(f"enrichments/{enrichment_name}.yaml")
                    sql_file = enrichment_info.get("sql", "")
                    if sql_file:
                        enrichment_files.append(f"enrichments/sql/{sql_file}.sql")

        return list(set(enrichment_files))

    def _parse_dimensions_hierarchy(self, repository: MetricsRepository) -> Dict[str, str]:
        """
        Парсит dimensions.yaml для построения иерархии parent relationships.

        Args:
            repository: Репозиторий метрик

        Returns:
            Dict вида {dimension_name: parent_dimension_name}
        """
        hierarchy = {}

        dimensions_content = repository.read_file_safe("dimensions/dimensions.yaml")
        if not dimensions_content:
            return {}

        try:
            dimensions_data = yaml.safe_load(dimensions_content)
            if isinstance(dimensions_data, dict):
                for dim_name, dim_config in dimensions_data.items():
                    if isinstance(dim_config, dict) and "parent" in dim_config:
                        hierarchy[dim_name] = dim_config["parent"]
        except Exception:
            pass

        return hierarchy

    def _get_parent_dimensions(self, dimension_name: str, hierarchy: Dict[str, str]) -> List[str]:
        """
        Возвращает список всех родительских dimensions.

        Args:
            dimension_name: Имя dimension
            hierarchy: Иерархия из _parse_dimensions_hierarchy

        Returns:
            Список parent dimensions (от immediate parent до root)
        """
        parents = []
        current = dimension_name

        while current in hierarchy:
            parent = hierarchy[current]
            if parent in parents:
                break
            parents.append(parent)
            current = parent

        return parents

    def _extract_referenced_metrics(self, metric_content: str) -> List[str]:
        """
        Извлекает имена метрик на которые ссылается данная метрика.

        Args:
            metric_content: Содержимое файла метрики

        Returns:
            Список имен referenced метрик
        """
        referenced_metrics = []

        try:
            metric_data = yaml.safe_load(metric_content)
            if not isinstance(metric_data, dict):
                return []

            for metric_type, metrics in metric_data.items():
                if not isinstance(metrics, dict):
                    continue

                for metric_name, metric_config in metrics.items():
                    if not isinstance(metric_config, dict):
                        continue

                    if "counter" in metric_config:
                        referenced_metrics.append(metric_config["counter"])

                    if "num" in metric_config:
                        referenced_metrics.append(metric_config["num"])

                    if "den" in metric_config:
                        referenced_metrics.append(metric_config["den"])

        except Exception:
            pass

        return list(set(referenced_metrics))

    def _find_readme_file(self, repository: MetricsRepository) -> Optional[str]:
        """
        Ищет README файл в корне репозитория.

        Args:
            repository: Репозиторий метрик

        Returns:
            Путь к README файлу относительно корня репозитория или None если не найден
        """
        # Проверяем различные варианты названий README файла
        readme_variants = ["README.md", "readme.md", "Readme.md", "README.MD", "readme.MD"]

        for readme_name in readme_variants:
            readme_path = repository.repo_path / readme_name
            if repository.read_file_safe(readme_path) is not None:
                return readme_name

        return None
