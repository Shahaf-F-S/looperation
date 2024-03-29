# operator.py

import time
import warnings
import threading
import asyncio
import datetime as dt
from typing import (
    Callable, Generic, Any, Iterable, TypeVar, Awaitable
)

from looperation.process import ProcessTime
from looperation.handler import Handler

__all__ = [
    "Operator",
    "time_seconds"
]

def time_seconds(wait: float | dt.timedelta | dt.datetime) -> float:
    """
    Runs a waiting for the process.

    :param wait: The duration of the start_timeout.

    :return: The waiting value.
    """

    if isinstance(wait, dt.datetime):
        wait = wait - dt.datetime.now()

    if isinstance(wait, dt.timedelta):
        wait = wait.total_seconds()

    return wait

_O = TypeVar("_O")

TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

class Operator(Generic[_O]):
    """A class to handle a loop operation."""

    DELAY = 0
    _SLEEP = 0.0001

    def __init__(
            self,
            name: str = None, *,
            operation: Callable[..., _O | Awaitable[_O]] = None,
            args_collector: Callable[[], Iterable[Any]] = None,
            kwargs_collector: Callable[[], dict[str, Any]] = None,
            stopping_collector: Callable[[], bool] = None,
            termination: Callable[[], Any] = None,
            handler: Handler = None,
            loop: bool = True,
            warn: bool = False,
            loop_stopping: bool = None,
            delay: TimeDuration = None,
            block: bool = False,
            coroutine: bool = False,
            wait: TimeDestination = None,
            timeout: TimeDestination = None
    ) -> None:
        """
        Defines the attributes of the handler.

        :param name: The name of the operation.
        :param operation: The callback to call.
        :param kwargs_collector: The callback to collect args.
        :param kwargs_collector: The callback to collect kwargs.
        :param stopping_collector: The callback to collect a value to indicate to stop.
        :param termination: The termination callback.
        :param handler: The handler object to handle the operation.
        :param loop: The value to run a loop.
        :param warn: The value to warn.
        :param loop_stopping: The value to evaluate stopping during a loop.
        :param delay: The delay for the process.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a start_timeout to the process.
        :param coroutine: The value to add the process as a coroutine to a running event loop.
        """

        if delay is None:
            delay = self.DELAY

        if loop_stopping is None and loop:
            loop_stopping = True

        elif not loop:
            loop_stopping = False

        self.name = name
        self.warn = warn
        self.coroutine = coroutine
        self.delay = delay
        self.loop_stopping = loop_stopping
        self._loop = loop

        self.timeout_value = timeout
        self.wait_value = wait
        self.block_value = block

        self._operating = False
        self._blocking = False
        self._timeout = False
        self._running = False
        self._paused = False
        self._stopping = False

        self._operation_process: threading.Thread | None = None
        self._timeout_process: threading.Thread | None = None
        self._stopping_process: threading.Thread | None = None

        self._start: dt.datetime | None = None
        self._end: dt.datetime | None = None

        self.operation = operation
        self.termination = termination
        self.args_collector = args_collector
        self.kwargs_collector = kwargs_collector
        self.stopping_collector = stopping_collector
        self.handler = handler

    def __getstate__(self) -> dict[str, Any]:
        """
        Gets the state of the object.

        :return: The state of the object.
        """

        data = self.__dict__.copy()

        data["_operation_process"] = None
        data["_timeout_process"] = None
        data["_stopping_process"] = None

        return data

    @property
    def blocking(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._blocking

    @property
    def loop(self) -> bool:
        """
        returns the value of the process being looped.

        :return: The value.
        """

        return self._loop

    @property
    def operating(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._operating

    @property
    def running(self) -> bool:
        """
        returns the value of the process running.

        :return: The value.
        """

        return self._running

    @property
    def paused(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._paused

    @property
    def timeout(self) -> bool:
        """
        returns the value of the process awaiting timeout.

        :return: The flag value.
        """

        return self._timeout

    @property
    def stopping(self) -> bool:
        """
        returns the value of the process being checked to stop.

        :return: The flag value.
        """

        return self._stopping

    @property
    def start(self) -> dt.datetime | None:
        """
        returns the value of the start time.

        :return: The start time value.
        """

        return self._start

    @property
    def end(self) -> dt.datetime | None:
        """
        returns the value of the end time.

        :return: The end time value.
        """

        if self.running and (not self.paused):
            self._end = dt.datetime.now()

        return self._end

    @property
    def time(self) -> ProcessTime | None:
        """
        returns the value of the start time.

        :return: The start time value.
        """

        if self._start is None:
            return None

        return ProcessTime(
            start=self._start,
            end=self.end or dt.datetime.now()
        )

    @property
    def is_async(self) -> bool:

        return self.operation and asyncio.iscoroutinefunction(self.operation)

    async def async_operate(self) -> None:
        """Calls the operation of the process."""

        args = (self.args_collector() if self.args_collector else ())
        kwargs = (self.kwargs_collector() if self.kwargs_collector else {})

        if self.is_async:
            await self.operation(*args, **kwargs)

        else:
            self.operation(*args, **kwargs)

    def operate(self) -> None:
        """Calls the operation of the process."""

        task = self.async_operate()

        if self.coroutine:
            asyncio.new_event_loop().create_task(task)

        else:
            asyncio.run(task)

    def continue_loop(self) -> bool:
        """Returns the value to continue the loop."""

        return (
            (not self.stopping_collector) or
            (not self.loop_stopping) or
            (not self.stopping_collector())
        )

    def stopping_loop(self) -> None:
        """Runs the process of stopping the operation."""

        while self.running:
            while (not self.loop_stopping) and self.stopping_collector:
                if self.paused:
                    break

                t = time.time()

                if self.stopping_collector and self.stopping_collector():
                    self.stop()

                    return

                if self.delay:
                    delay = time_seconds(self.delay)

                    time.sleep(max(delay - (time.time() - t), 0))

            while self.paused:
                time.sleep(self._SLEEP)

    async def async_operation_loop(self) -> None:
        """Runs the process of the operator."""

        if not self.loop:
            await self.async_operate()

        while self.running and self.continue_loop():
            while self.operating and self.continue_loop():
                if self.paused:
                    break

                t = time.time()

                if self.handler is None:
                    await self.async_operate()

                else:
                    with self.handler:
                        await self.async_operate()

                    if self.handler.caught and self.handler.exit:
                        self.stop()

                        break

                if self.delay:
                    delay = time_seconds(self.delay)

                    await asyncio.sleep(max(delay - (time.time() - t), 0))

            while self.paused:
                await asyncio.sleep(self._SLEEP)

        self.stop()

    def operation_loop(self) -> None:

        task = self.async_operation_loop()

        if self.coroutine:
            asyncio.new_event_loop().create_task(task)

        else:
            asyncio.run(task)

    def timeout_loop(self, duration: TimeDestination) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the timeout.
        """

        origin = False

        if isinstance(duration, dt.datetime):
            origin = True

        if isinstance(duration, (int, float)):
            duration = dt.timedelta(seconds=duration)

        if isinstance(duration, dt.timedelta):
            duration = dt.datetime.now() + duration

        last = dt.datetime.now()

        start = None

        paused = False

        while self.timeout and (duration > last):
            while self.paused:
                if not paused:
                    start = dt.datetime.now()

                    paused = True

                time.sleep(self._SLEEP)

            last = dt.datetime.now()

            if paused:
                if not origin:
                    duration += (last - start)

                paused = False

        if self.timeout:
            self.stop()

    def start_operation(self) -> None:
        """Starts the operation loop process."""

        if self.operating:
            if self.warn:
                warnings.warn(
                    f"Operation process"
                    f"{f' of operator {self.name}' if self.name else ''} "
                    f"is already running."
                )

            return

        self._operating = True
        self._running = True

        if self.blocking:
            self.operation_loop()

        else:
            self._operation_process = threading.Thread(
                target=self.operation_loop
            )

            self._operation_process.start()

    def start_waiting(self, wait: TimeDestination = None) -> None:
        """
        Runs a waiting for the process.

        :param wait: The duration of the waiting.
        """

        if wait is None:
            wait = self.wait_value

            if wait is None:
                raise ValueError(
                    "Waiting value"
                    f"{f' of operator {self.name}' if self.name else ''} "
                    "is not defined."
                )

        time.sleep(time_seconds(wait))

    def start_timeout(self, duration: TimeDestination = None) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the start_timeout.
        """

        if duration is None:
            duration = self.timeout_value

            if duration is None:
                raise ValueError(
                    "Timeout value"
                    f"{f' of operator {self.name}' if self.name else ''} "
                    "is not defined."
                )

        if self.timeout:
            if self.warn:
                warnings.warn(
                    f"Timeout process"
                    f"{f' of operator {self.name}' if self.name else ''} "
                    f"is already running."
                )

            return

        self._timeout = True

        self._timeout_process = threading.Thread(
            target=lambda: self.timeout_loop(duration=duration)
        )

        self._timeout_process.start()

    def start_stopping(self) -> None:
        """Runs a timeout for the process."""

        if self.timeout:
            if self.warn:
                warnings.warn(
                    f"Stopping process"
                    f"{f' or operator {self.name}' if self.name else ''} "
                    f"is already running."
                )

            return

        self._stopping = True

        self._stopping_process = threading.Thread(
            target=lambda: self.stopping_loop()
        )

        self._stopping_process.start()

    def run(
            self,
            loop: bool = None,
            loop_stopping: bool = None,
            block: bool = None,
            wait: TimeDestination = None,
            timeout: TimeDestination = None
    ) -> None:
        """
        Runs the process of the operator object.

        :param loop: The value to run a loop.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param loop_stopping: The value to evaluate stopping during a loop.
        :param timeout: The valur to add a start_timeout to the process.
        """

        if block is None:
            block = self.block_value

        if wait is None:
            wait = self.wait_value

        if timeout is None:
            timeout = self.timeout_value

        if loop is not None:
            self._loop = loop

        else:
            loop = self.loop

        if loop_stopping is None and loop:
            loop_stopping = True

        elif not loop:
            loop_stopping = False

        self.loop_stopping = loop_stopping

        self._running = True
        self._paused = False

        self._blocking = block

        self._start = dt.datetime.now()

        if timeout:
            self.start_timeout(timeout)

        if wait:
            self.start_waiting(wait)

        if (not loop_stopping or not loop) and (self.stopping_collector is not None):
            self.start_stopping()

        if self.operation is not None:
            self.start_operation()

    def stop_operation(self) -> None:
        """Stops the operation loop process."""

        if self.operating:
            self._operating = False

        if self.running:
            self._running = False

        if (
            isinstance(self._operation_process, threading.Thread) and
            self._operation_process.is_alive()
        ):
            self._operation_process = None

    def stop_timeout(self) -> None:
        """Stops the timeout process."""

        if self.timeout:
            self._timeout = False

        if (
            isinstance(self._timeout_process, threading.Thread) and
            self._timeout_process.is_alive()
        ):
            self._timeout_process = None

    def stop_stopping(self) -> None:
        """Stops the stopping process."""

        if self.stopping:
            self._stopping = False

        if (
            isinstance(self._stopping_process, threading.Thread) and
            self._stopping_process.is_alive()
        ):
            self._stopping_process = None

    def pause(self) -> None:
        """Stops the screening process."""

        self._paused = True

    def unpause(self) -> None:
        """Stops the screening process."""

        self._paused = False

    def stop(self) -> None:
        """Stops the screening process."""

        self._running = False
        self._blocking = False

        self.unpause()
        self.stop_operation()
        self.stop_timeout()

        if self.termination is not None:
            self.termination()
