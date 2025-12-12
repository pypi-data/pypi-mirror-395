"""Utility functions for common operations like polling."""
from typing import Callable, Any, Tuple
import time


def poll_for_status(get_status_fn: Callable[[str], Tuple[bool, Any]],
                    resource_id: str, interval: int = 5, timeout: int = 300) -> Any:
    """
    Poll a status function until target statuses are met or timeout.

    :param get_status_fn: Function that takes resource_id and returns (is_done: bool, result: Any)
    :param resource_id: ID to pass to the function
    :param interval: Poll interval in seconds
    :param timeout: Total timeout in seconds
    :return: The final result from get_status_fn
    :raises TimeoutError: If timeout exceeded
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        is_done, result = get_status_fn(resource_id)
        if is_done:
            return result
        time.sleep(interval)
    raise TimeoutError(f"Polling timed out after {timeout} seconds for resource {resource_id}")
