"""Сервис для работы с Git в пользовательском интерфейсе."""

import asyncio
import logging
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from ..git_wrapper import GitWorkflow

logger = logging.getLogger(__name__)


class ValidationResult(BaseModel):
    """Результат валидации операции."""

    is_valid: bool
    error_message: Optional[str] = Field(None, description="Сообщение об ошибке валидации")
    warning_message: Optional[str] = Field(None, description="Предупреждающее сообщение")

    class Config:
        """Конфигурация Pydantic модели."""

        frozen = True  # Делает модель неизменяемой
        str_strip_whitespace = True  # Автоматически убирает пробелы в строках


class SaveResult(BaseModel):
    """Результат операции сохранения."""

    success: bool
    commit_sha: Optional[str] = Field(None, description="SHA хеш созданного коммита")
    task_number: Optional[str] = Field(None, description="Номер задачи")
    error_message: Optional[str] = Field(None, description="Сообщение об ошибке")

    class Config:
        """Конфигурация Pydantic модели."""

        frozen = True
        str_strip_whitespace = True


class PublishResult(BaseModel):
    """Результат операции публикации."""

    success: bool
    pull_request_url: Optional[str] = Field(None, description="URL для создания Pull Request")
    error_message: Optional[str] = Field(None, description="Сообщение об ошибке")

    class Config:
        """Конфигурация Pydantic модели."""

        frozen = True
        str_strip_whitespace = True


class BranchResult(BaseModel):
    """Результат создания ветки."""

    success: bool
    branch_name: Optional[str] = Field(None, description="Название созданной ветки")
    error_message: Optional[str] = Field(None, description="Сообщение об ошибке")

    class Config:
        """Конфигурация Pydantic модели."""

        frozen = True
        str_strip_whitespace = True


class StatusInfo(BaseModel):
    """Информация о статусе Git репозитория."""

    current_branch: str = Field(description="Название текущей ветки")
    has_uncommitted_changes: bool = Field(description="Есть ли незакоммиченные изменения")
    changed_files: Dict[str, List[str]] = Field(
        description="Словарь измененных файлов по категориям"
    )
    commit_history: List[Dict[str, str]] = Field(description="История коммитов")
    diff_summary: Dict[str, int] = Field(description="Сводка изменений")

    class Config:
        """Конфигурация Pydantic модели."""

        frozen = True


