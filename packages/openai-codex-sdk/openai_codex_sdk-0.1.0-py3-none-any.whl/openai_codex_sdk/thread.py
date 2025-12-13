from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncIterator, List, Optional, Union

from pydantic import BaseModel, ConfigDict

from .exec import CodexExec, CodexExecArgs
from .output_schema_file import create_output_schema_file
from .parsing import parse_thread_event_line
from .types import (
    CodexOptions,
    Input,
    ThreadEvent,
    ThreadItem,
    ThreadOptions,
    TurnOptions,
    Usage,
)
from .utils import normalize_input
from .errors import ThreadRunError


class Turn(BaseModel):
    """Completed turn returned by `Thread.run()`."""

    model_config = ConfigDict(extra="forbid")

    items: List[ThreadItem]
    final_response: str
    usage: Optional[Usage] = None


@dataclass(frozen=True)
class StreamedTurn:
    """Result returned by `Thread.run_streamed()`."""

    events: AsyncIterator[ThreadEvent]


class Thread:
    """Represents a thread of conversation with the agent."""

    def __init__(
        self,
        exec_: CodexExec,
        codex_options: CodexOptions,
        thread_options: ThreadOptions,
        thread_id: Optional[str] = None,
    ) -> None:
        self._exec = exec_
        self._codex_options = codex_options
        self._thread_options = thread_options
        self._id: Optional[str] = thread_id

    @property
    def id(self) -> Optional[str]:
        """Thread identifier (populated after the first `thread.started` event)."""
        return self._id

    async def run_streamed(
        self,
        input_: Input,
        turn_options: Union[TurnOptions, dict[str, Any], None] = None,
    ) -> StreamedTurn:
        options = TurnOptions.model_validate(turn_options or {})
        return StreamedTurn(events=self._run_streamed_internal(input_, options))

    async def run(
        self,
        input_: Input,
        turn_options: Union[TurnOptions, dict[str, Any], None] = None,
    ) -> Turn:
        options = TurnOptions.model_validate(turn_options or {})
        generator = self._run_streamed_internal(input_, options)

        items: List[ThreadItem] = []
        final_response = ""
        usage: Optional[Usage] = None
        failure_message: Optional[str] = None

        async for event in generator:
            if event.type == "item.completed":
                item = event.item
                if item.type == "agent_message":
                    # Set final response to the last agent message in the turn.
                    final_response = item.text
                items.append(item)
            elif event.type == "turn.completed":
                usage = event.usage
            elif event.type == "turn.failed":
                failure_message = event.error.message
                break

        if failure_message is not None:
            raise ThreadRunError(failure_message)

        return Turn(items=items, final_response=final_response, usage=usage)

    # Aliases for TypeScript parity
    async def runStreamed(
        self,
        input_: Input,
        turn_options: Union[TurnOptions, dict[str, Any], None] = None,
    ) -> StreamedTurn:
        return await self.run_streamed(input_, turn_options)

    async def _run_streamed_internal(
        self,
        input_: Input,
        turn_options: TurnOptions,
    ) -> AsyncIterator[ThreadEvent]:
        schema_file = await create_output_schema_file(turn_options.output_schema)
        try:
            prompt, images = normalize_input(input_)

            opts = self._thread_options
            args = CodexExecArgs(
                input=prompt,
                base_url=self._codex_options.base_url,
                api_key=self._codex_options.api_key,
                thread_id=self._id,
                images=images,
                model=opts.model,
                sandbox_mode=opts.sandbox_mode,
                working_directory=opts.working_directory,
                additional_directories=opts.additional_directories,
                skip_git_repo_check=opts.skip_git_repo_check,
                output_schema_file=schema_file.schema_path,
                model_reasoning_effort=opts.model_reasoning_effort,
                signal=turn_options.signal,
                network_access_enabled=opts.network_access_enabled,
                web_search_enabled=opts.web_search_enabled,
                approval_policy=opts.approval_policy,
            )

            async for line in self._exec.run(args):
                event = parse_thread_event_line(line)
                if event.type == "thread.started":
                    self._id = event.thread_id
                yield event
        finally:
            await schema_file.cleanup()
