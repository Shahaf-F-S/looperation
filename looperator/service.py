# service.py

import time
import datetime as dt

from looperator.operator import Operator

__all__ = [
    "ServiceInterface"
]

Time = float | dt.timedelta, dt.datetime

class ServiceInterface:
    """A service interface for server client communication."""

    SLEEP = 0.0
    DELAY = 0.0001

    def __init__(self) -> None:
        """Defines the attribute of the server service."""

        self._paused = False

        self.refresh_value: float | dt.timedelta | None = None

        self._refresh_operator = Operator(
            operation=self._refresh,
            delay=self.DELAY
        )
        self._block_operator = Operator(
            operation=self.block, block=True,
            delay=self.DELAY
        )
        self._update_operator = Operator(
            operation=self.update,
            delay=self.DELAY
        )
        self._timeout_operator = Operator(
            termination=self.stop,
            delay=self.DELAY
        )

        self._operators = [
            self._refresh_operator,
            self._block_operator,
            self._update_operator,
            self._timeout_operator
        ]

        self._start_time = time.time()
        self._current_time = time.time()

    @property
    def paused(self) -> bool:
        """
        returns the value of the updating process run.

        :return: The value.
        """

        return self._paused

    @property
    def updating(self) -> bool:
        """
        Returns the value of the updating process.

        :return: The updating value.
        """

        return self._update_operator.operating

    @property
    def refreshing(self) -> bool:
        """
        Returns the value of te execution being refreshing by the service loop.

        :return: The refreshing value.
        """

        return self._refresh_operator.operating

    @property
    def blocking(self) -> bool:
        """
        Returns the value of te execution being refreshing by the service loop.

        :return: The refreshing value.
        """

        return self._block_operator.operating

    @property
    def timeout(self) -> bool:
        """
        Returns the value of te execution being a start_timeout loop.

        :return: The start_timeout value.
        """

        return self._timeout_operator.operating

    def update(self) -> None:
        """Updates the options according to the screeners."""

    def refresh(self) -> None:
        """Updates the options according to the screeners."""

    def block(self) -> None:
        """Blocks the run."""

        time.sleep(self.SLEEP)

    def start_blocking(self) -> None:
        """Starts the blocking process."""

        self._block_operator.start_operation()

    def _refresh(self) -> None:
        """Updates the options according to the screeners."""

        refresh = self.refresh_value

        if refresh:
            self._current_time = time.time()

            if isinstance(refresh, dt.timedelta):
                refresh = refresh.total_seconds()

            if (self._current_time - self._start_time) >= refresh:
                self._start_time = self._current_time

                self.refresh()

    def start_refreshing(self, refresh: float | dt.timedelta) -> None:
        """
        Starts the refreshing process.

        :param refresh: The value to refresh the service.
        """

        self.refresh_value = refresh

        self._refresh_operator.start_operation()

    def start_updating(self) -> None:
        """Starts the updating process."""

        self._update_operator.start_operation()

    def start_timeout(self, duration: Time = None) -> None:
        """
        Runs a start_timeout for the process.

        :param duration: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        self._timeout_operator.start_timeout(duration)

    def start_waiting(self, wait: Time = None) -> None:
        """
        Runs a waiting for the process.

        :param wait: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        self._timeout_operator.start_waiting(wait)

    def run(
            self,
            update: bool = False,
            block: bool = False,
            refresh: float | dt.timedelta = None,
            wait: Time = None,
            timeout: Time = None,
    ) -> None:
        """
        Runs the api service.

        :param update: The value to update the service.
        :param block: The value to block the execution and wain for the service.
        :param refresh: The value to refresh the service.
        :param wait: The waiting time.
        :param timeout: The start_timeout for the process.
        """

        if update:
            self.start_updating()

        if refresh:
            self.start_refreshing(refresh)

        if timeout:
            self.start_timeout(timeout)

        if wait:
            self.start_waiting(wait)

        if block:
            self.start_blocking()

    def pause(self) -> None:
        """Stops the screening process."""

        self._paused = True

        for operator in self._operators:
            operator.pause()

    def unpause(self) -> None:
        """Stops the screening process."""

        self._paused = False

        for operator in self._operators:
            operator.unpause()

    def stop_refreshing(self) -> None:
        """Stops the refreshing process."""

        self._refresh_operator.stop_operation()

    def stop_updating(self) -> None:
        """Stops the updating process."""

        self._update_operator.stop_operation()

    def stop_timeout(self) -> None:
        """Stops the start_timeout process."""

        self._timeout_operator.stop_timeout()

    def stop_blocking(self) -> None:
        """Stops the start_timeout process."""

        self._block_operator.stop_operation()

    def stop(self) -> None:
        """Stops the service."""

        self.stop_timeout()
        self.stop_updating()
        self.stop_refreshing()
        self.stop_blocking()

        for operator in self._operators:
            operator.stop_operation()
