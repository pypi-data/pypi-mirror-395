import time
from threading import Event

from common.utils.time import now_us


class Clock:
    """
    Real-time clock for LET-to-wall-time mapping (real mode only).

    Maps logical execution time to wall-clock time using a fixed start time.
    Provides precise timing for real-mode execution to avoid clock drift.
    """

    def __init__(self, start_timestamp_us: int, event: Event | None = None):
        """
        Create a new real-time clock.

        :param start_timestamp_us: Wall-clock time (microseconds since epoch) corresponding to LET=0.
        :param event: Optional event to check for shutdown requests during waits.
        """

        self._start_timestamp_us = start_timestamp_us
        self._event = event

    @property
    def let_us(self) -> int:
        """
        Get the current logical time in microseconds.

        :return: Current logical time.
        """

        return now_us() - self._start_timestamp_us

    def wait_until(self, let_us: int) -> bool:
        """
        Sleep until reaching target LET.

        Checks shutdown event every 100ms. Uses hybrid sleep approach:
        - For waits > 10ms: Sleep in chunks (max 100ms) for shutdown responsiveness
        - For waits < 10ms: Sleep in 100μs increments for precision

        :param let_us: Target logical execution time in microseconds.
        :return: True if wait completed normally, False if interrupted by event.
        """

        target_timestamp_us = self._start_timestamp_us + let_us
        while True:
            # Check if we should exit
            current = now_us()
            if current >= target_timestamp_us:
                return True

            # Check event if provided
            if self._event and self._event.is_set():
                return False

            # Sleep for chunk
            remaining_us = target_timestamp_us - current
            sleep_us = min(remaining_us, 100_000) if remaining_us > 10_000 else min(remaining_us, 100)
            time.sleep(sleep_us / 1_000_000)
