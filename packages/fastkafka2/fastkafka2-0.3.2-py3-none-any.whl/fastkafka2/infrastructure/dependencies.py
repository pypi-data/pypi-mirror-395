# fastkafka2\infrastructure\dependencies.py
import logging
from .admin import KafkaAdminService
from ..core.consumer import KafkaConsumerService
from ..core.registry import handlers_registry

logger = logging.getLogger(__name__)
_admin: KafkaAdminService | None = None
_consumer: KafkaConsumerService | None = None


async def start_kafka(bootstrap_servers: str, group_id: str | None = None) -> None:
    global _admin, _consumer
    if _admin is not None or _consumer is not None:
        logger.warning("Kafka dependencies are already started. Call stop_kafka() first.")
        return
    
    admin = None
    consumer = None
    try:
        admin = KafkaAdminService(bootstrap_servers)
        await admin.start()
        for topic in handlers_registry:
            await admin.create_topic(topic)
        
        consumer = KafkaConsumerService(
            topics=list(handlers_registry),
            bootstrap_servers=bootstrap_servers,
            group_id=group_id or bootstrap_servers,
        )
        await consumer.start()
        
        # Only assign to globals after successful start
        _admin = admin
        _consumer = consumer
        logger.info("Dependencies started")
    except Exception:
        logger.exception("Failed to start Kafka dependencies")
        # Cleanup on error
        if consumer:
            try:
                await consumer.stop()
            except Exception as e:
                logger.exception("Error stopping consumer during cleanup: %s", e)
        if admin:
            try:
                await admin.stop()
            except Exception as e:
                logger.exception("Error stopping admin during cleanup: %s", e)
        raise


async def stop_kafka() -> None:
    global _admin, _consumer
    if _admin is None and _consumer is None:
        logger.warning("Kafka dependencies are not started")
        return
    
    errors = []
    consumer = _consumer
    admin = _admin
    
    # Clear globals first to prevent re-entry
    _consumer = None
    _admin = None
    
    # Stop consumer first
    if consumer:
        try:
            await consumer.stop()
        except Exception as e:
            errors.append(f"consumer: {e}")
            logger.exception("Error stopping consumer: %s", e)
    
    # Stop admin last
    if admin:
        try:
            await admin.stop()
        except Exception as e:
            errors.append(f"admin: {e}")
            logger.exception("Error stopping admin: %s", e)
    
    if errors:
        logger.warning("Dependencies stopped with errors: %s", errors)
    else:
        logger.info("Dependencies stopped")
