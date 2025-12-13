from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import asyncio


class AbortError(Exception):
    """Raised when a turn is cancelled via an AbortSignal."""


@dataclass(frozen=True)
class AbortReason:
    message: str


class AbortSignal:
    """Cancellation primitive loosely analogous to the web AbortSignal.

    - `aborted` indicates cancellation.
    - `reason` is an optional value set by the controller.
    - `wait()` can be awaited to react to cancellation in async code.
    """

    __slots__ = ("_event", "_reason")

    def __init__(self) -> None:
        self._event = asyncio.Event()
        self._reason: Optional[Any] = None

    @property
    def aborted(self) -> bool:
        return self._event.is_set()

    @property
    def reason(self) -> Optional[Any]:
        return self._reason

    async def wait(self) -> None:
        await self._event.wait()

    def _abort(self, reason: Any = None) -> None:
        # Idempotent.
        if not self._event.is_set():
            self._reason = reason
            self._event.set()

    def throw_if_aborted(self) -> None:
        if self.aborted:
            raise AbortError(_format_abort_reason(self._reason))


class AbortController:
    """Creates an AbortSignal and can abort it."""

    __slots__ = ("signal",)

    def __init__(self) -> None:
        self.signal = AbortSignal()

    def abort(self, reason: Any = None) -> None:
        self.signal._abort(reason)


def _format_abort_reason(reason: Any) -> str:
    if reason is None:
        return "Operation aborted"
    if isinstance(reason, str):
        return reason
    if isinstance(reason, AbortReason):
        return reason.message
    if isinstance(reason, BaseException):
        return str(reason)
    return str(reason)
