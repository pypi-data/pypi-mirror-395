# fastkafka2\infrastructure\services\retry.py
import asyncio
import logging
from functools import wraps
from confluent_kafka import KafkaError, KafkaException
from typing import Callable, TypeVar, Awaitable, Any

__all__ = ["retry_on_connection"]

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def retry_on_connection(
    delay: int = 5,
    max_attempts: int | None = None,
    exponential_backoff: bool = True,
    max_delay: int | None = None,
) -> Callable[[F], F]:
    """
    Decorator that retries a function on Kafka connection errors.
    
    Args:
        delay: Initial delay between retries in seconds (default: 5, must be > 0)
        max_attempts: Maximum number of retry attempts. None for unlimited (default: None)
        exponential_backoff: Whether to use exponential backoff (default: True)
        max_delay: Maximum delay in seconds when using exponential backoff (default: None)
    
    Returns:
        Decorated function that retries on connection errors
    
    Raises:
        ValueError: If delay <= 0 or max_attempts <= 0
    """
    # Validate parameters
    if delay <= 0:
        raise ValueError("delay must be greater than 0")
    if max_attempts is not None and max_attempts <= 0:
        raise ValueError("max_attempts must be greater than 0 or None")
    if max_delay is not None and max_delay <= 0:
        raise ValueError("max_delay must be greater than 0 or None")
    
    def decorator(fn: F) -> F:
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            
            while True:
                attempt += 1
                try:
                    return await fn(*args, **kwargs)
                except (KafkaException, KafkaError) as e:
                    error_code = None
                    if isinstance(e, KafkaException):
                        if e.args and hasattr(e.args[0], 'code'):
                            error_code = e.args[0].code()
                    elif isinstance(e, KafkaError):
                        error_code = e.code()
                    
                    should_retry = False
                    if error_code is not None:
                        # Use public error codes for connection-related errors
                        should_retry = error_code in (
                            KafkaError.NETWORK_EXCEPTION,
                            KafkaError.TIMED_OUT,
                        )
                        # Check for transport/broker errors by code value
                        # Error codes < 0 typically indicate connection/transport issues
                        if error_code < 0:
                            # Common transport/broker down error codes
                            # -195: _TRANSPORT, -194: _ALL_BROKERS_DOWN (not public, but common)
                            should_retry = True
                    else:
                        # Fallback: check error message for connection-related keywords
                        error_str = str(e).lower()
                        should_retry = any(
                            keyword in error_str
                            for keyword in ['transport', 'network', 'timeout', 'connection', 'broker', 'unreachable']
                        )
                    
                    if should_retry:
                        if max_attempts is not None and attempt >= max_attempts:
                            logger.error(
                                "Max retry attempts (%d) reached for %s. Last error: %s",
                                max_attempts, fn.__name__, e
                            )
                            raise
                        
                        logger.warning(
                            "Retrying %s (attempt %d%s) due to connection error (code=%s): %s",
                            fn.__name__,
                            attempt,
                            f"/{max_attempts}" if max_attempts else "",
                            error_code,
                            e
                        )
                        
                        await asyncio.sleep(current_delay)
                        
                        # Exponential backoff
                        if exponential_backoff:
                            current_delay = min(
                                current_delay * 2,
                                max_delay if max_delay is not None else float('inf')
                            )
                    else:
                        # Re-raise non-connection errors
                        raise

        return wrapper

    return decorator
