# fastkafka2/message.py
import orjson
import logging
from typing import Generic, TypeVar, Any
from pydantic import BaseModel, Field

try:
    from pydantic import ConfigDict
    _CONFIG_DICT = ConfigDict(
        extra="forbid",
        frozen=True,
        arbitrary_types_allowed=True,
    )
except ImportError:
    # Pydantic v1 compatibility
    _CONFIG_DICT = None

logger = logging.getLogger(__name__)

TData = TypeVar("TData")
THeaders = TypeVar("THeaders")


class LazyDeserializedBody:
    """
    Класс для ленивой десериализации тела сообщения Kafka.
    Хранит raw bytes и десериализует их только при первом обращении.
    
    Это позволяет быстро фильтровать сообщения по заголовкам без десериализации тела,
    что значительно ускоряет обработку когда большинство сообщений не проходят фильтр.
    """
    __slots__ = ("_raw_bytes", "_deserialized", "_deserialization_error")
    
    def __init__(self, raw_bytes: bytes | None):
        """
        Args:
            raw_bytes: Сырые байты тела сообщения из Kafka
        """
        self._raw_bytes = raw_bytes
        self._deserialized: Any = None
        self._deserialization_error: Exception | None = None
    
    def get(self) -> Any:
        """
        Десериализует тело сообщения при первом вызове и возвращает результат.
        Последующие вызовы возвращают кешированный результат.
        
        Returns:
            Десериализованные данные (обычно dict или None)
            
        Raises:
            Exception: Если десериализация не удалась (ошибка сохраняется и повторяется)
        """
        if self._deserialized is None and self._deserialization_error is None:
            # Первое обращение - десериализуем
            try:
                if self._raw_bytes is None:
                    self._deserialized = None
                else:
                    self._deserialized = orjson.loads(self._raw_bytes)
            except Exception as e:
                self._deserialization_error = e
                logger.error("Failed to deserialize message body: %s", e)
                raise
        
        if self._deserialization_error is not None:
            raise self._deserialization_error
        
        return self._deserialized
    
    @property
    def is_deserialized(self) -> bool:
        """Проверяет, было ли тело уже десериализовано"""
        return self._deserialized is not None or self._deserialization_error is not None
    
    @property
    def raw_bytes(self) -> bytes | None:
        """Возвращает сырые байты без десериализации"""
        return self._raw_bytes


class KafkaMessage(BaseModel, Generic[TData, THeaders]):
    """
    Сообщение Kafka с типизированными данными и заголовками.
    
    Args:
        topic: Название топика Kafka
        data: Данные сообщения (типизированы через TData)
        headers: Заголовки сообщения (типизированы через THeaders, по умолчанию dict)
        key: Ключ сообщения (опционально)
    
    Example:
        >>> from pydantic import BaseModel
        >>> class Data(BaseModel):
        ...     id: int
        >>> class Headers(BaseModel):
        ...     source: str
        >>> msg = KafkaMessage[Data, Headers](
        ...     topic="test",
        ...     data=Data(id=1),
        ...     headers=Headers(source="api")
        ... )
    """
    topic: str
    data: TData
    headers: THeaders = Field(default_factory=dict)
    key: str | None = None

    if _CONFIG_DICT is not None:
        # Pydantic v2
        model_config = _CONFIG_DICT
    else:
        # Pydantic v1
        class Config:
            extra = "forbid"
            frozen = True
            arbitrary_types_allowed = True
