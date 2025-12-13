# fastkafka2\api\producer.py
import orjson
import logging
from typing import Any
from ..infrastructure.services.base import BaseKafkaService
from ..infrastructure.services.retry import retry_on_connection
from ..infrastructure.helpers.async_client import AsyncKafkaProducer
from ..shared.serialization import to_primitive

logger = logging.getLogger(__name__)


def _serialize_headers(headers: dict[str, str] | Any) -> list[tuple[str, bytes]]:
    """Сериализует headers в формат для Kafka"""
    # Если headers - Pydantic модель или dict с не-строками, конвертируем
    if not isinstance(headers, dict):
        headers = to_primitive(headers)
    
    # Убеждаемся, что headers - это dict после конвертации
    if not isinstance(headers, dict):
        raise TypeError(
            f"Headers must be dict or convertible to dict, got {type(headers).__name__}"
        )
    
    # Все значения должны быть строками для Kafka headers
    result = {}
    for k, v in headers.items():
        if v is None:
            continue
        # Конвертируем в строку (Enum уже обработан в to_primitive)
        result[str(k)] = str(v) if not isinstance(v, str) else v
    
    return [(k, v.encode()) for k, v in result.items()]


class KafkaProducer(BaseKafkaService):
    def __init__(self, bootstrap_servers: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self._producer: AsyncKafkaProducer | None = None

    @retry_on_connection()
    async def start(self) -> None:
        if self._producer is not None:
            logger.warning("KafkaProducer is already started")
            return
        
        config = {
            "bootstrap.servers": self.bootstrap_servers,
        }
        producer = AsyncKafkaProducer(config)
        try:
            await producer.start()
            self._producer = producer
            logger.info("KafkaProducer started")
        except Exception:
            logger.exception("Failed to start KafkaProducer")
            self._producer = None
            raise

    @retry_on_connection()
    async def send_message(
        self,
        topic: str,
        data: dict[str, Any] | Any,
        headers: dict[str, str] | Any = None,
        key: str | None = None,
    ) -> None:
        """
        Отправка сообщения в Kafka.
        
        Args:
            topic: название топика
            data: данные сообщения (может быть Pydantic моделью, dict, или другим типом)
            headers: заголовки сообщения (может быть Pydantic моделью или dict)
            key: ключ сообщения (для партиционирования)
        
        Raises:
            RuntimeError: если producer не запущен
        """
        if not self._producer:
            raise RuntimeError("Producer not started. Call start() first.")
        
        if not topic:
            raise ValueError("Topic cannot be empty")
        
        try:
            # Сериализуем данные (Pydantic модели, Enum, dataclass -> dict)
            message_data = to_primitive(data)
            
            # Serialize data to JSON bytes
            value_bytes = orjson.dumps(message_data)
            key_bytes = key.encode() if key else None
            
            # Сериализуем headers (Pydantic модели, Enum -> dict/str)
            kafka_headers = _serialize_headers(headers) if headers else None
            
            await self._producer.send(
                topic=topic,
                value=value_bytes,
                key=key_bytes,
                headers=kafka_headers,
            )
        except Exception:
            logger.exception(
                "Failed to send message to topic %s (key=%s)",
                topic, key
            )
            raise

    async def stop(self) -> None:
        if not self._producer:
            logger.debug("KafkaProducer is not started")
            return
        
        producer = self._producer
        self._producer = None
        
        try:
            await producer.stop()
            logger.info("KafkaProducer stopped")
        except Exception as e:
            logger.exception("Error stopping KafkaProducer: %s", e)
            raise
