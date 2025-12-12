"""Dropdown виджеты с поиском - списки раскрываются при фокусе."""

from typing import Any, List, Optional, Tuple

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Key
from textual.timer import Timer
from textual.widgets import Input, SelectionList
from textual.widgets.selection_list import Selection

MAX_DISPLAYED_OPTIONS = 100


class DropdownSelect(Vertical):
    """Выпадающий список для выбора одного элемента.

    Список скрыт по умолчанию, раскрывается при фокусе на Input.
    Поддерживает поиск по подстроке без необходимости клика.
    При выборе - закрывается и показывает выбранное значение.
    """

    DEFAULT_CSS = """
    DropdownSelect {
        padding: 0;
        margin: 0;
        height: auto;
        content-align: left top;
    }
    DropdownSelect > Input#search-input {
        padding: 0;
        margin: 0;
        height: 3;
        min-height: 3;
        max-height: 3;
    }
    DropdownSelect > SelectionList#item-list {
        padding: 0;
        margin: 0;
        height: auto;
        max-height: 10;
    }
    """

    def __init__(
        self,
        placeholder: str = "Выберите...",
        prompt: str = "Начните вводить для поиска",
        **kwargs: Any,
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
        self._collapse_timer: Optional[Timer] = None

    def compose(self) -> ComposeResult:
        """Создает интерфейс виджета."""
        yield Input(placeholder=self._placeholder, id="search-input")
        yield SelectionList[str](id="item-list")

    def on_mount(self) -> None:
        """Инициализация при монтировании."""
        self._update_list_options()
        try:
            item_list = self.query_one("#item-list", SelectionList)
            item_list.display = False
        except Exception:
            pass

        try:
            search_input = self.query_one("#search-input", Input)
            search_input.watch(search_input, "has_focus", self._on_input_focus_changed)
        except Exception:
            pass

    def _on_input_focus_changed(self, has_focus: bool) -> None:
        """Обработка изменения фокуса на поле поиска."""
        if has_focus:
            if self._collapse_timer:
                self._collapse_timer.stop()
                self._collapse_timer = None
            self._expand()
        else:
            self._collapse_timer = self.set_timer(0.3, self._collapse)

    def on_key(self, event: Key) -> None:
        """Обработка нажатия клавиш."""
        if event.key == "escape" and self._is_expanded:
            self._collapse()
            event.stop()
            event.prevent_default()

    def _update_list_options(self) -> None:
        """Обновляет опции в SelectionList."""
        try:
            item_list = self.query_one("#item-list", SelectionList)
            item_list.clear_options()

            for label, value in self._filtered_options:
                is_selected = value == self._selected_value
                item_list.add_option(Selection(label, value, is_selected))
        except Exception:
            pass

    def _expand(self) -> None:
        """Раскрывает список опций."""
        if self._is_expanded:
            return

        try:
            item_list = self.query_one("#item-list", SelectionList)
            item_list.display = True
            self._is_expanded = True

            search_input = self.query_one("#search-input", Input)
            search_input.value = ""
            if self._selected_label:
                search_input.placeholder = f"Поиск... (выбрано: {self._selected_label})"
            else:
                search_input.placeholder = "Поиск..."

            self._filtered_options = self._all_options[:MAX_DISPLAYED_OPTIONS]
            self._total_matches = len(self._all_options)
            self._update_list_options()
        except Exception:
            pass

    def _collapse(self) -> None:
        """Сворачивает список и показывает выбранное значение."""
        if not self._is_expanded:
            return

        self._is_expanded = False

        try:
            item_list = self.query_one("#item-list", SelectionList)
            item_list.display = False

            search_input = self.query_one("#search-input", Input)
            if self._selected_label:
                search_input.value = self._selected_label
                search_input.placeholder = ""
            else:
                search_input.value = ""
                search_input.placeholder = self._placeholder
        except Exception:
            pass

    def on_selection_list_selected_changed(self, event: SelectionList.SelectedChanged) -> None:
        """Обработка выбора элемента (только один элемент может быть выбран)."""
        if event.selection_list.id == "item-list":
            selected = list(event.selection_list.selected)

            if selected:
                new_value = selected[-1]

                if new_value != self._selected_value:
                    self._selected_value = new_value
                    for label, value in self._all_options:
                        if value == new_value:
                            self._selected_label = label
                            break

                    try:
                        item_list = self.query_one("#item-list", SelectionList)
                        item_list.clear_options()
                        for label, value in self._filtered_options:
                            is_selected = value == self._selected_value
                            item_list.add_option(Selection(label, value, is_selected))
                    except Exception:
                        pass
            else:
                self._selected_value = None
                self._selected_label = None

            if self._is_expanded:
                try:
                    search_input = self.query_one("#search-input", Input)
                    if self._selected_label:
                        search_input.placeholder = f"Поиск... (выбрано: {self._selected_label})"
                    else:
                        search_input.placeholder = "Поиск..."
                except Exception:
                    pass

    def on_input_changed(self, event: Input.Changed) -> None:
        """Обработка изменения поискового запроса."""
        if event.input.id == "search-input" and self._is_expanded:
            search_term = event.value.lower().strip()

            if search_term:
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

            self._update_list_options()

    @property
    def value(self) -> Any:
        """Возвращает выбранное значение."""
        return self._selected_value

    def set_options(self, options: List[Tuple[str, str]]) -> None:
        """Устанавливает список опций для выбора."""
        self._all_options = options.copy()
        self._filtered_options = options[:MAX_DISPLAYED_OPTIONS]
        self._selected_value = None
        self._selected_label = None

        try:
            search_input = self.query_one("#search-input", Input)
            search_input.value = ""
            search_input.placeholder = self._placeholder
        except Exception:
            pass

        self._update_list_options()


class DropdownMultiSelect(Vertical):
    """Выпадающий список для множественного выбора.

    Список скрыт по умолчанию, раскрывается при фокусе на Input.
    В свернутом состоянии показывает выбранные элементы через запятую.
    """

    DEFAULT_CSS = """
    DropdownMultiSelect {
        padding: 0;
        margin: 0;
        height: auto;
        content-align: left top;
    }
    DropdownMultiSelect > Input#search-input {
        padding: 0;
        margin: 0;
        height: 3;
        min-height: 3;
        max-height: 3;
    }
    DropdownMultiSelect > SelectionList#item-list {
        padding: 0;
        margin: 0;
        height: auto;
        max-height: 15;
    }
    """

    def __init__(self, placeholder: str = "Выберите элементы...", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._all_options: List[str] = []
        self._filtered_options: List[str] = []
        self._selected_values: List[str] = []
        self._total_matches: int = 0
        self._placeholder = placeholder
        self._is_expanded: bool = False
        self._collapse_timer: Optional[Timer] = None

    def compose(self) -> ComposeResult:
        """Создает интерфейс виджета."""
        yield Input(placeholder=self._placeholder, id="search-input")
        yield SelectionList[str](id="item-list")

    def on_mount(self) -> None:
        """Инициализация при монтировании."""
        self._update_selection_list()
        # Скрываем список по умолчанию
        try:
            selection_list = self.query_one("#item-list", SelectionList)
            selection_list.display = False
        except Exception:
            pass

        # Подписываемся на события Input
        try:
            search_input = self.query_one("#search-input", Input)
            search_input.watch(search_input, "has_focus", self._on_input_focus_changed)
        except Exception:
            pass

    def _on_input_focus_changed(self, has_focus: bool) -> None:
        """Обработка изменения фокуса на поле поиска."""
        if has_focus:
            if self._collapse_timer:
                self._collapse_timer.stop()
                self._collapse_timer = None
            self._expand()
        else:
            # Задержка чтобы успел отработать клик по SelectionList
            self._collapse_timer = self.set_timer(0.3, self._collapse)

    def on_key(self, event: Key) -> None:
        """Обработка нажатия клавиш."""
        if event.key == "escape" and self._is_expanded:
            self._collapse()
            event.stop()
            event.prevent_default()

    def _update_selection_list(self) -> None:
        """Обновляет опции в SelectionList.

        Выбранные элементы всегда вверху списка в порядке выбора.
        """
        try:
            selection_list = self.query_one("#item-list", SelectionList)
            selection_list.clear_options()

            # 1. Сначала выбранные элементы (в порядке выбора)
            for option in self._selected_values:
                selection_list.add_option(Selection(option, option, True))

            # 2. Затем отфильтрованные невыбранные
            unselected_options = [
                opt for opt in self._filtered_options if opt not in self._selected_values
            ]
            for option in unselected_options:
                selection_list.add_option(Selection(option, option, False))
        except Exception:
            pass

    def _expand(self) -> None:
        """Раскрывает список опций."""
        if self._is_expanded:
            return

        try:
            selection_list = self.query_one("#item-list", SelectionList)
            selection_list.display = True
            self._is_expanded = True

            # Очищаем Input для поиска
            search_input = self.query_one("#search-input", Input)
            search_input.value = ""
            count = len(self._selected_values)
            if count > 0:
                search_input.placeholder = f"Поиск... (выбрано: {count})"
            else:
                search_input.placeholder = "Поиск..."

            # Показываем все опции
            self._filtered_options = self._all_options[:MAX_DISPLAYED_OPTIONS]
            self._total_matches = len(self._all_options)
            self._update_selection_list()
        except Exception:
            pass

    def _collapse(self) -> None:
        """Сворачивает список и показывает выбранные значения в порядке выбора."""
        if not self._is_expanded:
            return

        self._is_expanded = False

        try:
            selection_list = self.query_one("#item-list", SelectionList)
            selection_list.display = False

            # Показываем выбранные значения в Input через запятую (в порядке выбора)
            search_input = self.query_one("#search-input", Input)
            if self._selected_values:
                display_text = ", ".join(self._selected_values)
                # Обрезаем если слишком длинный
                if len(display_text) > 50:
                    display_text = display_text[:47] + "..."
                search_input.value = display_text
                search_input.placeholder = ""
            else:
                search_input.value = ""
                search_input.placeholder = self._placeholder
        except Exception:
            pass

    def on_input_changed(self, event: Input.Changed) -> None:
        """Обработка изменения поискового запроса."""
        if event.input.id == "search-input" and self._is_expanded:
            search_term = event.value.lower().strip()

            if search_term:
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

    def on_selection_list_selected_changed(self, event: SelectionList.SelectedChanged) -> None:
        """Обработка изменения выбранных элементов с сохранением порядка выбора."""
        if event.selection_list.id == "item-list":
            new_selected = set(event.selection_list.selected)
            old_selected = set(self._selected_values)

            # Определяем что было добавлено и что было удалено
            added = new_selected - old_selected
            removed = old_selected - new_selected

            # Удаляем снятые элементы из списка
            for item in removed:
                if item in self._selected_values:
                    self._selected_values.remove(item)

            # Добавляем новые элементы в конец списка (сохраняя порядок выбора)
            for item in added:
                if item not in self._selected_values:
                    self._selected_values.append(item)

            # Обновляем placeholder с количеством выбранных
            if self._is_expanded:
                try:
                    search_input = self.query_one("#search-input", Input)
                    count = len(self._selected_values)
                    if count > 0:
                        search_input.placeholder = f"Поиск... (выбрано: {count})"
                    else:
                        search_input.placeholder = "Поиск..."
                except Exception:
                    pass

    @property
    def selected(self) -> List[str]:
        """Возвращает список выбранных значений в порядке выбора."""
        return self._selected_values.copy()

    def set_options(self, options: List[str]) -> None:
        """Устанавливает список опций для выбора."""
        self._all_options = sorted(options)
        self._filtered_options = self._all_options[:MAX_DISPLAYED_OPTIONS]
        self._selected_values.clear()

        try:
            search_input = self.query_one("#search-input", Input)
            search_input.value = ""
            search_input.placeholder = self._placeholder
        except Exception:
            pass

        self._update_selection_list()
