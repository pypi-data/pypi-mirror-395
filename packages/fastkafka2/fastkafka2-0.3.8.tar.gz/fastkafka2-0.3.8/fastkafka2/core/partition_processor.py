# fastkafka2/core/partition_processor.py
import asyncio
import logging
from typing import Any, Awaitable, Callable, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class QueuedMessage:
    """Сообщение в очереди с метаданными для обработки"""
    msg_data: Any
    headers: dict[str, str]
    key: Optional[str]
    offset: int
    handlers: list[Callable]
    commit_callback: Optional[Callable[[], Awaitable[None]]]
    retry_count: int = 0
    max_retries: int = 3


class PartitionProcessor:
    """Processor for a single partition - guarantees ordering"""
    
    def __init__(
        self,
        topic: str,
        partition: int,
        max_queue_size: int = 1000,
        max_retries: int = 3,
    ):
        self.topic = topic
        self.partition = partition
        self.max_queue_size = max_queue_size
        self.max_retries = max_retries
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self._processing = False
        self._task: Optional[asyncio.Task] = None
        self._processed_count = 0
        self._failed_count = 0
        self._dropped_count = 0
        
    async def process_message(
        self,
        msg_data: Any,
        headers: dict[str, str],
        key: Optional[str],
        offset: int,
        handlers: list[Callable],
        commit_callback: Optional[Callable[[], Awaitable[None]]] = None,
    ) -> None:
        """
        Add message to partition queue.
        
        Raises:
            asyncio.QueueFull: If queue is full (should not happen in normal operation)
        """
        queued_msg = QueuedMessage(
            msg_data=msg_data,
            headers=headers,
            key=key,
            offset=offset,
            handlers=handlers,
            commit_callback=commit_callback,
            max_retries=self.max_retries,
        )
        
        try:
            await asyncio.wait_for(
                self._queue.put(queued_msg),
                timeout=1.0
            )
        except asyncio.TimeoutError:
            # Queue is full - это критическая ситуация
            self._dropped_count += 1
            logger.error(
                "Queue full for partition %s:%s (size=%d, max=%d). "
                "Message at offset %d will be lost! Consider increasing max_queue_size or "
                "improving handler performance.",
                self.topic, self.partition, self._queue.qsize(), self.max_queue_size, offset
            )
            # НЕ коммитим offset - сообщение останется в Kafka для повторной попытки
            raise
        
    async def start(self) -> None:
        """Start partition processing - sequentially"""
        if self._processing:
            logger.warning(
                "Processor for partition %s:%s is already running",
                self.topic, self.partition
            )
            return
        
        # Clean up old task if it exists and is done
        if self._task and self._task.done():
            try:
                self._task.result()  # Check for exceptions
            except Exception:
                pass
            self._task = None
            
        self._processing = True
        self._task = asyncio.create_task(self._process_loop())
        
    async def _process_loop(self) -> None:
        """Main processing loop - sequential"""
        while self._processing:
            try:
                # Use timeout to periodically check if processing should stop
                try:
                    queued_msg: QueuedMessage = await asyncio.wait_for(
                        self._queue.get(), timeout=1.0
                    )
                except asyncio.TimeoutError:
                    # Timeout allows checking self._processing periodically
                    continue
                
                processing_successful = False
                try:
                    # Обрабатываем все handlers
                    for handler in queued_msg.handlers:
                        await handler(
                            queued_msg.msg_data,
                            queued_msg.headers,
                            queued_msg.key,
                            queued_msg.offset
                        )
                    
                    # Все handlers успешно обработаны - коммитим offset
                    if queued_msg.commit_callback:
                        try:
                            await queued_msg.commit_callback()
                        except Exception as e:
                            logger.error(
                                "Failed to commit offset for partition %s:%s offset %d: %s",
                                self.topic, self.partition, queued_msg.offset, e
                            )
                            # Не помечаем как успешное, если коммит не удался
                            raise
                    
                    processing_successful = True
                    self._processed_count += 1
                    
                except Exception as e:
                    self._failed_count += 1
                    queued_msg.retry_count += 1
                    
                    logger.exception(
                        "Error processing message in partition %s:%s offset %d (attempt %d/%d): %s",
                        self.topic, self.partition, queued_msg.offset,
                        queued_msg.retry_count, queued_msg.max_retries, e
                    )
                    
                    # Если превышено максимальное количество попыток - пропускаем сообщение
                    if queued_msg.retry_count >= queued_msg.max_retries:
                        logger.error(
                            "Message at partition %s:%s offset %d failed after %d attempts. "
                            "Skipping message to prevent infinite loop. "
                            "Offset will NOT be committed - message will be reprocessed on restart.",
                            self.topic, self.partition, queued_msg.offset,
                            queued_msg.max_retries
                        )
                        # НЕ коммитим offset - сообщение останется в Kafka
                        # При следующем запуске сервиса оно будет обработано снова
                    else:
                        # Повторная попытка - возвращаем сообщение в очередь
                        logger.warning(
                            "Retrying message at partition %s:%s offset %d (attempt %d/%d)",
                            self.topic, self.partition, queued_msg.offset,
                            queued_msg.retry_count, queued_msg.max_retries
                        )
                        # Небольшая задержка перед повторной попыткой
                        await asyncio.sleep(min(queued_msg.retry_count * 0.5, 5.0))
                        try:
                            await self._queue.put(queued_msg)
                            # Не вызываем task_done() так как сообщение вернулось в очередь
                            continue
                        except asyncio.QueueFull:
                            logger.error(
                                "Cannot retry message - queue is full. "
                                "Message at offset %d will be lost!",
                                queued_msg.offset
                            )
                            # Сообщение теряется, но offset не коммитится
                
                finally:
                    # Вызываем task_done() только если сообщение полностью обработано
                    # (успешно или после превышения лимита попыток)
                    if processing_successful or queued_msg.retry_count >= queued_msg.max_retries:
                        self._queue.task_done()
            except asyncio.CancelledError:
                logger.debug(
                    "Process loop cancelled for partition %s:%s",
                    self.topic, self.partition
                )
                break
            except Exception as e:
                logger.exception(
                    "Unexpected error in process loop for partition %s:%s: %s",
                    self.topic, self.partition, e
                )
                # Don't call task_done() if we didn't get an item
                if not self._queue.empty():
                    try:
                        self._queue.task_done()
                    except ValueError:
                        pass
                
    async def stop(self) -> None:
        """Stop processing and wait for completion"""
        if not self._processing:
            logger.debug(
                "Processor for partition %s:%s is not running",
                self.topic, self.partition
            )
            return
            
        self._processing = False
        
        if self._task:
            # Wait for queue to be processed with timeout
            try:
                await asyncio.wait_for(self._queue.join(), timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning(
                    "Timeout waiting for queue to empty in partition %s:%s",
                    self.topic, self.partition
                )
            
            # Cancel the task
            if not self._task.done():
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass
            else:
                # Task already done, check for exceptions
                try:
                    self._task.result()
                except Exception as e:
                    logger.exception(
                        "Task for partition %s:%s completed with error: %s",
                        self.topic, self.partition, e
                    )
            
            self._task = None
        
    def get_stats(self) -> dict[str, Any]:
        """Возвращает статистику обработки для мониторинга"""
        return {
            "topic": self.topic,
            "partition": self.partition,
            "queue_size": self._queue.qsize(),
            "max_queue_size": self.max_queue_size,
            "processed_count": self._processed_count,
            "failed_count": self._failed_count,
            "dropped_count": self._dropped_count,
            "is_processing": self._processing,
        }

