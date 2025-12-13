"""
Тесты для infrastructure/admin.py
Покрывает KafkaAdminService
Использует реальные объекты как на проде
"""
import pytest
from confluent_kafka import KafkaException

from fastkafka2.infrastructure.admin import KafkaAdminService


class TestKafkaAdminService:
    """Тесты для KafkaAdminService"""
    
    @pytest.fixture
    def admin_service(self, bootstrap_servers):
        return KafkaAdminService(bootstrap_servers=bootstrap_servers)
    
    @pytest.mark.asyncio
    async def test_init(self, admin_service, bootstrap_servers):
        """Проверка инициализации"""
        assert admin_service._bootstrap == bootstrap_servers
        assert admin_service._client is None
    
    @pytest.mark.asyncio
    async def test_start_success(self, admin_service):
        """Успешный запуск admin service"""
        try:
            await admin_service.start()
            
            assert admin_service._client is not None
        finally:
            await admin_service.stop()
    
    @pytest.mark.asyncio
    async def test_create_topic_not_initialized(self, admin_service):
        """Создание топика без инициализации должно вызывать ошибку"""
        with pytest.raises(RuntimeError, match="Admin client not initialized"):
            await admin_service.create_topic("test_topic")
    
    @pytest.mark.asyncio
    async def test_create_topic_empty_name(self, admin_service):
        """Создание топика с пустым именем должно вызывать ошибку"""
        try:
            await admin_service.start()
            
            with pytest.raises(ValueError, match="Topic name cannot be empty"):
                await admin_service.create_topic("")
        finally:
            await admin_service.stop()
    
    @pytest.mark.asyncio
    async def test_create_topic_invalid_partitions(self, admin_service):
        """Создание топика с невалидным количеством партиций"""
        try:
            await admin_service.start()
            
            with pytest.raises(ValueError, match="num_partitions must be greater than 0"):
                await admin_service.create_topic("test_topic", num_partitions=0)
            
            with pytest.raises(ValueError, match="num_partitions must be greater than 0"):
                await admin_service.create_topic("test_topic", num_partitions=-1)
        finally:
            await admin_service.stop()
    
    @pytest.mark.asyncio
    async def test_create_topic_invalid_replication(self, admin_service):
        """Создание топика с невалидным replication factor"""
        try:
            await admin_service.start()
            
            with pytest.raises(ValueError, match="replication_factor must be greater than 0"):
                await admin_service.create_topic("test_topic", replication_factor=0)
            
            with pytest.raises(ValueError, match="replication_factor must be greater than 0"):
                await admin_service.create_topic("test_topic", replication_factor=-1)
        finally:
            await admin_service.stop()
    
    @pytest.mark.asyncio
    async def test_stop(self, admin_service):
        """Остановка admin service"""
        await admin_service.start()
        assert admin_service._client is not None
        
        await admin_service.stop()
        
        # После остановки клиент должен быть очищен
        # (проверяем что stop не вызывает ошибок)
