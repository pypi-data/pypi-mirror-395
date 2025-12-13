"""
Бенчмарк для проверки извлечения моделей из вложенных классов.
Запускается перед публикацией в PyPI для проверки работоспособности.
"""
import sys
import time
from typing import get_type_hints, get_args, get_origin
from enum import StrEnum
from pydantic import BaseModel
from fastkafka2 import KafkaMessage
from fastkafka2.core.registry import _resolve_nested_class, _extract_model_from_type_arg


# Импортируем тестовые схемы
try:
    from tests.test_nested_models_extraction import (
        MachinesUpdatesTopic,
        MachinesHeartbeatsTopic,
        MachinesCommandsTopic,
        MachinesOrdersTopic,
    )
except ImportError:
    # Если запускаем напрямую из директории tests
    from test_nested_models_extraction import (
        MachinesUpdatesTopic,
        MachinesHeartbeatsTopic,
        MachinesCommandsTopic,
        MachinesOrdersTopic,
    )


def benchmark_nested_class_resolution():
    """Бенчмарк разрешения вложенных классов"""
    print("\n" + "="*60)
    print("БЕНЧМАРК: Разрешение вложенных классов")
    print("="*60)
    
    import sys
    # Получаем модуль с тестовыми схемами
    try:
        import tests.test_nested_models_extraction as test_module
    except ImportError:
        import test_nested_models_extraction as test_module
    module = test_module
    
    test_cases = [
        ("MachinesUpdatesTopic.Headers", MachinesUpdatesTopic.Headers),
        ("MachinesUpdatesTopic.CellStatusMessage.Data", MachinesUpdatesTopic.CellStatusMessage.Data),
        ("MachinesUpdatesTopic.OrderStatusMessage.Data", MachinesUpdatesTopic.OrderStatusMessage.Data),
        ("MachinesUpdatesTopic.CarriagePositionUpdateMessage.Data", MachinesUpdatesTopic.CarriagePositionUpdateMessage.Data),
        ("MachinesHeartbeatsTopic.Headers", MachinesHeartbeatsTopic.Headers),
        ("MachinesHeartbeatsTopic.HeartbeatMessage.Data", MachinesHeartbeatsTopic.HeartbeatMessage.Data),
    ]
    
    passed = 0
    failed = 0
    
    for class_path, expected_class in test_cases:
        start = time.perf_counter()
        resolved = _resolve_nested_class(class_path, module)
        elapsed = (time.perf_counter() - start) * 1000  # в миллисекундах
        
        if resolved == expected_class:
            print(f"✓ {class_path:60s} -> {resolved.__name__:30s} ({elapsed:.3f}ms)")
            passed += 1
        else:
            print(f"✗ {class_path:60s} -> FAILED")
            print(f"  Expected: {expected_class}")
            print(f"  Got:      {resolved}")
            failed += 1
    
    print(f"\nРезультат: {passed} passed, {failed} failed")
    return failed == 0


def benchmark_type_extraction():
    """Бенчмарк извлечения моделей из типов KafkaMessage"""
    print("\n" + "="*60)
    print("БЕНЧМАРК: Извлечение моделей из KafkaMessage типов")
    print("="*60)
    
    import sys
    # Получаем модуль с тестовыми схемами
    try:
        import tests.test_nested_models_extraction as test_module
    except ImportError:
        import test_nested_models_extraction as test_module
    module = test_module
    func_module = test_module.__name__
    
    # Создаем тестовые функции с аннотациями типов
    async def test_handler_1(
        message: KafkaMessage[
            MachinesUpdatesTopic.CellStatusMessage.Data,
            MachinesUpdatesTopic.Headers,
        ],
    ):
        pass
    
    async def test_handler_2(
        message: KafkaMessage[
            MachinesUpdatesTopic.CarriagePositionUpdateMessage.Data,
            MachinesUpdatesTopic.Headers,
        ],
    ):
        pass
    
    async def test_handler_3(
        message: KafkaMessage[
            MachinesHeartbeatsTopic.HeartbeatMessage.Data,
            MachinesHeartbeatsTopic.Headers,
        ],
    ):
        pass
    
    test_handlers = [
        (test_handler_1, MachinesUpdatesTopic.CellStatusMessage.Data, MachinesUpdatesTopic.Headers),
        (test_handler_2, MachinesUpdatesTopic.CarriagePositionUpdateMessage.Data, MachinesUpdatesTopic.Headers),
        (test_handler_3, MachinesHeartbeatsTopic.HeartbeatMessage.Data, MachinesHeartbeatsTopic.Headers),
    ]
    
    from inspect import signature
    from typing import get_type_hints
    
    passed = 0
    failed = 0
    
    for func, expected_data_model, expected_headers_model in test_handlers:
        sig = signature(func)
        type_hints = get_type_hints(func, include_extras=True)
        
        for param_name, param in sig.parameters.items():
            ann = type_hints.get(param_name, param.annotation)
            if ann is param.empty:
                continue
            
            origin = get_origin(ann)
            if origin is KafkaMessage:
                args = get_args(ann)
                
                # Извлекаем data_model
                data_model = _extract_model_from_type_arg(args[0], module, func_module, 0)
                headers_model = _extract_model_from_type_arg(args[1], module, func_module, 1)
                
                if data_model == expected_data_model and headers_model == expected_headers_model:
                    print(f"✓ {func.__name__:40s} -> Data: {data_model.__name__:30s} Headers: {headers_model.__name__}")
                    passed += 1
                else:
                    print(f"✗ {func.__name__:40s} -> FAILED")
                    print(f"  Expected Data:    {expected_data_model}")
                    print(f"  Got Data:        {data_model}")
                    print(f"  Expected Headers: {expected_headers_model}")
                    print(f"  Got Headers:      {headers_model}")
                    failed += 1
                break
    
    print(f"\nРезультат: {passed} passed, {failed} failed")
    return failed == 0


