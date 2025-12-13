"""
RAFAEL Enhanced Error Handling
Comprehensive error handling, recovery, and monitoring
"""

import functools
import traceback
import sys
from typing import Callable, Optional, Any, Dict, List
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger("RAFAEL.ErrorHandling")


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories"""
    NETWORK = "network"
    DATABASE = "database"
    COMPUTATION = "computation"
    VALIDATION = "validation"
    RESOURCE = "resource"
    SECURITY = "security"
    UNKNOWN = "unknown"


class RAFAELError(Exception):
    """Base exception for RAFAEL Framework"""
    
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.severity = severity
        self.category = category
        self.recoverable = recoverable
        self.context = context or {}
        self.timestamp = datetime.now()
        self.traceback = traceback.format_exc()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary"""
        return {
            "message": self.message,
            "severity": self.severity.value,
            "category": self.category.value,
            "recoverable": self.recoverable,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "traceback": self.traceback
        }


class GenomeError(RAFAELError):
    """Errors related to genome operations"""
    pass


class MutationError(RAFAELError):
    """Errors related to mutations"""
    pass


class ChaosError(RAFAELError):
    """Errors related to chaos testing"""
    pass


class PersistenceError(RAFAELError):
    """Errors related to data persistence"""
    pass


class GuardianError(RAFAELError):
    """Errors related to Guardian layer"""
    pass


class ErrorHandler:
    """
    Centralized error handling and recovery
    """
    
    def __init__(self):
        self.error_history: List[RAFAELError] = []
        self.error_callbacks: Dict[ErrorCategory, List[Callable]] = {}
        self.recovery_strategies: Dict[ErrorCategory, Callable] = {}
        self.max_history = 1000
    
    def register_callback(
        self,
        category: ErrorCategory,
        callback: Callable[[RAFAELError], None]
    ):
        """
        Register callback for specific error category
        
        Args:
            category: Error category
            callback: Callback function
        """
        if category not in self.error_callbacks:
            self.error_callbacks[category] = []
        self.error_callbacks[category].append(callback)
        logger.info(f"Callback registered for {category.value} errors")
    
    def register_recovery_strategy(
        self,
        category: ErrorCategory,
        strategy: Callable[[RAFAELError], Any]
    ):
        """
        Register recovery strategy for error category
        
        Args:
            category: Error category
            strategy: Recovery function
        """
        self.recovery_strategies[category] = strategy
        logger.info(f"Recovery strategy registered for {category.value} errors")
    
    def handle_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        """
        Handle an error with appropriate strategy
        
        Args:
            error: The exception
            context: Additional context
            
        Returns:
            Recovery result if applicable
        """
        # Convert to RAFAELError if needed
        if not isinstance(error, RAFAELError):
            rafael_error = self._convert_to_rafael_error(error, context)
        else:
            rafael_error = error
        
        # Log error
        self._log_error(rafael_error)
        
        # Store in history
        self._store_error(rafael_error)
        
        # Execute callbacks
        self._execute_callbacks(rafael_error)
        
        # Attempt recovery if possible
        if rafael_error.recoverable:
            return self._attempt_recovery(rafael_error)
        
        return None
    
    def _convert_to_rafael_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]]
    ) -> RAFAELError:
        """Convert standard exception to RAFAELError"""
        category = self._categorize_error(error)
        severity = self._assess_severity(error)
        
        return RAFAELError(
            message=str(error),
            severity=severity,
            category=category,
            recoverable=self._is_recoverable(error),
            context=context
        )
    
    def _categorize_error(self, error: Exception) -> ErrorCategory:
        """Categorize error based on type and message"""
        error_type = type(error).__name__
        error_msg = str(error).lower()
        
        if any(keyword in error_msg for keyword in ['network', 'connection', 'timeout']):
            return ErrorCategory.NETWORK
        elif any(keyword in error_msg for keyword in ['database', 'sql', 'query']):
            return ErrorCategory.DATABASE
        elif any(keyword in error_msg for keyword in ['memory', 'cpu', 'resource']):
            return ErrorCategory.RESOURCE
        elif any(keyword in error_msg for keyword in ['permission', 'auth', 'security']):
            return ErrorCategory.SECURITY
        elif any(keyword in error_msg for keyword in ['validation', 'invalid', 'format']):
            return ErrorCategory.VALIDATION
        elif isinstance(error, (ArithmeticError, ValueError, TypeError)):
            return ErrorCategory.COMPUTATION
        else:
            return ErrorCategory.UNKNOWN
    
    def _assess_severity(self, error: Exception) -> ErrorSeverity:
        """Assess error severity"""
        error_type = type(error).__name__
        
        # Critical errors
        if isinstance(error, (SystemError, MemoryError, KeyboardInterrupt)):
            return ErrorSeverity.CRITICAL
        
        # High severity
        if isinstance(error, (RuntimeError, OSError)):
            return ErrorSeverity.HIGH
        
        # Medium severity
        if isinstance(error, (ValueError, TypeError, AttributeError)):
            return ErrorSeverity.MEDIUM
        
        # Low severity
        return ErrorSeverity.LOW
    
    def _is_recoverable(self, error: Exception) -> bool:
        """Determine if error is recoverable"""
        # Non-recoverable errors
        if isinstance(error, (SystemExit, KeyboardInterrupt, MemoryError)):
            return False
        
        # Most errors are potentially recoverable
        return True
    
    def _log_error(self, error: RAFAELError):
        """Log error with appropriate level"""
        log_msg = f"[{error.severity.value.upper()}] {error.category.value}: {error.message}"
        
        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_msg)
        elif error.severity == ErrorSeverity.HIGH:
            logger.error(log_msg)
        elif error.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_msg)
        else:
            logger.info(log_msg)
        
        if error.context:
            logger.debug(f"Context: {error.context}")
    
    def _store_error(self, error: RAFAELError):
        """Store error in history"""
        self.error_history.append(error)
        
        # Limit history size
        if len(self.error_history) > self.max_history:
            self.error_history = self.error_history[-self.max_history:]
    
    def _execute_callbacks(self, error: RAFAELError):
        """Execute registered callbacks for error category"""
        callbacks = self.error_callbacks.get(error.category, [])
        
        for callback in callbacks:
            try:
                callback(error)
            except Exception as e:
                logger.error(f"Error callback failed: {e}")
    
    def _attempt_recovery(self, error: RAFAELError) -> Optional[Any]:
        """Attempt to recover from error"""
        strategy = self.recovery_strategies.get(error.category)
        
        if strategy:
            try:
                logger.info(f"Attempting recovery for {error.category.value} error")
                result = strategy(error)
                logger.info("Recovery successful")
                return result
            except Exception as e:
                logger.error(f"Recovery failed: {e}")
        
        return None
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics"""
        if not self.error_history:
            return {
                "total_errors": 0,
                "by_severity": {},
                "by_category": {},
                "recoverable_rate": 0.0
            }
        
        by_severity = {}
        by_category = {}
        recoverable_count = 0
        
        for error in self.error_history:
            # Count by severity
            severity = error.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1
            
            # Count by category
            category = error.category.value
            by_category[category] = by_category.get(category, 0) + 1
            
            # Count recoverable
            if error.recoverable:
                recoverable_count += 1
        
        return {
            "total_errors": len(self.error_history),
            "by_severity": by_severity,
            "by_category": by_category,
            "recoverable_rate": recoverable_count / len(self.error_history),
            "recent_errors": [
                {
                    "message": e.message,
                    "severity": e.severity.value,
                    "category": e.category.value,
                    "timestamp": e.timestamp.isoformat()
                }
                for e in self.error_history[-10:]
            ]
        }
    
    def clear_history(self):
        """Clear error history"""
        self.error_history.clear()
        logger.info("Error history cleared")


# Global error handler instance
_global_error_handler = ErrorHandler()


def get_error_handler() -> ErrorHandler:
    """Get global error handler instance"""
    return _global_error_handler


def safe_execute(
    func: Callable,
    *args,
    fallback: Optional[Any] = None,
    context: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Any:
    """
    Safely execute a function with error handling
    
    Args:
        func: Function to execute
        *args: Positional arguments
        fallback: Fallback value if error occurs
        context: Additional context
        **kwargs: Keyword arguments
        
    Returns:
        Function result or fallback value
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        handler = get_error_handler()
        result = handler.handle_error(e, context)
        return result if result is not None else fallback


