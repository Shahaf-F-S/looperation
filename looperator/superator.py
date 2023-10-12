# superator.py

import datetime as dt
from typing import Union, Optional, Iterable

from looperator.operator import Operator
from looperator.handler import Handler

__all__ = [
    "Superator"
]

class Superator(Operator):
    """A super operator to control multiple operators."""

    def __init__(
            self,
            operators: Iterable[Operator],
            handler: Optional[Handler] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            block: Optional[bool] = False,
            wait: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
            timeout: Optional[Union[float, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Defines the attributes of the operators controller.

        :param operators: The operators to control.
        :param handler: The handler object to handle the operation.
        :param delay: The delay for the process.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a start_timeout to the process.
        """

        self.operators = list(operators)

        super().__init__(
            operation=lambda: (),
            handler=handler, delay=delay,
            block=block, wait=wait, timeout=timeout
        )
    # end __init__

    def operate(self) -> None:
        """Runs the process of the price screening."""

        for operator in self.operators:
            if all((operator.running, operator.operating, operator.blocking)):
                operator.operate()
            # end if
        # end if
    # end operate

    def start_operations(self) -> None:
        """Starts the screening process."""

        for operator in self.operators:
            if not any((operator.running, operator.operating, operator.blocking)):
                operator.start_operation()
            # end if
        # end if
    # end start_operations

    def start_timeouts(self, duration: Optional[Union[float, dt.timedelta, dt.datetime]] = None) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        if duration is None:
            duration = self.timeout_value

            if duration is None:
                raise ValueError("Timeout value is not defined.")
            # end if
        # end if

        for operator in self.operators:
            if not any((operator.running, operator.operating, operator.blocking)):
                operator.start_timeout(duration)
            # end if
        # end if
    # end start_timeouts

    def run(
            self,
            block: Optional[bool] = None,
            wait: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
            timeout: Optional[Union[float, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a start_timeout to the process.
        """

        super().run(block=block, wait=wait, timeout=timeout)

        for operator in self.operators:
            if not any((operator.running, operator.operating)):
                operator.run()
            # end if
        # end if
    # end start_timeout

    def stop_operation(self) -> None:
        """Stops the screening process."""

        for operator in self.operators:
            operator.stop_operation()
        # end if

        super().stop_operation()
    # end stop_operation

    def stop_timeout(self) -> None:
        """Stops the screening process."""

        for operator in self.operators:
            operator.stop_timeout()
        # end if

        super().stop_timeout()
    # end stop_timeout

    def pause(self) -> None:
        """Stops the screening process."""

        for operator in self.operators:
            operator.pause()
        # end for

        super().pause()
    # end pause

    def unpause(self) -> None:
        """Stops the screening process."""

        for operator in self.operators:
            operator.unpause()
        # end for

        super().unpause()
    # end unpause

    def stop(self) -> None:
        """Stops the screening process."""

        for operator in self.operators:
            operator.stop()
        # end if

        super().stop()
    # end stop
# end Superator