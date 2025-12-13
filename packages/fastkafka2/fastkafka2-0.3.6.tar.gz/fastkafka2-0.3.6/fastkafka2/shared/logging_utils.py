# fastkafka2\shared\logging_utils.py
import logging
from typing import Optional


def suppress_external_logs(
    level: int = logging.CRITICAL,
    logger_names: Optional[list[str]] = None,
) -> None:
    """
    Подавляет логи от внешних библиотек, устанавливая высокий уровень логирования
    и отключая распространение логов.
    
    Args:
        level: Уровень логирования для установки (по умолчанию CRITICAL)
        logger_names: Список имен логгеров для подавления.
                     Если None, используется список по умолчанию.
    
    Example:
        >>> suppress_external_logs()
        >>> suppress_external_logs(level=logging.ERROR)
        >>> suppress_external_logs(logger_names=["custom_logger"])
    """
    if logger_names is None:
        logger_names = [
            "confluent_kafka",
            "confluent_kafka.cimpl",
            "kafka",
            "asyncio",
        ]
    
    for name in logger_names:
        try:
            lg = logging.getLogger(name)
            lg.setLevel(level)
            lg.propagate = False
        except Exception:
            # Игнорируем ошибки при настройке логгеров
            # (например, если имя логгера некорректно)
            pass
