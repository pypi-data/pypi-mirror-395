"""Утилиты для транслитерации."""

from transliterate import translit


def transliterate_cyrillic(text: str) -> str:
    """
    Транслитерирует кириллицу в латиницу с использованием фонетических правил.

    Преобразует кириллические символы в латинские по фонетическим правилам:
    - ж → zh, ч → ch, ш → sh, щ → shh, ю → yu, я → ya и т.д.
    - Латинские символы, цифры и спецсимволы остаются без изменений

    Args:
        text: Текст для транслитерации (может содержать кириллицу, латиницу, символы)

    Returns:
        Транслитерированный текст с кириллицей, замененной на латиницу.
        При ошибке транслитерации возвращается оригинальный текст.

    Examples:
        >>> transliterate_cyrillic("Исправить баг")
        "Ispravit' bag"
        >>> transliterate_cyrillic("Fix баг в metrics")
        "Fix bag v metrics"
        >>> transliterate_cyrillic("already latin")
        "already latin"
    """
    if not text:
        return text

    try:
        # translit(text, 'ru', reversed=True) конвертирует ru → en
        return translit(text, 'ru', reversed=True)
    except Exception:
        # Fallback: если транслитерация не удалась, возвращаем оригинал
        # Это может произойти если библиотека не поддерживает какие-то символы
        return text
