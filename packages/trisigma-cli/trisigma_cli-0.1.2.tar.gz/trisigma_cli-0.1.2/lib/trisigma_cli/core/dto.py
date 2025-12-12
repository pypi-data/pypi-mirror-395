"""DTO модели для Trisigma API."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field


class EntityType(str, Enum):
    """Типы сущностей для генерации SQL."""

    SOURCE = "source"
    METRIC = "metric"


class Granularity(str, Enum):
    """Гранулярность данных."""

    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class ErrorCode(str, Enum):
    """Коды ошибок API."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class FeedbackRating(str, Enum):
    """Оценка фидбека пользователя для AI анализа."""

    LIKE = "like"
    DISLIKE = "dislike"


# Base models
class BaseAPIModel(BaseModel):
    """Базовая модель для API."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, validate_default=True)


# Repository content models
class RepoContentDict(BaseAPIModel):
    """Содержимое репозитория в формате API."""

    sources: Tuple[str, bool] = Field(
        default=("", False), description="Файлы источников: (content, contains_changes)"
    )
    sources_sql: Dict[str, Tuple[str, bool]] = Field(
        default_factory=dict, description="SQL файлы источников: (content, contains_changes)"
    )
    dimensions: Tuple[str, bool] = Field(
        default=("", False), description="Файлы дименшенов: (content, contains_changes)"
    )
    dimensions_sql: Dict[str, Tuple[str, bool]] = Field(
        default_factory=dict, description="SQL файлы дименшенов: (content, contains_changes)"
    )
    enrichments: Dict[str, Tuple[str, bool]] = Field(
        default_factory=dict, description="Файлы обогащений: (content, contains_changes)"
    )
    configs: Dict[str, Tuple[str, bool]] = Field(
        default_factory=dict, description="Конфиги метрик: (content, contains_changes)"
    )
    cubes_configs: Dict[str, Tuple[str, bool]] = Field(
        default_factory=dict, description="Конфиги кубов M42: (content, contains_changes)"
    )
    m42_reports: Dict[str, Tuple[str, bool]] = Field(
        default_factory=dict, description="Отчеты M42: (content, contains_changes)"
    )
    ab_schedules: Tuple[str, bool] = Field(
        default=("", False), description="Расписания AB тестов: (content, contains_changes)"
    )


# FastValidateRepoContent models
class FastValidateRepoContentRequest(BaseAPIModel):
    """Запрос валидации репозитория."""

    repo_content: RepoContentDict = Field(description="Содержимое репозитория")


class ValidationErrorMark(BaseAPIModel):
    """Метка ошибки валидации."""

    line: int = Field(description="Номер строки")
    column: int = Field(description="Номер столбца")
    message: str = Field(description="Сообщение об ошибке")


class ValidationError(BaseAPIModel):
    """Ошибка валидации."""

    file: str = Field(description="Имя файла")
    message: str = Field(description="Сообщение об ошибке")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Дополнительные детали")


class ProcessedValidationError(BaseAPIModel):
    """Обработанная ошибка валидации для клиентского API."""

    component: str = Field(description="Компонент где произошла ошибка")
    message: str = Field(description="Сообщение об ошибке")
    file: Optional[str] = Field(default=None, description="Имя файла")
    line: Optional[int] = Field(default=None, description="Номер строки")
    column: Optional[int] = Field(default=None, description="Номер столбца")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Дополнительные детали")


class ComponentValidationResult(BaseAPIModel):
    """Результат валидации компонента."""

    success: bool = Field(description="Успешность валидации")
    errors: List[Union[ValidationError, Dict[str, Any]]] = Field(
        default_factory=list, description="Ошибки валидации"
    )
    error_marks: List[ValidationErrorMark] = Field(
        default_factory=list, description="Метки ошибок"
    )


# Type aliases for better readability
ComponentValidationDict = Dict[str, ComponentValidationResult]


class ValidationResults(BaseAPIModel):
    """Результаты валидации репозитория."""

    ab_schedules: Optional[ComponentValidationResult] = Field(
        default=None, description="Результат валидации AB расписаний"
    )
    configs: Optional[ComponentValidationDict] = Field(
        default=None, description="Результаты валидации метрик"
    )
    cubes_configs: Optional[ComponentValidationDict] = Field(
        default=None, description="Результаты валидации конфигов кубов"
    )
    dimensions: Optional[ComponentValidationResult] = Field(
        default=None, description="Результат валидации дименшенов"
    )
    sources: Optional[ComponentValidationResult] = Field(
        default=None, description="Результат валидации источников"
    )
    m42_reports: Optional[ComponentValidationDict] = Field(
        default=None, description="Результаты валидации отчетов M42"
    )
    enrichments: Optional[ComponentValidationDict] = Field(
        default=None, description="Результаты валидации отчетов обогащений"
    )
    fatal_errors: Optional[List[str]] = Field(default=None, description="Критические ошибки")


class FastValidateRepoContentResponse(BaseAPIModel):
    """Ответ валидации репозитория."""

    success: bool = Field(description="Общий успех валидации")
    results: ValidationResults = Field(description="Результаты валидации по компонентам")
    source_names: Optional[List[str]] = Field(default=None, description="Список имен источников")
    dimension_names: Optional[List[str]] = Field(
        default=None, description="Список имен dimensions"
    )
    metric_names: Optional[List[str]] = Field(default=None, description="Список имен метрик")


# GenerateSqlFromRepo models
class SqlGenerationItem(BaseAPIModel):
    """Элемент для генерации SQL источников."""

    source_name: str = Field(description="Имя источника")
    dimensions: Optional[List[str]] = Field(default=None, description="Список дименшенов")
    columns: Optional[List[str]] = Field(default=None, description="Список колонок")
    first_date: Optional[str] = Field(
        default=None, description="Начальная дата в формате YYYY-MM-DD"
    )
    last_date: Optional[str] = Field(
        default=None, description="Конечная дата в формате YYYY-MM-DD"
    )
    granularity: Granularity = Field(default=Granularity.DAY, description="Гранулярность данных")


class SqlGenerationMetricItem(BaseAPIModel):
    """Элемент для генерации SQL метрик."""

    metric_names: List[str] = Field(description="Список имен метрик")
    dimensions: Optional[List[str]] = Field(default=None, description="Список дименшенов")
    columns: Optional[List[str]] = Field(default=None, description="Список колонок")
    first_date: Optional[str] = Field(
        default=None, description="Начальная дата в формате YYYY-MM-DD"
    )
    last_date: Optional[str] = Field(
        default=None, description="Конечная дата в формате YYYY-MM-DD"
    )
    granularity: Granularity = Field(default=Granularity.DAY, description="Гранулярность данных")


class GenerateSqlFromRepoRequest(BaseAPIModel):
    """Запрос генерации SQL из репозитория."""

    repo_content: RepoContentDict = Field(description="Содержимое репозитория")
    entity_type: EntityType = Field(description="Тип сущности для генерации")
    source_items: Optional[List[SqlGenerationItem]] = Field(
        default=None, description="Элементы для генерации SQL источников"
    )
    metric_items: Optional[List[SqlGenerationMetricItem]] = Field(
        default=None, description="Элементы для генерации SQL метрик"
    )


class SqlGenerationMeta(BaseAPIModel):
    """Метаданные генерации SQL."""

    requested_dimensions: List[str] = Field(
        default_factory=list, description="Запрошенные дименшены"
    )
    resolved_columns: List[str] = Field(default_factory=list, description="Разрешенные колонки")
    used_enrichments: List[str] = Field(
        default_factory=list, description="Использованные обогащения"
    )
    missing_columns: List[str] = Field(default_factory=list, description="Отсутствующие колонки")


class SqlGenerationResult(BaseAPIModel):
    """Результат генерации SQL."""

    source_names: List[str] = Field(description="Имена используемых источников")
    first_date: str = Field(description="Начальная дата")
    last_date: str = Field(description="Конечная дата")
    granularity: Granularity = Field(description="Гранулярность")
    sql: str = Field(description="Сгенерированный SQL код")
    meta: SqlGenerationMeta = Field(description="Метаданные генерации")


class APIError(BaseAPIModel):
    """Ошибка API."""

    code: ErrorCode = Field(description="Код ошибки")
    message: str = Field(description="Сообщение об ошибке")


class GenerateSqlFromRepoResponse(BaseAPIModel):
    """Ответ генерации SQL из репозитория."""

    results: List[SqlGenerationResult] = Field(
        default_factory=list, description="Результаты генерации"
    )
    error: Optional[APIError] = Field(default=None, description="Ошибка, если произошла")
    validation_results: Union[ValidationResults, None] = Field(
        default=None, description="Результаты валидации по компонентам"
    )


# Health check model
class HealthCheckResponse(BaseAPIModel):
    """Ответ проверки здоровья API."""

    status: str = Field(description="Статус API")
    timestamp: Optional[datetime] = Field(default=None, description="Временная метка")
