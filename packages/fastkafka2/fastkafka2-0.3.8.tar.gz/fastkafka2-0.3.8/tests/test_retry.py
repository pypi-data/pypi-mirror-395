"""
Тесты для infrastructure/services/retry.py
Покрывает retry_on_connection декоратор
Использует реальные объекты как на проде
"""
import pytest
import asyncio
from confluent_kafka import KafkaError, KafkaException

from fastkafka2.infrastructure.services.retry import retry_on_connection


class TestRetryOnConnection:
    """Тесты для retry_on_connection декоратора"""
    
    @pytest.mark.asyncio
    async def test_success_no_retry(self):
        """Успешное выполнение без retry"""
        @retry_on_connection()
        async def test_func():
            return "success"
        
        result = await test_func()
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_no_retry_on_non_connection_error(self):
        """Не должно быть retry для не-connection ошибок"""
        attempt_count = 0
        
        @retry_on_connection(delay=0.1, max_attempts=3)
        async def test_func():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Not a connection error")
        
        with pytest.raises(ValueError, match="Not a connection error"):
            await test_func()
        
        assert attempt_count == 1
    
    def test_invalid_delay(self):
        """Невалидный delay должен вызывать ошибку"""
        with pytest.raises(ValueError, match="delay must be greater than 0"):
            retry_on_connection(delay=0)
        
        with pytest.raises(ValueError, match="delay must be greater than 0"):
            retry_on_connection(delay=-1)
    
    def test_invalid_max_attempts(self):
        """Невалидный max_attempts должен вызывать ошибку"""
        with pytest.raises(ValueError, match="max_attempts must be greater than 0"):
            retry_on_connection(max_attempts=0)
        
        with pytest.raises(ValueError, match="max_attempts must be greater than 0"):
            retry_on_connection(max_attempts=-1)
    
    def test_invalid_max_delay(self):
        """Невалидный max_delay должен вызывать ошибку"""
        with pytest.raises(ValueError, match="max_delay must be greater than 0"):
            retry_on_connection(max_delay=0)
        
        with pytest.raises(ValueError, match="max_delay must be greater than 0"):
            retry_on_connection(max_delay=-1)
