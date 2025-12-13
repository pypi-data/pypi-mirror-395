# fastkafka2\core\registry.py
import logging
from inspect import signature, iscoroutinefunction
from typing import Any, Callable, get_origin, get_args, get_type_hints
from pydantic import BaseModel
from ..api.message import KafkaMessage, LazyDeserializedBody
from ..infrastructure.di.di_container import resolve

__all__ = ["kafka_handler"]

logger = logging.getLogger(__name__)
handlers_registry: dict[str, list["CompiledHandler"]] = {}


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
            try:
                type_hints = get_type_hints(func, include_extras=True)
            except Exception:
                # Fallback если get_type_hints не работает
                type_hints = {}
            
            for param_name, param in sig.parameters.items():
                # Используем type_hints если доступны, иначе param.annotation
                ann = type_hints.get(param_name, param.annotation)
                if ann is param.empty:
                    continue
                
                origin = get_origin(ann)
                if origin is KafkaMessage:
                    args = get_args(ann)
                    if dm is None and len(args) >= 1:
                        try:
                            arg = args[0]
                            # get_type_hints уже разрешил forward references
                            if isinstance(arg, type) and issubclass(arg, BaseModel):
                                dm = arg
                        except Exception as e:
                            logger.debug(f"Failed to extract data_model from {args[0]}: {e}")
                    if hm is None and len(args) >= 2:
                        try:
                            arg = args[1]
                            if isinstance(arg, type) and issubclass(arg, BaseModel):
                                hm = arg
                        except Exception as e:
                            logger.debug(f"Failed to extract headers_model from {args[1]}: {e}")
            
            # Если не удалось извлечь из KafkaMessage, проверяем что обработчик имеет KafkaMessage параметр
            if dm is None or hm is None:
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
                        f"KafkaMessage[Data, Headers] where Data and Headers are Pydantic BaseModel classes. "
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
