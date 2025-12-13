"""
Тесты для core/registry.py
Покрывает kafka_handler и функции извлечения моделей
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from pydantic import BaseModel
from typing import get_type_hints

from fastkafka2.core.registry import (
    kafka_handler,
    handlers_registry,
    _resolve_nested_class,
    _extract_model_from_type_arg,
)
from fastkafka2.api.message import KafkaMessage


class TestResolveNestedClass:
    """Тесты для _resolve_nested_class"""
    
    def test_resolve_simple_class(self):
        """Разрешение простого класса"""
        class TestModel(BaseModel):
            name: str
        
        # Создаем модуль с классом
        class TestModule:
            pass
        
        # Присваиваем класс как атрибут после создания
        TestModule.TestModel = TestModel
        
        result = _resolve_nested_class("TestModel", TestModule())
        assert result == TestModel
    
    def test_resolve_nested_class(self):
        """Разрешение вложенного класса"""
        class Headers(BaseModel):
            key: str
        
        class TestTopic:
            pass
        
        # Присваиваем класс как атрибут после создания
        TestTopic.Headers = Headers
        
        class TestModule:
            pass
        
        TestModule.TestTopic = TestTopic
        
        module = TestModule()
        result = _resolve_nested_class("TestTopic.Headers", module)
        assert result == Headers
    
    def test_resolve_deeply_nested_class(self):
        """Разрешение глубоко вложенного класса"""
        class Data(BaseModel):
            value: str
        
        class Message:
            pass
        
        Message.Data = Data
        
        class Topic:
            pass
        
        Topic.Message = Message
        
        class Module:
            pass
        
        Module.Topic = Topic
        
        module = Module()
        result = _resolve_nested_class("Topic.Message.Data", module)
        assert result == Data
    
    def test_resolve_nonexistent_class(self):
        """Разрешение несуществующего класса"""
        class TestModule:
            pass
        
        result = _resolve_nested_class("NonExistent", TestModule())
        assert result is None
    
    def test_resolve_nonexistent_nested_class(self):
        """Разрешение несуществующего вложенного класса"""
        class TestModule:
            pass
        
        result = _resolve_nested_class("Test.NonExistent", TestModule())
        assert result is None
    
    def test_resolve_not_basemodel(self):
        """Разрешение класса, который не BaseModel"""
        class NotBaseModel:
            pass
        
        class TestModule:
            pass
        
        TestModule.NotBaseModel = NotBaseModel
        
        result = _resolve_nested_class("NotBaseModel", TestModule())
        assert result is None
    
    def test_resolve_empty_path(self):
        """Разрешение пустого пути"""
        class TestModule:
            pass
        
        result = _resolve_nested_class("", TestModule())
        assert result is None
        
        result = _resolve_nested_class(None, TestModule())
        assert result is None


class TestExtractModelFromTypeArg:
    """Тесты для _extract_model_from_type_arg"""
    
    def test_extract_basemodel_type(self):
        """Извлечение BaseModel типа"""
        class TestModel(BaseModel):
            name: str
        
        result = _extract_model_from_type_arg(TestModel, None, None, 0)
        assert result == TestModel
    
    def test_extract_string_reference(self):
        """Извлечение строковой ссылки"""
        class TestModel(BaseModel):
            name: str
        
        class TestModule:
            pass
        
        TestModule.TestModel = TestModel
        
        module = TestModule()
        result = _extract_model_from_type_arg("TestModel", module, None, 0)
        assert result == TestModel
    
    def test_extract_nested_string_reference(self):
        """Извлечение вложенной строковой ссылки"""
        class Data(BaseModel):
            value: str
        
        class Topic:
            pass
        
        Topic.Data = Data
        
        class TestModule:
            pass
        
        TestModule.Topic = Topic
        
        module = TestModule()
        result = _extract_model_from_type_arg("Topic.Data", module, None, 0)
        assert result == Data
    
    def test_extract_none(self):
        """Извлечение None"""
        result = _extract_model_from_type_arg(None, None, None, 0)
        assert result is None
    
    def test_extract_not_basemodel(self):
        """Извлечение не-BaseModel типа"""
        class NotBaseModel:
            pass
        
        result = _extract_model_from_type_arg(NotBaseModel, None, None, 0)
        assert result is None


class TestKafkaHandler:
    """Тесты для kafka_handler декоратора"""
    
    def test_handler_registration(self):
        """Регистрация handler"""
        handlers_registry.clear()
        
        class DataModel(BaseModel):
            name: str
        
        class HeadersModel(BaseModel):
            key: str
        
        @kafka_handler("test_topic", DataModel, HeadersModel, None)
        async def test_handler(message: KafkaMessage[DataModel, HeadersModel]):
            pass
        
        assert "test_topic" in handlers_registry
        assert len(handlers_registry["test_topic"]) > 0
    
    def test_handler_with_headers_filter(self):
        """Регистрация handler с фильтром headers"""
        handlers_registry.clear()
        
        class DataModel(BaseModel):
            name: str
        
        class HeadersModel(BaseModel):
            key: str
        
        headers_filter = {"type": "test"}
        
        @kafka_handler("test_topic", DataModel, HeadersModel, headers_filter)
        async def test_handler(message: KafkaMessage[DataModel, HeadersModel]):
            pass
        
        assert "test_topic" in handlers_registry
    
    def test_handler_multiple_handlers_same_topic(self):
        """Несколько handlers для одного топика"""
        handlers_registry.clear()
        
        class DataModel1(BaseModel):
            name: str
        
        class HeadersModel1(BaseModel):
            key1: str
        
        class DataModel2(BaseModel):
            value: int
        
        class HeadersModel2(BaseModel):
            key2: str
        
        @kafka_handler("test_topic", DataModel1, HeadersModel1, None)
        async def handler1(message: KafkaMessage[DataModel1, HeadersModel1]):
            pass
        
        @kafka_handler("test_topic", DataModel2, HeadersModel2, None)
        async def handler2(message: KafkaMessage[DataModel2, HeadersModel2]):
            pass
        
        assert "test_topic" in handlers_registry
        assert len(handlers_registry["test_topic"]) == 2

