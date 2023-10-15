# handler.py

import warnings
from typing import (
    Optional, Any, Callable, Type, Iterable
)

from represent import represent

__all__ = [
    "Handler"
]

@represent
class Handler:
    """A class to handle operations."""

    try:
        from typing import Self

    except ImportError:
        Self = Any
    # end try

    def __init__(
            self,
            success_callback: Optional[Callable[[], Any]] = None,
            exception_callback: Optional[Callable[[], Any]] = None,
            cleanup_callback: Optional[Callable[[], Any]] = None,
            exception_handler: Optional[Callable[[Exception], Any]] = None,
            exceptions: Optional[Iterable[Type[Exception]]] = None,
            warn: Optional[bool] = True,
            catch: Optional[bool] = True,
            silence: Optional[bool] = False
    ) -> None:
        """
        Handles the communication between the server and client.

        :param success_callback: The callback to run for success.
        :param exception_handler: The exception handler.
        :param exception_callback: The callback to run for exception.
        :param cleanup_callback: The callback to run on finish.
        :param exceptions: The exceptions to catch.
        :param catch: The value to not raise an exception.
        :param silence: The value to silence the output.
        :param warn: The value to raise a warning instead of printing the message.

        :return: Any returned value.
        """

        self.success_callback = success_callback
        self.exception_callback = exception_callback
        self.cleanup_callback = cleanup_callback
        self.exception_handler = exception_handler

        self.exceptions = exceptions or ()

        self.warn = warn
        self.catch = catch
        self.silence = silence
    # end __init__

    def __enter__(self) -> Self:
        """
        Enters the generator.

        :return: The generator object.
        """

        if self.success_callback is not None:
            self.success_callback()
        # end if

        return self
    # end __enter__

    def __exit__(self, base: Type[Exception], exception: Exception, traceback) -> bool:
        """
        Exits the generator with exception.

        :param base: The base type of the exception.
        :param exception: The exception object.
        :param traceback: The traceback object.
        """

        caught = False

        if isinstance(exception, tuple(self.exceptions) or Exception):
            caught = self.catch and True

            if self.exception_callback is not None:
                self.exception_callback()
            # end if

            if self.exception_handler is None:
                if not self.silence:
                    message = f"{base.__name__}: {str(exception)}"

                    if self.warn:
                        warnings.warn(message)

                    else:
                        print(message)
                    # end if
                # end if

            else:
                self.exception_handler(exception)
            # end if
        # end if

        if self.cleanup_callback is not None:
            self.cleanup_callback()
        # end if

        return caught
    # end try
# end Handler