def with_error_handling(
    fallback: Optional[Any] = None,
    category: Optional[ErrorCategory] = None,
    severity: Optional[ErrorSeverity] = None
):
    """
    Decorator for automatic error handling
    
    Args:
        fallback: Fallback value on error
        category: Error category override
        severity: Error severity override
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = get_error_handler()
                
                # Create or enhance error
                if isinstance(e, RAFAELError):
                    error = e
                else:
                    error = RAFAELError(
                        message=str(e),
                        severity=severity or handler._assess_severity(e),
                        category=category or handler._categorize_error(e),
                        context={"function": func.__name__}
                    )
                
                result = handler.handle_error(error)
                return result if result is not None else fallback
        
        return wrapper
    return decorator


def validate_input(
    validation_func: Callable[[Any], bool],
    error_message: str = "Validation failed"
):
    """
    Decorator for input validation
    
    Args:
        validation_func: Function to validate inputs
        error_message: Error message if validation fails
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not validation_func(*args, **kwargs):
                raise RAFAELError(
                    message=error_message,
                    severity=ErrorSeverity.MEDIUM,
                    category=ErrorCategory.VALIDATION,
                    context={
                        "function": func.__name__,
                        "args": str(args)[:100],
                        "kwargs": str(kwargs)[:100]
                    }
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


class ErrorRecoveryContext:
    """Context manager for error recovery"""
    
    def __init__(
        self,
        fallback: Optional[Any] = None,
        suppress: bool = False,
        context: Optional[Dict[str, Any]] = None
    ):
        self.fallback = fallback
        self.suppress = suppress
        self.context = context
        self.error: Optional[RAFAELError] = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            handler = get_error_handler()
            self.error = handler.handle_error(exc_val, self.context)
            
            if self.suppress:
                return True  # Suppress exception
        
        return False


# Recovery strategies
def network_recovery_strategy(error: RAFAELError) -> Optional[Any]:
    """Recovery strategy for network errors"""
    logger.info("Attempting network recovery...")
    # Implement network-specific recovery
    # e.g., retry with exponential backoff
    return None


def database_recovery_strategy(error: RAFAELError) -> Optional[Any]:
    """Recovery strategy for database errors"""
    logger.info("Attempting database recovery...")
    # Implement database-specific recovery
    # e.g., reconnect, use read replica
    return None


def resource_recovery_strategy(error: RAFAELError) -> Optional[Any]:
    """Recovery strategy for resource errors"""
    logger.info("Attempting resource recovery...")
    # Implement resource-specific recovery
    # e.g., free memory, reduce load
    return None


# Register default recovery strategies
_global_error_handler.register_recovery_strategy(
    ErrorCategory.NETWORK,
    network_recovery_strategy
)
_global_error_handler.register_recovery_strategy(
    ErrorCategory.DATABASE,
    database_recovery_strategy
)
_global_error_handler.register_recovery_strategy(
    ErrorCategory.RESOURCE,
    resource_recovery_strategy
)
