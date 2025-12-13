"""
Тест для проверки поддержки глубокой вложенности классов (4+ уровней)
"""
import pytest
from pydantic import BaseModel
from fastkafka2 import KafkaHandler, KafkaMessage


class Level1Topic:
    topic = "level1_topic"
    
    class Level2Message:
        class Level3Payload:
            class Level4Data(BaseModel):
                field1: str
                
            class Level4Meta(BaseModel):
                field2: int
            
            class Level3Config(BaseModel):
                field3: bool
        
        class Level3Headers(BaseModel):
            message_type: str


# Тест с еще более глубокой вложенностью (5-6 уровней)
class VeryDeepTopic:
    topic = "very_deep_topic"
    
    class Level1:
        class Level2:
            class Level3:
                class Level4:
                    class Level5:
                        class Level6Data(BaseModel):
                            deep_field: str
                        
                        class Level6Meta(BaseModel):
                            deep_meta: int
                    
                    class Level5Headers(BaseModel):
                        deep_header: str


handler = KafkaHandler()
deep_handler = KafkaHandler()


@handler("level1_topic")
async def handle_deep_nested(
    message: KafkaMessage[
        Level1Topic.Level2Message.Level3Payload.Level4Data,
        Level1Topic.Level2Message.Level3Headers,
    ],
):
    """Handler с 4 уровнями вложенности"""
    assert message.data.field1 == "test"
    assert message.headers.message_type == "test_type"


@deep_handler("very_deep_topic")
async def handle_very_deep_nested(
    message: KafkaMessage[
        VeryDeepTopic.Level1.Level2.Level3.Level4.Level5.Level6Data,
        VeryDeepTopic.Level1.Level2.Level3.Level4.Level5Headers,
    ],
):
    """Handler с 6 уровнями вложенности"""
    assert message.data.deep_field == "test"
    assert message.headers.deep_header == "test_header"


def test_deep_nesting_handler():
    """Проверка handler с глубокой вложенностью (4 уровня)"""
    from fastkafka2.core.registry import handlers_registry
    
    handlers = handlers_registry.get("level1_topic", [])
    assert len(handlers) >= 1
    
    deep_handler = None
    for h in handlers:
        if h.func.__name__ == "handle_deep_nested":
            deep_handler = h
            break
    
    assert deep_handler is not None, "Handler not found"
    assert deep_handler.data_model == Level1Topic.Level2Message.Level3Payload.Level4Data
    assert deep_handler.headers_model == Level1Topic.Level2Message.Level3Headers


def test_deep_nesting_resolution():
    """Проверка разрешения глубоко вложенных классов"""
    from fastkafka2.core.registry import _resolve_nested_class
    import sys
    
    module = sys.modules[__name__]
    
    # Проверяем разрешение 4 уровней вложенности
    resolved = _resolve_nested_class(
        "Level1Topic.Level2Message.Level3Payload.Level4Data",
        module
    )
    assert resolved is not None
    assert resolved == Level1Topic.Level2Message.Level3Payload.Level4Data
    
    # Проверяем разрешение 4 уровней для headers
    resolved_headers = _resolve_nested_class(
        "Level1Topic.Level2Message.Level3Headers",
        module
    )
    assert resolved_headers is not None
    assert resolved_headers == Level1Topic.Level2Message.Level3Headers


def test_very_deep_nesting_handler():
    """Проверка handler с очень глубокой вложенностью (6 уровней)"""
    from fastkafka2.core.registry import handlers_registry
    
    handlers = handlers_registry.get("very_deep_topic", [])
    assert len(handlers) >= 1
    
    very_deep_handler = None
    for h in handlers:
        if h.func.__name__ == "handle_very_deep_nested":
            very_deep_handler = h
            break
    
    assert very_deep_handler is not None, "Handler not found"
    assert very_deep_handler.data_model == VeryDeepTopic.Level1.Level2.Level3.Level4.Level5.Level6Data
    assert very_deep_handler.headers_model == VeryDeepTopic.Level1.Level2.Level3.Level4.Level5Headers


def test_very_deep_nesting_resolution():
    """Проверка разрешения очень глубоко вложенных классов (6 уровней)"""
    from fastkafka2.core.registry import _resolve_nested_class
    import sys
    
    module = sys.modules[__name__]
    
    # Проверяем разрешение 6 уровней вложенности
    resolved = _resolve_nested_class(
        "VeryDeepTopic.Level1.Level2.Level3.Level4.Level5.Level6Data",
        module
    )
    assert resolved is not None
    assert resolved == VeryDeepTopic.Level1.Level2.Level3.Level4.Level5.Level6Data
    
    # Проверяем разрешение 5 уровней для headers
    resolved_headers = _resolve_nested_class(
        "VeryDeepTopic.Level1.Level2.Level3.Level4.Level5Headers",
        module
    )
    assert resolved_headers is not None
    assert resolved_headers == VeryDeepTopic.Level1.Level2.Level3.Level4.Level5Headers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

