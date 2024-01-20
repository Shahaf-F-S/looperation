# superator.py

import datetime as dt
from typing import Iterable, Callable, Any

from looperation.operator import Operator
from looperation.handler import Handler

__all__ = [
    "Superator"
]

TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

class Superator(Operator):
    """A super operator to control multiple operators."""

    def __init__(
            self,
            operators: Iterable[Operator],
            handler: Handler = None,
            stopping_collector: Callable[[], bool] = None,
            termination: Callable[[], Any] = None,
            delay: TimeDuration = None,
            block: bool = False,
            wait: TimeDestination = None,
            timeout: TimeDestination = None
    ) -> None:
        """
        Defines the attributes of the operators controller.

        :param operators: The operators to control.
        :param handler: The handler object to handle the operation.
        :param stopping_collector: The callback to collect a value to indicate to stop.
        :param termination: The termination callback.
        :param delay: The delay for the process.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a start_timeout to the process.
        """

        self.operators = list(operators)

        super().__init__(
            handler=handler,
            delay=delay,
            block=block,
            wait=wait,
            timeout=timeout,
            termination=termination,
            stopping_collector=stopping_collector
        )

    def operate(self) -> None:
        """Runs the process of the price screening."""

        for operator in self.operators:
            operator.operate()

    def start_operations(self) -> None:
        """Starts the screening process."""

        for operator in self.operators:
            operator.start_operation()

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

        for operator in self.operators:
            if not any((operator.running, operator.operating)):
                operator.run()

        super().run(
            block=block, wait=wait, timeout=timeout,
            loop=loop, loop_stopping=loop_stopping
        )

    def stop_operation(self) -> None:
        """Stops the screening process."""

        for operator in self.operators:
            operator.stop_operation()

        super().stop_operation()

    def stop_timeout(self) -> None:
        """Stops the screening process."""

        super().stop_timeout()

    def pause(self, operations: bool = True) -> None:
        """
        Pauses the screening process.

        :param operations: The value to pause all operations.
        """

        if operations:
            for operator in self.operators:
                operator.pause()

        super().pause()

    def unpause(self, operations: bool = True) -> None:
        """
        Unpauses the screening process.

        :param operations: The value to unpause all operations.
        """

        if operations:
            for operator in self.operators:
                operator.unpause()

        super().unpause()

    def stop(self, operations: bool = True) -> None:
        """
        Stops the screening process.

        :param operations: The value to stop all operations.
        """

        if operations:
            for operator in self.operators:
                operator.stop()

        super().stop()
