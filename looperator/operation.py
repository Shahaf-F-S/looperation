# operation.py

import datetime as dt
from typing import Optional, Tuple, Generic, Any, Dict, TypeVar

from attrs import define, field

from represent import represent

__all__ = [
    "ProcessTime",
    "Inputs",
    "Outputs",
    "Operation"
]

@represent
@define(repr=False, frozen=True)
class ProcessTime:
    """A class to contain the info of a call to the results."""

    start: dt.datetime
    end: dt.datetime

    @property
    def time(self) -> dt.timedelta:
        """
        Returns the time duration of the call.

        :return: The call time.
        """

        return self.end - self.start
    # end time
# end ProcessTime

@represent
@define(repr=False, frozen=True)
class Inputs:
    """A class to represent an arbitrage event."""

    args: Optional[Tuple] = field(factory=tuple)
    kwargs: Optional[Dict[str, Any]] = field(factory=dict)
# end BaseCallbackEvent

_O = TypeVar("_O")

@represent
@define(repr=False, frozen=True)
class Outputs(Generic[_O]):
    """A class to represent an arbitrage event."""

    returns: Optional[_O] = None
# end Outputs

@represent
@define(repr=False, frozen=True)
class Operation(Generic[_O]):
    """A class to represent an arbitrage event."""

    time: ProcessTime
    inputs: Inputs
    outputs: Outputs[_O]
# end Operation