"""
Тесты для core/partition_manager.py и core/partition_processor.py
Покрывает PartitionManager и PartitionProcessor
Использует реальные объекты как на проде
"""
import pytest
import asyncio
from fastkafka2.core.partition_manager import PartitionManager
from fastkafka2.core.partition_processor import PartitionProcessor, QueuedMessage


class TestQueuedMessage:
    """Тесты для QueuedMessage"""
    
    def test_init(self):
        """Проверка инициализации QueuedMessage"""
        msg = QueuedMessage(
            msg_data={"key": "value"},
            headers={"header": "value"},
            key="test_key",
            offset=123,
            handlers=[],
            commit_callback=None,
        )
        
        assert msg.msg_data == {"key": "value"}
        assert msg.headers == {"header": "value"}
        assert msg.key == "test_key"
        assert msg.offset == 123
        assert msg.handlers == []
        assert msg.retry_count == 0
        assert msg.max_retries == 3


class TestPartitionProcessor:
    """Тесты для PartitionProcessor"""
    
    @pytest.fixture
    def processor(self):
        return PartitionProcessor(
            topic="test_topic",
            partition=0,
            max_queue_size=10,
            max_retries=3
        )
    
    def test_init(self, processor):
        """Проверка инициализации"""
        assert processor.topic == "test_topic"
        assert processor.partition == 0
        assert processor.max_queue_size == 10
        assert processor.max_retries == 3
        assert processor._processing is False
        assert processor._task is None
        assert processor._processed_count == 0
        assert processor._failed_count == 0
    
    @pytest.mark.asyncio
    async def test_start(self, processor):
        """Запуск processor"""
        try:
            await processor.start()
            
            assert processor._processing is True
            assert processor._task is not None
        finally:
            await processor.stop()
    
    @pytest.mark.asyncio
    async def test_stop(self, processor):
        """Остановка processor"""
        await processor.start()
        assert processor._processing is True
        
        await processor.stop()
        
        assert processor._processing is False
        assert processor._task is None


class TestPartitionManager:
    """Тесты для PartitionManager"""
    
    @pytest.fixture
    def manager(self):
        return PartitionManager(max_queue_size=10, max_retries=3)
    
    def test_init(self, manager):
        """Проверка инициализации"""
        assert manager.max_queue_size == 10
        assert manager.max_retries == 3
        assert len(manager._processors) == 0
    
    @pytest.mark.asyncio
    async def test_stop_partition(self, manager):
        """Остановка конкретной партиции"""
        # Создаем processor через process_message
        async def dummy_handler(msg_data, headers, key):
            pass
        
        try:
            await manager.process_message(
                topic="test_topic",
                partition=0,
                msg_data={},
                headers={},
                key=None,
                offset=0,
                handlers=[dummy_handler],
            )
            
            assert ("test_topic", 0) in manager._processors
            
            await manager.stop_partition("test_topic", 0)
            
            assert ("test_topic", 0) not in manager._processors
        finally:
            await manager.stop_all()
    
    @pytest.mark.asyncio
    async def test_stop_all(self, manager):
        """Остановка всех партиций"""
        async def dummy_handler(msg_data, headers, key):
            pass
        
        try:
            await manager.process_message(
                topic="test_topic",
                partition=0,
                msg_data={},
                headers={},
                key=None,
                offset=0,
                handlers=[dummy_handler],
            )
            
            await manager.process_message(
                topic="test_topic",
                partition=1,
                msg_data={},
                headers={},
                key=None,
                offset=0,
                handlers=[dummy_handler],
            )
            
            assert len(manager._processors) == 2
            
            await manager.stop_all()
            
            assert len(manager._processors) == 0
        finally:
            await manager.stop_all()
    
    def test_get_all_stats(self, manager):
        """Получение статистики"""
        stats = manager.get_all_stats()
        
        assert isinstance(stats, list)
