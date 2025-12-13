from __future__ import annotations

import asyncio
import os
from typing import List, Optional

import pytest

from openai_codex_sdk.abort import AbortController, AbortError
from openai_codex_sdk.errors import CodexExecError
from openai_codex_sdk.exec import CodexExec, CodexExecArgs, INTERNAL_ORIGINATOR_ENV


class _FakeStdin:
    def __init__(self) -> None:
        self.data = b""
        self.closed = False

    def write(self, b: bytes) -> None:
        self.data += b

    async def drain(self) -> None:
        return

    def close(self) -> None:
        self.closed = True


class _FakeStdout:
    def __init__(
        self,
        lines: List[bytes],
        block: bool = False,
        block_event: Optional[asyncio.Event] = None,
    ) -> None:
        self._lines = list(lines)
        self._block = block
        self._block_event = block_event or asyncio.Event()

    async def readline(self) -> bytes:
        if self._block:
            await self._block_event.wait()
            return b""
        if not self._lines:
            return b""
        return self._lines.pop(0)


class _FakeStderr:
    def __init__(self, chunks: List[bytes]) -> None:
        self._chunks = list(chunks)

    async def read(self, n: int) -> bytes:  # noqa: ARG002
        if not self._chunks:
            return b""
        return self._chunks.pop(0)


class _FakeProcess:
    def __init__(
        self,
        stdout: _FakeStdout,
        stderr: _FakeStderr,
        returncode: int = 0,
    ) -> None:
        self.stdin = _FakeStdin()
        self.stdout = stdout
        self.stderr = stderr
        self.returncode: Optional[int] = None  # set on kill()/wait completion
        self._target_returncode = returncode
        self._wait_event = asyncio.Event()

    async def wait(self) -> int:
        await self._wait_event.wait()
        assert self.returncode is not None
        return self.returncode

    def kill(self) -> None:
        if self.returncode is None:
            self.returncode = self._target_returncode
            self._wait_event.set()


@pytest.mark.asyncio
async def test_exec_run_yields_stdout_lines(monkeypatch):
    lines = [
        b'{"type":"turn.started"}\n',
        b'{"type":"turn.completed","usage":{"input_tokens":1,"cached_input_tokens":0,"output_tokens":1}}\n',
    ]
    proc = _FakeProcess(stdout=_FakeStdout(lines), stderr=_FakeStderr([b""]), returncode=0)
    called = {"env": None}

    async def fake_create_subprocess_exec(exe, *args, **kwargs):  # noqa: ARG001
        called["env"] = kwargs.get("env")

        async def auto_kill_when_stdout_drained():
            while True:
                if not proc.stdout._lines:
                    proc.kill()
                    break
                await asyncio.sleep(0)

        asyncio.create_task(auto_kill_when_stdout_drained())
        return proc

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create_subprocess_exec)

    exec_ = CodexExec(executable_path="/bin/codex", env={"CUSTOM": "1"})
    out = []
    async for line in exec_.run(CodexExecArgs(input="hi")):
        out.append(line)

    assert out == [
        '{"type":"turn.started"}',
        '{"type":"turn.completed","usage":{"input_tokens":1,"cached_input_tokens":0,"output_tokens":1}}',
    ]
    assert called["env"]["CUSTOM"] == "1"
    assert INTERNAL_ORIGINATOR_ENV in called["env"]


@pytest.mark.asyncio
async def test_exec_run_raises_on_nonzero_exit(monkeypatch):
    proc = _FakeProcess(stdout=_FakeStdout([b""]), stderr=_FakeStderr([b"oops"]), returncode=7)

    async def fake_create_subprocess_exec(exe, *args, **kwargs):  # noqa: ARG001
        proc.kill()  # end immediately
        return proc

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create_subprocess_exec)

    exec_ = CodexExec(executable_path="/bin/codex")
    with pytest.raises(CodexExecError, match=r"code 7: oops"):
        async for _ in exec_.run(CodexExecArgs(input="hi")):
            pass


@pytest.mark.asyncio
async def test_exec_env_override_does_not_inherit_os_environ(monkeypatch):
    os.environ["CODEX_ENV_SHOULD_NOT_LEAK"] = "leak"
    captured_env = {}

    try:
        proc = _FakeProcess(stdout=_FakeStdout([b""]), stderr=_FakeStderr([b""]), returncode=0)

        async def fake_create_subprocess_exec(exe, *args, **kwargs):  # noqa: ARG001
            captured_env.update(kwargs.get("env") or {})
            proc.kill()
            return proc

        monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create_subprocess_exec)

        exec_ = CodexExec(executable_path="/bin/codex", env={"CUSTOM_ENV": "custom"})
        args = CodexExecArgs(input="hi", base_url="http://example", api_key="test")

        async for _ in exec_.run(args):
            pass

        assert captured_env["CUSTOM_ENV"] == "custom"
        assert "CODEX_ENV_SHOULD_NOT_LEAK" not in captured_env
        assert captured_env["OPENAI_BASE_URL"] == "http://example"
        assert captured_env["CODEX_API_KEY"] == "test"
        assert INTERNAL_ORIGINATOR_ENV in captured_env
    finally:
        del os.environ["CODEX_ENV_SHOULD_NOT_LEAK"]


@pytest.mark.asyncio
async def test_exec_abort_pre_aborted_does_not_spawn(monkeypatch):
    controller = AbortController()
    controller.abort("Test abort")

    async def fake_create_subprocess_exec(*args, **kwargs):
        raise AssertionError("Should not spawn when signal is already aborted")

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create_subprocess_exec)

    exec_ = CodexExec(executable_path="/bin/codex")
    with pytest.raises(AbortError):
        async for _ in exec_.run(CodexExecArgs(input="hi", signal=controller.signal)):
            pass


@pytest.mark.asyncio
async def test_exec_abort_during_execution(monkeypatch):
    # stdout blocks forever; abort should cancel promptly.
    block_event = asyncio.Event()
    proc = _FakeProcess(
        stdout=_FakeStdout([], block=True, block_event=block_event),
        stderr=_FakeStderr([b""]),
        returncode=0,
    )

    async def fake_create_subprocess_exec(exe, *args, **kwargs):  # noqa: ARG001
        return proc

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create_subprocess_exec)

    controller = AbortController()
    exec_ = CodexExec(executable_path="/bin/codex")

    async def consume():
        async for _ in exec_.run(CodexExecArgs(input="hi", signal=controller.signal)):
            pass

    task = asyncio.create_task(consume())
    await asyncio.sleep(0)
    controller.abort("Aborted during execution")

    with pytest.raises(AbortError):
        await task

    assert proc.returncode is not None
