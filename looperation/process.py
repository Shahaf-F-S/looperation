# process.py

import datetime as dt
from typing import ClassVar, Any, Self

from dataclasses import dataclass

try:
    import pandas as pd

except ImportError:
    pd = None

try:
    import numpy as np

except ImportError:
    np = None

__all__ = [
    "ProcessTime",
    "to_datetime"
]

def to_datetime(index: Any, adjust: bool = True) -> dt.datetime:
    """
    Converts the index into a datetime object.

    :param index: The value to convert.
    :param adjust: The value to adjust the process for errors.

    :return: The datetime object.
    """

    try:
        if isinstance(index, str):
            index = dt.datetime.fromisoformat(index)

        elif isinstance(index, (int, float)):
            index = dt.datetime.fromtimestamp(index)

        if (pd is not None) and isinstance(index, pd.Timestamp):
            index = index.to_pydatetime()

        if (np is not None) and isinstance(index, np.datetime64):
            index = index.astype(dt.datetime)

    except (TypeError, ValueError) as e:
        if adjust:
            pass

        else:
            raise e

    return index

@dataclass(slots=True, frozen=True)
class ProcessTime:
    """A class to contain the info of a call to the results."""

    start: dt.datetime
    end: dt.datetime

    START: ClassVar[str] = "start"
    END: ClassVar[str] = "end"

    @property
    def time(self) -> dt.timedelta:
        """
        Returns the time duration of the call.

        :return: The call time.
        """

        return self.end - self.start

    @classmethod
    def load(cls, data: dict[str, float]) -> Self:
        """
        Creates an instance of the class for the data.

        :param data: The data to load into an object.

        :return: The new instance with the data.
        """

        return cls(
            start=to_datetime(data[cls.START]),
            end=to_datetime(data[cls.END])
        )

    def json(self) -> dict[str, float]:
        """
        Returns a json object to represent the data of the object.

        :return: The data of the object.
        """

        return {
            self.START: self.start.timestamp(),
            self.END: self.end.timestamp()
        }
