# fastkafka2\core\registry.py
import logging
from inspect import signature, iscoroutinefunction
from typing import Any, Callable, get_origin, get_args, get_type_hints, ForwardRef, TypeVar
from pydantic import BaseModel
from ..api.message import KafkaMessage, LazyDeserializedBody
from ..infrastructure.di.di_container import resolve

__all__ = ["kafka_handler"]

logger = logging.getLogger(__name__)
handlers_registry: dict[str, list["CompiledHandler"]] = {}


def _resolve_nested_class(class_path: str, module: Any) -> type[BaseModel] | None:
    """
    Рекурсивно разрешает вложенный класс по пути атрибутов.
    Поддерживает любую глубину вложенности.
    
    Примеры:
        - "MachinesUpdatesTopic.Headers"
        - "MachinesUpdatesTopic.CellStatusMessage.Data"
        - "Topic.Level1.Level2.Level3.Model"
    """
    if not class_path or not module:
        return None
    
    try:
        # Разбиваем путь на части
        parts = class_path.split('.')
        if not parts:
            return None
        
        # Начинаем с модуля
        obj = module
        
        # Рекурсивно проходим по атрибутам
        for part in parts:
            if not hasattr(obj, part):
                logger.debug(f"Attribute '{part}' not found in {obj} (path: {class_path})")
                return None
            obj = getattr(obj, part)
        
        # Проверяем что это класс и BaseModel
        if isinstance(obj, type):
            try:
                if issubclass(obj, BaseModel):
                    logger.debug(f"Resolved nested class {class_path} to {obj.__name__}")
                    return obj
                else:
                    logger.debug(f"Resolved {class_path} to {obj}, but it's not a BaseModel subclass")
            except TypeError:
                logger.debug(f"{obj} is not a class")
        
        return None
    except Exception as e:
        logger.debug(f"Error resolving nested class {class_path}: {e}", exc_info=True)
        return None


