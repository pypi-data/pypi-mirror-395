# fastkafka2\core\consumer.py
import asyncio
import logging
from typing import Any, Awaitable, Callable, Optional
from confluent_kafka import Message

from ..infrastructure.services.base import BaseKafkaService
from .registry import handlers_registry
from ..infrastructure.helpers.async_client import AsyncKafkaConsumer
from .partition_manager import PartitionManager
from .rebalance_handler import RebalanceHandler
from ..api.message import LazyDeserializedBody

logger = logging.getLogger(__name__)


class KafkaConsumerService(BaseKafkaService):
    def __init__(
        self,
        topics: list[str],
        bootstrap_servers: str,
        group_id: str | None = None,
        enable_auto_commit: bool = False,
        auto_offset_reset: str = "earliest",
        max_queue_size: int = 1000,
        max_retries: int = 3,
    ):
        self._topics = topics
        self._bootstrap = bootstrap_servers
        self._group_id = group_id or "fastkafka_group"
        self._enable_auto_commit = enable_auto_commit
        self._auto_offset_reset = auto_offset_reset
        
        self._consumer: Optional[AsyncKafkaConsumer] = None
        self._partition_manager = PartitionManager(
            max_queue_size=max_queue_size,
            max_retries=max_retries,
        )
        self._rebalance_handler = RebalanceHandler(self._partition_manager)
        self._consume_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        if self._running:
            logger.warning("KafkaConsumerService is already running")
            return
            
        config = {
            "bootstrap.servers": self._bootstrap,
            "group.id": self._group_id,
            "auto.offset.reset": self._auto_offset_reset,
            "enable.auto.commit": "true" if self._enable_auto_commit else "false",
        }
        
        try:
            self._consumer = AsyncKafkaConsumer(
                config=config,
                topics=self._topics,
                on_assign=self._rebalance_handler.on_assign,
                on_revoke=self._rebalance_handler.on_revoke,
                on_lost=self._rebalance_handler.on_lost,
            )
            
            await self._consumer.start()
            self._running = True
            self._consume_task = asyncio.create_task(self._consume_loop())
            
            logger.info(
                "KafkaConsumerService started on topics %s (group_id=%s, auto_commit=%s)",
                self._topics, self._group_id, self._enable_auto_commit
            )
        except Exception:
            logger.exception("Failed to start KafkaConsumerService")
            self._running = False
            self._consumer = None
            raise

    async def stop(self) -> None:
        if not self._running:
            logger.warning("KafkaConsumerService is not running")
            return
            
        self._running = False
        
        # Cancel consume task first
        if self._consume_task:
            self._consume_task.cancel()
            try:
                await self._consume_task
            except asyncio.CancelledError:
                pass
            finally:
                self._consume_task = None
                
        # Stop partition manager to finish processing current messages
        try:
            await self._partition_manager.stop_all()
        except Exception as e:
            logger.exception("Error stopping partition manager: %s", e)
        
        # Stop consumer last
        if self._consumer:
            try:
                await self._consumer.stop()
            except Exception as e:
                logger.exception("Error stopping consumer: %s", e)
            finally:
                self._consumer = None
            
        logger.info("Consumer stopped")
    
    def get_stats(self) -> dict[str, Any]:
        """Возвращает статистику обработки сообщений для мониторинга"""
        return {
            "topics": self._topics,
            "group_id": self._group_id,
            "auto_commit": self._enable_auto_commit,
            "running": self._running,
            "partitions": self._partition_manager.get_all_stats(),
        }

    async def _consume_loop(self) -> None:
        """Main consumption loop"""
        while self._running:
            if not self._consumer:
                logger.error("Consumer is None, stopping consume loop")
                break
                
            try:
                msg: Optional[Message] = await self._consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                    
                commit_callback = None
                if not self._enable_auto_commit:
                    msg_to_commit = msg
                    consumer_ref = self._consumer
                    async def commit_offset():
                        try:
                            if consumer_ref:
                                await consumer_ref.commit(msg_to_commit, asynchronous=False)
                        except Exception as e:
                            logger.error("Error committing offset: %s", e)
                    commit_callback = commit_offset
                
                await self._process_message(msg, commit_callback)
                        
            except asyncio.CancelledError:
                logger.debug("Consume loop cancelled")
                break
            except Exception:
                logger.exception("Error in consume loop")
                if self._running:
                    await asyncio.sleep(1)
                else:
                    break

    async def _process_message(
        self, 
        msg: Message,
        commit_callback: Optional[Callable[[], Awaitable[None]]] = None
    ) -> None:
        """
        Process single message through PartitionManager.
        Тело сообщения НЕ десериализуется сразу - используется LazyDeserializedBody
        для ленивой десериализации только когда обработчик принял сообщение.
        """
        topic = msg.topic()
        partition = msg.partition()
        offset = msg.offset()
        
        # Читаем только заголовки (быстро) - тело остается в raw bytes
        try:
            headers = {}
            if msg.headers():
                for k, v in msg.headers():
                    headers[k] = v.decode() if isinstance(v, bytes) else v
            key = None
            msg_key = msg.key()
            if msg_key:
                key = msg_key.decode() if isinstance(msg_key, bytes) else msg_key
            
            # Создаем lazy-объект для тела сообщения (десериализация отложена)
            lazy_body = LazyDeserializedBody(msg.value())
        except Exception as e:
            logger.error("Error reading headers/key for topic %s partition %s offset %s: %s", 
                        topic, partition, offset, e)
            return
        
        # Фильтруем обработчики по заголовкам БЕЗ десериализации тела
        handlers = handlers_registry.get(topic, [])
        if not handlers:
            logger.warning(
                "No handlers found for topic: %s. Message at offset %d will NOT be committed. "
                "It will be reprocessed on restart. Consider registering a handler for this topic.",
                topic, offset
            )
            # НЕ коммитим offset - сообщение останется в Kafka для обработки после регистрации handler
            return
            
        matching_handlers = []
        for handler in handlers:
            try:
                if hasattr(handler, "matches_headers"):
                    if not handler.matches_headers(headers):
                        continue
                matching_handlers.append(handler)
            except Exception as e:
                logger.exception("Header predicate failed for topic %s", topic)
                continue
        
        # Если нет подходящих обработчиков - тело не десериализуется вообще
        if not matching_handlers:
            logger.debug(
                "No handlers matched headers for topic %s offset %d. "
                "Message will NOT be committed and will be reprocessed.",
                topic, offset
            )
            # НЕ коммитим offset - сообщение останется в Kafka
            # Возможно, handler появится позже или headers изменятся
            return
                
        handler_wrappers = []
        for h in matching_handlers:
            # Явно захватываем handler через замыкание с дефолтным значением
            def make_handler(handler):
                async def handle_message(
                    lazy_body_obj, 
                    msg_headers, 
                    msg_key, 
                    msg_offset
                ):
                    try:
                        # Тело десериализуется только здесь, когда обработчик принял сообщение
                        await handler.handle(lazy_body_obj, msg_headers, msg_key)
                    except Exception as e:
                        logger.error("Handler error on topic %s: %s", handler.topic, e)
                        raise
                return handle_message
            handler_wrappers.append(make_handler(h))
                    
        try:
            await self._partition_manager.process_message(
                topic=topic,
                partition=partition,
                msg_data=lazy_body,  # Передаем LazyDeserializedBody вместо десериализованных данных
                headers=headers,
                key=key,
                offset=offset,
                handlers=handler_wrappers,
                commit_callback=commit_callback,
            )
        except asyncio.TimeoutError:
            # Очередь переполнена (timeout при добавлении) - критическая ситуация
            logger.error(
                "Cannot add message to queue for topic %s partition %d offset %d (queue full/timeout). "
                "Message will NOT be committed and will be reprocessed. "
                "Consider increasing max_queue_size or improving handler performance.",
                topic, partition, offset
            )
            # НЕ коммитим offset - сообщение останется в Kafka
            # При следующем запуске или когда очередь освободится, сообщение будет обработано снова
