"""Утилиты для работы с консольным выводом."""

from typing import Any

from rich.console import Console


def create_console(plain: bool = False) -> Console:
    """
    Создает экземпляр Console с учетом режима вывода.

    Args:
        plain: Если True, отключает форматирование и цвета

    Returns:
        Настроенный экземпляр Console
    """
    if plain:
        return Console(
            force_terminal=False,
            no_color=True,
            width=None,
            legacy_windows=False,
            markup=False,
            emoji=False,
            highlight=False,
        )
    else:
        return Console()


def create_error_console() -> Console:
    """
    Создает экземпляр Console для вывода ошибок (всегда plain).

    Returns:
        Console без форматирования для лучшего копирования ошибок
    """
    return Console(
        force_terminal=False,
        no_color=True,
        width=None,
        legacy_windows=False,
        markup=False,
        emoji=False,
        highlight=False,
    )


def format_text(
    text: str, style: str, plain: bool = False, force_plain_errors: bool = True
) -> str:
    """
    Форматирует текст с учетом режима вывода.

    Args:
        text: Текст для форматирования
        style: Rich стиль (например, "[red]", "[bold blue]")
        plain: Если True, возвращает текст без форматирования
        force_plain_errors: Если True, ошибки (red стиль) всегда отображаются без форматирования

    Returns:
        Отформатированный или простой текст
    """
    # Принудительно убираем форматирование для ошибок
    if force_plain_errors and style and "red" in style:
        return text

    if plain:
        return text
    else:
        # Если стиль передан и не пустой, применяем форматирование
        if style and not style.isspace():
            # Убедимся что стиль заключен в скобки
            if not style.startswith("["):
                style = f"[{style}]"
            if not style.endswith("]") or style.endswith("[/]"):
                return f"{style}{text}[/]"
            else:
                return f"{style}{text}[/]"
        return text


def conditional_print(console: Console, text: Any, plain: bool = False, **kwargs: Any) -> None:
    """
    Выводит текст с учетом режима форматирования.

    Args:
        console: Экземпляр Console
        text: Текст для вывода
        plain: Если True, выводит без форматирования
        **kwargs: Дополнительные аргументы для console.print
    """
    if plain:
        # В plain режиме убираем стилизацию из kwargs
        cleaned_kwargs = {
            k: v for k, v in kwargs.items() if k not in ["style", "markup", "emoji", "highlight"]
        }
        console.print(text, **cleaned_kwargs)
    else:
        console.print(text, **kwargs)
