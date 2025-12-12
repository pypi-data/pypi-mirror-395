from __future__ import annotations

from typing import TYPE_CHECKING, Literal, NoReturn, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable


class TokenError(Exception):
    """Base class for all cancellation-related errors. Raised when a
    cancellation event affects the current operation. Serves as the common
    superclass for all token error types.
    """


class TokenCancelledError(TokenError):
    """Raised when an operation is cancelled via a cancellation token. This
    exception indicates that the token was explicitly cancelled.
    """


class TokenTimeoutError(TokenError):
    """Raised when a token is cancelled due to a timeout. This exception
    indicates that the token's cancellation was triggered by an internal
    timeout mechanism (for example via :func:`brikk.cancel.with_timeout`).
    """


class Token(Protocol):
    """A cooperative cancellation token interface. Represents a handle that can
    be checked or awaited to respond to cancellation events triggered elsewhere
    """

    def register(self, fn: Callable[[TokenError], None]) -> None:
        """Register a callback to be invoked when the token is cancelled.

        :param fn: A function to call when cancellation occurs. Receives a
            `TokenError`.
        """
        ...

    def is_cancelled(self) -> bool:
        """Check whether the token has been cancelled.

        :returns: True if the token has been cancelled, False otherwise.
        """
        ...

    def get_error(self) -> TokenError | None:
        """Get the cancellation error if the token has been cancelled.

        :returns: The `TokenError` if cancelled, or None.
        """
        ...

    def raise_if_cancelled(self):
        """Raise the cancellation error if the token has been cancelled.

        :raises TokenError: If the token is cancelled.
        """
        ...

    def wait(self, timeout: float | None) -> TokenError | None:
        """Block until the token is cancelled or the timeout expires.

        :param timeout: Maximum time to wait in seconds, or None to wait
            indefinitely.
        :returns: The `TokenError` if cancelled, or None if the timeout expires.
        """
        ...


class CancelledToken(Token, Protocol):
    """A token that is already cancelled. This specialization of `Token`
    ensures that cancellation has occurred and provides non-optional return
    types

    Example:

    .. code-block:: python
        :linenos:

        if is_token_cancelled(token):
            reveal_type(token) # CancelledToken
    """

    def is_cancelled(self) -> Literal[True]:
        """Always returns True, since the token is cancelled.

        :returns: True
        """
        ...

    def get_error(self) -> TokenError:
        """Get the cancellation error.

        :returns: The `TokenError` associated with this cancelled token.
        """
        ...

    def raise_if_cancelled(self) -> NoReturn:
        """Always raises the cancellation error.

        :raises TokenError: The associated cancellation error.
        """
        ...

    def wait(self, timeout: float | None) -> TokenError:
        """Immediately returns the cancellation error.

        :param timeout: Ignored. Present for interface compatibility.
        :returns: The `TokenError` associated with this cancelled token.
        """
        ...
