# handler.py
import warnings
from typing import Any, Callable, Iterable, Self
from represent import represent
__all__ = [
    "Handler"
]
@represent
class Handler:
    """A class to handle operations."""
    def __init__(
            self,
            success_callback: Callable[[], Any] = None,
            exception_callback: Callable[[], Any] = None,
            cleanup_callback: Callable[[], Any] = None,
            exception_handler: Callable[[Exception], Any] = None,
            exceptions: Iterable[type[Exception]] = None,
            warn: bool = True,
            catch: bool = True,
            silence: bool = False
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
    def __enter__(self) -> Self:
        """
        Enters the generator.
        :return: The generator object.
        """
        if self.success_callback is not None:
            self.success_callback()
        return self
    def __exit__(self, base: type[Exception], exception: Exception, traceback) -> bool:
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
            if self.exception_handler is None:
                if not self.silence:
                    message = f"{base.__name__}: {str(exception)}"
                    if self.warn:
                        warnings.warn(message)
                    else:
                        print(message)
            else:
                self.exception_handler(exception)
        if self.cleanup_callback is not None:
            self.cleanup_callback()
        return caught
