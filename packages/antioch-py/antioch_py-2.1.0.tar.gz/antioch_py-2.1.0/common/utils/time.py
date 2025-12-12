import math
import time


def now_us() -> int:
    """
    Get current wall time in microseconds.

    :return: Current time in microseconds since epoch.
    """

    return time.time_ns() // 1000


def us_to_s(us: int) -> float:
    """
    Convert microseconds to seconds, flooring to the nearest
    millisecond.

    :param us: The time in microseconds.
    :return: The time in seconds.
    """

    if not math.isfinite(us) or us < 0:
        return 0.0

    return int(us / 1_000) / 1_000.0


def s_to_us(s: float) -> int:
    """
    Convert seconds to microseconds, flooring to the nearest
    millisecond.

    :param s: The time in seconds.
    :return: The time in microseconds.
    """

    if not math.isfinite(s) or s < 0:
        return 0

    return int(s * 1_000) * 1_000
