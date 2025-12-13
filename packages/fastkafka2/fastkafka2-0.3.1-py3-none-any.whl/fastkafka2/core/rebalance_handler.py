# fastkafka2/core/rebalance_handler.py
import logging
from typing import Callable, Optional
from confluent_kafka import Consumer, TopicPartition

from .partition_manager import PartitionManager

logger = logging.getLogger(__name__)


class RebalanceHandler:
    """Handles Kafka rebalance events"""
    
    def __init__(self, partition_manager: PartitionManager):
        self.partition_manager = partition_manager
        
    async def on_assign(
        self,
        consumer: Consumer,
        partitions: list[TopicPartition]
    ) -> None:
        """Called when partitions are assigned"""
        if not partitions:
            logger.debug("No partitions assigned")
            return
        
        try:
            logger.info(
                "Partitions assigned: %s",
                [(p.topic, p.partition) for p in partitions]
            )
        except Exception as e:
            logger.exception("Error logging assigned partitions: %s", e)
        
    async def on_revoke(
        self,
        consumer: Consumer,
        partitions: list[TopicPartition]
    ) -> None:
        """Called when partitions are revoked"""
        if not partitions:
            logger.debug("No partitions revoked")
            return
        
        try:
            logger.info(
                "Partitions revoked: %s",
                [(p.topic, p.partition) for p in partitions]
            )
        except Exception as e:
            logger.exception("Error logging revoked partitions: %s", e)
        
        # Stop all revoked partitions
        errors = []
        for p in partitions:
            if p is None:
                logger.warning("Received None partition in revoke callback")
                continue
            try:
                await self.partition_manager.stop_partition(p.topic, p.partition)
            except Exception as e:
                errors.append((p.topic, p.partition, e))
                logger.exception(
                    "Error stopping partition %s:%s: %s",
                    p.topic, p.partition, e
                )
        
        if errors:
            logger.warning(
                "Failed to stop %d partitions during revoke: %s",
                len(errors), errors
            )
                    
    async def on_lost(
        self,
        consumer: Consumer,
        partitions: list[TopicPartition]
    ) -> None:
        """Called when partitions are lost"""
        if not partitions:
            logger.debug("No partitions lost")
            return
        
        try:
            logger.warning(
                "Partitions lost: %s",
                [(p.topic, p.partition) for p in partitions]
            )
        except Exception as e:
            logger.exception("Error logging lost partitions: %s", e)
        
        # Stop all lost partitions
        errors = []
        for p in partitions:
            if p is None:
                logger.warning("Received None partition in lost callback")
                continue
            try:
                await self.partition_manager.stop_partition(p.topic, p.partition)
            except Exception as e:
                errors.append((p.topic, p.partition, e))
                logger.exception(
                    "Error stopping lost partition %s:%s: %s",
                    p.topic, p.partition, e
                )
        
        if errors:
            logger.warning(
                "Failed to stop %d partitions during lost: %s",
                len(errors), errors
            )

