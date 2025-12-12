"""Обертка над Git для управления рабочими процессами."""

import re
from pathlib import Path
from typing import Dict, List, Optional

from git import Actor, GitCommandError, InvalidGitRepositoryError, PushInfo, Repo

from ..utils.exceptions import GitError
from ..utils.transliteration import transliterate_cyrillic
from ..utils.validation import sanitize_commit_message, validate_task_number


class GitWorkflow:
    """Менеджер Git workflow для репозитория метрик."""

    def __init__(self, repo_path: str):
        """
        Инициализирует Git workflow.

        Args:
            repo_path: Путь к Git репозиторию

        Raises:
            GitError: Если путь не является Git репозиторием или Git недоступен
        """
        self.repo_path = Path(repo_path)
        self._repo: Optional[Repo] = None

    @property
    def repo(self) -> Repo:
        """Ленивая инициализация git репозитория."""
        if self._repo is None:
            try:
                self._repo = Repo(str(self.repo_path))
            except InvalidGitRepositoryError:
                raise GitError(f"Директория не является Git репозиторием: {self.repo_path}")
        return self._repo

    def get_current_branch(self) -> str:
        """
        Получает название текущей ветки.

        Returns:
            Название текущей ветки

        Raises:
            GitError: При ошибке Git
        """
        try:
            return str(self.repo.active_branch)
        except Exception as e:
            raise GitError(f"Не удалось получить текущую ветку: {e}")

    def get_branches(self) -> List[str]:
        """
        Получает список всех локальных веток.

        Returns:
            Список названий веток

        Raises:
            GitError: При ошибке Git
        """
        try:
            return [b.name for b in self.repo.branches]
        except Exception as e:
            raise GitError(f"Не удалось получить список веток: {e}")

    def has_uncommitted_changes(self) -> bool:
        """
        Проверяет есть ли незакоммиченные изменения.

        Returns:
            True если есть незакоммиченные изменения
        """
        return (
            self.repo.is_dirty()
            or len(self.repo.untracked_files) > 0
            or len(self.repo.index.diff("HEAD")) > 0
        )

    def get_changed_files(self) -> Dict[str, List[str]]:
        """
        Получает список измененных файлов.

        Сравнивает рабочую директорию с HEAD (последним коммитом).
        Это показывает реальное состояние файлов независимо от индекса.

        Returns:
            Словарь с категориями измененных файлов
        """
        try:
            diff_items = self.repo.head.commit.diff(None)
        except ValueError:
            diff_items = []

        return {
            "modified": [
                item.a_path for item in diff_items if item.change_type == "M" and item.a_path
            ],
            "added": [
                item.b_path for item in diff_items if item.change_type == "A" and item.b_path
            ],
            "deleted": [
                item.a_path for item in diff_items if item.change_type == "D" and item.a_path
            ],
            "untracked": self.repo.untracked_files,
        }

    def _detect_default_branch(self) -> str:
        """
        Получает default/target ветку из конфигурации backend.

        Returns:
            Название default ветки из backend config

        Raises:
            GitError: Если конфигурация backend недоступна
        """
        from .config import config

        cli_config = config.get_cli_config()
        if not cli_config or not cli_config.git or not cli_config.git.default_branch:
            raise GitError(
                "Default branch configuration is not available. "
                "Run 'trisigma init' to refresh configuration from backend."
            )

        return cli_config.git.default_branch

    def create_task_branch(
        self,
        task_number: Optional[str] = None,
        description: Optional[str] = None,
        task_required: bool = True,
        task_pattern: Optional[str] = None,
        task_example: str = "PROJECT-123"
    ) -> str:
        """
        Создает новую ветку для задачи.
        Всегда создает ветку от обновленного default branch.

        Args:
            task_number: Номер задачи (например AB-1000), может быть None если task_required=False
            description: Краткое описание (опционально)
            task_required: Обязательно ли указание task ID (из backend config)
            task_pattern: Regex паттерн для валидации task ID (из backend config)
            task_example: Пример формата task ID для сообщений об ошибках

        Returns:
            Название созданной ветки

        Raises:
            GitError: При ошибке создания ветки
        """
        # Валидируем номер задачи с учетом настроек из конфига
        validated_task = validate_task_number(
            task_number or "",
            required=task_required,
            pattern=task_pattern,
            example=task_example
        )

        # Формируем название ветки
        if description:
            # Транслитерируем кириллицу в латиницу
            transliterated_desc = transliterate_cyrillic(description)
            # Очищаем описание для имени ветки
            clean_desc = re.sub(r"[^a-zA-Z0-9\s-]", "", transliterated_desc.lower())
            clean_desc = re.sub(r"\s+", "-", clean_desc.strip())[:30]

            # Если есть task_number, добавляем его как префикс
            if validated_task:
                branch_name = f"{validated_task.lower()}-{clean_desc}"
            else:
                branch_name = clean_desc
        else:
            # Если нет description, но есть task_number
            if validated_task:
                branch_name = validated_task.lower()
            else:
                # Нет ни task_number ни description - генерируем автоимя
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                branch_name = f"feature-{timestamp}"

        try:
            # Определяем текущую ветку и защищённые ветки
            current_branch = self.get_current_branch()
            protected_branches = ["master", "main"]

            # Проверяем есть ли незакоммиченные изменения
            has_changes = self.has_uncommitted_changes()
            use_stash = False

            if has_changes:
                # Если мы в защищённой ветке (master/main) - используем stash для переноса изменений
                if current_branch in protected_branches:
                    use_stash = True
                    # Сохраняем изменения в stash
                    self.repo.git.stash(
                        "push", "-u", "-m", f"CLI: переключение на {branch_name}"
                    )
                else:
                    # Если в другой ветке - требуем сначала закоммитить
                    raise GitError(
                        "Обнаружены незакоммиченные изменения. "
                        "Выполните 'trisigma sl save' перед созданием новой ветки."
                    )

            # Определяем основную ветку (master или main)
            master_branch = "master"
            if master_branch not in self.get_branches():
                master_branch = "main"

            # Переключаемся на master для обновления (изменения уже в stash если были)
            if current_branch != master_branch:
                self.repo.git.checkout(master_branch)

            # ОБЯЗАТЕЛЬНО обновляем master из origin
            try:
                self.repo.remotes.origin.pull()
            except GitCommandError:
                # Если pull завершился с ошибкой, пробуем fetch
                try:
                    self.repo.remotes.origin.fetch()
                    # Сбрасываем локальный master на origin/master
                    self.repo.git.reset("--hard", f"origin/{master_branch}")
                except Exception:
                    raise GitError(
                        f"Не удалось обновить {master_branch} из origin. "
                        "Проверьте подключение к интернету и права доступа к репозиторию."
                    )
            except Exception as e:
                # Для любых других ошибок тоже пробуем fetch
                try:
                    self.repo.remotes.origin.fetch()
                    self.repo.git.reset("--hard", f"origin/{master_branch}")
                except Exception:
                    raise GitError(f"Не удалось обновить {master_branch} из origin: {e}")

            # Если ветка уже существует - удаляем её и создаем заново от свежего master
            if branch_name in self.get_branches():
                # Если мы находимся на этой ветке, переключаемся на master
                if self.get_current_branch() == branch_name:
                    self.repo.git.checkout(master_branch)

                # Удаляем локальную ветку
                self.repo.git.branch("-D", branch_name)

            # Создаем новую ветку от обновленного master
            new_branch = self.repo.create_head(branch_name, master_branch)
            new_branch.checkout()

            # Если использовали stash - восстанавливаем изменения в новой ветке
            if use_stash:
                try:
                    self.repo.git.stash("pop")
                except GitCommandError as e:
                    raise GitError(
                        f"Не удалось применить сохранённые изменения в новой ветке: {e}. "
                        "Изменения остались в stash, используйте 'git stash pop' для ручного применения."
                    )

            return branch_name

        except GitCommandError as e:
            raise GitError(f"Не удалось создать ветку '{branch_name}': {e}")
        except Exception as e:
            raise GitError(f"Ошибка при создании ветки: {e}")

    def commit_changes(
        self,
        message: str,
        task_number: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> str:
        """
        Коммитит все изменения.

        Args:
            message: Сообщение коммита
            task_number: Номер задачи для добавления в начало сообщения
            author_name: Имя автора коммита (из JWT токена)
            author_email: Email автора коммита (из JWT токена)

        Returns:
            SHA коммита

        Raises:
            GitError: При ошибке коммита
        """
        try:
            # Очищаем сообщение коммита
            clean_message = sanitize_commit_message(message)

            # Добавляем номер задачи если указан
            if task_number:
                validated_task = validate_task_number(task_number)
                clean_message = f"[{validated_task}] {clean_message}"

            # Проверяем есть ли что коммитить
            if not self.has_uncommitted_changes():
                raise GitError("Нет изменений для коммита")

            # Сначала добавляем все SQL и YAML файлы (важные файлы метрик)
            self._add_metrics_files()

            # Затем добавляем все остальные файлы (кроме игнорируемых)
            self.repo.git.add(".")

            # Проверяем наличие информации об авторе
            if not author_name or not author_email:
                raise GitError(
                    "Не удалось получить информацию об авторе из JWT токена. "
                    "Выполните 'trisigma login' для повторной авторизации."
                )

            # Настраиваем автора и коммиттера
            author = Actor(author_name, author_email)
            committer = Actor(author_name, author_email)

            # Коммитим
            commit = self.repo.index.commit(clean_message, author=author, committer=committer)

            return commit.hexsha

        except GitCommandError as e:
            raise GitError(f"Не удалось создать коммит: {e}")
        except Exception as e:
            raise GitError(f"Ошибка при коммите: {e}")

    def _add_metrics_files(self) -> None:
        """
        Добавляет все SQL и YAML файлы в индекс Git.
        Это важно для обеспечения того, чтобы все изменения в метриках попали в коммит.
        """
        try:
            # Добавляем все YAML файлы (метрики, дименшены, обогащения)
            self.repo.git.add("*.yaml", "*.yml")

            # Добавляем все SQL файлы (DDL, источники)
            self.repo.git.add("*.sql")

            # Добавляем конкретные директории с метриками
            metrics_dirs = ["metrics/", "dimensions/", "enrichments/", "sources/", "ddl/"]
            for dir_name in metrics_dirs:
                dir_path = self.repo_path / dir_name
                if dir_path.exists():
                    self.repo.git.add(f"{dir_name}")

        except GitCommandError:
            # Не критично если некоторые файлы не найдены
            pass
        except Exception:
            # Игнорируем любые ошибки при добавлении файлов
            pass

    def push_branch(self, branch_name: Optional[str] = None) -> None:
        """
        Отправляет ветку в удаленный репозиторий.

        Args:
            branch_name: Название ветки (по умолчанию текущая)

        Raises:
            GitError: При ошибке push
        """
        if branch_name is None:
            branch_name = self.get_current_branch()

        try:
            # Проверяем есть ли незакоммиченные изменения
            if self.has_uncommitted_changes():
                raise GitError(
                    "Обнаружены незакоммиченные изменения. Выполните коммит перед публикацией."
                )

            # Отправляем ветку
            origin = self.repo.remotes.origin

            # Проверяем существует ли ветка в удаленном репозитории
            remote_branches = [ref.name.split("/")[-1] for ref in origin.refs]

            # Выполняем push и сохраняем результат
            if branch_name not in remote_branches:
                # Первый push с установкой upstream
                push_infos = origin.push(f"{branch_name}:{branch_name}", set_upstream=True)
            else:
                # Обычный push
                push_infos = origin.push(branch_name)

            # Проверяем результаты push
            self._check_push_results(push_infos, branch_name)

        except GitCommandError as e:
            if "rejected" in str(e).lower():
                raise GitError(
                    "Push отклонен. Возможно ветка была обновлена в удаленном репозитории. "
                    "Выполните pull перед push."
                )
            raise GitError(f"Не удалось отправить ветку '{branch_name}': {e}")
        except GitError:
            # Пробрасываем GitError без изменений
            raise
        except Exception as e:
            raise GitError(f"Ошибка при push: {e}")

    def _check_push_results(self, push_infos: List[PushInfo], branch_name: str) -> None:
        """
        Проверяет результаты push операции на наличие ошибок.

        Args:
            push_infos: Список результатов push от GitPython
            branch_name: Название ветки

        Raises:
            GitError: Если обнаружены ошибки в результатах push
        """
        for push_info in push_infos:
            flags = push_info.flags

            if flags & PushInfo.ERROR:
                raise GitError(
                    f"Ошибка при push ветки '{branch_name}': {push_info.summary or 'неизвестная ошибка'}"
                )

            if flags & PushInfo.REJECTED:
                raise GitError(
                    f"Push ветки '{branch_name}' отклонен удаленным репозиторием. "
                    f"Возможно ветка была обновлена. Выполните pull перед push. "
                    f"Детали: {push_info.summary or 'нет информации'}"
                )

            if flags & PushInfo.REMOTE_REJECTED:
                raise GitError(
                    f"Push ветки '{branch_name}' отклонен pre-receive hook на сервере. "
                    f"Детали: {push_info.summary or 'нет информации'}"
                )

            if flags & PushInfo.REMOTE_FAILURE:
                raise GitError(
                    f"Ошибка на удаленном сервере при push ветки '{branch_name}'. "
                    f"Детали: {push_info.summary or 'нет информации'}"
                )

    def add_metrics_files(self) -> List[str]:
        """
        Явно добавляет все SQL и YAML файлы в индекс Git.

        Returns:
            Список добавленных файлов

        Raises:
            GitError: При ошибке добавления файлов
        """
        try:
            added_files = []

            # Получаем все SQL и YAML файлы в репозитории
            sql_files = list(self.repo_path.rglob("*.sql"))
            yaml_files = list(self.repo_path.rglob("*.yaml")) + list(self.repo_path.rglob("*.yml"))

            all_files = sql_files + yaml_files

            for file_path in all_files:
                # Проверяем что файл не в .git директории
                if ".git" not in str(file_path):
                    try:
                        relative_path = file_path.relative_to(self.repo_path)
                        self.repo.git.add(str(relative_path))
                        added_files.append(str(relative_path))
                    except Exception:
                        # Игнорируем ошибки для отдельных файлов
                        continue

            return added_files

        except Exception as e:
            raise GitError(f"Не удалось добавить файлы метрик: {e}")

    def get_remote_url(self) -> str:
        """
        Получает URL удаленного репозитория.

        Returns:
            URL удаленного репозитория

        Raises:
            GitError: Если не удалось получить URL
        """
        try:
            origin = self.repo.remotes.origin
            return origin.url
        except Exception as e:
            raise GitError(f"Не удалось получить URL удаленного репозитория: {e}")

    def generate_pull_request_url(self, branch_name: str = None) -> str:
        """
        Генерирует URL для создания Pull Request используя template из backend config.

        Args:
            branch_name: Название ветки (по умолчанию текущая)

        Returns:
            URL для создания PR

        Raises:
            GitError: Если template не настроен или при ошибке генерации URL
        """
        if branch_name is None:
            branch_name = self.get_current_branch()

        target_branch = self._detect_default_branch()

        from .config import config

        cli_config = config.get_cli_config()
        if not cli_config or not cli_config.git or not cli_config.git.pr_url_template:
            raise GitError(
                "PR URL template не настроен. Выполните 'trisigma init' для обновления конфигурации."
            )

        return cli_config.git.pr_url_template.format(
            source_branch=branch_name, target_branch=target_branch
        )

    def _get_default_branch_name(self) -> str:
        """
        Определяет название основной ветки репозитория (master или main).

        Returns:
            Название основной ветки
        """
        branches = self.get_branches()
        if "master" in branches:
            return "master"
        elif "main" in branches:
            return "main"
        # Fallback: пытаемся получить из remote
        try:
            # Получаем default branch из origin/HEAD
            head_ref = self.repo.git.symbolic_ref("refs/remotes/origin/HEAD", short=True)
            return head_ref.replace("origin/", "")
        except Exception:
            # Если ничего не работает, возвращаем master
            return "master"

    def get_commit_history(self, since_branch: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Получает историю коммитов с момента отделения от указанной ветки.

        Args:
            since_branch: Ветка от которой считать (если None — автоопределение master/main)

        Returns:
            Список коммитов
        """
        try:
            current_branch = self.get_current_branch()

            # Автоопределение базовой ветки если не указана
            if since_branch is None:
                since_branch = self._get_default_branch_name()

            # Если мы на базовой ветке — нет истории для показа
            if current_branch == since_branch:
                return []

            # Проверяем что базовая ветка существует
            if since_branch not in self.get_branches():
                return []

            # Получаем коммиты, которых нет в базовой ветке
            commits = list(self.repo.iter_commits(f"{since_branch}..{current_branch}"))

            result = []
            for commit in reversed(commits):  # От старых к новым
                result.append(
                    {
                        "sha": commit.hexsha[:8],
                        "message": commit.message.strip(),
                        "author": str(commit.author),
                        "date": commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

            return result

        except GitCommandError as e:
            raise GitError(f"Не удалось получить историю коммитов: {e}")
        except Exception as e:
            raise GitError(f"Ошибка при получении истории: {e}")

    def get_diff_summary(self, since_branch: Optional[str] = None) -> Dict[str, int]:
        """
        Получает сводку изменений с момента отделения от указанной ветки.

        Args:
            since_branch: Ветка от которой считать (если None — автоопределение master/main)

        Returns:
            Словарь со статистикой изменений
        """
        try:
            current_branch = self.get_current_branch()

            # Автоопределение базовой ветки если не указана
            if since_branch is None:
                since_branch = self._get_default_branch_name()

            # Если мы на базовой ветке — нет diff для показа
            if current_branch == since_branch:
                return {"files_changed": 0, "insertions": 0, "deletions": 0}

            # Проверяем что базовая ветка существует
            if since_branch not in self.get_branches():
                return {"files_changed": 0, "insertions": 0, "deletions": 0}

            # Получаем diff статистику
            diff = self.repo.git.diff("--stat", f"{since_branch}..{current_branch}")

            # Парсим статистику
            stats = {"files_changed": 0, "insertions": 0, "deletions": 0}

            lines = diff.strip().split("\n")
            if len(lines) > 1:
                summary_line = lines[-1]  # Последняя строка содержит сводку

                # Парсим строку вида "5 files changed, 123 insertions(+), 45 deletions(-)"
                parts = summary_line.split(",")

                for part in parts:
                    part = part.strip()
                    if "file" in part:
                        stats["files_changed"] = int(part.split()[0])
                    elif "insertion" in part:
                        stats["insertions"] = int(part.split()[0])
                    elif "deletion" in part:
                        stats["deletions"] = int(part.split()[0])

            return stats

        except Exception:
            # При любой ошибке возвращаем пустую статистику
            return {"files_changed": 0, "insertions": 0, "deletions": 0}
