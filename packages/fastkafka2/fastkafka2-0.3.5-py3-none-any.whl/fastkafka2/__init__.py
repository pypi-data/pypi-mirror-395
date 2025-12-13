from importlib.metadata import PackageNotFoundError, version
from typing import Any

from .api import KafkaApp, KafkaHandler, KafkaMessage, KafkaProducer

__all__ = ["KafkaApp", "KafkaHandler", "KafkaMessage", "KafkaProducer"]

try:
    __version__ = version("fastkafka2")
except PackageNotFoundError:
    __version__ = "0.0.0"


def __getattr__(name: str) -> Any:
    """
    Lazy import support for module attributes.
    
    This allows for lazy loading of modules if needed in the future,
    though currently all exports are eagerly imported.
    """
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    """
    Return list of attributes available in this module.
    
    Includes all public exports and private attributes (starting with _).
    """
    return list(__all__) + [n for n in globals() if n.startswith("_")]
