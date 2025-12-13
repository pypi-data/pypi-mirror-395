from datetime import datetime


def time_ns_to_formatted_string(time_ns: int) -> str:
    """
    Transfer nanoseconds to formatted string YYYY-MM-DD HH:MM:SS:{milliseconds}.

    Args:
        time_ns (int): Time in nanoseconds

    Returns:
        str: Formatted time string
    """
    seconds = time_ns // 1_000_000_000
    milliseconds = (time_ns % 1_000_000_000) // 1_000_000
    return timestamp_to_formatted_string(seconds, milliseconds)


def time_ms_to_formatted_string(time_ms: int) -> str:
    """
    Transfer milliseconds to formatted string.

    Args:
        time_ms (int): Time in milliseconds

    Returns:
        str: Formatted time string
    """
    seconds = time_ms // 1000
    milliseconds = time_ms % 1000
    return timestamp_to_formatted_string(seconds, milliseconds)


def timestamp_to_formatted_string(seconds: int, milliseconds: int) -> str:
    """
    Convert timestamp to formatted string.

    Args:
        seconds (int): Seconds since epoch
        milliseconds (int): Milliseconds part

    Returns:
        str: Formatted time string
    """
    dt = datetime.fromtimestamp(seconds)
    formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
    formatted += f":{milliseconds:03d}"
    return formatted


def get_current_time() -> str:
    """
    Get current time as formatted string.

    Returns:
        str: Current time in format YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
