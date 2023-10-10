# operation.py

from typing import Optional, Tuple, Generic, Any, Dict, TypeVar

from attrs import define, field

from represent import represent

from looperator.process import ProcessTime

__all__ = [
    "Inputs",
    "Outputs",
    "Operation"
]

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