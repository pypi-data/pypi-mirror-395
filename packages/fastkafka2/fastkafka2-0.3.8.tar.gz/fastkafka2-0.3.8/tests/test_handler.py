"""
Тесты для api/handler.py
Покрывает KafkaHandler
Использует реальные объекты как на проде
"""
import pytest
from pydantic import BaseModel

from fastkafka2.api.handler import KafkaHandler
from fastkafka2.core.registry import handlers_registry
from fastkafka2.api.message import KafkaMessage


# Классы на уровне модуля для тестов (не начинаются с Test чтобы pytest не пытался их собирать)
class HandlerTestDataModel(BaseModel):
    name: str


class HandlerTestHeadersModel(BaseModel):
    key: str


class TestKafkaHandler:
    """Тесты для KafkaHandler"""
    
    def test_init_with_prefix(self):
        """Инициализация с префиксом"""
        handler = KafkaHandler(prefix="test.prefix")
        assert handler.prefix == "test.prefix"
    
    def test_init_without_prefix(self):
        """Инициализация без префикса"""
        handler = KafkaHandler()
        assert handler.prefix == ""
    
    def test_call_registers_handler(self):
        """Проверка регистрации handler через __call__"""
        handlers_registry.clear()
        
        handler = KafkaHandler(prefix="test")
        
        @handler("my_topic")
        async def test_handler(message: KafkaMessage[HandlerTestDataModel, HandlerTestHeadersModel]):
            pass
        
        # Проверяем, что handler был зарегистрирован
        assert "test.my_topic" in handlers_registry
        assert len(handlers_registry["test.my_topic"]) > 0
    
    def test_call_with_prefix(self):
        """Проверка добавления префикса к топику"""
        handlers_registry.clear()
        
        handler = KafkaHandler(prefix="test")
        
        @handler("my_topic")
        async def test_handler(message: KafkaMessage[HandlerTestDataModel, HandlerTestHeadersModel]):
            pass
        
        # Проверяем, что был зарегистрирован полный топик с префиксом
        assert "test.my_topic" in handlers_registry
    
    def test_call_without_prefix(self):
        """Проверка без префикса"""
        handlers_registry.clear()
        
        handler = KafkaHandler()
        
        @handler("my_topic")
        async def test_handler(message: KafkaMessage[HandlerTestDataModel, HandlerTestHeadersModel]):
            pass
        
        assert "my_topic" in handlers_registry
    
    def test_call_with_headers_filter(self):
        """Проверка с фильтром headers"""
        handlers_registry.clear()
        
        handler = KafkaHandler()
        
        headers_filter = {"type": "test"}
        
        @handler("my_topic", headers_filter=headers_filter)
        async def test_handler(message: KafkaMessage[HandlerTestDataModel, HandlerTestHeadersModel]):
            pass
        
        assert "my_topic" in handlers_registry
    
    def test_include_handler_success(self):
        """Успешное включение другого handler"""
        handler1 = KafkaHandler(prefix="prefix1")
        handler2 = KafkaHandler(prefix="prefix2")
        
        handler1.include_handler(handler2)
        
        assert handler1.prefix == "prefix1.prefix2"
    
    def test_include_handler_empty_prefix(self):
        """Включение handler с пустым префиксом"""
        handler1 = KafkaHandler(prefix="prefix1")
        handler2 = KafkaHandler(prefix="")
        
        handler1.include_handler(handler2)
        
        assert handler1.prefix == "prefix1"
    
    def test_include_handler_both_empty(self):
        """Включение handler когда оба префикса пустые"""
        handler1 = KafkaHandler(prefix="")
        handler2 = KafkaHandler(prefix="")
        
        handler1.include_handler(handler2)
        
        assert handler1.prefix == ""
    
    def test_include_handler_wrong_type(self):
        """Включение неправильного типа должно вызывать ошибку"""
        handler = KafkaHandler()
        
        with pytest.raises(TypeError, match="Expected KafkaHandler"):
            handler.include_handler("not a handler")
        
        with pytest.raises(TypeError, match="Expected KafkaHandler"):
            handler.include_handler(None)
        
        with pytest.raises(TypeError, match="Expected KafkaHandler"):
            handler.include_handler(123)
