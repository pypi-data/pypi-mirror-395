"""Утилита для обработки исключений."""

# Безопасный импорт RetryError
try:
    from tenacity import RetryError
except Exception:

    class RetryError(Exception):  # type: ignore
        """Fallback когда tenacity не установлена."""

        pass


class ExceptionHandler:
    """Утилита для обработки и форматирования исключений."""

    @staticmethod
    def extract_root_exception(exc: BaseException) -> BaseException:
        """
        Извлекает корневую причину цепочки исключений / RetryError.

        Args:
            exc: Исключение для анализа

        Returns:
            Корневое исключение в цепочке
        """
        # Специальная обработка RetryError (tenacity) – берём последнюю попытку
        if isinstance(exc, RetryError):
            try:
                last = getattr(exc, "last_attempt", None)
                if last and last.exception():
                    return last.exception()
            except Exception:
                pass

        current = exc
        visited = set()
        while current and id(current) not in visited:
            visited.add(id(current))
            nxt = getattr(current, "__cause__", None) or getattr(current, "__context__", None)
            if nxt:
                current = nxt
                continue
            break
        return current or exc

    @staticmethod
    def format_exception_message(exc: BaseException, *, friendly_retry: bool = True) -> str:
        """
        Форматирует исключение в человеко-понятное сообщение.

        Args:
            exc: Исключение для форматирования
            friendly_retry: Если True, для RetryError показывает дружелюбное сообщение

        Returns:
            Отформатированное сообщение об ошибке
        """
        if isinstance(exc, RetryError) and friendly_retry:
            root = ExceptionHandler.extract_root_exception(exc)
            root_msg = str(root) if root else str(exc)
            return f"Операция не завершилась успешно после нескольких повторов: {root_msg}"

        root = ExceptionHandler.extract_root_exception(exc)
        if root is not exc and str(root):
            parent_msg = str(exc)
            root_msg = str(root)
            # Отбрасываем дублирование
            if root_msg in parent_msg:
                return root_msg
            return f"{parent_msg} (корневая причина: {root_msg})"
        return str(exc)

    @staticmethod
    def sanitize_message(message: str) -> str:
        """
        Очищает сообщение от символов, ломающих Rich markup, сохраняя читаемость.

        Args:
            message: Сообщение для очистки

        Returns:
            Очищенное сообщение
        """
        if not message:
            return ""
        clean = message.replace("<", "&lt;").replace(">", "&gt;")
        # Экранируем квадратные скобки только в пользовательском тексте
        clean = clean.replace("[", "\\[").replace("]", "\\]")
        return clean
