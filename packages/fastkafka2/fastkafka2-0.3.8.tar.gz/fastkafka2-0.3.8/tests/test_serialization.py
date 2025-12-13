"""
Тесты для shared/serialization.py
Покрывает to_primitive и вспомогательные функции
"""
import pytest
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel

from fastkafka2.shared.serialization import to_primitive, _to_dict_fast, _is_pydantic_model


class TestIsPydanticModel:
    """Тесты для _is_pydantic_model"""
    
    def test_is_pydantic_model_true(self):
        """Проверка Pydantic модели"""
        class TestModel(BaseModel):
            name: str
        
        model = TestModel(name="test")
        assert _is_pydantic_model(model) is True
    
    def test_is_pydantic_model_false(self):
        """Проверка не-Pydantic объекта"""
        assert _is_pydantic_model({"key": "value"}) is False
        assert _is_pydantic_model("string") is False
        assert _is_pydantic_model(123) is False


class TestToDictFast:
    """Тесты для _to_dict_fast"""
    
    def test_to_dict_fast_pydantic_v2(self):
        """Конвертация Pydantic v2 модели"""
        class TestModel(BaseModel):
            name: str
            age: int
        
        model = TestModel(name="John", age=30)
        result = _to_dict_fast(model)
        
        assert result == {"name": "John", "age": 30}
    
    def test_to_dict_fast_not_pydantic(self):
        """Конвертация не-Pydantic объекта должна вызывать ошибку"""
        with pytest.raises(TypeError, match="Expected Pydantic BaseModel"):
            _to_dict_fast({"key": "value"})


class TestToPrimitive:
    """Тесты для to_primitive"""
    
    def test_primitive_types(self):
        """Примитивные типы возвращаются как есть"""
        assert to_primitive(None) is None
        assert to_primitive(123) == 123
        assert to_primitive("string") == "string"
        assert to_primitive(True) is True
        assert to_primitive(False) is False
        assert to_primitive(3.14) == 3.14
    
    def test_enum(self):
        """Конвертация Enum"""
        class TestEnum(Enum):
            VALUE1 = "value1"
            VALUE2 = "value2"
        
        assert to_primitive(TestEnum.VALUE1) == "value1"
        assert to_primitive(TestEnum.VALUE2) == "value2"
    
    def test_pydantic_model(self):
        """Конвертация Pydantic модели"""
        class TestModel(BaseModel):
            name: str
            age: int
        
        model = TestModel(name="John", age=30)
        result = to_primitive(model)
        
        assert result == {"name": "John", "age": 30}
    
    def test_pydantic_model_nested(self):
        """Конвертация вложенной Pydantic модели"""
        class NestedModel(BaseModel):
            value: str
        
        class TestModel(BaseModel):
            name: str
            nested: NestedModel
        
        model = TestModel(name="John", nested=NestedModel(value="test"))
        result = to_primitive(model)
        
        assert result == {"name": "John", "nested": {"value": "test"}}
    
    def test_dataclass(self):
        """Конвертация dataclass"""
        @dataclass
        class TestDataClass:
            name: str
            age: int
        
        obj = TestDataClass(name="John", age=30)
        result = to_primitive(obj)
        
        assert result == {"name": "John", "age": 30}
    
    def test_dataclass_nested(self):
        """Конвертация вложенного dataclass"""
        @dataclass
        class NestedDataClass:
            value: str
        
        @dataclass
        class TestDataClass:
            name: str
            nested: NestedDataClass
        
        obj = TestDataClass(name="John", nested=NestedDataClass(value="test"))
        result = to_primitive(obj)
        
        assert result == {"name": "John", "nested": {"value": "test"}}
    
    def test_list(self):
        """Конвертация списка"""
        result = to_primitive([1, 2, 3])
        assert result == [1, 2, 3]
    
    def test_list_with_objects(self):
        """Конвертация списка с объектами"""
        class TestModel(BaseModel):
            name: str
        
        result = to_primitive([TestModel(name="John"), TestModel(name="Jane")])
        assert result == [{"name": "John"}, {"name": "Jane"}]
    
    def test_dict(self):
        """Конвертация словаря"""
        result = to_primitive({"key1": "value1", "key2": "value2"})
        assert result == {"key1": "value1", "key2": "value2"}
    
    def test_dict_with_objects(self):
        """Конвертация словаря с объектами"""
        class TestModel(BaseModel):
            name: str
        
        result = to_primitive({"user": TestModel(name="John")})
        assert result == {"user": {"name": "John"}}
    
    def test_mixed_types(self):
        """Конвертация смешанных типов"""
        class TestEnum(Enum):
            STATUS = "active"
        
        class TestModel(BaseModel):
            name: str
        
        @dataclass
        class TestDataClass:
            value: int
        
        result = to_primitive({
            "string": "test",
            "number": 123,
            "enum": TestEnum.STATUS,
            "model": TestModel(name="John"),
            "dataclass": TestDataClass(value=42),
            "list": [1, TestModel(name="Jane")],
        })
        
        assert result == {
            "string": "test",
            "number": 123,
            "enum": "active",
            "model": {"name": "John"},
            "dataclass": {"value": 42},
            "list": [1, {"name": "Jane"}],
        }
    
    def test_cyclic_reference(self):
        """Защита от циклических ссылок"""
        class TestModel(BaseModel):
            name: str
            ref: 'TestModel | None' = None
        
        model1 = TestModel(name="model1")
        model2 = TestModel(name="model2", ref=model1)
        model1.ref = model2  # Создаем цикл
        
        result = to_primitive(model1)
        
        # Должна быть защита от цикла
        assert "name" in result
        assert result["name"] == "model1"
        # Проверяем, что циклическая ссылка обработана
        assert "ref" in result

