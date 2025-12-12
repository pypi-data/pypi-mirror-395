"""Панель статуса для интерактивного режима."""

from typing import Any, Optional

from textual.events import Mount, Resize
from textual.reactive import reactive
from textual.widgets import Static


class StatusPanel(Static):
    """Панель отображения текущего статуса."""

    # Reactive свойства для автоматического обновления
    branch = reactive("неизвестно")
    repository = reactive("")
    has_changes = reactive(False)
    monitoring_active = reactive(False)
    monitored_paths_count = reactive(0)
    loading_status = reactive("")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.border_title = "Статус"

    def watch_branch(self, branch: str) -> None:
        """Реактивное обновление при изменении ветки."""
        self._update_display()

    def watch_repository(self, repository: str) -> None:
        """Реактивное обновление при изменении репозитория."""
        self._update_display()

    def watch_has_changes(self, has_changes: bool) -> None:
        """Реактивное обновление при изменении статуса изменений."""
        self._update_display()

    def watch_monitoring_active(self, monitoring_active: bool) -> None:
        """Реактивное обновление при изменении статуса мониторинга."""
        self._update_display()

    def watch_monitored_paths_count(self, monitored_paths_count: int) -> None:
        """Реактивное обновление при изменении количества отслеживаемых путей."""
        self._update_display()

    def watch_loading_status(self, loading_status: str) -> None:
        """Реактивное обновление при изменении статуса загрузки."""
        self._update_display()

    def _update_display(self) -> None:
        """Обновляет отображение статуса."""
        try:
            # Укорачиваем путь к репозиторию для отображения
            repo_display = (
                self._shorten_path(self.repository) if self.repository else "не настроен"
            )

            # Статус изменений
            changes_status = "🔶 Есть изменения" if self.has_changes else "✅ Чисто"

            # Статус мониторинга
            monitoring_status = "🟢 Активен" if self.monitoring_active else "🔴 Неактивен"
            paths_info = f"({self.monitored_paths_count} путей)" if self.monitoring_active else ""

            # Получаем размеры виджета для адаптации контента
            width = self.size.width if self.size.width > 0 else 25

            # Адаптируем длину пути под ширину виджета
            max_path_length = max(15, width - 10)
            repo_display = (
                self._shorten_path(self.repository, max_path_length)
                if self.repository
                else "не настроен"
            )

            content = f"""[bold]Текущая ветка:[/bold]
[cyan]{self.branch}[/cyan]

[bold]Репозиторий:[/bold]
[dim]{repo_display}[/dim]

[bold]Изменения:[/bold]
{changes_status}

[bold]Мониторинг:[/bold]
{monitoring_status} {paths_info}"""

            # Добавляем статус загрузки если он есть
            if self.loading_status:
                content += f"\n\n[bold yellow]{self.loading_status}[/bold yellow]"

            self.update(content)
            self.refresh()

            # Логируем для отладки
            self.log.debug(f"StatusPanel updated: size={self.size}, branch={self.branch}")

        except Exception as e:
            self.log.error(f"Ошибка обновления StatusPanel: {e}")
            self.update("[red]Ошибка отображения статуса[/red]")

    def _shorten_path(self, path: str, max_length: int = 40) -> str:
        """Укорачивает длинный путь для отображения."""
        if len(path) <= max_length:
            return path

        # Показываем начало и конец пути
        start_length = max_length // 2 - 3
        end_length = max_length - start_length - 3

        return f"{path[:start_length]}...{path[-end_length:]}"

    async def update_status(
        self,
        branch: Optional[str] = None,
        repository: Optional[str] = None,
        has_changes: Optional[bool] = None,
        monitoring_active: Optional[bool] = None,
        monitored_paths_count: Optional[int] = None,
        loading_status: Optional[str] = None,
    ) -> None:
        """
        Обновляет статус.

        Args:
            branch: Текущая ветка
            repository: Путь к репозиторию
            has_changes: Есть ли незакоммиченные изменения
            monitoring_active: Активен ли мониторинг файловой системы
            monitored_paths_count: Количество отслеживаемых путей
            loading_status: Статус загрузки данных
        """
        if branch is not None:
            self.branch = branch

        if repository is not None:
            self.repository = repository

        if has_changes is not None:
            self.has_changes = has_changes

        if monitoring_active is not None:
            self.monitoring_active = monitoring_active

        if monitored_paths_count is not None:
            self.monitored_paths_count = monitored_paths_count

        if loading_status is not None:
            self.loading_status = loading_status

    def on_mount(self, event: Mount) -> None:
        """Вызывается при монтировании виджета."""
        self._update_display()

    def on_resize(self, event: Resize) -> None:
        """Вызывается при изменении размера терминала."""
        self.call_after_refresh(self._update_display)
