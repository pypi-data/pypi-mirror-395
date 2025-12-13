from __future__ import annotations

from typing import Any, Optional, Union

from .exec import CodexExec
from .thread import Thread
from .types import CodexOptions, ThreadOptions


class Codex:
    """Main entry-point for interacting with the Codex agent."""

    def __init__(self, options: Union[CodexOptions, dict[str, Any], None] = None) -> None:
        self._options = CodexOptions.model_validate(options or {})
        self._exec = CodexExec(self._options.codex_path_override, self._options.env)

    def start_thread(self, options: Union[ThreadOptions, dict[str, Any], None] = None) -> Thread:
        """Start a new conversation (thread) with an agent."""
        thread_options = ThreadOptions.model_validate(options or {})
        return Thread(self._exec, self._options, thread_options, thread_id=None)

    def resume_thread(
        self,
        thread_id: str,
        options: Union[ThreadOptions, dict[str, Any], None] = None,
    ) -> Thread:
        """Resume a previously started thread by id."""
        thread_options = ThreadOptions.model_validate(options or {})
        return Thread(self._exec, self._options, thread_options, thread_id=thread_id)

    # Aliases for TypeScript parity
    def startThread(self, options: Union[ThreadOptions, dict[str, Any], None] = None) -> Thread:
        return self.start_thread(options)

    def resumeThread(
        self,
        thread_id: str,
        options: Union[ThreadOptions, dict[str, Any], None] = None,
    ) -> Thread:
        return self.resume_thread(thread_id, options)
