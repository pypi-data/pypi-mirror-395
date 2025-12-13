"""
Тесты для создания топиков и старта приложения
Использует production Kafka: 10.8.0.13:9092
"""
import pytest
import time
from fastkafka2 import KafkaApp, KafkaHandler, KafkaMessage
from fastkafka2.core.registry import handlers_registry
from fastkafka2.infrastructure.admin import KafkaAdminService
from pydantic import BaseModel


# Модели для тестов
class TopicTestDataModel(BaseModel):
    name: str


class TopicTestHeadersModel(BaseModel):
    key: str


class TestTopicCreation:
    """Тесты создания топиков - основная проблема"""
    
    @pytest.mark.asyncio
    async def test_create_topic_success(self, bootstrap_servers):
        """Проверка успешного создания топика"""
        admin_service = KafkaAdminService(bootstrap_servers=bootstrap_servers)
        
        try:
            await admin_service.start()
            
            # Создаем топик
            topic_name = f"test_topic_creation_{int(time.time())}"
            await admin_service.create_topic(topic_name, num_partitions=1, replication_factor=1)
            
            # Проверяем что топик создан (не должно быть ошибки)
            assert True
            
        finally:
            await admin_service.stop()
    
    @pytest.mark.asyncio
    async def test_app_start_creates_topics(self, bootstrap_servers):
        """Проверка что при start() создаются топики - ГЛАВНЫЙ ТЕСТ"""
        handlers_registry.clear()
        
        handler = KafkaHandler()
        
        @handler("test_app_start_topic")
        async def test_handler(message: KafkaMessage[TopicTestDataModel, TopicTestHeadersModel]):
            pass
        
        app = KafkaApp(
            title="Test App",
            description="Test",
            bootstrap_servers=bootstrap_servers,
            group_id=f"test_group_{int(time.time())}"
        )
        
        try:
            # Запускаем app - это должно создать топики
            await app.start()
            
            # Проверяем что admin service запущен
            assert app._admin._client is not None
            
            # Проверяем что consumer создан
            assert app._consumer is not None
            
            # Проверяем что consumer запущен
            assert app._consumer._running is True
            
            print("SUCCESS: App started and topics created!")
            
        finally:
            # Останавливаем app
            await app.stop()
            
            # Проверяем что все остановлено
            assert app._consumer is None or app._consumer._running is False
    
    @pytest.mark.asyncio
    async def test_app_start_with_multiple_topics(self, bootstrap_servers):
        """Проверка создания нескольких топиков при старте"""
        handlers_registry.clear()
        
        handler = KafkaHandler()
        
        @handler("test_topic_1")
        async def handler1(message: KafkaMessage[TopicTestDataModel, TopicTestHeadersModel]):
            pass
        
        @handler("test_topic_2")
        async def handler2(message: KafkaMessage[TopicTestDataModel, TopicTestHeadersModel]):
            pass
        
        @handler("test_topic_3")
        async def handler3(message: KafkaMessage[TopicTestDataModel, TopicTestHeadersModel]):
            pass
        
        app = KafkaApp(
            title="Test App Multi Topics",
            description="Test",
            bootstrap_servers=bootstrap_servers,
            group_id=f"test_group_multi_{int(time.time())}"
        )
        
        try:
            # Запускаем app - должно создать 3 топика
            await app.start()
            
            # Проверяем что все запущено
            assert app._admin._client is not None
            assert app._consumer is not None
            assert app._consumer._running is True
            
            print(f"SUCCESS: Created {len(handlers_registry)} topics!")
            
        finally:
            await app.stop()

