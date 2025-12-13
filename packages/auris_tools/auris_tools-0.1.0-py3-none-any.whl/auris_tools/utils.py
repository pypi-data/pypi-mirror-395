import time
from contextlib import contextmanager
from datetime import datetime
from uuid import uuid4


def collect_timestamp(as_str: bool = True):
    """
    Collect the current timestamp in ISO 8601 format.

    Parameters
    ----------
    as_str : bool, default=True
        If True, returns the timestamp as an ISO 8601 formatted string.
        If False, returns a datetime object.

    Returns
    -------
    str or datetime
        Current timestamp as an ISO 8601 formatted string (if as_str=True)
        or as a datetime object (if as_str=False).

    Examples
    --------
    >>> collect_timestamp()
    '2023-05-18T15:30:45.123456'

    >>> collect_timestamp(as_str=False)
    datetime.datetime(2023, 5, 18, 15, 30, 45, 123456)
    """
    if as_str:
        return datetime.now().isoformat()
    return datetime.now()


def parse_timestamp(timestamp_input):
    """Parse a timestamp to a datetime object.

    Args:
        timestamp_input: Either an ISO 8601 timestamp string or a datetime object.

    Returns:
        datetime: The parsed datetime object.
    """
    if isinstance(timestamp_input, datetime):
        return timestamp_input
    return datetime.fromisoformat(timestamp_input)


def generate_uuid():
    """
    Generate a unique Universally Unique Identifier (UUID) string.

    This function creates a random UUID using version 4 (random) of the UUID
    specification and returns it as a string. UUIDs are 128-bit identifiers
    that are guaranteed to be unique across space and time.

    Returns:
        str: A string representation of a UUID4 (e.g., '9f8d8f79-2d6d-4b96-a3f5-e1f025e6379b')

    Example:
        >>> unique_id = generate_uuid()
        >>> print(unique_id)
        '9f8d8f79-2d6d-4b96-a3f5-e1f025e6379b'
    """
    return str(uuid4())


def collect_processing_time():
    """
    Context manager for measuring code execution time.

    This function provides a context manager that measures the execution time of
    code within its scope. The execution time is returned in seconds.

    Returns
    -------
    callable
        Function that returns the current elapsed time in seconds when called.

    Examples
    --------
    >>> with collect_processing_time() as total_time:
    ...     # Your code here
    ...     import time
    ...     time.sleep(1)
    >>> print(f"Execution took {total_time()} seconds")
    Execution took 1.001234 seconds

    >>> # Example with multiple measurements during execution
    >>> with collect_processing_time() as get_time:
    ...     # First operation
    ...     time.sleep(0.5)
    ...     first_step = get_time()
    ...     print(f"First step: {first_step:.2f}s")
    ...
    ...     # Second operation
    ...     time.sleep(0.5)
    ...     second_step = get_time()
    ...     print(f"Second step: {second_step:.2f}s")
    First step: 0.50s
    Second step: 1.00s
    """

    @contextmanager
    def _timing_context():
        start_time = time.time()

        # Create a function to get the current elapsed time
        def get_elapsed_time():
            return time.time() - start_time

        try:
            # Yield the function that returns elapsed time
            yield get_elapsed_time
        finally:
            # No cleanup needed
            pass

    return _timing_context()
