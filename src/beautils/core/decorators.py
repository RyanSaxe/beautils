import functools
import logging
import time
from typing import Any, Callable


def timer(func: Callable) -> Callable:
    """Measure the execution time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute.")
        return result

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1) -> Callable:
    """Retry a function if it raises an exception, with a specified number of attempts and delay."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(delay)

        return wrapper

    return decorator


def log_function_call(func: Callable) -> Callable:
    """Log function calls, including arguments and return values."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned: {result}")
        return result

    return wrapper


# TODO: generalize this to work without specifications --- make it work according to type annotations
def validate_types(*types: Any, return_type: Any = None) -> Callable:
    """Validate the types of function arguments and return value."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg, expected_type in zip(args, types, strict=False):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Argument {arg} is not of type {expected_type}")
            result = func(*args, **kwargs)
            if return_type and not isinstance(result, return_type):
                raise TypeError(f"Return value {result} is not of type {return_type}")
            return result

        return wrapper

    return decorator


def deprecated(func: Callable) -> Callable:
    """Mark a function as deprecated and issue a warning when it's used."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning(
            f"Function {func.__name__} is deprecated and will be removed in future versions."
        )
        return func(*args, **kwargs)

    return wrapper