def _extract_model_from_type_arg(
    arg: Any,
    module: Any,
    func_module: str | None,
    arg_index: int,
    func_globals: dict[str, Any] | None = None
) -> type[BaseModel] | None:
    """
    Извлекает модель BaseModel из аргумента типа KafkaMessage.
    Обрабатывает строки, ForwardRef объекты и уже разрешенные типы.
    """
    if arg is None:
        return None
    
    # Если это уже класс BaseModel - возвращаем его
    if isinstance(arg, type):
        try:
            if issubclass(arg, BaseModel):
                logger.debug(f"arg[{arg_index}] is already a BaseModel: {arg.__name__}")
                return arg
        except TypeError:
            pass
    
    # Если это строка (forward reference)
    if isinstance(arg, str):
        logger.debug(f"arg[{arg_index}] is a string forward reference: {arg}")
        if module:
            resolved = _resolve_nested_class(arg, module)
            if resolved:
                return resolved
        
        # Пытаемся через eval как fallback
        # Используем func_globals если доступен (содержит вложенные классы), иначе vars(module)
        eval_context = func_globals if func_globals else {}
        if not eval_context and module:
            # Используем vars(module) как контекст для eval
            try:
                eval_context = vars(module).copy()
            except (TypeError, AttributeError):
                # Если module не модуль, а словарь или другой объект
                if isinstance(module, dict):
                    eval_context = module.copy()
                elif hasattr(module, '__dict__'):
                    eval_context = vars(module).copy()
        
        if eval_context:
            try:
                resolved = eval(arg, eval_context)
                if isinstance(resolved, type) and issubclass(resolved, BaseModel):
                    logger.debug(f"Resolved {arg} via eval to {resolved.__name__}")
                    return resolved
            except (NameError, AttributeError, SyntaxError, TypeError) as e:
                logger.debug(f"eval failed for {arg}: {e}")
        
        return None
    
    # Если это ForwardRef объект
    if isinstance(arg, ForwardRef):
        logger.debug(f"arg[{arg_index}] is a ForwardRef: {arg.__forward_arg__}")
        forward_arg = arg.__forward_arg__
        if module:
            resolved = _resolve_nested_class(forward_arg, module)
            if resolved:
                return resolved
        
        # Пытаемся через eval
        # Используем func_globals если доступен (содержит вложенные классы), иначе vars(module)
        eval_context = func_globals if func_globals else {}
        if not eval_context and module:
            try:
                eval_context = vars(module).copy()
            except (TypeError, AttributeError):
                if isinstance(module, dict):
                    eval_context = module.copy()
                elif hasattr(module, '__dict__'):
                    eval_context = vars(module).copy()
        
        if eval_context:
            try:
                resolved = eval(forward_arg, eval_context)
                if isinstance(resolved, type) and issubclass(resolved, BaseModel):
                    logger.debug(f"Resolved ForwardRef {forward_arg} via eval to {resolved.__name__}")
                    return resolved
            except (NameError, AttributeError, SyntaxError, TypeError) as e:
                logger.debug(f"eval failed for ForwardRef {forward_arg}: {e}")
        
        return None
    
    # Если это что-то другое - пытаемся получить строковое представление
    try:
        arg_str = str(arg)
        logger.debug(f"arg[{arg_index}] string representation: {arg_str}")
        
        # Если это похоже на путь к классу (содержит точки)
        if '.' in arg_str and module:
            class_path = None
            
            # Пытаемся извлечь путь из строкового представления класса
            # Вариант 1: "<class 'module.path.Class.Nested.Deep'>"
            if "'" in arg_str:
                parts = arg_str.split("'")
                if len(parts) >= 2:
                    full_path = parts[-2]  # Берем последний путь в кавычках
                    # Убираем префикс модуля если есть
                    if func_module and full_path.startswith(func_module + '.'):
                        class_path = full_path[len(func_module) + 1:]
                    else:
                        # Пытаемся найти последнюю часть пути (начиная с имени класса топика)
                        # Например: "source.app.core.domains.enums.kafka.MachinesUpdatesTopic.CellStatusMessage.Data"
                        # Нужно найти "MachinesUpdatesTopic.CellStatusMessage.Data"
                        path_parts = full_path.split('.')
                        # Ищем начало с имени класса топика (обычно заканчивается на "Topic")
                        for i in range(len(path_parts) - 1, -1, -1):
                            if 'Topic' in path_parts[i] or 'Message' in path_parts[i]:
                                class_path = '.'.join(path_parts[i:])
                                break
                        if not class_path:
                            # Fallback: берем последние части пути
                            class_path = '.'.join(path_parts[-3:]) if len(path_parts) >= 3 else full_path
            
            # Вариант 2: просто путь без кавычек
            if not class_path:
                # Если это уже похоже на путь класса (начинается с заглавной буквы)
                if arg_str[0].isupper() or '.' in arg_str:
                    class_path = arg_str
            
            # Пытаемся разрешить найденный путь
            if class_path:
                logger.debug(f"Attempting to resolve class path: {class_path}")
                resolved = _resolve_nested_class(class_path, module)
                if resolved:
                    return resolved
                
                # Если не получилось, пытаемся через eval
                try:
                    resolved = eval(class_path, vars(module))
                    if isinstance(resolved, type) and issubclass(resolved, BaseModel):
                        logger.debug(f"Resolved {class_path} via eval to {resolved.__name__}")
                        return resolved
                except (NameError, AttributeError, SyntaxError, TypeError) as e:
                    logger.debug(f"eval failed for {class_path}: {e}")
    except Exception as e:
        logger.debug(f"Failed to extract string representation from arg[{arg_index}]: {e}", exc_info=True)
    
    logger.debug(f"Could not extract model from arg[{arg_index}]: {arg}, type: {type(arg)}")
    return None


