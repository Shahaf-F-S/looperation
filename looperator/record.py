# record.py

import datetime as dt
from typing import (
    Callable, Generic, Any, Protocol, Iterable, TypeVar
)

from looperator.operator import Operator
from looperator.operation import Operation, Inputs, Outputs
from looperator.process import ProcessTime

__all__ = [
    "RecordOperator",
    "QueueOperator",
    "ListOperator",
    "OperationQueue",
    "BaseQueue",
    "QueueProtocol"
]

_O = TypeVar("_O")

class RecordOperator(Operator[_O]):
    """A class to handle arbitrage option values."""

    def __init__(
            self,
            operation: Callable[..., _O],
            args_collector: Callable[[], Iterable[Any]] = None,
            kwargs_collector: Callable[[], dict[str, Any]] = None,
            delay: float | dt.timedelta = None
    ) -> None:
        """
        Defines the attributes of the handler.

        :param operation: The callback to call.
        :param kwargs_collector: The callback to collect args.
        :param kwargs_collector: The callback to collect kwargs.
        :param delay: The delay for the process.
        """

        super().__init__(
            operation=operation,
            args_collector=args_collector,
            kwargs_collector=kwargs_collector,
            delay=delay
        )
    # end __init__

    def produce(self) -> Operation[_O]:
        """Runs the process of the price screening."""

        start = dt.datetime.now()

        args = self.args_collector() if self.args_collector else ()
        kwargs = self.kwargs_collector() if self.kwargs_collector else {}

        returns = self.operation(*args, **kwargs)

        end = dt.datetime.now()

        return Operation[_O](
            time=ProcessTime(start=start, end=end),
            inputs=Inputs(args=args, kwargs=kwargs),
            outputs=Outputs[_O](returns=returns)
        )
    # end produce

    def operate(self) -> None:
        """Runs the process of the price screening."""

        self.produce()
    # end handle
# end RecordOperator

class ListOperator(RecordOperator[_O]):
    """A class to handle arbitrage option values."""

    def __init__(
            self,
            operation: Callable[..., _O],
            args_collector: Callable[[], Iterable[Any]] = None,
            kwargs_collector: Callable[[], dict[str, Any]] = None,
            delay: float | dt.timedelta = None,
            record: list[Operation[_O]] = None
    ) -> None:
        """
        Defines the attributes of the handler.

        :param record: The event queue.
        :param operation: The callback to call.
        :param kwargs_collector: The callback to collect args.
        :param kwargs_collector: The callback to collect kwargs.
        :param delay: The delay for the process.
        """

        super().__init__(
            operation=operation,
            args_collector=args_collector,
            kwargs_collector=kwargs_collector,
            delay=delay
        )

        if record is None:
            record = []
        # end if

        self.record = record
    # end __init__

    def operate(self) -> None:
        """Runs the process of the price screening."""

        self.record.append(self.produce())
    # end handle
# end ListOperator

class QueueProtocol(Protocol):
    """A class to represent an event queue protocol."""

    def insert(self, event: Any) -> None:
        """
        Pushes the event into the queue.

        :param event: The event to push.
        """
    # end push
# end QueueProtocol

_V = TypeVar("_V")

class BaseQueue(Generic[_V]):
    """A class to represent an event queue protocol."""

    def __init__(self, values: Iterable[_V] = None) -> None:
        """
        Defines the attributes of the queue.

        :param values: The values to insert.
        """

        self.values: list[_V] = []

        self.extend(values or ())
    # end __init__

    def __len__(self) -> int:
        """
        Returns the length of the queue.

        :return: The amount of values in the queue.
        """

        return len(self.values)
    # end __len__

    def __bool__(self) -> bool:
        """
        Checks if there are values in the queue.

        :return: The existence of values in the queue.
        """

        return bool(self.values)
    # end __bool__

    def insert(self, value: _V) -> None:
        """
        Pushes the value into the queue.

        :param value: The event to push.
        """

        self.values.append(value)
    # end push

    def extend(self, values: Iterable[_V]) -> None:
        """
        Pushes the values into the queue.

        :param values: The values to push.
        """

        self.values.extend(values)
    # end insert_all

    def remove(self) -> _V:
        """
        Removes the first value from the queue.

        :return: The removed event.
        """

        try:
            return self.values.pop(0)

        except IndexError:
            raise ValueError("Events queue is empty.")
        # end try
    # end remove

    def remove_all(self) -> list[_V]:
        """
        Removes all values first value from the queue.

        :return: The removed values.
        """

        events = list(self.values)

        self.empty()

        return events
    # end remove

    def empty(self) -> None:
        """Empties the queue."""

        self.values.clear()
    # end empty

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.

        :return: The validation flag.
        """

        return len(self.values) > 0
    # end is_empty

    def get(self) -> _V:
        """
        Gets the event first value from the queue.

        :return: The first value.
        """

        try:
            return self.values[0]

        except IndexError:
            raise ValueError("Events queue is empty.")
        # end try
    # end get
# end BaseQueue

class OperationQueue(BaseQueue[Operation[_O]]):
    """A class to represent an event queue protocol."""
# end OperationQueue

class QueueOperator(RecordOperator[_O]):
    """A class to handle arbitrage option values."""

    def __init__(
            self,
            operation: Callable[..., _O],
            args_collector: Callable[[], Iterable[Any]] = None,
            kwargs_collector: Callable[[], dict[str, Any]] = None,
            delay: float | dt.timedelta = None,
            queue: QueueProtocol = None
    ) -> None:
        """
        Defines the attributes of the handler.

        :param queue: The event queue.
        :param operation: The callback to call.
        :param kwargs_collector: The callback to collect args.
        :param kwargs_collector: The callback to collect kwargs.
        :param delay: The delay for the process.
        """

        super().__init__(
            operation=operation,
            args_collector=args_collector,
            kwargs_collector=kwargs_collector,
            delay=delay
        )

        if queue is None:
            queue = OperationQueue()
        # end if

        self.queue = queue
    # end __init__

    def operate(self) -> None:
        """Runs the process of the price screening."""

        self.queue.insert(self.produce())
    # end handle
# end QueueOperator