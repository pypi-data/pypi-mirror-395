# fastkafka2\api\app.py
import asyncio
import logging
import signal
from typing import Callable, Any
from contextlib import AbstractAsyncContextManager

from .producer import KafkaProducer
from ..infrastructure.admin import KafkaAdminService
from ..core.consumer import KafkaConsumerService
from ..core.registry import handlers_registry
from .handler import KafkaHandler

logger = logging.getLogger(__name__)


class KafkaApp:
    def __init__(
            self,
            title: str,
            description: str,
            bootstrap_servers: str = "localhost:9092",
            group_id: str | None = None,
            lifespan: Callable[["KafkaApp"], AbstractAsyncContextManager] | None = None,
            max_queue_size: int = 1000,
            max_retries: int = 3,
    ) -> None:
        self.title = title
        self.description = description
        self.bootstrap = bootstrap_servers
        self.group_id = group_id or bootstrap_servers
        self._lifespan_func = lifespan
        self._lifespan_context: AbstractAsyncContextManager | None = None
        self.max_queue_size = max_queue_size
        self.max_retries = max_retries

        self._producer = KafkaProducer(self.bootstrap)
        self._admin = KafkaAdminService(self.bootstrap)
        self._consumer: KafkaConsumerService | None = None
        self._groups: list[KafkaHandler] = []

    def include_handler(self, handler: KafkaHandler) -> None:
        self._groups.append(handler)
        logger.debug("Included handler group %s", handler.prefix)

    async def start(self) -> None:
        logger.info("Starting %s", self.title)
        try:
            if self._lifespan_func:
                self._lifespan_context = self._lifespan_func(self)
                await self._lifespan_context.__aenter__()
            await self._admin.start()
            for topic in handlers_registry:
                await self._admin.create_topic(topic)
            self._consumer = KafkaConsumerService(
                topics=list(handlers_registry),
                bootstrap_servers=self.bootstrap,
                group_id=self.group_id,
                max_queue_size=self.max_queue_size,
                max_retries=self.max_retries,
            )
            await self._consumer.start()
            logger.info("%s started", self.title)
        except Exception:
            logger.exception("KafkaApp.start failed")
            # Cleanup lifespan if it was started
            if self._lifespan_context:
                try:
                    await self._lifespan_context.__aexit__(None, None, None)
                except Exception:
                    logger.exception("Error during lifespan cleanup in start")
            raise

    async def stop(self) -> None:
        logger.info("Stopping %s", self.title)
        errors = []
        try:
            if self._consumer:
                try:
                    await self._consumer.stop()
                except Exception as e:
                    errors.append(e)
                    logger.exception("Error stopping consumer")
            try:
                await self._admin.stop()
            except Exception as e:
                errors.append(e)
                logger.exception("Error stopping admin")
            if self._lifespan_context:
                try:
                    await self._lifespan_context.__aexit__(None, None, None)
                except Exception as e:
                    errors.append(e)
                    logger.exception("Error exiting lifespan context")
                finally:
                    self._lifespan_context = None
            logger.info("%s stopped", self.title)
        except Exception:
            logger.exception("KafkaApp.stop failed")
            raise
        if errors:
            raise RuntimeError(f"Errors during stop: {errors}")

    async def run(self) -> None:
        loop = asyncio.get_running_loop()
        shutdown_event = asyncio.Event()
        try:
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, shutdown_event.set)
        except (NotImplementedError, AttributeError, OSError):
            # Windows doesn't support SIGTERM, fallback to SIGINT only
            try:
                signal.signal(signal.SIGINT, lambda *_: shutdown_event.set())
            except (ValueError, OSError):
                logger.warning("Could not set signal handlers")
        try:
            await self.start()
            await shutdown_event.wait()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        finally:
            await self.stop()
    
    def get_stats(self) -> dict[str, Any]:
        """Возвращает статистику обработки сообщений для мониторинга"""
        if self._consumer:
            return self._consumer.get_stats()
        return {
            "topics": [],
            "group_id": self.group_id,
            "running": False,
            "partitions": [],
        }