class CompiledHandler:
    __slots__ = (
        "topic",
        "func",
        "sig",
        "data_model",
        "headers_model",
        "_headers_predicate",
        "dependencies",
    )

    def __init__(
        self,
        topic: str,
        func: Callable[..., Any],
        data_model: type[BaseModel] | None,
        headers_model: type[BaseModel] | None,
        headers_filter: dict[str, str] | Callable[[dict[str, str]], bool] | None = None,
    ):
        self.topic = topic
        self.func = func
        self.sig = signature(func)
        self.data_model = data_model
        self.headers_model = headers_model

        if headers_filter is None:
            self._headers_predicate = lambda _h: True
        elif callable(headers_filter):
            self._headers_predicate = headers_filter
        else:
            expected: dict[str, str] = headers_filter
            def _eq_predicate(headers: dict[str, str]) -> bool:
                for k, v in expected.items():
                    if headers.get(k) != v:
                        return False
                return True
            self._headers_predicate = _eq_predicate

        self.dependencies: dict[str, Any] = {}
        for name, param in self.sig.parameters.items():
            ann = param.annotation
            if ann is param.empty:
                continue
            
            # Skip KafkaMessage (both direct and Generic types like KafkaMessage[TData, THeaders])
            # KafkaMessage is provided by the handler framework in the handle() method
            origin = get_origin(ann)
            
            # Check if it's KafkaMessage by checking origin, annotation itself, or string representation
            # This handles both direct KafkaMessage and Generic types like KafkaMessage[TData, THeaders]
            is_kafka_message = False
            if origin is KafkaMessage:
                is_kafka_message = True
            elif ann is KafkaMessage:
                is_kafka_message = True
            elif hasattr(ann, '__origin__') and ann.__origin__ is KafkaMessage:
                is_kafka_message = True
            elif isinstance(ann, type) and issubclass(ann, KafkaMessage):
                is_kafka_message = True
            else:
                # Fallback: check string representation for Generic types
                ann_str = str(ann)
                if 'KafkaMessage' in ann_str and ('[' in ann_str or origin is not None):
                    is_kafka_message = True
            
            if is_kafka_message:
                continue
            
            # Skip all Generic types (they can't be resolved by DI)
            # Examples: List[str], Dict[str, int], Optional[str], etc.
            # KafkaMessage is already handled above
            if origin is not None:
                continue
            
            try:
                self.dependencies[name] = resolve(ann)
            except (TypeError, RuntimeError, ValueError) as e:
                # Don't log warning for Generic types or KafkaMessage - they're expected to be skipped
                # Only log for actual resolution failures of concrete types
                logger.warning(
                    "Failed to resolve dependency '%s' of type %s for handler %s: %s",
                    name, ann, func.__name__, e
                )
                # Skip this dependency - handler will need to provide it manually
                continue

    def matches_headers(self, headers: dict[str, str]) -> bool:
        try:
            return bool(self._headers_predicate(headers))
        except Exception:
            logger.exception("Headers predicate raised for topic %s", self.topic)
            return False

    async def handle(
        self, raw_data: Any, raw_headers: dict[str, str] | None, key: str | None
    ):
        """
        Обработка сообщения. Если raw_data является LazyDeserializedBody,
        десериализация происходит только здесь (при первом обращении к get()).
        """
        headers_src: dict[str, str] = raw_headers or {}

        # Если raw_data - это LazyDeserializedBody, десериализуем его сейчас
        # (это происходит только когда обработчик принял сообщение по заголовкам)
        if isinstance(raw_data, LazyDeserializedBody):
            try:
                raw_data = raw_data.get()  # Десериализуем тело сообщения
            except Exception as e:
                logger.error(
                    "Failed to deserialize message body for topic %s: %s",
                    self.topic, e
                )
                raise

        # Валидация данных через Pydantic модель
        try:
            if self.data_model:
                if isinstance(raw_data, dict):
                    try:
                        msg_data = self.data_model(**raw_data)
                    except Exception as e:
                        logger.error(
                            "Failed to validate data model for topic %s: %s",
                            self.topic, e
                        )
                        raise
                elif isinstance(raw_data, BaseModel):
                    # Если уже Pydantic модель нужного типа, используем как есть
                    if isinstance(raw_data, self.data_model):
                        msg_data = raw_data
                    else:
                        # Иначе валидируем через нашу модель
                        # Поддержка Pydantic v1 и v2
                        try:
                            dump_data = raw_data.model_dump() if hasattr(raw_data, "model_dump") else raw_data.dict()
                        except Exception as e:
                            logger.error(
                                "Failed to dump model for topic %s: %s",
                                self.topic, e
                            )
                            raise
                        try:
                            msg_data = self.data_model(**dump_data)
                        except Exception as e:
                            logger.error(
                                "Failed to validate converted data model for topic %s: %s",
                                self.topic, e
                            )
                            raise
                else:
                    # Примитивные типы - пытаемся создать модель
                    try:
                        msg_data = self.data_model(**{"value": raw_data})
                    except Exception:
                        # Если не удалось создать модель с оберткой, используем как есть
                        logger.debug(
                            "Could not wrap primitive %s in model for topic %s, using as-is",
                            type(raw_data).__name__, self.topic
                        )
                        msg_data = raw_data
            else:
                msg_data = raw_data
        except Exception as e:
            logger.exception(
                "Error processing data for topic %s: %s",
                self.topic, e
            )
            raise
            
        # Валидация headers через Pydantic модель
        try:
            if self.headers_model:
                try:
                    msg_headers = self.headers_model(**headers_src)
                except Exception as e:
                    logger.error(
                        "Failed to validate headers model for topic %s: %s",
                        self.topic, e
                    )
                    raise
            else:
                msg_headers = headers_src
        except Exception as e:
            logger.exception(
                "Error processing headers for topic %s: %s",
                self.topic, e
            )
            raise

        try:
            message = KafkaMessage(
                topic=self.topic, data=msg_data, headers=msg_headers, key=key
            )
        except Exception as e:
            logger.exception(
                "Failed to create KafkaMessage for topic %s: %s",
                self.topic, e
            )
            raise

        kwargs: dict[str, Any] = {}
        try:
            for name, param in self.sig.parameters.items():
                ann = param.annotation
                origin = get_origin(ann)
                
                # Check if parameter is KafkaMessage (direct or Generic type)
                is_kafka_message = (
                    origin is KafkaMessage or
                    ann is KafkaMessage or
                    (hasattr(ann, '__origin__') and ann.__origin__ is KafkaMessage) or
                    (isinstance(ann, type) and issubclass(ann, KafkaMessage))
                )
                
                if is_kafka_message:
                    kwargs[name] = message
                else:
                    kwargs[name] = self.dependencies.get(name)
        except Exception as e:
            logger.exception(
                "Error preparing kwargs for handler %s on topic %s: %s",
                self.func.__name__, self.topic, e
            )
            raise

        try:
            return await self.func(**kwargs)
        except Exception as e:
            logger.exception(
                "Error executing handler %s for topic %s: %s",
                self.func.__name__, self.topic, e
            )
            raise


