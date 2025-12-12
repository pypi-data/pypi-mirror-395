from __future__ import annotations

import threading
from functools import partial
from typing import TYPE_CHECKING, TypeGuard

from brikk.cancel._types import (
    CancelledToken,
    Token,
    TokenCancelledError,
    TokenError,
    TokenTimeoutError,
)

if TYPE_CHECKING:
    from collections.abc import Callable


def default() -> Token:
    """Create a default, non-cancellable token. This token will never be
    cancelled and can be used as a placeholder when no cancellation logic is
    required.

    :returns: A default `Token` that is never cancelled.
    """
    return _DefaultToken()


def with_cancel(parent: Token) -> tuple[Token, Callable[[], None]]:
    """Create a new cancellable token linked to a parent token. The returned
    token can be cancelled independently, and will also be cancelled if the
    parent token is cancelled.

    :param parent: The parent `Token` to link cancellation from.
    :returns: A tuple containing, the new `Token` and a callable to cancel
        the token manually
    """

    token = _CancellableToken()
    parent.register(token.cancel)
    return token, partial(token.cancel, None)


def with_timeout(parent: Token, timeout: float) -> tuple[Token, Callable[[], None]]:
    """Create a new cancellable token with a timeout, linked to a parent token.
    The token will be cancelled if either: the parent token is cancelled or the
    specified timeout elapses.

    :param parent: The parent `Token` to link cancellation from.
    :param timeout: Timeout duration in seconds before automatic cancellation.
    :returns: A tuple containing, the new `Token` and a callable to cancel
        the token manually
    """

    token = _CancellableToken()
    timer = threading.Timer(timeout, partial(token.cancel, TokenTimeoutError()))

    def _cancel(error: TokenError | None):
        token.cancel(error)
        timer.cancel()

    parent.register(_cancel)
    timer.start()
    return token, partial(_cancel, None)


def is_token_cancelled(token: Token) -> TypeGuard[CancelledToken]:
    """Type guard to check if a token is cancelled. This function refines the
    type of the given token to `CancelledToken` for type checkers if the token
    is indeed cancelled.

    :param token: The token to check.
    :returns: True if the token is cancelled, False otherwise.
    """

    return token.is_cancelled()


class _DefaultToken:
    def register(self, fn: Callable[[TokenError], None]) -> None:
        pass

    def is_cancelled(self) -> bool:
        return False

    def get_error(self) -> TokenError | None:
        return None

    def raise_if_cancelled(self) -> None:
        pass

    def wait(self, timeout: float | None) -> TokenError | None:
        return None


class _CancellableToken:
    def __init__(self) -> None:
        self.__lock = threading.RLock()
        self.__signal = threading.Event()

        self.__callbacks: list[Callable[[TokenError], None]] = []
        self.__error: TokenError | None = None

    def cancel(self, error: TokenError | None = None) -> None:
        with self.__lock:
            if self.is_cancelled():
                return

            self.__error = error or TokenCancelledError()
            for callback in self.__callbacks:
                callback(self.__error)
            self.__signal.set()

    def register(self, fn: Callable[[TokenError], None]) -> None:
        with self.__lock:
            self.__callbacks.append(fn)

    def is_cancelled(self) -> bool:
        return self.__signal.is_set()

    def get_error(self) -> TokenError | None:
        return self.__error

    def raise_if_cancelled(self) -> None:
        if self.__signal.is_set() and self.__error is not None:
            raise self.__error

    def wait(self, timeout: float | None) -> TokenError | None:
        self.__signal.wait(timeout)
        return self.__error