class GitUIService:
    """Сервис для Git операций с UI логикой."""

    def __init__(self, git_workflow: Optional[GitWorkflow] = None):
        """
        Инициализация сервиса.

        Args:
            git_workflow: Экземпляр GitWorkflow, если None - Git недоступен
        """
        self._git_workflow = git_workflow

    @property
    def is_available(self) -> bool:
        """Проверяет доступность Git."""
        return self._git_workflow is not None

    def validate_save_operation(self) -> ValidationResult:
        """
        Валидирует возможность сохранения изменений.

        Returns:
            Результат валидации
        """
        if not self.is_available:
            return ValidationResult(is_valid=False, error_message="Git недоступен")

        try:
            current_branch = self._git_workflow.get_current_branch()
            if current_branch in ["master", "main"]:
                return ValidationResult(
                    is_valid=False,
                    error_message=(
                        "Нельзя сохранять изменения напрямую в master ветку.\n"
                        "Сначала нужно переключиться на новую задачу "
                        "и привязать свои изменения к ней."
                    ),
                )

            if not self._git_workflow.has_uncommitted_changes():
                return ValidationResult(
                    is_valid=False, warning_message="Нет изменений для сохранения"
                )

            return ValidationResult(is_valid=True)

        except Exception as e:
            return ValidationResult(is_valid=False, error_message=f"Ошибка при проверке: {e}")

    def validate_publish_operation(self) -> ValidationResult:
        """
        Валидирует возможность публикации изменений.

        Returns:
            Результат валидации
        """
        if not self.is_available:
            return ValidationResult(is_valid=False, error_message="Git недоступен")

        try:
            current_branch = self._git_workflow.get_current_branch()
            if current_branch in ["master", "main"]:
                return ValidationResult(
                    is_valid=False,
                    error_message="Нельзя публиковать напрямую в master/main ветку.\n"
                    "Создайте ветку для задачи через 'Переключиться на новую задачу'",
                )

            if self._git_workflow.has_uncommitted_changes():
                return ValidationResult(
                    is_valid=False,
                    error_message="Обнаружены незакоммиченные изменения.\n"
                    "Сохраните их перед публикацией",
                )

            return ValidationResult(is_valid=True)

        except Exception as e:
            return ValidationResult(is_valid=False, error_message=f"Ошибка при проверке: {e}")

    async def save_changes(
        self,
        message: str,
        task_number: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> SaveResult:
        """
        Сохраняет изменения (создает коммит).

        Args:
            message: Сообщение коммита
            task_number: Номер задачи
            author_name: Имя автора коммита (из JWT токена)
            author_email: Email автора коммита (из JWT токена)

        Returns:
            Результат операции
        """
        if not self.is_available:
            return SaveResult(success=False, error_message="Git недоступен")

        validation = self.validate_save_operation()
        if not validation.is_valid:
            return SaveResult(success=False, error_message=validation.error_message)

        try:
            message = message.strip()
            if not message:
                return SaveResult(success=False, error_message="Введите сообщение коммита")

            task_number = task_number.strip() if task_number else None

            # Выполняем Git операцию в пуле потоков
            loop = asyncio.get_event_loop()
            commit_sha = await loop.run_in_executor(
                None,
                lambda: self._git_workflow.commit_changes(
                    message, task_number, author_name, author_email
                ),
            )

            return SaveResult(success=True, commit_sha=commit_sha, task_number=task_number)

        except Exception as e:
            return SaveResult(success=False, error_message=str(e))

    async def publish_changes(self) -> PublishResult:
        """
        Публикует изменения (push + PR URL).

        Returns:
            Результат операции
        """
        if not self.is_available:
            return PublishResult(success=False, error_message="Git недоступен")

        validation = self.validate_publish_operation()
        if not validation.is_valid:
            return PublishResult(success=False, error_message=validation.error_message)

        try:
            current_branch = self._git_workflow.get_current_branch()

            # Выполняем Git операции в пуле потоков
            loop = asyncio.get_event_loop()

            # Push ветки
            await loop.run_in_executor(None, self._git_workflow.push_branch, current_branch)

            # Генерируем ссылку на PR
            pr_url = await loop.run_in_executor(
                None, self._git_workflow.generate_pull_request_url, current_branch
            )

            return PublishResult(success=True, pull_request_url=pr_url)

        except Exception as e:
            return PublishResult(success=False, error_message=str(e))

    async def create_task_branch(
        self, task_number: Optional[str], description: Optional[str] = None
    ) -> BranchResult:
        """
        Создает новую ветку для задачи.

        Args:
            task_number: Номер задачи (может быть None если не обязателен)
            description: Описание задачи

        Returns:
            Результат операции
        """
        if not self.is_available:
            return BranchResult(success=False, error_message="Git недоступен")

        try:
            # Получаем конфигурацию валидации из backend
            from ..config import config

            cli_config = config.get_cli_config()
            task_required = False
            task_pattern = None
            task_example = "PROJECT-123"

            if cli_config and cli_config.ui:
                task_required = cli_config.ui.task_id_required
                task_pattern = cli_config.ui.task_id_regex
                task_example = cli_config.ui.task_format_example

            # Нормализуем task_number
            task_num = task_number.strip() if task_number else None

            # Валидируем что task_number указан если обязателен
            if task_required and not task_num:
                return BranchResult(
                    success=False,
                    error_message=f"Введите номер задачи (формат: {task_example})"
                )

            description = description.strip() if description else None

            # Выполняем Git операцию в пуле потоков
            loop = asyncio.get_event_loop()
            branch_name = await loop.run_in_executor(
                None,
                lambda: self._git_workflow.create_task_branch(
                    task_number=task_num,
                    description=description,
                    task_required=task_required,
                    task_pattern=task_pattern,
                    task_example=task_example
                )
            )

            return BranchResult(success=True, branch_name=branch_name)

        except Exception as e:
            return BranchResult(success=False, error_message=str(e))

    def get_git_status_info(self) -> StatusInfo:
        """
        Получает полную информацию о статусе Git репозитория.

        Returns:
            Информация о статусе
        """
        if not self.is_available:
            return StatusInfo(
                current_branch="Git недоступен",
                has_uncommitted_changes=False,
                changed_files={"modified": [], "added": [], "deleted": [], "untracked": []},
                commit_history=[],
                diff_summary={"files_changed": 0, "insertions": 0, "deletions": 0},
            )

        try:
            current_branch = self._git_workflow.get_current_branch()
            has_changes = self._git_workflow.has_uncommitted_changes()
            changed_files = self._git_workflow.get_changed_files()
            commit_history = self._git_workflow.get_commit_history()
            diff_summary = self._git_workflow.get_diff_summary()

            return StatusInfo(
                current_branch=current_branch,
                has_uncommitted_changes=has_changes,
                changed_files=changed_files,
                commit_history=commit_history,
                diff_summary=diff_summary,
            )

        except Exception as e:
            logger.warning(f"Ошибка получения статуса Git: {e}", exc_info=True)
            return StatusInfo(
                current_branch="Ошибка",
                has_uncommitted_changes=False,
                changed_files={"modified": [], "added": [], "deleted": [], "untracked": []},
                commit_history=[],
                diff_summary={"files_changed": 0, "insertions": 0, "deletions": 0},
            )

    def format_git_status_content(self) -> str:
        """
        Форматирует информацию о статусе Git для отображения в UI.

        Returns:
            Отформатированный текст статуса
        """
        status = self.get_git_status_info()

        content = "[bold blue]Статус репозитория:[/bold blue]\n\n"
        content += f"Ветка: [cyan]{status.current_branch}[/cyan]\n"

        if status.has_uncommitted_changes:
            content += "[yellow]⚠ Есть незакоммиченные изменения[/yellow]\n\n"

            changes = status.changed_files
            if changes.get("modified"):
                content += f"[yellow]Изменены ({len(changes['modified'])}):[/yellow]\n"
                for file in changes["modified"][:10]:
                    content += f"  • {file}\n"
                if len(changes["modified"]) > 10:
                    content += f"  ... и еще {len(changes['modified']) - 10}\n"
                content += "\n"

            if changes.get("added"):
                content += f"[green]Добавлены ({len(changes['added'])}):[/green]\n"
                for file in changes["added"][:5]:
                    content += f"  • {file}\n"
                if len(changes["added"]) > 5:
                    content += f"  ... и еще {len(changes['added']) - 5}\n"
                content += "\n"

            if changes.get("deleted"):
                content += f"[red]Удалены ({len(changes['deleted'])}):[/red]\n"
                for file in changes["deleted"][:5]:
                    content += f"  • {file}\n"
                if len(changes["deleted"]) > 5:
                    content += f"  ... и еще {len(changes['deleted']) - 5}\n"
                content += "\n"

            if changes.get("untracked"):
                content += f"[blue]Не отслеживаются ({len(changes['untracked'])}):[/blue]\n"
                for file in changes["untracked"][:5]:
                    content += f"  • {file}\n"
                if len(changes["untracked"]) > 5:
                    content += f"  ... и еще {len(changes['untracked']) - 5}\n"
        else:
            content += "[green]✓ Рабочая директория чистая[/green]\n\n"

        return content

    def format_branch_info_for_publish(self) -> str:
        """
        Форматирует информацию о ветке для диалога публикации.

        Returns:
            Отформатированная информация о ветке
        """
        status = self.get_git_status_info()

        info = f"Текущая ветка: [cyan]{status.current_branch}[/cyan]\n"

        if status.commit_history:
            info += f"Коммитов: {len(status.commit_history)}\n"

        if status.diff_summary["files_changed"] > 0:
            info += (
                f"Файлов изменено: {status.diff_summary['files_changed']}, "
                f"добавлений: +{status.diff_summary['insertions']}, "
                f"удалений: -{status.diff_summary['deletions']}"
            )

        return info

    def extract_task_from_branch(self, branch_name: str) -> str:
        """
        Извлекает номер задачи из названия ветки.

        Args:
            branch_name: Название ветки

        Returns:
            Номер задачи или пустая строка
        """
        import re

        match = re.search(r"([A-Z]+-\d+)", branch_name.upper())
        return match.group(1) if match else ""
