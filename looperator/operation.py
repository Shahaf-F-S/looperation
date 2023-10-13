# operation.py

from typing import (
    Optional, Tuple, Generic, Any,
    Dict, TypeVar, ClassVar, Union
)

from attrs import define, field

from represent import represent

from looperator.process import ProcessTime

__all__ = [
    "Inputs",
    "Outputs",
    "Operation"
]

InputsData = Dict[str, Union[Tuple, Dict[str, Any]]]

@represent
@define(repr=False, frozen=True)
class Inputs:
    """A class to represent an arbitrage event."""

    args: Optional[Tuple] = field(factory=tuple)
    kwargs: Optional[Dict[str, Any]] = field(factory=dict)

    ARGS: ClassVar[str] = "args"
    KWARGS: ClassVar[str] = "kwargs"

    try:
        from typing import Self

    except ImportError:
        Self = Any
    # end try

    @classmethod
    def load(cls, data: InputsData) -> Self:
        """
        Creates an instance of the class for the data.

        :param data: The data to load into an object.

        :return: The new instance with the data.
        """

        return cls(
            args=data[cls.ARGS],
            kwargs=data[cls.KWARGS]
        )
    # end load

    def json(self) -> InputsData:
        """
        Returns a json object to represent the data of the object.

        :return: The data of the object.
        """

        return {
            self.ARGS: self.args,
            self.KWARGS: self.kwargs
        }
    # end json
# end BaseCallbackEvent

_O = TypeVar("_O")

OutputsData = Dict[str, _O]

@represent
@define(repr=False, frozen=True)
class Outputs(Generic[_O]):
    """A class to represent an arbitrage event."""

    returns: Optional[_O] = None

    RETURNS: ClassVar[str] = "returns"

    try:
        from typing import Self

    except ImportError:
        Self = Any
    # end try

    @classmethod
    def load(cls, data: OutputsData) -> Self:
        """
        Creates an instance of the class for the data.

        :param data: The data to load into an object.

        :return: The new instance with the data.
        """

        return cls(returns=data[cls.RETURNS])
    # end load

    def json(self) -> OutputsData:
        """
        Returns a json object to represent the data of the object.

        :return: The data of the object.
        """

        return {self.RETURNS: self.returns}
    # end json
# end Outputs

TimeData = Dict[str, float]
OperationData = Dict[str, Union[InputsData, OutputsData, TimeData]]

@represent
@define(repr=False, frozen=True)
class Operation(Generic[_O]):
    """A class to represent an arbitrage event."""

    time: ProcessTime
    inputs: Inputs
    outputs: Outputs[_O]

    TIME: ClassVar[str] = "time"
    INPUTS: ClassVar[str] = "inputs"
    OUTPUTS: ClassVar[str] = "outputs"

    try:
        from typing import Self

    except ImportError:
        Self = Any
    # end try

    @classmethod
    def load(cls, data: OperationData) -> Self:
        """
        Creates an instance of the class for the data.

        :param data: The data to load into an object.

        :return: The new instance with the data.
        """

        return cls(
            time=ProcessTime.load(data[cls.TIME]),
            inputs=Inputs.load(data[cls.INPUTS]),
            outputs=Outputs.load(data[cls.OUTPUTS])
        )
    # end load

    def json(self) -> OperationData:
        """
        Returns a json object to represent the data of the object.

        :return: The data of the object.
        """

        return {
            self.TIME: self.time.json(),
            self.INPUTS: self.inputs.json(),
            self.OUTPUTS: self.outputs.json()
        }
    # end json
# end Operation