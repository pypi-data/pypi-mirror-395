"""
Тесты для api/app.py
Покрывает KafkaApp
Использует реальные объекты как на проде
"""
import pytest
import asyncio
from contextlib import asynccontextmanager

from fastkafka2.api.app import KafkaApp
from fastkafka2.api.handler import KafkaHandler
from fastkafka2.core.registry import handlers_registry


class TestKafkaApp:
    """Тесты для KafkaApp"""
    
    @pytest.fixture
    def app(self, bootstrap_servers):
        return KafkaApp(
            title="Test App",
            description="Test Description",
            bootstrap_servers=bootstrap_servers,
            group_id="test_group"
        )
    
    def test_init(self, app, bootstrap_servers):
        """Проверка инициализации"""
        assert app.title == "Test App"
        assert app.description == "Test Description"
        assert app.bootstrap == bootstrap_servers
        assert app.group_id == "test_group"
        assert app._producer is not None
        assert app._admin is not None
        assert app._consumer is None
        assert app._groups == []
    
    def test_init_default_group_id(self, bootstrap_servers):
        """Проверка дефолтного group_id"""
        app = KafkaApp(
            title="Test",
            description="Test",
            bootstrap_servers=bootstrap_servers
        )
        assert app.group_id == bootstrap_servers
    
    def test_include_handler(self, app):
        """Проверка добавления handler"""
        handler = KafkaHandler(prefix="test")
        app.include_handler(handler)
        
        assert len(app._groups) == 1
        assert app._groups[0] == handler
    
    def test_get_stats_without_consumer(self, app):
        """Получение статистики без consumer"""
        stats = app.get_stats()
        
        assert stats == {
            "topics": [],
            "group_id": app.group_id,
            "running": False,
            "partitions": [],
        }
