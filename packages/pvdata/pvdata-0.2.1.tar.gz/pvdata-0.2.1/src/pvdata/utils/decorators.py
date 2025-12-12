"""
Utility decorators for error handling and logging

Provides decorators for common patterns like error handling,
logging, and performance monitoring.
"""

import functools
import time
from typing import Callable, Any, Optional, Type
import logging

from pvdata.utils.exceptions import PVDataError


def handle_errors(
    exception_type: Type[Exception] = PVDataError,
    logger: Optional[logging.Logger] = None,
    reraise: bool = True,
    default_return: Any = None,
) -> Callable:
    """
    Decorator to handle exceptions with logging

    Args:
        exception_type: Type of exception to catch (default: PVDataError)
        logger: Logger instance to use (default: creates one)
        reraise: Whether to re-raise the exception after logging
        default_return: Value to return if exception is caught and not re-raised

    Examples:
        >>> @handle_errors(FileNotFoundError)
        ... def read_file(path):
        ...     with open(path) as f:
        ...         return f.read()

        >>> @handle_errors(reraise=False, default_return=[])
        ... def process_data():
        ...     # If error occurs, returns []
        ...     return result
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)

            try:
                return func(*args, **kwargs)
            except exception_type as e:
                logger.error(
                    f"Error in {func.__name__}: {str(e)}",
                    exc_info=True,
                )
                if reraise:
                    raise
                return default_return

        return wrapper

    return decorator


def log_execution(
    logger: Optional[logging.Logger] = None,
    level: str = "INFO",
    include_args: bool = False,
) -> Callable:
    """
    Decorator to log function execution

    Args:
        logger: Logger instance to use
        level: Log level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        include_args: Whether to include function arguments in log

    Examples:
        >>> @log_execution(level='DEBUG')
        ... def process_file(filename):
        ...     return data

        >>> @log_execution(include_args=True)
        ... def calculate(x, y):
        ...     return x + y
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)

            log_func = getattr(logger, level.lower())

            # Prepare log message
            if include_args:
                args_str = ", ".join(repr(a) for a in args)
                kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
                params = ", ".join(filter(None, [args_str, kwargs_str]))
                log_func(f"Calling {func.__name__}({params})")
            else:
                log_func(f"Calling {func.__name__}")

            result = func(*args, **kwargs)

            log_func(f"Finished {func.__name__}")
            return result

        return wrapper

    return decorator


def measure_time(
    logger: Optional[logging.Logger] = None,
    level: str = "INFO",
    message_template: str = "Function {name} took {elapsed:.3f}s",
) -> Callable:
    """
    Decorator to measure and log function execution time

    Args:
        logger: Logger instance to use
        level: Log level for timing message
        message_template: Template for timing message (available vars: name, elapsed)

    Examples:
        >>> @measure_time()
        ... def slow_function():
        ...     time.sleep(1)
        ...     return "done"

        >>> @measure_time(message_template="{name}: {elapsed:.2f} seconds")
        ... def process_data():
        ...     return result
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)

            log_func = getattr(logger, level.lower())

            start_time = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.time() - start_time
                message = message_template.format(name=func.__name__, elapsed=elapsed)
                log_func(message)

        return wrapper

    return decorator


def validate_args(**validators: Callable) -> Callable:
    """
    Decorator to validate function arguments

    Args:
        **validators: Keyword arguments mapping parameter names to validator functions

    Examples:
        >>> @validate_args(x=lambda x: x > 0, y=lambda y: isinstance(y, str))
        ... def process(x, y):
        ...     return f"{y}: {x}"

        >>> process(10, "value")  # OK
        >>> process(-5, "value")  # Raises ValueError
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get function signature
            import inspect

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Validate arguments
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator(value):
                        raise ValueError(
                            f"Validation failed for parameter '{param_name}' "
                            f"with value {value!r}"
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    logger: Optional[logging.Logger] = None,
) -> Callable:
    """
    Decorator to retry function on failure

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries (seconds)
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch
        logger: Logger instance for retry messages

    Examples:
        >>> @retry(max_attempts=3, delay=1.0)
        ... def unstable_operation():
        ...     # May fail occasionally
        ...     return result

        >>> @retry(exceptions=(ConnectionError,))
        ... def connect_to_api():
        ...     return api.connect()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)

            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} failed for "
                            f"{func.__name__}: {str(e)}. "
                            f"Retrying in {current_delay:.1f}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")

            # If we get here, all attempts failed
            raise last_exception

        return wrapper

    return decorator


# Alias for batch processing retry logic (Task 1.7)
def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    logger: Optional[logging.Logger] = None,
) -> Callable:
    """
    Decorator to retry function on failure (optimized for batch processing)

    This is an alias for the retry() decorator, specifically named for
    batch processing operations where transient failures may occur.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Multiplier for delay after each retry (default: 2.0)
        exceptions: Tuple of exceptions to catch and retry (default: all exceptions)
        logger: Logger instance for retry messages (default: auto-created)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> from pvdata.utils.decorators import retry_on_failure
        >>>
        >>> @retry_on_failure(max_attempts=3, delay=1.0, backoff=2.0)
        ... def convert_file(input_path, output_path):
        ...     # File conversion that may fail due to I/O errors
        ...     return process(input_path, output_path)
        >>>
        >>> # Retry only on specific exceptions
        >>> @retry_on_failure(
        ...     max_attempts=5,
        ...     exceptions=(IOError, OSError)
        ... )
        ... def read_remote_file(url):
        ...     return fetch(url)

    Notes:
        - Implements exponential backoff: delay * (backoff ^ attempt_number)
        - Logs warnings on retry, error on final failure
        - Re-raises last exception if all attempts fail
        - Designed for transient failures in batch processing
    """
    return retry(
        max_attempts=max_attempts,
        delay=delay,
        backoff=backoff,
        exceptions=exceptions,
        logger=logger,
    )
