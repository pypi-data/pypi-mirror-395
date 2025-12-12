"""Widgets that do not auto-scroll the container when focused."""

from textual.widgets import Input, OptionList, Select


class NoScrollInput(Input):
    """Input that disables scroll-to-visible on focus."""

    def focus(self, scroll_visible: bool = True) -> None:  # type: ignore[override]
        try:
            super().focus(scroll_visible=False)
        except TypeError:
            super().focus()


class NoScrollSelect(Select):
    """Select that disables scroll-to-visible on focus."""

    def focus(self, scroll_visible: bool = True) -> None:  # type: ignore[override]
        try:
            super().focus(scroll_visible=False)
        except TypeError:
            super().focus()


class NoScrollOptionList(OptionList):
    """OptionList that disables scroll-to-visible on focus."""

    def focus(self, scroll_visible: bool = True) -> None:  # type: ignore[override]
        try:
            super().focus(scroll_visible=False)
        except TypeError:
            super().focus()
