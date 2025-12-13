"""
RAFAEL Decorators
Provides @AntiFragile and other decorators for easy integration
"""

import functools
import asyncio
import time
from typing import Callable, Optional, Any, Dict
from enum import Enum
import logging

from .rafael_engine import (
    RafaelCore,
    ResilienceStrategy,
    IsolationLevel,
    Gene
)

logger = logging.getLogger("RAFAEL.Decorators")


class RetryPolicy(Enum):
    """Retry policies"""
    NONE = "none"
    FIXED = "fixed"
    EXPONENTIAL = "exponential"
    ADAPTIVE = "adaptive"


class FallbackStrategy(Enum):
    """Fallback strategies"""
    NONE = "none"
    DEFAULT_VALUE = "default_value"
    ALTERNATIVE_FUNCTION = "alternative_function"
    GENOMIC = "genomic"  # Use genome-based fallback


class AntiFragile:
    """
    Main decorator for making functions resilient and adaptive
    
    Usage:
        @AntiFragile(
            retry_policy="adaptive",
            fallback="genomic",
            isolation_level="high"
        )
        async def critical_function():
            pass
    """
    
    _rafael_core: Optional[RafaelCore] = None
    
    @classmethod
    def set_core(cls, core: RafaelCore):
        """Set the global RAFAEL core instance"""
        cls._rafael_core = core
    
    def __init__(
        self,
        retry_policy: str = "adaptive",
        max_retries: int = 3,
        timeout: Optional[float] = None,
        fallback: str = "none",
        fallback_value: Any = None,
        fallback_function: Optional[Callable] = None,
        isolation_level: str = "medium",
        circuit_breaker: bool = True,
        rate_limit: Optional[int] = None,
        cache_results: bool = False,
        threat_model: Optional[str] = None,
        load_strategy: Optional[str] = None,
        blockchain_fallback: Optional[str] = None
    ):
        self.retry_policy = RetryPolicy(retry_policy)
        self.max_retries = max_retries
        self.timeout = timeout
        self.fallback = FallbackStrategy(fallback)
        self.fallback_value = fallback_value
        self.fallback_function = fallback_function
        self.isolation_level = IsolationLevel(isolation_level)
        self.circuit_breaker = circuit_breaker
        self.rate_limit = rate_limit
        self.cache_results = cache_results
        self.threat_model = threat_model
        self.load_strategy = load_strategy
        self.blockchain_fallback = blockchain_fallback
        
        # State
        self.failure_count = 0
        self.circuit_open = False
        self.last_failure_time = 0
        self.cache: Dict[str, Any] = {}
        self.request_times: list = []
    
    def __call__(self, func: Callable) -> Callable:
        """Wrap the function with resilience logic"""
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            module_id = f"{func.__module__}.{func.__name__}"
            
            # Register module with RAFAEL if available
            if self._rafael_core and module_id not in self._rafael_core.genomes:
                self._rafael_core.register_module(module_id)
            
            # Check circuit breaker
            if self.circuit_breaker and self.circuit_open:
                if time.time() - self.last_failure_time < 60:  # 60s timeout
                    logger.warning(f"Circuit breaker open for {module_id}")
                    return await self._execute_fallback(args, kwargs)
                else:
                    self.circuit_open = False
                    self.failure_count = 0
            
            # Check rate limit
            if self.rate_limit and not self._check_rate_limit():
                logger.warning(f"Rate limit exceeded for {module_id}")
                await asyncio.sleep(0.1)  # Brief backoff
            
            # Check cache
            if self.cache_results:
                cache_key = self._make_cache_key(args, kwargs)
                if cache_key in self.cache:
                    logger.debug(f"Cache hit for {module_id}")
                    return self.cache[cache_key]
            
            # Execute with resilience
            result = await self._execute_with_resilience(
                func, args, kwargs, module_id
            )
            
            # Update cache
            if self.cache_results and result is not None:
                cache_key = self._make_cache_key(args, kwargs)
                self.cache[cache_key] = result
            
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            """Synchronous wrapper"""
            # For sync functions, create event loop if needed
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            return loop.run_until_complete(async_wrapper(*args, **kwargs))
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    async def _execute_with_resilience(
        self,
        func: Callable,
        args: tuple,
        kwargs: dict,
        module_id: str
    ) -> Any:
        """Execute function with full resilience logic"""
        
        last_exception = None
        retry_count = 0
        
        while retry_count <= self.max_retries:
            try:
                # Apply timeout if specified
                if self.timeout:
                    result = await asyncio.wait_for(
                        self._call_function(func, args, kwargs),
                        timeout=self.timeout
                    )
                else:
                    result = await self._call_function(func, args, kwargs)
                
                # Success! Update metrics
                if self._rafael_core and module_id in self._rafael_core.genomes:
                    genome = self._rafael_core.genomes[module_id]
                    for gene in genome.genes:
                        gene.success_count += 1
                
                self.failure_count = 0
                return result
                
            except asyncio.TimeoutError:
                logger.warning(f"Timeout in {module_id} (attempt {retry_count + 1})")
                last_exception = TimeoutError(f"Function timed out after {self.timeout}s")
                
            except Exception as e:
                logger.error(f"Error in {module_id}: {e} (attempt {retry_count + 1})")
                last_exception = e
                
                # Update failure metrics
                if self._rafael_core and module_id in self._rafael_core.genomes:
                    genome = self._rafael_core.genomes[module_id]
                    for gene in genome.genes:
                        gene.failure_count += 1
            
            # Increment retry count
            retry_count += 1
            
            # Check if we should retry
            if retry_count <= self.max_retries:
                delay = self._calculate_retry_delay(retry_count)
                logger.info(f"Retrying {module_id} in {delay}s...")
                await asyncio.sleep(delay)
            
            # Update failure tracking
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            # Open circuit breaker if too many failures
            if self.circuit_breaker and self.failure_count >= 5:
                self.circuit_open = True
                logger.error(f"Circuit breaker opened for {module_id}")
        
        # All retries exhausted, execute fallback
        logger.error(f"All retries exhausted for {module_id}")
        return await self._execute_fallback(args, kwargs, last_exception)
    
    async def _call_function(self, func: Callable, args: tuple, kwargs: dict) -> Any:
        """Call function (async or sync)"""
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    
    def _calculate_retry_delay(self, retry_count: int) -> float:
        """Calculate delay before next retry"""
        if self.retry_policy == RetryPolicy.NONE:
            return 0.0
        elif self.retry_policy == RetryPolicy.FIXED:
            return 1.0
        elif self.retry_policy == RetryPolicy.EXPONENTIAL:
            return min(2 ** retry_count, 30.0)  # Cap at 30s
        elif self.retry_policy == RetryPolicy.ADAPTIVE:
            # Adaptive: consider recent failure rate
            base_delay = 2 ** retry_count
            if self.failure_count > 3:
                base_delay *= 1.5  # Increase delay if many recent failures
            return min(base_delay, 30.0)
        return 1.0
    
    async def _execute_fallback(
        self,
        args: tuple,
        kwargs: dict,
        exception: Optional[Exception] = None
    ) -> Any:
        """Execute fallback strategy"""
        if self.fallback == FallbackStrategy.NONE:
            if exception:
                raise exception
            return None
        
        elif self.fallback == FallbackStrategy.DEFAULT_VALUE:
            logger.info("Using default fallback value")
            return self.fallback_value
        
        elif self.fallback == FallbackStrategy.ALTERNATIVE_FUNCTION:
            if self.fallback_function:
                logger.info("Using alternative fallback function")
                return await self._call_function(self.fallback_function, args, kwargs)
            return self.fallback_value
        
        elif self.fallback == FallbackStrategy.GENOMIC:
            logger.info("Using genomic fallback strategy")
            # Use best-performing gene's strategy as fallback
            # This is a placeholder - in production, would use actual genomic data
            return self.fallback_value
        
        return None
    
    def _check_rate_limit(self) -> bool:
        """Check if request is within rate limit"""
        if not self.rate_limit:
            return True
        
        now = time.time()
        # Remove old requests (older than 1 minute)
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        if len(self.request_times) >= self.rate_limit:
            return False
        
        self.request_times.append(now)
        return True
    
    def _make_cache_key(self, args: tuple, kwargs: dict) -> str:
        """Create cache key from arguments"""
        import hashlib
        import json
        
        # Simple cache key based on args/kwargs
        key_data = {
            "args": str(args),
            "kwargs": str(sorted(kwargs.items()))
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()


# Convenience decorators for specific use cases

def resilient(
    max_retries: int = 3,
    timeout: float = 10.0
) -> Callable:
    """Simple resilient decorator with retries and timeout"""
    return AntiFragile(
        retry_policy="exponential",
        max_retries=max_retries,
        timeout=timeout
    )


def circuit_protected(
    failure_threshold: int = 5,
    timeout: float = 60.0
) -> Callable:
    """Decorator with circuit breaker protection"""
    return AntiFragile(
        circuit_breaker=True,
        max_retries=3,
        timeout=timeout
    )


def rate_limited(
    max_requests: int = 100
) -> Callable:
    """Decorator with rate limiting"""
    return AntiFragile(
        rate_limit=max_requests,
        retry_policy="adaptive"
    )


def cached_resilient(
    timeout: float = 10.0,
    cache_ttl: int = 300
) -> Callable:
    """Decorator with caching and resilience"""
    return AntiFragile(
        cache_results=True,
        timeout=timeout,
        retry_policy="adaptive"
    )
