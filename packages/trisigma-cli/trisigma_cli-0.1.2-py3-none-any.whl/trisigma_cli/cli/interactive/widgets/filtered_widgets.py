"""Композитные виджеты с поиском на основе встроенных Textual компонентов."""

from typing import Any, List, Optional, Set, Tuple

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Select, SelectionList
from textual.widgets.selection_list import Selection

MIN_SEARCH_LENGTH = 3
MAX_DISPLAYED_OPTIONS = 100


class FilteredSelect(Vertical):
    """Виджет для выбора одного элемента с поиском по подстроке.

    Композит из Input (поиск) + Select (выбор).
    Список опций открывается при фокусе на Input и закрывается при потере фокуса.
    """

    DEFAULT_CSS = """
    FilteredSelect {
        padding: 0;
        margin: 0;
        height: auto;
        content-align: left top;
    }
    FilteredSelect > Input#search-input {
        padding: 0;
        margin: 0 0 1 0;
        height: 3;
        min-height: 3;
        max-height: 3;
    }
    FilteredSelect > Select#item-select {
        padding: 0;
        margin: 0;
        height: 3;
    }
    FilteredSelect .hidden {
        display: none;
    }
    """

    def __init__(
        self, placeholder: str = "Поиск...", prompt: str = "Выберите элемент", **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self._all_options: List[Tuple[str, str]] = []
        self._filtered_options: List[Tuple[str, str]] = []
        self._total_matches: int = 0
        self._placeholder = placeholder
        self._prompt = prompt
        self._is_expanded: bool = False
        self._selected_value: Optional[str] = None
        self._selected_label: Optional[str] = None

    def compose(self) -> ComposeResult:
        """Создает интерфейс виджета."""
        yield Input(placeholder=self._placeholder, id="search-input")
        yield Select([], prompt=self._prompt, allow_blank=True, id="item-select")

    def on_mount(self) -> None:
        """Инициализация при монтировании."""
        self._update_select_options()

    def _update_select_options(self) -> None:
        """Обновляет опции в Select."""
        try:
            select = self.query_one("#item-select", Select)
            select.set_options(self._filtered_options)
        except Exception:
            pass

    def _update_search_placeholder(self) -> None:
        """Обновляет placeholder с информацией о количестве результатов."""
        try:
            search_input = self.query_one("#search-input", Input)
            if self._total_matches > MAX_DISPLAYED_OPTIONS:
                search_input.placeholder = self._placeholder
            else:
                search_input.placeholder = self._placeholder
        except Exception:
            pass

    def on_input_changed(self, event: Input.Changed) -> None:
        """Обработка изменения поискового запроса."""
        if event.input.id == "search-input":
            search_term = event.value.lower().strip()

            if search_term and len(search_term) >= MIN_SEARCH_LENGTH:
                exact_matches = []
                startswith_matches = []
                contains_matches = []

                for label, value in self._all_options:
                    label_lower = label.lower()
                    if label_lower == search_term:
                        exact_matches.append((label, value))
                    elif label_lower.startswith(search_term):
                        startswith_matches.append((label, value))
                    elif search_term in label_lower:
                        contains_matches.append((label, value))

                all_matches = exact_matches + startswith_matches + contains_matches
                self._total_matches = len(all_matches)
                self._filtered_options = all_matches[:MAX_DISPLAYED_OPTIONS]
            else:
                self._total_matches = len(self._all_options)
                self._filtered_options = self._all_options[:MAX_DISPLAYED_OPTIONS]

            self._update_select_options()
            self._update_search_placeholder()

    @property
    def value(self) -> Any:
        """Возвращает выбранное значение."""
        try:
            return self.query_one("#item-select", Select).value
        except Exception:
            return None

    def set_options(self, options: List[Tuple[str, str]]) -> None:
        """Устанавливает список опций для выбора.

        Args:
            options: Список кортежей (label, value)
        """
        self._all_options = options.copy()
        self._filtered_options = options[:MAX_DISPLAYED_OPTIONS]

        try:
            self.query_one("#search-input", Input).value = ""
        except Exception:
            pass

        self._update_select_options()


class FilteredSelectionList(Vertical):
    """Виджет для множественного выбора элементов с поиском по подстроке.

    Композит из Input (поиск) + SelectionList (множественный выбор).
    Сохраняет выбранные элементы при фильтрации.
    """

    DEFAULT_CSS = """
    FilteredSelectionList {
        padding: 0;
        margin: 0;
        height: auto;
        content-align: left top;
    }
    FilteredSelectionList > Input#search-input {
        padding: 0;
        margin: 0 0 1 0;
        height: 3;
        min-height: 3;
        max-height: 3;
    }
    FilteredSelectionList > SelectionList#item-list {
        padding: 0;
        margin: 0;
        height: auto;
        max-height: 10;
    }
    """

    def __init__(self, placeholder: str = "Поиск...", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._all_options: List[str] = []
        self._filtered_options: List[str] = []
        self._selected_values: Set[str] = set()
        self._total_matches: int = 0
        self._placeholder = placeholder

    def compose(self) -> ComposeResult:
        """Создает интерфейс виджета."""
        yield Input(placeholder=self._placeholder, id="search-input")
        yield SelectionList[str](id="item-list")

    def on_mount(self) -> None:
        """Инициализация при монтировании."""
        self._update_selection_list()

    def _update_selection_list(self) -> None:
        """Обновляет опции в SelectionList с сохранением выбранных.

        Выбранные элементы всегда отображаются вверху списка,
        независимо от текущего поискового запроса.
        """
        try:
            selection_list = self.query_one("#item-list", SelectionList)
            selection_list.clear_options()

            # 1. Сначала добавляем все выбранные элементы (всегда видны)
            selected_sorted = sorted(self._selected_values)
            for option in selected_sorted:
                selection_list.add_option(Selection(option, option, True))

            # 2. Затем добавляем отфильтрованные невыбранные элементы
            unselected_options = [
                opt for opt in self._filtered_options if opt not in self._selected_values
            ]
            for option in unselected_options:
                selection_list.add_option(Selection(option, option, False))
        except Exception:
            pass

    def _update_search_placeholder(self) -> None:
        """Обновляет placeholder с информацией о количестве результатов."""
        try:
            search_input = self.query_one("#search-input", Input)
            selected_count = len(self._selected_values)

            if selected_count > 0:
                base_text = f"{self._placeholder} (выбрано: {selected_count})"
            else:
                base_text = self._placeholder

            search_input.placeholder = base_text
        except Exception:
            pass

    def on_input_changed(self, event: Input.Changed) -> None:
        """Обработка изменения поискового запроса."""
        if event.input.id == "search-input":
            search_term = event.value.lower().strip()

            if search_term and len(search_term) >= MIN_SEARCH_LENGTH:
                exact_matches = []
                startswith_matches = []
                contains_matches = []

                for option in self._all_options:
                    option_lower = option.lower()
                    if option_lower == search_term:
                        exact_matches.append(option)
                    elif option_lower.startswith(search_term):
                        startswith_matches.append(option)
                    elif search_term in option_lower:
                        contains_matches.append(option)

                all_matches = exact_matches + startswith_matches + contains_matches
                self._total_matches = len(all_matches)
                self._filtered_options = all_matches[:MAX_DISPLAYED_OPTIONS]
            else:
                self._total_matches = len(self._all_options)
                self._filtered_options = self._all_options[:MAX_DISPLAYED_OPTIONS]

            self._update_selection_list()
            self._update_search_placeholder()

    def on_selection_list_selected_changed(self, event: SelectionList.SelectedChanged) -> None:
        """Обработка изменения выбранных элементов."""
        if event.selection_list.id == "item-list":
            self._selected_values = set(event.selection_list.selected)
            self._update_search_placeholder()

    @property
    def selected(self) -> List[str]:
        """Возвращает список выбранных значений."""
        return list(self._selected_values)

    def set_options(self, options: List[str]) -> None:
        """Устанавливает список опций для выбора.

        Args:
            options: Список значений для выбора
        """
        self._all_options = sorted(options)
        self._filtered_options = self._all_options[:MAX_DISPLAYED_OPTIONS]
        self._selected_values.clear()

        try:
            self.query_one("#search-input", Input).value = ""
        except Exception:
            pass

        self._update_selection_list()
