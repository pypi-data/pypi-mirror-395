# fastkafka2\infrastructure\services\base.py
from abc import ABC, abstractmethod

__all__ = ["BaseKafkaService"]


class BaseKafkaService(ABC):
    """
    Base abstract class for all Kafka services.
    
    All Kafka services must implement start() and stop() methods.
    The class also supports async context manager protocol for convenient usage:
    
    Example:
        async with KafkaProducer("localhost:9092") as producer:
            await producer.send_message(...)
    """
    
    @abstractmethod
    async def start(self) -> None:
        """Start the service"""
        ...
    
    @abstractmethod
    async def stop(self) -> None:
        """Stop the service"""
        ...
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.stop()
        return False
