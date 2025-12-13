# fastkafka2\api\handler.py
import logging
from typing import Callable, Any
from ..core.registry import kafka_handler

logger = logging.getLogger(__name__)


class KafkaHandler:
    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix

    def __call__(
        self,
        topic: str,
        headers_filter: Any | None = None,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        Регистрация handler для топика.
        
        Args:
            topic: название топика
            headers_filter: фильтр по headers (dict или callable)
            
        Note:
            Обработчик должен принимать параметр типа KafkaMessage[Data, Headers].
            Модели Data и Headers извлекаются автоматически из аннотации типа.
        """
        full_topic = f"{self.prefix}.{topic}" if self.prefix else topic
        return kafka_handler(full_topic, None, None, headers_filter)

    def include_handler(self, other: "KafkaHandler") -> None:
        """
        Включает другой handler, объединяя префиксы.
        После вызова этого метода, все обработчики, зарегистрированные через self,
        будут использовать объединенный префикс.
        
        Args:
            other: другой KafkaHandler для включения
        """
        if not isinstance(other, KafkaHandler):
            raise TypeError(f"Expected KafkaHandler, got {type(other).__name__}")
        
        if other.prefix:
            if self.prefix:
                self.prefix = f"{self.prefix}.{other.prefix}"
            else:
                self.prefix = other.prefix
