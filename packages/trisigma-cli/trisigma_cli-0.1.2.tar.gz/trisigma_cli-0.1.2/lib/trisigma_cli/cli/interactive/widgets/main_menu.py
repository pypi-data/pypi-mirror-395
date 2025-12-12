"""Главное меню интерактивного режима."""

from textual import events
from textual.reactive import reactive
from textual.widgets import OptionList
from textual.widgets.option_list import Option


class MainMenu(OptionList):
    """Главное меню с основными действиями."""

    current_selection = reactive("")
    menu_state = reactive("main")  # "main" или "compile_sql"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_title = "Главное меню"
        self._setup_menu_items()

    def _setup_menu_items(self):
        """Настраивает пункты меню в зависимости от состояния."""
        self.clear_options()

        if self.menu_state == "main":
            self._setup_main_menu()
        elif self.menu_state == "compile_sql":
            self._setup_compile_sql_menu()

    def _setup_main_menu(self):
        """Настраивает главное меню."""
        self.border_title = "Главное меню"
        self.add_options(
            [
                Option("📖 Начало работы", id="getting_started"),
                Option("🌿 Создать ветку под задачу", id="branches"),
                Option("🔍 Валидация репозитория", id="validate"),
                Option("⚙️  Компиляция SQL", id="compile_menu"),
                Option("📝 Статус изменений", id="git-status"),
                Option("💾 Сохранить изменения", id="save"),
                Option("🚀 Опубликовать изменения", id="publish"),
                Option("⚙️  Настройки", id="settings"),
                Option("🚪 Выход", id="exit"),
            ]
        )

    def _setup_compile_sql_menu(self):
        """Настраивает подменю компиляции SQL."""
        self.border_title = "Главное меню > Компиляция SQL"
        self.add_options(
            [
                Option("📄 Компиляция Source", id="compile_source"),
                Option("📊 Компиляция метрик", id="compile_metrics"),
                Option("← Назад к главному меню", id="back_to_main"),
            ]
        )

    async def update_menu(self):
        """Обновляет состояние пунктов меню."""
        # Здесь можно добавить логику для включения/отключения пунктов
        # в зависимости от состояния приложения
        pass

    async def reset_to_main_menu(self):
        """Программно возвращает к главному меню."""
        if self.menu_state != "main":
            await self._navigate_to_main()

    async def on_option_list_option_selected(self, event):
        """Обрабатывает выбор пункта меню."""
        option_id = event.option.id
        app = self.app

        try:
            # Обработка навигации между меню
            if option_id == "back_to_main":
                await self._navigate_to_main()
                return
            elif option_id == "compile_menu":
                await self._navigate_to_compile_sql()
                return

            # Обработка основных действий
            if option_id == "getting_started":
                await app.show_getting_started()

            elif option_id == "validate":
                await app.show_validation_results()

            elif option_id == "compile_source":
                await self._show_compile_dialog()

            elif option_id == "compile_metrics":
                await self._show_metrics_compile_dialog()

            elif option_id == "branches":
                await self._show_branches_dialog()

            elif option_id == "git-status":
                await app.show_git_status()

            elif option_id == "save":
                await self._show_save_dialog()

            elif option_id == "publish":
                await self._show_publish_dialog()

            elif option_id == "settings":
                await self._show_settings_dialog()

            elif option_id == "exit":
                app.exit()

        except Exception as e:
            app.log.error(f"Ошибка в меню {option_id}: {e}")
            await app.show_content(f"[red]Ошибка:[/red] {e}", clear_buttons=True)

    async def _navigate_to_main(self):
        """Переход к главному меню."""
        self.menu_state = "main"
        self._setup_menu_items()
        # Устанавливаем фокус на первый элемент
        if self.option_count > 0:
            self.highlighted = 0

    async def _navigate_to_compile_sql(self):
        """Переход к подменю компиляции SQL."""
        self.menu_state = "compile_sql"
        self._setup_menu_items()
        # Устанавливаем фокус на первый элемент
        if self.option_count > 0:
            self.highlighted = 0

    async def _show_compile_dialog(self):
        """Показывает диалог компиляции SQL источников."""
        from .compile_dialog import CompileDialog

        dialog = CompileDialog()
        await self.app.push_screen(dialog)

    async def _show_metrics_compile_dialog(self):
        """Показывает диалог компиляции SQL метрик."""
        from .metrics_compile_dialog import MetricsCompileDialog

        dialog = MetricsCompileDialog()
        await self.app.push_screen(dialog)

    async def _show_branches_dialog(self):
        """Показывает диалог управления ветками."""
        from .branch_dialog import BranchDialog

        dialog = BranchDialog()
        await self.app.push_screen(dialog)

    async def _show_save_dialog(self):
        """Показывает диалог сохранения изменений."""
        from .save_dialog import SaveDialog

        validation = self.app.git_ui_service.validate_save_operation()
        if not validation.is_valid:
            if validation.error_message:
                await self.app.show_content(
                    f"[red]Ошибка:[/red] {validation.error_message}", clear_buttons=True
                )
            elif validation.warning_message:
                await self.app.show_content(
                    f"[yellow]{validation.warning_message}[/yellow]", clear_buttons=True
                )
            return

        dialog = SaveDialog()
        await self.app.push_screen(dialog)

    async def _show_publish_dialog(self):
        """Показывает диалог публикации изменений."""
        from .publish_dialog import PublishDialog

        validation = self.app.git_ui_service.validate_publish_operation()
        if not validation.is_valid:
            if validation.error_message:
                await self.app.show_content(
                    f"[red]Ошибка:[/red] {validation.error_message}", clear_buttons=True
                )
            elif validation.warning_message:
                await self.app.show_content(
                    f"[yellow]{validation.warning_message}[/yellow]", clear_buttons=True
                )
            return

        dialog = PublishDialog()
        await self.app.push_screen(dialog)

    async def _show_settings_dialog(self):
        """Показывает диалог настроек."""
        from .settings_dialog import SettingsDialog

        dialog = SettingsDialog()
        await self.app.push_screen(dialog)

    def on_key(self, event: events.Key) -> None:
        """Обработка нажатий клавиш."""
        if event.key == "escape" and self.menu_state != "main":
            # Если мы не в главном меню, возвращаемся назад
            self.call_after_refresh(self._navigate_to_main)
            event.prevent_default()
        # Для остальных клавиш используем стандартную обработку OptionList
