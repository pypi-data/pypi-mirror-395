from typing import Optional

from textual.reactive import reactive
from textual.widgets import Static


class UpdateBanner(Static):
    current_version: reactive[str] = reactive("")
    latest_version: reactive[str] = reactive("")
    is_visible: reactive[bool] = reactive(False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def watch_current_version(self, current_version: str) -> None:
        self._update_display()

    def watch_latest_version(self, latest_version: str) -> None:
        self._update_display()

    def watch_is_visible(self, is_visible: bool) -> None:
        self._update_display()
        if is_visible:
            self.add_class("visible")
        else:
            self.remove_class("visible")

    def _update_display(self) -> None:
        if not self.is_visible:
            self.update("")
            return

        content = (
            f"⚠️  Доступно обновление: {self.current_version} → {self.latest_version} "
            f"| Выполните: [bold black]trisigma self-update[/bold black]"
        )
        self.update(content)

    def update_version(
        self,
        current_version: Optional[str] = None,
        latest_version: Optional[str] = None,
        is_visible: Optional[bool] = None,
    ) -> None:
        if current_version is not None:
            self.current_version = current_version

        if latest_version is not None:
            self.latest_version = latest_version

        if is_visible is not None:
            self.is_visible = is_visible

    def on_mount(self) -> None:
        self._update_display()
