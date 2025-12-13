# fastkafka2\infrastructure\di\di_container.py
import logging
from inspect import isclass, signature, Parameter
from typing import Any, Callable, Type
from abc import ABC

logger = logging.getLogger(__name__)

_singletons: dict[Type[Any], Any] = {}
_factories: dict[Type[Any], Callable[..., Any]] = {}
_resolving_stack: set[Type[Any]] = set()
_sig_cache: dict[Type[Any], Any] = {}

# Примитивные типы, которые нельзя автоматически резолвить
_PRIMITIVE_TYPES = {int, str, bool, float, bytes, type(None)}


def register_singleton(cls: Type[Any], instance: Any) -> None:
    """Register a singleton instance for a class"""
    _singletons[cls] = instance


def register_factory(cls: Type[Any], factory: Callable[..., Any]) -> None:
    """Register a factory function for a class"""
    _factories[cls] = factory


def clear() -> None:
    """Clear all registered singletons, factories, and caches. Useful for testing."""
    _singletons.clear()
    _factories.clear()
    _resolving_stack.clear()
    _sig_cache.clear()


def resolve(cls: Type[Any]) -> Any:
    """
    Resolve a class to an instance using dependency injection.
    
    Raises:
        TypeError: If cls is not a class or is a primitive type
        RuntimeError: If circular dependency is detected
        ValueError: If class cannot be instantiated
    """
    if cls in _singletons:
        return _singletons[cls]
    if cls in _factories:
        return _factories[cls]()
    if not isclass(cls):
        raise TypeError(f"Cannot resolve non-class type: {cls}")
    if cls in _PRIMITIVE_TYPES:
        raise TypeError(
            f"Cannot resolve primitive type {cls.__name__}. "
            f"Register a singleton or factory for it."
        )
    if issubclass(cls, ABC):
        raise TypeError(
            f"Cannot resolve abstract class {cls.__name__}. "
            f"Register a concrete implementation."
        )
    if cls in _resolving_stack:
        raise RuntimeError(f"Circular dependency detected: {cls.__name__}")

    _resolving_stack.add(cls)
    try:
        sig = _sig_cache.get(cls) or signature(cls.__init__)
        _sig_cache[cls] = sig
        
        kwargs = {}
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            # Skip parameters without annotations or with default values
            if param.annotation is Parameter.empty:
                if param.default is Parameter.empty:
                    raise ValueError(
                        f"Cannot resolve {cls.__name__}: parameter '{name}' "
                        f"has no annotation and no default value"
                    )
                continue
            
            try:
                kwargs[name] = resolve(param.annotation)
            except (TypeError, RuntimeError, ValueError) as e:
                # If resolution fails and parameter has default, skip it
                if param.default is not Parameter.empty:
                    continue
                raise ValueError(
                    f"Cannot resolve {cls.__name__}: failed to resolve "
                    f"parameter '{name}' of type {param.annotation}: {e}"
                ) from e
        
        return cls(**kwargs)
    except Exception as e:
        if isinstance(e, (TypeError, RuntimeError, ValueError)):
            raise
        raise ValueError(
            f"Failed to instantiate {cls.__name__}: {e}"
        ) from e
    finally:
        _resolving_stack.remove(cls)
