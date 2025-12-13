# fastkafka2/core/partition_manager.py
import asyncio
import logging
from typing import Any, Awaitable, Callable, Optional

from .partition_processor import PartitionProcessor, QueuedMessage

logger = logging.getLogger(__name__)


class PartitionManager:
    """Manages partition processors - one task per partition"""
    
    def __init__(
        self,
        max_queue_size: int = 1000,
        max_retries: int = 3,
    ):
        self._processors: dict[tuple[str, int], PartitionProcessor] = {}
        self._lock = asyncio.Lock()
        self.max_queue_size = max_queue_size
        self.max_retries = max_retries
        
    async def process_message(
        self,
        topic: str,
        partition: int,
        msg_data: Any,
        headers: dict[str, str],
        key: Optional[str],
        offset: int,
        handlers: list[Callable],
        commit_callback: Optional[Callable[[], Awaitable[None]]] = None,
    ) -> None:
        """Process message through partition processor"""
        partition_key = (topic, partition)
        
        async with self._lock:
            if partition_key not in self._processors:
                processor = PartitionProcessor(
                    topic=topic,
                    partition=partition,
                    max_queue_size=self.max_queue_size,
                    max_retries=self.max_retries,
                )
                try:
                    await processor.start()
                    self._processors[partition_key] = processor
                except Exception as e:
                    logger.exception(
                        "Failed to start processor for partition %s:%s: %s",
                        topic, partition, e
                    )
                    raise
            processor = self._processors.get(partition_key)
            if processor is None:
                raise RuntimeError(
                    f"Processor for partition {topic}:{partition} was removed"
                )
                
        await processor.process_message(
            msg_data, headers, key, offset, handlers, commit_callback
        )
        
    async def stop_partition(self, topic: str, partition: int) -> None:
        """Stop processing for specific partition"""
        partition_key = (topic, partition)
        async with self._lock:
            processor = self._processors.get(partition_key)
            if processor:
                try:
                    await processor.stop()
                except Exception as e:
                    logger.exception(
                        "Error stopping processor for partition %s:%s: %s",
                        topic, partition, e
                    )
                finally:
                    # Always remove processor even if stop failed
                    self._processors.pop(partition_key, None)
                
    async def stop_all(self) -> None:
        """Stop all processors"""
        async with self._lock:
            processors = list(self._processors.values())
            partition_keys = list(self._processors.keys())
            self._processors.clear()
        
        # Stop processors outside lock to avoid deadlock
        if processors:
            tasks = [processor.stop() for processor in processors]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log any errors that occurred during stop
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    topic, partition = partition_keys[i]
                    logger.exception(
                        "Error stopping processor for partition %s:%s: %s",
                        topic, partition, result
                    )
            
    def get_partitions(self) -> list[tuple[str, int]]:
        """Get list of all active partitions"""
        return list(self._processors.keys())
    
    def get_all_stats(self) -> list[dict[str, Any]]:
        """Возвращает статистику всех партиций для мониторинга"""
        return [processor.get_stats() for processor in self._processors.values()]

