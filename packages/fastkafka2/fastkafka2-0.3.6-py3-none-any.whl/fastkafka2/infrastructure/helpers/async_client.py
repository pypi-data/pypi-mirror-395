# fastkafka2/infrastructure/helpers/async_client.py
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Optional, Sequence
from contextlib import suppress

from confluent_kafka import Consumer, Producer, Message, KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic

logger = logging.getLogger(__name__)


class AsyncKafkaConsumer:
    """Async wrapper over confluent_kafka.Consumer"""
    
    def __init__(
        self,
        config: dict,
        topics: Optional[Sequence[str]] = None,
        on_assign: Optional[Callable] = None,
        on_revoke: Optional[Callable] = None,
        on_lost: Optional[Callable] = None,
    ):
        self.config = config
        self.topics = topics
        self._consumer: Optional[Consumer] = None
        self._thread_pool: Optional[ThreadPoolExecutor] = None
        self._running = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._stopped = False
        
        # Rebalance callbacks
        self._on_assign = on_assign
        self._on_revoke = on_revoke
        self._on_lost = on_lost
        
    async def start(self) -> None:
        """Start the consumer and subscribe to topics"""
        if self._running:
            return
        if self._stopped:
            raise RuntimeError("Consumer has been stopped and cannot be restarted")
        
        loop = asyncio.get_running_loop()
        
        # Store loop for callbacks
        self._loop = loop
        
        # Create thread pool if not exists
        if self._thread_pool is None:
            self._thread_pool = ThreadPoolExecutor(max_workers=1)
        
        def create_consumer():
            consumer = Consumer(self.config)
            
            # Set up rebalance callbacks
            if self._on_assign or self._on_revoke or self._on_lost:
                def safe_run_coro(coro, loop_ref):
                    """Safely run coroutine in thread-safe manner"""
                    try:
                        if loop_ref and not loop_ref.is_closed():
                            asyncio.run_coroutine_threadsafe(coro, loop_ref)
                        else:
                            logger.warning("Event loop is closed, skipping callback")
                    except Exception as e:
                        logger.exception("Error in rebalance callback: %s", e)
                
                def on_assign(consumer, partitions):
                    if self._on_assign:
                        coro = self._on_assign(consumer, partitions)
                        safe_run_coro(coro, self._loop)
                
                def on_revoke(consumer, partitions):
                    if self._on_revoke:
                        coro = self._on_revoke(consumer, partitions)
                        safe_run_coro(coro, self._loop)
                
                def on_lost(consumer, partitions):
                    if self._on_lost:
                        coro = self._on_lost(consumer, partitions)
                        safe_run_coro(coro, self._loop)
                
                consumer.subscribe(
                    self.topics or [],
                    on_assign=on_assign,
                    on_revoke=on_revoke,
                    on_lost=on_lost,
                )
            elif self.topics:
                consumer.subscribe(self.topics)
            
            return consumer
        
        self._consumer = await loop.run_in_executor(
            self._thread_pool,
            create_consumer
        )
        self._running = True
        logger.info("AsyncKafkaConsumer started")
        
    async def poll(self, timeout: float = 1.0) -> Optional[Message]:
        """Poll for a message"""
        if not self._consumer or not self._running or not self._thread_pool:
            return None
            
        loop = asyncio.get_running_loop()
        try:
            msg = await loop.run_in_executor(
                self._thread_pool,
                self._consumer.poll,
                timeout
            )
            
            if msg is None:
                return None
                
            if msg.error():
                error = msg.error()
                if error.code() == KafkaError._PARTITION_EOF:
                    return None
                raise KafkaException(error)
                
            return msg
        except Exception as e:
            logger.exception("Error polling message")
            raise
            
    async def commit(self, message: Optional[Message] = None, asynchronous: bool = False) -> None:
        """Commit offset"""
        if not self._consumer or not self._thread_pool:
            raise RuntimeError("Consumer not started")
            
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            self._thread_pool,
            self._consumer.commit,
            message,
            asynchronous
        )
        
    async def stop(self) -> None:
        """Stop the consumer"""
        if self._stopped:
            return
        
        self._running = False
        self._stopped = True
        
        if self._consumer:
            # Commit pending offsets before closing
            try:
                await self.commit(asynchronous=False)
            except Exception as e:
                logger.warning("Error committing offsets on stop: %s", e)
            
            try:
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(
                    self._thread_pool,
                    self._consumer.close
                )
            except RuntimeError:
                # Loop is closed, close consumer synchronously
                if self._thread_pool:
                    self._thread_pool.submit(self._consumer.close).result(timeout=5.0)
            except Exception as e:
                logger.warning("Error closing consumer: %s", e)
            
        if self._thread_pool:
            self._thread_pool.shutdown(wait=True)
            self._thread_pool = None
        
        logger.info("AsyncKafkaConsumer stopped")


