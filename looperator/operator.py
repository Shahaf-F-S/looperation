# operator.py

import time
import warnings
import threading
import datetime as dt
from typing import (
    Union, Optional, Callable, Generic,
    Any, Dict, Iterable, TypeVar
)

from represent import represent

from looperator.process import ProcessTime
from looperator.handler import Handler

__all__ = [
    "Operator"
]

def time_seconds(wait: Union[float, dt.timedelta, dt.datetime]) -> float:
    """
    Runs a waiting for the process.

    :param wait: The duration of the start_timeout.

    :return: The waiting value.
    """

    if isinstance(wait, dt.datetime):
        wait = wait - dt.datetime.now()
    # end if

    if isinstance(wait, dt.timedelta):
        wait = wait.total_seconds()
    # end if

    return wait
# end time_seconds

_O = TypeVar("_O")

@represent
class Operator(Generic[_O]):
    """A class to handle a loop operation."""

    DELAY = 0
    _SLEEP = 0.0001

    def __init__(
            self,
            operation: Callable[..., _O],
            args_collector: Optional[Callable[[], Iterable[Any]]] = None,
            kwargs_collector: Optional[Callable[[], Dict[str, Any]]] = None,
            handler: Optional[Handler] = None,
            delay: Optional[Union[float, dt.timedelta]] = None
    ) -> None:
        """
        Defines the attributes of the handler.

        :param operation: The callback to call.
        :param kwargs_collector: The callback to collect args.
        :param kwargs_collector: The callback to collect kwargs.
        :param delay: The delay for the process.
        """

        if delay is None:
            delay = self.DELAY
        # end if

        self.delay = delay

        self._operating = False
        self._blocking = False
        self._timeout = False
        self._running = False
        self._paused = False

        self._operation_process: Optional[threading.Thread] = None
        self._timeout_process: Optional[threading.Thread] = None

        self._start: Optional[dt.datetime] = None
        self._end: Optional[dt.datetime] = None

        self.operation = operation
        self.args_collector = args_collector
        self.kwargs_collector = kwargs_collector
        self.handler = handler
    # end __init__

    @property
    def blocking(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._blocking
    # end blocking

    @property
    def operating(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._operating
    # end operating

    @property
    def running(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._running
    # end running

    @property
    def paused(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._paused
    # end paused

    @property
    def timeout(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The flag value.
        """

        return self._timeout
    # end timeout

    @property
    def start(self) -> Optional[dt.datetime]:
        """
        returns the value of the start time.

        :return: The start time value.
        """

        return self._start
    # end start

    @property
    def end(self) -> Optional[dt.datetime]:
        """
        returns the value of the end time.

        :return: The end time value.
        """

        if self.running and (not self.paused):
            self._end = dt.datetime.now()
        # end if

        return self._end
    # end end

    @property
    def time(self) -> Optional[ProcessTime]:
        """
        returns the value of the start time.

        :return: The start time value.
        """

        if self._start is None:
            return None
        # end if

        return ProcessTime(
            start=self._start,
            end=self.end or dt.datetime.now()
        )
    # end time

    def operate(self) -> None:
        """Runs the process of the price screening."""

        self.operation(
            *(self.args_collector() if self.args_collector else ()),
            **(self.kwargs_collector() if self.kwargs_collector else {})
        )
    # end operate

    def operation_loop(self) -> None:
        """Runs the process of the price screening."""

        while self.running:
            while self.operating:
                t = time.time()

                if self.handler is None:
                    self.operate()

                else:
                    with self.handler:
                        self.operate()
                    # end with
                # end try

                if self.delay:
                    delay = time_seconds(self.delay)

                    time.sleep(max(delay - (time.time() - t), 0))
                # end if
            # end while

            while self.paused:
                time.sleep(self._SLEEP)
            # end while
        # end while
    # end operation_loop

    def timeout_loop(self, duration: Union[float, dt.timedelta, dt.datetime]) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        if isinstance(duration, (int, float)):
            duration = dt.timedelta(seconds=duration)
        # end if

        if isinstance(duration, dt.timedelta):
            duration = dt.datetime.now() + duration
        # end if

        last = dt.datetime.now()

        start = None

        paused = False

        while self.timeout and (duration > last):
            while self.paused:
                if not paused:
                    start = dt.datetime.now()

                    paused = True
                # end if

                time.sleep(self._SLEEP)
            # end while

            last = dt.datetime.now()

            if paused:
                duration += (last - start)

                paused = False
            # end if
        # end while

        if self.timeout:
            self.stop()
        # end if
    # end timeout_loop

    def start_operation(self) -> None:
        """Starts the screening process."""

        if self.operating:
            warnings.warn(f"Handling process of {repr(self)} is already running.")

            return
        # end if

        self._operating = True

        if self.blocking:
            self.operation_loop()

        else:
            self._operation_process = threading.Thread(
                target=self.operation_loop
            )

            self._operation_process.start()
        # end if
    # end start_operation

    @staticmethod
    def start_waiting(wait: Union[float, dt.timedelta, dt.datetime]) -> None:
        """
        Runs a waiting for the process.

        :param wait: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        time.sleep(time_seconds(wait))
    # end start_waiting

    def start_timeout(self, duration: Union[float, dt.timedelta, dt.datetime]) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        if self.timeout:
            warnings.warn(f"Timeout process of {repr(self)} is already running.")

            return
        # end if

        self._timeout = True

        self._timeout_process = threading.Thread(
            target=lambda: self.timeout_loop(duration=duration)
        )

        self._timeout_process.start()
    # end start_timeout

    def run(
            self,
            block: Optional[bool] = False,
            wait: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
            timeout: Optional[Union[float, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a start_timeout to the process.
        """

        self._running = True
        self._paused = False

        self._blocking = block

        self._start = dt.datetime.now()

        if timeout:
            self.start_timeout(timeout)
        # end if

        if wait:
            self.start_waiting(wait)
        # end if

        self.start_operation()
    # end run

    def stop_operation(self) -> None:
        """Stops the screening process."""

        if self.operating:
            self._operating = False
        # end if

        if (
            isinstance(self._operation_process, threading.Thread) and
            self._operation_process.is_alive()
        ):
            self._operation_process = None
        # end if
    # end stop_operation

    def stop_timeout(self) -> None:
        """Stops the screening process."""

        if self.timeout:
            self._timeout = False
        # end if

        if (
            isinstance(self._timeout_process, threading.Thread) and
            self._timeout_process.is_alive()
        ):
            self._timeout_process = None
        # end if
    # end stop_timeout

    def pause(self) -> None:
        """Stops the screening process."""

        self._paused = True
    # end pause

    def unpause(self) -> None:
        """Stops the screening process."""

        self._paused = False
    # end unpause

    def stop(self) -> None:
        """Stops the screening process."""

        self._running = False

        self.unpause()
        self.stop_operation()
        self.stop_timeout()
    # end stop
# end Operator