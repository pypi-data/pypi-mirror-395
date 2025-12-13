# fastkafka2\infrastructure\admin.py
import logging
from confluent_kafka.admin import NewTopic
from confluent_kafka import KafkaException
from .services.base import BaseKafkaService
from .services.retry import retry_on_connection
from .helpers.async_client import AsyncKafkaAdmin

logger = logging.getLogger(__name__)


class KafkaAdminService(BaseKafkaService):
    def __init__(self, bootstrap_servers: str = "localhost:9092") -> None:
        self._bootstrap = bootstrap_servers
        self._client: AsyncKafkaAdmin | None = None

    async def start(self) -> None:
        await self._start()

    async def stop(self) -> None:
        await self._stop()

    @retry_on_connection()
    async def _start(self) -> None:
        config = {
            "bootstrap.servers": self._bootstrap,
        }
        self._client = AsyncKafkaAdmin(config)
        await self._client.start()
        logger.info("KafkaAdminService started")

    async def create_topic(
        self, 
        topic: str,
        num_partitions: int = 1,
        replication_factor: int = 1,
        ignore_if_exists: bool = True,
    ) -> None:
        """
        Create a Kafka topic.
        
        Args:
            topic: Topic name (must be valid Kafka topic name)
            num_partitions: Number of partitions (must be > 0)
            replication_factor: Replication factor (must be > 0)
            ignore_if_exists: If True, don't raise error if topic already exists (default: True)
        
        Raises:
            RuntimeError: If admin client is not initialized
            ValueError: If parameters are invalid
            KafkaException: If topic creation fails
        """
        if not self._client:
            raise RuntimeError("Admin client not initialized")
        
        # Validate parameters
        if not topic or not topic.strip():
            raise ValueError("Topic name cannot be empty")
        if num_partitions <= 0:
            raise ValueError("num_partitions must be greater than 0")
        if replication_factor <= 0:
            raise ValueError("replication_factor must be greater than 0")
        
        try:
            new_topic = NewTopic(
                topic,
                num_partitions=num_partitions,
                replication_factor=replication_factor
            )
            results = await self._client.create_topics([new_topic])
            
            # Check results
            for topic_name, error in results.items():
                if error:
                    error_str = str(error).lower()
                    is_already_exists = (
                        "already exists" in error_str 
                        or "topic_already_exists" in error_str
                        or "topic exists" in error_str
                    )
                    
                    if is_already_exists and ignore_if_exists:
                        logger.debug("Topic %s already exists, skipping", topic_name)
                        continue
                    elif is_already_exists and not ignore_if_exists:
                        logger.warning("Topic %s already exists", topic_name)
                        raise KafkaException(f"Topic {topic_name} already exists")
                    else:
                        logger.error("Error creating topic %s: %s", topic_name, error)
                        if isinstance(error, Exception):
                            raise error
                        else:
                            raise KafkaException(f"Failed to create topic {topic_name}: {error}")
                else:
                    logger.info("Topic created: %s (partitions=%d, replication=%d)", 
                              topic_name, num_partitions, replication_factor)
        except KafkaException:
            raise
        except ValueError:
            raise
        except Exception as e:
            logger.exception("Error creating topic %s", topic)
            raise KafkaException(f"Failed to create topic {topic}: {e}") from e

    async def _stop(self) -> None:
        if self._client:
            await self._client.stop()
            logger.info("KafkaAdminService stopped")