class AsyncKafkaProducer:
    """Async wrapper over confluent_kafka.Producer"""
    
    def __init__(self, config: dict):
        self.config = config
        self._producer: Optional[Producer] = None
        self._poll_task: Optional[asyncio.Task] = None
        self._running = False
        self._stopped = False
        self._thread_pool: Optional[ThreadPoolExecutor] = None
        
    async def start(self) -> None:
        """Start the producer"""
        if self._running:
            return
        if self._stopped:
            raise RuntimeError("Producer has been stopped and cannot be restarted")
        
        loop = asyncio.get_running_loop()
        
        # Create thread pool if not exists
        if self._thread_pool is None:
            self._thread_pool = ThreadPoolExecutor(max_workers=1)
        
        self._producer = await loop.run_in_executor(
            self._thread_pool,
            lambda: Producer(self.config)
        )
        self._running = True
        self._poll_task = asyncio.create_task(self._poll_loop())
        logger.info("AsyncKafkaProducer started")
        
    async def _poll_loop(self) -> None:
        """Poll loop for producer callbacks"""
        while self._running:
            try:
                if self._producer:
                    loop = asyncio.get_running_loop()
                    await loop.run_in_executor(
                        self._thread_pool,
                        self._producer.poll,
                        0.1
                    )
                await asyncio.sleep(0.01)
            except Exception as e:
                logger.exception("Error in producer poll loop")
                await asyncio.sleep(0.1)
                
    async def send(
        self,
        topic: str,
        value: bytes,
        key: Optional[bytes] = None,
        headers: Optional[list[tuple[str, bytes]]] = None,
        partition: Optional[int] = None,
    ) -> Message:
        """Send a message"""
        if not self._producer or not self._thread_pool:
            raise RuntimeError("Producer not started")
            
        loop = asyncio.get_running_loop()
        future: asyncio.Future[Message] = loop.create_future()
        
        def delivery_callback(err: Optional[KafkaError], msg: Optional[Message]) -> None:
            if err:
                loop.call_soon_threadsafe(
                    future.set_exception,
                    KafkaException(err)
                )
            elif msg and msg.error():
                loop.call_soon_threadsafe(
                    future.set_exception,
                    KafkaException(msg.error())
                )
            else:
                loop.call_soon_threadsafe(
                    future.set_result,
                    msg
                )
        
        # Produce must be called from the same thread as producer was created
        def produce():
            try:
                produce_kwargs = {
                    "topic": topic,
                    "value": value,
                    "callback": delivery_callback,
                }
                if key is not None:
                    produce_kwargs["key"] = key
                if headers is not None:
                    produce_kwargs["headers"] = headers
                if partition is not None:
                    produce_kwargs["partition"] = partition
                self._producer.produce(**produce_kwargs)
            except Exception as e:
                loop.call_soon_threadsafe(future.set_exception, e)
        
        await loop.run_in_executor(self._thread_pool, produce)
        return await future
        
    async def flush(self, timeout: float = 10.0) -> None:
        """Flush pending messages"""
        if not self._producer or not self._thread_pool:
            return
            
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            self._thread_pool,
            self._producer.flush,
            timeout
        )
        
    async def stop(self) -> None:
        """Stop the producer"""
        if self._stopped:
            return
        
        self._running = False
        self._stopped = True
        
        if self._poll_task:
            self._poll_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._poll_task
                
        if self._producer:
            try:
                await self.flush()
            except Exception as e:
                logger.warning("Error flushing producer: %s", e)
            
        if self._thread_pool:
            self._thread_pool.shutdown(wait=True)
            self._thread_pool = None
        
        logger.info("AsyncKafkaProducer stopped")


class AsyncKafkaAdmin:
    """Async wrapper over confluent_kafka.admin.AdminClient"""
    
    def __init__(self, config: dict):
        self.config = config
        self._client: Optional[AdminClient] = None
        self._thread_pool: Optional[ThreadPoolExecutor] = None
        self._stopped = False
        
    async def start(self) -> None:
        """Start the admin client"""
        if self._client is not None:
            return
        if self._stopped:
            raise RuntimeError("Admin client has been stopped and cannot be restarted")
        
        loop = asyncio.get_running_loop()
        
        # Create thread pool if not exists
        if self._thread_pool is None:
            self._thread_pool = ThreadPoolExecutor(max_workers=1)
        
        self._client = await loop.run_in_executor(
            self._thread_pool,
            lambda: AdminClient(self.config)
        )
        logger.info("AsyncKafkaAdmin started")
        
    async def create_topics(
        self,
        topics: list[NewTopic],
        timeout: float = 10.0,
    ) -> dict[str, Any]:
        """Create topics"""
        if not self._client or not self._thread_pool:
            raise RuntimeError("Admin client not started")
            
        loop = asyncio.get_running_loop()
        
        def create():
            futures = self._client.create_topics(topics, request_timeout=timeout)
            # Wait for all futures
            results = {}
            for topic, future in futures.items():
                try:
                    future.result(timeout=timeout)
                    results[topic] = None
                except Exception as e:
                    results[topic] = e
            return results
        
        return await loop.run_in_executor(self._thread_pool, create)
        
    async def stop(self) -> None:
        """Stop the admin client"""
        if self._stopped:
            return
        
        self._stopped = True
        # AdminClient doesn't have explicit close, but we can clean up executor
        if self._thread_pool:
            self._thread_pool.shutdown(wait=True)
            self._thread_pool = None
        logger.info("AsyncKafkaAdmin stopped")

