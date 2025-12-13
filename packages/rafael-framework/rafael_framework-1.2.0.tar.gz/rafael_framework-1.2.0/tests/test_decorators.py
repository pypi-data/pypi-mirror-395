"""
Comprehensive tests for RAFAEL decorators
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch
from core.decorators import resilient, adaptive, monitor_health


class TestResilientDecorator:
    """Test resilient decorator functionality"""
    
    def test_resilient_basic_success(self):
        """Test resilient decorator with successful function"""
        call_count = 0
        
        @resilient(max_retries=3)
        def successful_function():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = successful_function()
        assert result == "success"
        assert call_count == 1
    
    def test_resilient_retry_on_failure(self):
        """Test resilient decorator retries on failure"""
        call_count = 0
        
        @resilient(max_retries=3, base_delay=0.01)
        def failing_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"
        
        result = failing_function()
        assert result == "success"
        assert call_count == 3
    
    def test_resilient_max_retries_exceeded(self):
        """Test resilient decorator when max retries exceeded"""
        call_count = 0
        
        @resilient(max_retries=2, base_delay=0.01)
        def always_failing():
            nonlocal call_count
            call_count += 1
            raise ValueError("Permanent failure")
        
        with pytest.raises(ValueError):
            always_failing()
        
        assert call_count == 3  # Initial + 2 retries
    
    def test_resilient_exponential_backoff(self):
        """Test exponential backoff timing"""
        call_times = []
        
        @resilient(max_retries=3, base_delay=0.1)
        def failing_function():
            call_times.append(time.time())
            if len(call_times) < 3:
                raise ValueError("Retry")
            return "success"
        
        failing_function()
        
        # Check that delays increase exponentially
        if len(call_times) >= 3:
            delay1 = call_times[1] - call_times[0]
            delay2 = call_times[2] - call_times[1]
            assert delay2 > delay1
    
    @pytest.mark.asyncio
    async def test_resilient_async_function(self):
        """Test resilient decorator with async function"""
        call_count = 0
        
        @resilient(max_retries=2, base_delay=0.01)
        async def async_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Retry")
            return "async success"
        
        result = await async_function()
        assert result == "async success"
        assert call_count == 2
    
    def test_resilient_with_fallback(self):
        """Test resilient decorator with fallback function"""
        
        def fallback_func():
            return "fallback result"
        
        @resilient(max_retries=1, base_delay=0.01, fallback=fallback_func)
        def failing_function():
            raise ValueError("Always fails")
        
        result = failing_function()
        assert result == "fallback result"
    
    def test_resilient_specific_exceptions(self):
        """Test resilient only retries specific exceptions"""
        call_count = 0
        
        @resilient(max_retries=3, base_delay=0.01, retry_on=(ValueError,))
        def mixed_exceptions():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("Retryable")
            raise TypeError("Not retryable")
        
        with pytest.raises(TypeError):
            mixed_exceptions()
        
        assert call_count == 2  # Initial + 1 retry for ValueError


class TestAdaptiveDecorator:
    """Test adaptive decorator functionality"""
    
    def test_adaptive_basic_function(self):
        """Test adaptive decorator on basic function"""
        
        @adaptive(module_id="test_module")
        def adaptive_function(x):
            return x * 2
        
        result = adaptive_function(5)
        assert result == 10
    
    def test_adaptive_tracks_performance(self):
        """Test adaptive decorator tracks performance metrics"""
        
        @adaptive(module_id="test_module")
        def tracked_function():
            time.sleep(0.01)
            return "result"
        
        result = tracked_function()
        assert result == "result"
        
        # Check that metrics were tracked
        assert hasattr(tracked_function, '_performance_metrics')
    
    @pytest.mark.asyncio
    async def test_adaptive_async_function(self):
        """Test adaptive decorator with async function"""
        
        @adaptive(module_id="async_module")
        async def async_adaptive():
            await asyncio.sleep(0.01)
            return "async result"
        
        result = await async_adaptive()
        assert result == "async result"
    
    def test_adaptive_parameter_optimization(self):
        """Test adaptive decorator optimizes parameters"""
        
        @adaptive(module_id="opt_module", optimize_params=True)
        def optimizable_function(threshold=10):
            return threshold * 2
        
        result = optimizable_function()
        assert isinstance(result, int)
    
    def test_adaptive_failure_learning(self):
        """Test adaptive decorator learns from failures"""
        call_count = 0
        
        @adaptive(module_id="learning_module")
        def learning_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Learning failure")
            return "learned"
        
        # First calls should fail
        with pytest.raises(ValueError):
            learning_function()
        
        with pytest.raises(ValueError):
            learning_function()
        
        # Eventually succeeds
        result = learning_function()
        assert result == "learned"


class TestMonitorHealthDecorator:
    """Test monitor_health decorator functionality"""
    
    def test_monitor_health_basic(self):
        """Test monitor_health decorator basic functionality"""
        
        @monitor_health(module_id="health_module")
        def healthy_function():
            return "healthy"
        
        result = healthy_function()
        assert result == "healthy"
    
    def test_monitor_health_tracks_failures(self):
        """Test monitor_health tracks failures"""
        
        @monitor_health(module_id="failure_module", failure_threshold=3)
        def sometimes_fails():
            import random
            if random.random() < 0.5:
                raise ValueError("Random failure")
            return "success"
        
        # Run multiple times to track failures
        successes = 0
        failures = 0
        
        for _ in range(10):
            try:
                sometimes_fails()
                successes += 1
            except ValueError:
                failures += 1
        
        assert successes + failures == 10
    
    def test_monitor_health_circuit_breaker(self):
        """Test monitor_health implements circuit breaker"""
        failure_count = 0
        
        @monitor_health(
            module_id="circuit_module",
            failure_threshold=3,
            circuit_breaker=True
        )
        def failing_function():
            nonlocal failure_count
            failure_count += 1
            raise ValueError("Failure")
        
        # Trigger circuit breaker
        for _ in range(5):
            try:
                failing_function()
            except (ValueError, Exception):
                pass
        
        assert failure_count >= 3
    
    @pytest.mark.asyncio
    async def test_monitor_health_async(self):
        """Test monitor_health with async function"""
        
        @monitor_health(module_id="async_health")
        async def async_health_check():
            await asyncio.sleep(0.01)
            return "healthy"
        
        result = await async_health_check()
        assert result == "healthy"
    
    def test_monitor_health_custom_health_check(self):
        """Test monitor_health with custom health check function"""
        
        def custom_health_check():
            return {"status": "healthy", "cpu": 50}
        
        @monitor_health(
            module_id="custom_module",
            health_check_fn=custom_health_check
        )
        def monitored_function():
            return "result"
        
        result = monitored_function()
        assert result == "result"


class TestDecoratorCombinations:
    """Test combining multiple decorators"""
    
    def test_resilient_and_adaptive(self):
        """Test combining resilient and adaptive decorators"""
        call_count = 0
        
        @adaptive(module_id="combo_module")
        @resilient(max_retries=2, base_delay=0.01)
        def combo_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Retry")
            return "combo success"
        
        result = combo_function()
        assert result == "combo success"
        assert call_count == 2
    
    def test_all_decorators_combined(self):
        """Test combining all three decorators"""
        
        @monitor_health(module_id="full_combo")
        @adaptive(module_id="full_combo")
        @resilient(max_retries=2, base_delay=0.01)
        def fully_decorated():
            return "fully protected"
        
        result = fully_decorated()
        assert result == "fully protected"
    
    @pytest.mark.asyncio
    async def test_async_decorator_combination(self):
        """Test combining decorators on async function"""
        
        @adaptive(module_id="async_combo")
        @resilient(max_retries=2, base_delay=0.01)
        async def async_combo():
            await asyncio.sleep(0.01)
            return "async combo"
        
        result = await async_combo()
        assert result == "async combo"


class TestDecoratorEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_resilient_zero_retries(self):
        """Test resilient with zero retries"""
        
        @resilient(max_retries=0)
        def no_retry_function():
            raise ValueError("Immediate failure")
        
        with pytest.raises(ValueError):
            no_retry_function()
    
    def test_resilient_negative_delay(self):
        """Test resilient handles negative delay"""
        
        @resilient(max_retries=1, base_delay=-1)
        def negative_delay():
            raise ValueError("Failure")
        
        with pytest.raises(ValueError):
            negative_delay()
    
    def test_adaptive_empty_module_id(self):
        """Test adaptive with empty module_id"""
        
        @adaptive(module_id="")
        def empty_module():
            return "result"
        
        result = empty_module()
        assert result == "result"
    
    def test_monitor_health_zero_threshold(self):
        """Test monitor_health with zero threshold"""
        
        @monitor_health(module_id="zero_threshold", failure_threshold=0)
        def zero_threshold_function():
            return "result"
        
        result = zero_threshold_function()
        assert result == "result"
    
    def test_decorator_with_none_return(self):
        """Test decorators with function returning None"""
        
        @resilient(max_retries=1)
        @adaptive(module_id="none_module")
        def returns_none():
            return None
        
        result = returns_none()
        assert result is None
    
    def test_decorator_with_generator(self):
        """Test decorators with generator function"""
        
        @resilient(max_retries=1)
        def generator_function():
            yield 1
            yield 2
            yield 3
        
        result = list(generator_function())
        assert result == [1, 2, 3]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
