"""
Тесты для core/consumer.py
Покрывает KafkaConsumerService
Использует реальные объекты как на проде
"""
import pytest
from fastkafka2.core.consumer import KafkaConsumerService
from fastkafka2.core.registry import handlers_registry


class TestKafkaConsumerService:
    """Тесты для KafkaConsumerService"""
    
    @pytest.fixture
    def consumer_service(self, bootstrap_servers):
        return KafkaConsumerService(
            topics=["test_topic"],
            bootstrap_servers=bootstrap_servers,
            group_id="test_group"
        )
    
    def test_init(self, consumer_service, bootstrap_servers):
        """Проверка инициализации"""
        assert consumer_service._topics == ["test_topic"]
        assert consumer_service._bootstrap == bootstrap_servers
        assert consumer_service._group_id == "test_group"
        assert consumer_service._enable_auto_commit is False
        assert consumer_service._consumer is None
        assert consumer_service._running is False
    
    def test_init_default_group_id(self, bootstrap_servers):
        """Проверка дефолтного group_id"""
        service = KafkaConsumerService(
            topics=["test_topic"],
            bootstrap_servers=bootstrap_servers
        )
        assert service._group_id == "fastkafka_group"
    
    @pytest.mark.asyncio
    async def test_start_already_running(self, consumer_service):
        """Повторный запуск не должен делать ничего"""
        try:
            await consumer_service.start()
            assert consumer_service._running is True
            
            # Повторный запуск
            await consumer_service.start()
            assert consumer_service._running is True
        finally:
            await consumer_service.stop()
    
    @pytest.mark.asyncio
    async def test_stop_not_running(self, consumer_service):
        """Остановка без запуска не должна вызывать ошибку"""
        await consumer_service.stop()
        
        assert consumer_service._running is False
    
    def test_get_stats(self, consumer_service):
        """Получение статистики"""
        stats = consumer_service.get_stats()
        
        assert "topics" in stats
        assert "group_id" in stats
        assert "running" in stats
        assert stats["running"] is False
        assert stats["topics"] == ["test_topic"]
    
    def test_get_stats_not_running(self, consumer_service):
        """Получение статистики когда не запущен"""
        stats = consumer_service.get_stats()
        
        assert stats["running"] is False
