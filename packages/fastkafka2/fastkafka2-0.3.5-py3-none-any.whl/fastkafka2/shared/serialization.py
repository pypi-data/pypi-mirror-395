# fastkafka2/shared/serialization.py
"""
Утилиты для автоматической сериализации Pydantic моделей, Enum, dataclass и т.д.
Оптимизировано с кешированием для высокой производительности.
"""

import enum
import logging
from dataclasses import fields, is_dataclass
from functools import lru_cache
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


# =========================
# ВСПОМОГАТЕЛЬНЫЕ УТИЛИТЫ
# =========================

@lru_cache(maxsize=128)
def _cached_fields(dc_type):
    """
    Кешируем поля dataclass для ускорения.
    
    Args:
        dc_type: тип dataclass
        
    Returns:
        Кортеж полей dataclass
        
    Raises:
        TypeError: если переданный тип не является dataclass
    """
    if not is_dataclass(dc_type):
        raise TypeError(f"Expected dataclass type, got {type(dc_type).__name__}")
    return fields(dc_type)


def _is_pydantic_model(obj) -> bool:
    """Проверка, является ли объект Pydantic моделью"""
    return isinstance(obj, BaseModel)


def _to_dict_fast(obj: Any) -> dict:
    """
    Быстрая конвертация Pydantic → dict (v2/v1 поддержка).
    Оптимизировано: сначала проверяем методы, затем __dict__.
    
    Args:
        obj: Pydantic модель для конвертации
        
    Returns:
        Словарь с данными модели
        
    Raises:
        TypeError: если объект не является Pydantic моделью
    """
    if not _is_pydantic_model(obj):
        raise TypeError(f"Expected Pydantic BaseModel, got {type(obj).__name__}")
    
    # Pydantic v2 - используем model_dump (предпочтительно)
    if hasattr(obj, "model_dump"):
        try:
            return obj.model_dump()
        except Exception:
            pass
    
    # Pydantic v1 - используем dict()
    if hasattr(obj, "dict"):
        try:
            return obj.dict()
        except Exception:
            pass
    
    # Fallback на __dict__ для Pydantic v2 (если методы недоступны)
    if hasattr(obj, "__dict__"):
        try:
            return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        except Exception:
            pass
    
    # Если ничего не сработало, возвращаем пустой dict
    return {}


def to_primitive(val: Any, _visited: set[int] | None = None) -> Any:
    """
    Рекурсивно преобразует Pydantic/Enum/dataclass/list/dict в простые типы.
    
    Используется для сериализации перед отправкой в Kafka.
    Оптимизировано с кешированием полей dataclass.
    Защищено от циклических ссылок.
    
    Args:
        val: значение для преобразования
        _visited: внутренний параметр для отслеживания посещенных объектов (защита от циклов)
    
    Returns:
        Преобразованное значение в примитивных типах
    
    Example:
        >>> from pydantic import BaseModel
        >>> class User(BaseModel):
        ...     name: str
        >>> to_primitive(User(name="John"))
        {'name': 'John'}
    """
    if val is None:
        return None
    
    # Защита от циклических ссылок
    if _visited is None:
        _visited = set()
    
    # Для объектов, которые могут иметь циклические ссылки
    obj_id = id(val)
    if obj_id in _visited:
        # Возвращаем строковое представление для циклических ссылок
        return f"<cyclic reference: {type(val).__name__}>"
    
    try:
        # Enum -> value
        if isinstance(val, enum.Enum):
            return val.value
        
        # Pydantic модель -> dict
        if _is_pydantic_model(val):
            _visited.add(obj_id)
            try:
                dict_val = _to_dict_fast(val)
                result = to_primitive(dict_val, _visited)
            finally:
                _visited.discard(obj_id)
            return result
        
        # dataclass -> dict (с кешированием полей)
        if is_dataclass(val):
            _visited.add(obj_id)
            try:
                result = {
                    f.name: to_primitive(getattr(val, f.name, None), _visited)
                    for f in _cached_fields(type(val))
                }
            finally:
                _visited.discard(obj_id)
            return result
        
        # list -> рекурсивно обрабатываем элементы
        if isinstance(val, list):
            _visited.add(obj_id)
            try:
                result = [to_primitive(i, _visited) for i in val]
            finally:
                _visited.discard(obj_id)
            return result
        
        # dict -> рекурсивно обрабатываем значения
        if isinstance(val, dict):
            _visited.add(obj_id)
            try:
                result = {k: to_primitive(v, _visited) for k, v in val.items()}
            finally:
                _visited.discard(obj_id)
            return result
        
        # Примитивные типы возвращаем как есть
        return val
    except Exception as e:
        # Если произошла ошибка, возвращаем строковое представление
        logger.warning(
            "Error converting %s to primitive: %s. Returning string representation.",
            type(val).__name__, e
        )
        return str(val)


