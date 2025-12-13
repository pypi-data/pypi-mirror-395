import asyncio
from pathlib import Path
from typing import Any, Callable, cast
from unittest import skip
import openai_codex_sdk.codex as cx
import openai_codex_sdk.types as types

codex = cx.Codex(options=types.CodexOptions(
    codexPathOverride=(Path.home() / ".bun" / "bin" / "codex").as_posix()
))

t = codex.start_thread(
    options=types.ThreadOptions(
        model="gpt-5.1-codex-mini",
        skipGitRepoCheck=True,
        networkAccessEnabled=True,
        approvalPolicy="never"
    )
)

async def arun(prompt: str, logger: Callable[[str], Any]):
    turn = await t.run_streamed(prompt)
    async for event in turn.events:
        if event.type == "item.completed":
            logger(f"Item completed: {event.item.text}")
        elif event.type == "turn.completed":
            logger(f"Turn completed: {event.usage.model_dump()}")
        elif event.type == "thread.started":
            thread_started_event = cast(types.ThreadStartedEvent, event)
            logger(f"Thread ID: {thread_started_event.thread_id}")
        elif event.type == "turn.completed":
            event = cast(types.TurnCompletedEvent, event)
            logger(f"Turn completed: {event.model_dump()}")
        elif event.type == "item.started":
            event = cast(types.ItemStartedEvent, event)
            logger(f"Item started: {event.item.model_dump()}")
        elif event.type == "item.updated":
            event = cast(types.ItemUpdatedEvent, event)
            logger(f"Item updated: {event.item.model_dump()}")
        elif event.type == "item.completed":
            event = cast(types.ItemCompletedEvent, event)
            logger(f"Item completed: {event.item.model_dump()}")
        elif event.type == "turn.failed":
            event = cast(types.TurnFailedEvent, event)
            logger(f"Turn failed: {event.error.message}")
        elif event.type == "error":
            event = cast(types.ThreadErrorEvent, event)
            logger(f"Error: {event.message}")
        elif event.type == "turn.started":
            event = cast(types.TurnStartedEvent, event)
            logger(f"Turn started: {event.model_dump()}")
        else:
            event = cast(types.UnknownThreadEvent, event)
            logger(f"Unknown thread event: {event.model_dump()}")

asyncio.run(arun("Without persisting any code, generate conway's game of life in python and deliver the code as a message", logger=print))