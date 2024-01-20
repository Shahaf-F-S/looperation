# operation.py

from typing import Generic, Any, TypeVar

from dataclasses import dataclass, field

from looperation.process import ProcessTime

__all__ = [
    "Inputs",
    "Outputs",
    "Operation"
]

InputsData = dict[str, tuple | dict[str, Any]]

@dataclass(slots=True, frozen=True)
class Inputs:
    """A class to represent an arbitrage event."""

    args: tuple = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)

_O = TypeVar("_O")

OutputsData = dict[str, _O]

@dataclass(slots=True, frozen=True)
class Outputs(Generic[_O]):
    """A class to represent an arbitrage event."""

    returns: _O = None

TimeData = dict[str, float]
OperationData = dict[str, InputsData | OutputsData | TimeData]

@dataclass(slots=True, frozen=True)
class Operation(Generic[_O]):
    """A class to represent an arbitrage event."""

    time: ProcessTime
    inputs: Inputs
    outputs: Outputs[_O]