def kafka_handler(
    topic: str,
    data_model: type[BaseModel] | None = None,
    headers_model: type[BaseModel] | None = None,
    headers_filter: dict[str, str] | Callable[[dict[str, str]], bool] | None = None,
):
    """
    Декоратор для регистрации обработчика Kafka сообщений.
    
    Args:
        topic: название топика Kafka
        data_model: Pydantic модель для валидации данных сообщения (deprecated, извлекается автоматически)
        headers_model: Pydantic модель для валидации заголовков (deprecated, извлекается автоматически)
        headers_filter: фильтр по заголовкам (dict или callable)
    
    Returns:
        Декоратор функции-обработчика
        
    Note:
        Обработчик должен принимать параметр типа KafkaMessage[Data, Headers].
        Модели Data и Headers извлекаются автоматически из аннотации типа.
    """
    if not topic or not isinstance(topic, str):
        raise ValueError("Topic must be a non-empty string")
    
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if not iscoroutinefunction(func):
            raise TypeError(f"Handler {func.__name__} must be async")
        dm = data_model
        hm = headers_model
        if dm is None or hm is None:
            sig = signature(func)
            # Используем get_type_hints для разрешения forward references и вложенных классов
            # Важно: используем globalns и localns для правильного разрешения вложенных классов
            func_module = func.__module__
            func_globals = func.__globals__ if hasattr(func, '__globals__') else {}
            
            # Собираем все доступные глобальные переменные из замыканий и модуля
            import sys
            
            # Получаем модуль функции
            module = sys.modules.get(func_module) if func_module else None
            
            # Если функция определена внутри другой функции (замыкание),
            # пытаемся найти классы в замыканиях родительских функций
            if func.__closure__:
                for cell in func.__closure__:
                    try:
                        cell_contents = cell.cell_contents
                        # Если это словарь (глобальные переменные родительской функции)
                        if isinstance(cell_contents, dict):
                            func_globals.update(cell_contents)
                        # Если это модуль
                        elif hasattr(cell_contents, '__module__'):
                            if cell_contents.__module__ == func_module:
                                # Это может быть класс из модуля
                                if isinstance(cell_contents, type):
                                    func_globals[cell_contents.__name__] = cell_contents
                    except (ValueError, AttributeError):
                        # Ячейка может быть пустой или недоступной
                        pass
            
            # Добавляем переменные из модуля функции
            if module:
                func_globals.update(vars(module))
            
            # Важно: добавляем все вложенные классы в func_globals для eval
            # Это нужно для разрешения вложенных классов типа MachinesUpdatesTopic.CellStatusMessage.Data
            # Используем рекурсивную функцию для поддержки неограниченной глубины вложенности
            def add_nested_classes_to_globals(obj: Any, prefix: str, max_depth: int = 10, current_depth: int = 0):
                """Рекурсивно добавляет вложенные классы в func_globals"""
                if current_depth >= max_depth:
                    return
                
                if not isinstance(obj, type):
                    return
                
                # Добавляем текущий класс если есть префикс (вложенный класс)
                if prefix:
                    func_globals[prefix] = obj
                
                # Рекурсивно обрабатываем все атрибуты класса
                for attr_name in dir(obj):
                    if attr_name.startswith('_'):
                        continue
                    try:
                        attr = getattr(obj, attr_name)
                        if isinstance(attr, type):
                            nested_prefix = f"{prefix}.{attr_name}" if prefix else attr_name
                            add_nested_classes_to_globals(attr, nested_prefix, max_depth, current_depth + 1)
                    except (AttributeError, TypeError):
                        pass
            
            if module:
                # Создаем копию items() чтобы избежать RuntimeError при изменении словаря во время итерации
                for name, obj in list(vars(module).items()):
                    if isinstance(obj, type):
                        # Добавляем сам класс
                        func_globals[name] = obj
                        # Рекурсивно добавляем все вложенные классы
                        add_nested_classes_to_globals(obj, name)
            
            # Используем localns для разрешения вложенных классов
            # localns должен содержать все классы из модуля, включая вложенные
            localns = func_globals.copy() if func_globals else None
            
            # Логируем доступные классы для отладки
            if logger.isEnabledFor(logging.DEBUG):
                available_classes = [k for k, v in func_globals.items() if isinstance(v, type) and ('Topic' in k or '.' in k)]
                logger.debug(f"Available classes in func_globals for {func.__name__}: {available_classes[:15]}")
            
            try:
                type_hints = get_type_hints(func, include_extras=True, globalns=func_globals, localns=localns)
                # Логируем что получили от get_type_hints
                if logger.isEnabledFor(logging.DEBUG):
                    for param_name, hint in type_hints.items():
                        logger.debug(f"get_type_hints for {func.__name__}.{param_name}: {hint}, type={type(hint)}")
            except Exception as e:
                logger.debug(f"get_type_hints failed, using fallback: {e}")
                # Fallback если get_type_hints не работает - используем прямые аннотации
                type_hints = {}
                for param_name, param in sig.parameters.items():
                    if param.annotation is not param.empty:
                        type_hints[param_name] = param.annotation
            
            # Если модуль не найден, пытаемся найти его через inspect
            if not module:
                try:
                    import inspect
                    module = inspect.getmodule(func)
                    if module:
                        func_globals.update(vars(module))
                except Exception:
                    pass
            
            # Если все еще нет модуля, пытаемся найти классы по именам из аннотаций
            # Это помогает когда функция определена внутри другой функции
            if not module and func_globals:
                # Ищем первый класс из аннотаций в sys.modules
                for param_name, param in sig.parameters.items():
                    ann = type_hints.get(param_name, param.annotation)
                    if ann is param.empty:
                        continue
                    origin = get_origin(ann)
                    if origin is KafkaMessage:
                        args = get_args(ann)
                        for arg in args:
                            if isinstance(arg, str):
                                # Извлекаем имя первого класса из пути
                                first_class = arg.split('.')[0]
                                # Ищем этот класс в sys.modules
                                for mod_name, mod in sys.modules.items():
                                    if mod and hasattr(mod, first_class):
                                        module = mod
                                        func_globals.update(vars(mod))
                                        logger.debug(f"Found module {mod_name} containing class {first_class}")
                                        break
                                if module:
                                    break
                        if module:
                            break
            
            for param_name, param in sig.parameters.items():
                # Используем type_hints если доступны, иначе param.annotation
                ann = type_hints.get(param_name, param.annotation)
                if ann is param.empty:
                    continue
                
                origin = get_origin(ann)
                # Проверяем если это KafkaMessage (либо через get_origin, либо через isinstance для разрешенных типов)
                is_kafka_message_type = False
                if origin is KafkaMessage:
                    is_kafka_message_type = True
                elif isinstance(ann, type):
                    try:
                        is_kafka_message_type = issubclass(ann, KafkaMessage)
                    except TypeError:
                        pass
                
                logger.debug(f"Checking param {param_name} for {func.__name__}: ann={ann}, origin={origin}, is_kafka_message_type={is_kafka_message_type}, ann_type={type(ann)}")
                
                if is_kafka_message_type:
                    args = get_args(ann)
                    logger.debug(f"Initial args from get_args: {args}, types: {[type(a).__name__ for a in args]}")
                    
                    # Если get_args вернул пустой кортеж, но ann это класс KafkaMessage, пытаемся получить args из __args__
                    if not args:
                        if hasattr(ann, '__args__') and ann.__args__:
                            args = ann.__args__
                        elif hasattr(ann, '__orig_bases__') and ann.__orig_bases__:
                            # Для разрешенных Pydantic generic классов, args могут быть в __orig_bases__
                            for base in ann.__orig_bases__:
                                base_args = get_args(base)
                                if base_args:
                                    args = base_args
                                    break
                    
                    # Если args содержат TypeVars вместо реальных типов, используем оригинальную аннотацию или строковое представление
                    if args and all(isinstance(arg, TypeVar) for arg in args):
                        logger.debug(f"args are TypeVars, trying original annotation or string extraction")
                        # Пытаемся использовать оригинальную аннотацию
                        orig_ann = param.annotation
                        if orig_ann is not param.empty:
                            orig_origin = get_origin(orig_ann)
                            if orig_origin is KafkaMessage:
                                args = get_args(orig_ann)
                                logger.debug(f"Got args from original annotation: {args}")
                        
                        # Если все еще TypeVars или оригинальная аннотация не помогла, извлекаем из строкового представления
                        if not args or all(isinstance(arg, TypeVar) for arg in args):
                            import re
                            ann_str = str(ann)
                            match = re.search(r'KafkaMessage\[([^\]]+)\]', ann_str)
                            if match:
                                args_str = match.group(1)
                                args = [arg.strip() for arg in args_str.split(',')]
                                logger.debug(f"Extracted args from string representation: {args}")
                    logger.debug(
                        f"Extracting models from KafkaMessage for handler {func.__name__}: "
                        f"args={args}, arg_types={[type(a).__name__ if not isinstance(a, (str, ForwardRef)) else f'{type(a).__name__}({a})' for a in args]}, "
                        f"args_len={len(args)}, annotation={ann}, origin={origin}, module={module}"
                    )
                    logger.debug(f"args[0]={args[0] if len(args) > 0 else None}, args[1]={args[1] if len(args) > 1 else None}")
                    
                    # Извлекаем data_model (первый аргумент)
                    if dm is None and len(args) >= 1:
                        logger.debug(f"Trying to extract data_model from arg[0]={args[0]}, type={type(args[0])}")
                        # Сначала пытаемся через модуль
                        resolved_dm = _extract_model_from_type_arg(args[0], module, func_module, 0, func_globals)
                        if resolved_dm:
                            dm = resolved_dm
                            logger.debug(f"Extracted data_model: {dm.__name__}")
                        else:
                            logger.debug(f"Failed to extract via module, trying func_globals. args[0]={args[0]}, func_globals has {len(func_globals)} keys")
                            # Если не удалось через модуль, пытаемся через func_globals
                            if args[0] and isinstance(args[0], str) and func_globals:
                                # Проверяем что первый класс есть в func_globals
                                first_class = args[0].split('.')[0]
                                logger.debug(f"First class: {first_class}, in func_globals: {first_class in func_globals}")
                                
                                # Прямой eval с func_globals (самый надежный способ для вложенных классов)
                                try:
                                    resolved_dm = eval(args[0], func_globals)
                                    if isinstance(resolved_dm, type) and issubclass(resolved_dm, BaseModel):
                                        dm = resolved_dm
                                        logger.debug(f"Extracted data_model via direct eval(func_globals): {dm.__name__}")
                                except (NameError, AttributeError, SyntaxError, TypeError) as e:
                                    logger.debug(f"Direct eval(func_globals) failed for {args[0]}: {e}")
                                    # Fallback: рекурсивный getattr через func_globals
                                    try:
                                        parts = args[0].split('.')
                                        obj = func_globals.get(parts[0])
                                        if obj:
                                            for part in parts[1:]:
                                                obj = getattr(obj, part, None)
                                                if obj is None:
                                                    break
                                            if obj and isinstance(obj, type) and issubclass(obj, BaseModel):
                                                dm = obj
                                                logger.debug(f"Extracted data_model via recursive getattr: {dm.__name__}")
                                    except (AttributeError, TypeError) as e2:
                                        logger.debug(f"Recursive getattr failed for {args[0]}: {e2}")
                    
                    # Извлекаем headers_model (второй аргумент)
                    if hm is None and len(args) >= 2:
                        logger.debug(f"Trying to extract headers_model from arg[1]={args[1]}, type={type(args[1])}")
                        # Проверяем, не является ли это None/NoneType (headers опциональны)
                        if args[1] is None or (isinstance(args[1], str) and args[1] in ("None", "NoneType", "type(None)")):
                            logger.debug("headers_model is None (optional), skipping extraction")
                            # hm остается None, что допустимо для опциональных headers
                        else:
                            # Сначала пытаемся через модуль
                            resolved_hm = _extract_model_from_type_arg(args[1], module, func_module, 1, func_globals)
                            if resolved_hm:
                                hm = resolved_hm
                                logger.debug(f"Extracted headers_model: {hm.__name__}")
                            else:
                                logger.debug(f"Failed to extract via module, trying func_globals. args[1]={args[1]}, func_globals has {len(func_globals)} keys")
                                # Если не удалось через модуль, пытаемся через func_globals
                                if args[1] and isinstance(args[1], str) and func_globals:
                                    # Проверяем что первый класс есть в func_globals
                                    first_class = args[1].split('.')[0]
                                    logger.debug(f"First class: {first_class}, in func_globals: {first_class in func_globals}")
                                    
                                    # Прямой eval с func_globals (самый надежный способ для вложенных классов)
                                    try:
                                        resolved_hm = eval(args[1], func_globals)
                                        if isinstance(resolved_hm, type) and issubclass(resolved_hm, BaseModel):
                                            hm = resolved_hm
                                            logger.debug(f"Extracted headers_model via direct eval(func_globals): {hm.__name__}")
                                    except (NameError, AttributeError, SyntaxError, TypeError) as e:
                                        logger.debug(f"Direct eval(func_globals) failed for {args[1]}: {e}")
                                        # Fallback: рекурсивный getattr через func_globals
                                        try:
                                            parts = args[1].split('.')
                                            obj = func_globals.get(parts[0])
                                            if obj:
                                                for part in parts[1:]:
                                                    obj = getattr(obj, part, None)
                                                    if obj is None:
                                                        break
                                                if obj and isinstance(obj, type) and issubclass(obj, BaseModel):
                                                    hm = obj
                                                    logger.debug(f"Extracted headers_model via recursive getattr: {hm.__name__}")
                                        except (AttributeError, TypeError) as e2:
                                            logger.debug(f"Recursive getattr failed for {args[1]}: {e2}")
            
            # Если не удалось извлечь из KafkaMessage, проверяем что обработчик имеет KafkaMessage параметр
            # headers_model может быть None (опциональные headers), но data_model обязателен
            if dm is None:
                has_kafka_message = False
                for param_name, param in sig.parameters.items():
                    ann = type_hints.get(param_name, param.annotation)
                    if ann is param.empty:
                        continue
                    origin = get_origin(ann)
                    if origin is KafkaMessage:
                        has_kafka_message = True
                        break
                
                if not has_kafka_message:
                    raise ValueError(
                        f"Handler {func.__name__} must have a parameter annotated with "
                        f"KafkaMessage[Data, Headers] where Data is a Pydantic BaseModel class. "
                        f"Found data_model={dm}, headers_model={hm}"
                    )
                else:
                    raise ValueError(
                        f"Failed to extract models from KafkaMessage annotation in handler {func.__name__}. "
                        f"Make sure Data and Headers are Pydantic BaseModel classes. "
                        f"Found data_model={dm}, headers_model={hm}"
                    )

        handlers_registry.setdefault(topic, []).append(
            CompiledHandler(topic, func, dm, hm, headers_filter)
        )
        logger.debug(
            "Registered handler %s for topic %s (data_model=%s, headers_model=%s)",
            func.__name__,
            topic,
            getattr(dm, "__name__", None),
            getattr(hm, "__name__", None),
        )
        return func

    return decorator
