# process.py

import datetime as dt

from attrs import define

from represent import represent

__all__ = [
    "ProcessTime"
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