"""Сервис для объяснения ошибок валидации через LLM."""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .backend_llm_client import LLMMessage
from .dto import ProcessedValidationError
from .rag_analyzer import RAGAnalyzer, RAGContext
from .repository import MetricsRepository


class LLMExplainService:
    """Сервис для получения AI объяснений ошибок валидации."""

    def __init__(self, llm_client: Any, rag_analyzer: Optional[RAGAnalyzer] = None):
        """
        Инициализирует сервис объяснений.

        Args:
            llm_client: Клиент для работы с LLM
            rag_analyzer: Анализатор для RAG (создается автоматически если не передан)
        """
        self.llm_client = llm_client

        # Если RAG анализатор не передан, создаем с динамическим размером контекста
        if rag_analyzer is None:
            # Получаем лимит токенов для модели по умолчанию
            token_limit = llm_client.get_model_token_limit()
            # Грубая оценка: 1 токен ≈ 4 байта
            llm_byte_limit = token_limit * 4
            rag_analyzer = RAGAnalyzer(max_context_size=llm_byte_limit)

        self.rag_analyzer = rag_analyzer
        self._base_prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        from .config import config

        prompt = """
        Ты любезный и очень профессиональный помощник, который предназначен
для того, чтобы кратко и понятно объяснить пользователю причину проблемы,
которая зафиксирована в логах. Ты объясняешь аналитику, поэтому не бойся терминов.


Проанализируй текст ошибки и дай аргументированный ответ что может быть не так настройках yaml и sql файлов.

## Инструкции для анализа:

1. **Изучи контекст ошибки**: внимательно прочитай сообщение об ошибке, файл и строку где она произошла
2. **Проанализируй доступные файлы**: изучи содержимое связанных файлов чтобы понять структуру и связи
3. **Определи возможные причины**: предложи несколько вероятных причин ошибки
4. **Дай конкретные рекомендации**: предложи шаги для исправления проблемы
5. **Учитывай отсутствующие файлы**: если файлы не найдены, объясни почему это может быть проблемой

## Формат ответа:

Отвечай в markdown формате со следующей структурой:

### 🔍 Анализ ошибки
Краткое описание что пошло не так

### 🎯 Вероятные причины
- Причина 1: описание
- Причина 2: описание
- Причина 3: описание

### 💡 Рекомендации по исправлению
1. **Шаг 1**: подробное описание действия
2. **Шаг 2**: подробное описание действия
3. **Шаг 3**: подробное описание действия

### 📋 Дополнительные проверки
Список того, что стоит проверить дополнительно

Будь конкретным и практичным в рекомендациях. Ссылайся на конкретные файлы и строки когда это уместно.


Не задавай дополнительных вопросов.
Всегда отвечай на русском языке

Отвечай кратко.
{support_section}
Ответ выведи в формате markdown и всегда возвращай его валидным.

        """

        cli_config = config.get_cli_config()
        support_section = ""
        if cli_config and cli_config.support:
            if cli_config.support.support_chat_url and cli_config.support.support_chat_text:
                support_section = f"""

Обязательно напиши в конце ответа следующий текст:

```
{cli_config.support.support_chat_text}
{cli_config.support.support_chat_url}
```
"""

        return prompt.format(support_section=support_section)

    async def explain_validation_errors(
        self,
        errors: List[ProcessedValidationError],
        repository: MetricsRepository,
        chunk_callback: Optional[Callable[[str], None]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        context: Union[RAGContext, None] = None,
    ) -> str:
        """
        Получает объяснение ошибок валидации от LLM.

        Args:
            errors: Список ошибок для анализа
            repository: Репозиторий метрик
            chunk_callback: Callback для обработки полученного ответа
            model: Модель LLM для использования (если не указана, используется первая доступная)
            temperature: Температура генерации
            context: Предварительно подготовленный RAG контекст (опционально)

        Returns:
            Полное объяснение ошибок от LLM

        Raises:
            ValueError: Если список ошибок пуст
            Exception: При ошибках LLM или RAG анализа
        """
        if not errors:
            raise ValueError("Список ошибок не может быть пустым")

        try:
            # 1. Анализируем ошибки через RAG для получения контекста
            if not context:
                context = self.rag_analyzer.analyze_errors(errors, repository)

            # 2. Формируем полный prompt с контекстом
            full_prompt = context.to_llm_prompt(self._base_prompt)

            # 3. Подготавливаем сообщение для LLM
            messages = [LLMMessage(role="user", content=full_prompt)]

            # 4. Отправляем запрос к LLM
            content = await self.llm_client.chat_completion(
                messages=messages, model=model, temperature=temperature
            )

            # Вызываем chunk_callback если предоставлен
            if chunk_callback:
                chunk_callback(content)

            return content

        except Exception as e:
            # В случае ошибки возвращаем информативное сообщение
            error_message = "### ❌ Ошибка получения AI объяснения\n\n"
            error_message += f"Не удалось получить объяснение от AI: {str(e)}\n\n"
            error_message += "**Возможные причины:**\n"
            error_message += "- Проблемы с подключением к LLM\n"
            error_message += "- Превышен лимит токенов\n"
            error_message += "- Некорректная конфигурация LLM\n\n"
            error_message += "**Рекомендация:** Проверьте настройки LLM через `trisigma init`"

            return error_message

    async def explain_single_error(
        self,
        error: ProcessedValidationError,
        repository: MetricsRepository,
        chunk_callback: Optional[Callable[[str], None]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """
        Получает объяснение для одной ошибки.

        Args:
            error: Ошибка для анализа
            repository: Репозиторий метрик
            chunk_callback: Callback для обработки полученного ответа
            model: Модель LLM (если не указана, используется первая доступная)
            temperature: Температура генерации

        Returns:
            Полное объяснение ошибки от LLM
        """
        return await self.explain_validation_errors(
            errors=[error],
            repository=repository,
            chunk_callback=chunk_callback,
            model=model,
            temperature=temperature,
        )

    async def get_prompt_preview(
        self,
        errors: List[ProcessedValidationError],
        repository: MetricsRepository,
    ) -> str:
        """
        Возвращает preview того какой prompt будет отправлен в LLM.
        Полезно для отладки и понимания контекста.

        Args:
            errors: Список ошибок
            repository: Репозиторий метрик

        Returns:
            Полный prompt который будет отправлен в LLM
        """
        if not errors:
            return "Список ошибок пуст"

        try:
            context = self.rag_analyzer.analyze_errors(errors, repository)
            return context.to_llm_prompt(self._base_prompt)
        except Exception as e:
            return f"Ошибка формирования prompt: {e}"

    def get_context_stats(
        self,
        errors: List[ProcessedValidationError],
        repository: MetricsRepository,
    ) -> Tuple[Dict, Optional[RAGContext]]:
        """
        Возвращает статистику по контексту который будет отправлен в LLM.

        Args:
            errors: Список ошибок
            repository: Репозиторий метрик

        Returns:
            Словарь со статистикой контекста
        """
        if not errors:
            return {"error": "Список ошибок пуст"}, None

        try:
            context = self.rag_analyzer.analyze_errors(errors, repository)
            full_prompt = context.to_llm_prompt(self._base_prompt)

            return {
                "errors_count": len(context.errors),
                "found_files_count": len(context.found_files),
                "missing_files_count": len(context.missing_files),
                "total_context_size": len(full_prompt),
                "found_files": list(context.found_files.keys()),
                "missing_files": context.missing_files,
                "context_utilization": f"{context.current_size / context.max_total_size * 100:.1f}%",
            }, context
        except Exception as e:
            return {"error": f"Ошибка анализа контекста: {e}"}, None

    async def get_available_models(self) -> List[str]:
        """
        Возвращает список доступных моделей от LLM API.

        Returns:
            Список названий доступных моделей
        """
        return await self.llm_client.get_models()
