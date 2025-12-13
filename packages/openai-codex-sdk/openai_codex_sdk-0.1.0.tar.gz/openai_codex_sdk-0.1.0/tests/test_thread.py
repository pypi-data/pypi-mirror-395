from __future__ import annotations

import os
import pytest

from openai_codex_sdk import Codex
from openai_codex_sdk.abort import AbortController
from openai_codex_sdk.errors import ThreadRunError
from openai_codex_sdk.types import ThreadOptions
from tests.helpers import FakeExec, j


def _events_for_hi(thread_id: str = "thread_1"):
    return [
        j({"type": "thread.started", "thread_id": thread_id}),
        j({"type": "turn.started"}),
        j({"type": "item.completed", "item": {"id": "item_0", "type": "agent_message", "text": "Hi!"}}),
        j({"type": "turn.completed", "usage": {"input_tokens": 42, "cached_input_tokens": 12, "output_tokens": 5}}),
    ]


@pytest.mark.asyncio
async def test_thread_run_returns_items_usage_and_sets_thread_id(tmp_path):
    fake_exec = FakeExec([_events_for_hi()])
    codex = Codex({"codex_path_override": "/bin/codex"})
    codex._exec = fake_exec  # type: ignore[attr-defined]

    thread = codex.start_thread()
    result = await thread.run("Hello, world!")

    assert thread.id == "thread_1"
    assert result.final_response == "Hi!"
    assert len(result.items) == 1
    assert result.items[0].type == "agent_message"
    assert result.usage is not None
    assert result.usage.input_tokens == 42
    assert result.usage.cached_input_tokens == 12
    assert result.usage.output_tokens == 5


@pytest.mark.asyncio
async def test_thread_run_streamed_yields_events_in_order():
    fake_exec = FakeExec([_events_for_hi("thread_stream")])
    codex = Codex({"codex_path_override": "/bin/codex"})
    codex._exec = fake_exec  # type: ignore[attr-defined]

    thread = codex.start_thread()
    streamed = await thread.run_streamed("Hello, world!")

    types = []
    async for ev in streamed.events:
        types.append(ev.type)

    assert types == ["thread.started", "turn.started", "item.completed", "turn.completed"]
    assert thread.id == "thread_stream"


@pytest.mark.asyncio
async def test_thread_run_twice_passes_thread_id_second_time():
    fake_exec = FakeExec([_events_for_hi("thread_abc"), _events_for_hi("thread_abc")])
    codex = Codex({"codex_path_override": "/bin/codex"})
    codex._exec = fake_exec  # type: ignore[attr-defined]

    thread = codex.start_thread()
    await thread.run("first input")
    await thread.run("second input")

    assert len(fake_exec.calls) == 2
    assert fake_exec.calls[0].thread_id is None
    assert fake_exec.calls[1].thread_id == "thread_abc"


@pytest.mark.asyncio
async def test_resume_thread_passes_thread_id_on_first_call():
    fake_exec = FakeExec([_events_for_hi("thread_resume")])
    codex = Codex({"codex_path_override": "/bin/codex"})
    codex._exec = fake_exec  # type: ignore[attr-defined]

    thread = codex.resume_thread("thread_resume")
    await thread.run("input")

    assert len(fake_exec.calls) == 1
    assert fake_exec.calls[0].thread_id == "thread_resume"


@pytest.mark.asyncio
async def test_thread_turn_failed_raises_thread_run_error():
    fake_exec = FakeExec(
        [
            [
                j({"type": "thread.started", "thread_id": "t"}),
                j({"type": "turn.started"}),
                j({"type": "turn.failed", "error": {"message": "boom"}}),
            ]
        ]
    )
    codex = Codex({"codex_path_override": "/bin/codex"})
    codex._exec = fake_exec  # type: ignore[attr-defined]

    thread = codex.start_thread()
    with pytest.raises(ThreadRunError, match="boom"):
        await thread.run("fail")


@pytest.mark.asyncio
async def test_thread_writes_output_schema_file_and_cleans_up_after_run(tmp_path):
    recorded_schema_path = {"path": None}

    class SchemaPathExec(FakeExec):
        async def run(self, args):  # type: ignore[override]
            recorded_schema_path["path"] = args.output_schema_file
            # The file should exist during execution.
            assert args.output_schema_file is not None
            assert os.path.exists(args.output_schema_file)
            async for line in super().run(args):
                yield line

    fake_exec = SchemaPathExec([_events_for_hi("thread_schema")])
    codex = Codex({"codex_path_override": "/bin/codex"})
    codex._exec = fake_exec  # type: ignore[attr-defined]

    schema = {"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"]}
    thread = codex.start_thread()
    await thread.run("structured", {"output_schema": schema})

    schema_path = recorded_schema_path["path"]
    assert schema_path is not None
    assert not os.path.exists(schema_path)