def benchmark_handler_registration():
    """Бенчмарк регистрации handlers через декоратор"""
    print("\n" + "="*60)
    print("БЕНЧМАРК: Регистрация handlers через @handler декоратор")
    print("="*60)
    
    from fastkafka2 import KafkaHandler
    from fastkafka2.core.registry import handlers_registry
    
    # Очищаем registry перед тестом
    handlers_registry.clear()
    
    handler = KafkaHandler()
    
    @handler("test_topic_1")
    async def handler_1(
        message: KafkaMessage[
            MachinesUpdatesTopic.CellStatusMessage.Data,
            MachinesUpdatesTopic.Headers,
        ],
    ):
        pass
    
    @handler("test_topic_2")
    async def handler_2(
        message: KafkaMessage[
            MachinesUpdatesTopic.CarriagePositionUpdateMessage.Data,
            MachinesUpdatesTopic.Headers,
        ],
    ):
        pass
    
    @handler("test_topic_3")
    async def handler_3(
        message: KafkaMessage[
            MachinesHeartbeatsTopic.HeartbeatMessage.Data,
            MachinesHeartbeatsTopic.Headers,
        ],
    ):
        pass
    
    expected_results = [
        ("test_topic_1", MachinesUpdatesTopic.CellStatusMessage.Data, MachinesUpdatesTopic.Headers),
        ("test_topic_2", MachinesUpdatesTopic.CarriagePositionUpdateMessage.Data, MachinesUpdatesTopic.Headers),
        ("test_topic_3", MachinesHeartbeatsTopic.HeartbeatMessage.Data, MachinesHeartbeatsTopic.Headers),
    ]
    
    passed = 0
    failed = 0
    
    for topic, expected_data_model, expected_headers_model in expected_results:
        handlers = handlers_registry.get(topic, [])
        if len(handlers) == 0:
            print(f"✗ {topic:40s} -> No handlers found")
            failed += 1
            continue
        
        h = handlers[0]
        if h.data_model == expected_data_model and h.headers_model == expected_headers_model:
            print(f"✓ {topic:40s} -> Data: {h.data_model.__name__:30s} Headers: {h.headers_model.__name__}")
            passed += 1
        else:
            print(f"✗ {topic:40s} -> FAILED")
            print(f"  Expected Data:    {expected_data_model}")
            print(f"  Got Data:         {h.data_model}")
            print(f"  Expected Headers: {expected_headers_model}")
            print(f"  Got Headers:      {h.headers_model}")
            failed += 1
    
    print(f"\nРезультат: {passed} passed, {failed} failed")
    return failed == 0


def run_all_benchmarks():
    """Запускает все бенчмарки"""
    print("\n" + "="*60)
    print("ЗАПУСК БЕНЧМАРКОВ ДЛЯ ПРОВЕРКИ ИЗВЛЕЧЕНИЯ МОДЕЛЕЙ")
    print("="*60)
    
    results = []
    
    # Бенчмарк 1: Разрешение вложенных классов
    results.append(("Разрешение вложенных классов", benchmark_nested_class_resolution()))
    
    # Бенчмарк 2: Извлечение моделей из типов
    results.append(("Извлечение моделей из KafkaMessage", benchmark_type_extraction()))
    
    # Бенчмарк 3: Регистрация handlers
    results.append(("Регистрация handlers", benchmark_handler_registration()))
    
    # Итоговый результат
    print("\n" + "="*60)
    print("ИТОГОВЫЙ РЕЗУЛЬТАТ")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name:50s} -> {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✓ ВСЕ БЕНЧМАРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print("  Библиотека готова к публикации в PyPI.")
        return 0
    else:
        print("\n✗ НЕКОТОРЫЕ БЕНЧМАРКИ ПРОВАЛИЛИСЬ!")
        print("  НЕ публикуйте библиотеку в PyPI до исправления ошибок.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_benchmarks())

