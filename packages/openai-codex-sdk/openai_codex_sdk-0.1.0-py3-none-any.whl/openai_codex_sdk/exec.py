from __future__ import annotations

import asyncio
import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator, Dict, List, Optional

from .abort import AbortError, AbortSignal, _format_abort_reason
from .errors import CodexExecError
from .types import ApprovalMode, ModelReasoningEffort, SandboxMode


INTERNAL_ORIGINATOR_ENV = "CODEX_INTERNAL_ORIGINATOR_OVERRIDE"
PYTHON_SDK_ORIGINATOR = "codex_sdk_py"


@dataclass(frozen=True)
class CodexExecArgs:
    input: str

    base_url: Optional[str] = None
    api_key: Optional[str] = None
    thread_id: Optional[str] = None

    images: Optional[List[str]] = None
    model: Optional[str] = None
    sandbox_mode: Optional[SandboxMode] = None
    working_directory: Optional[str] = None
    additional_directories: Optional[List[str]] = None
    skip_git_repo_check: Optional[bool] = None
    output_schema_file: Optional[str] = None
    model_reasoning_effort: Optional[ModelReasoningEffort] = None
    signal: Optional[AbortSignal] = None
    network_access_enabled: Optional[bool] = None
    web_search_enabled: Optional[bool] = None
    approval_policy: Optional[ApprovalMode] = None


class CodexExec:
    def __init__(
        self,
        executable_path: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> None:
        self.executable_path = executable_path or find_codex_path()
        self.env_override = env

    def _build_command_args(self, args: CodexExecArgs) -> List[str]:
        command_args: List[str] = ["exec", "--experimental-json"]

        if args.model:
            command_args += ["--model", args.model]

        if args.sandbox_mode:
            command_args += ["--sandbox", args.sandbox_mode]

        if args.working_directory:
            command_args += ["--cd", args.working_directory]

        if args.additional_directories:
            for d in args.additional_directories:
                command_args += ["--add-dir", d]

        if args.skip_git_repo_check:
            command_args.append("--skip-git-repo-check")

        if args.output_schema_file:
            command_args += ["--output-schema", args.output_schema_file]

        if args.model_reasoning_effort:
            command_args += ["--config", f'model_reasoning_effort="{args.model_reasoning_effort}"']

        if args.network_access_enabled is not None:
            val = "true" if args.network_access_enabled else "false"
            command_args += ["--config", f"sandbox_workspace_write.network_access={val}"]

        if args.web_search_enabled is not None:
            val = "true" if args.web_search_enabled else "false"
            command_args += ["--config", f"features.web_search_request={val}"]

        if args.approval_policy:
            command_args += ["--config", f'approval_policy="{args.approval_policy}"']

        if args.images:
            for image in args.images:
                command_args += ["--image", image]

        if args.thread_id:
            command_args += ["resume", args.thread_id]

        return command_args

    def _build_env(self, args: CodexExecArgs) -> Dict[str, str]:
        env: Dict[str, str] = {}
        if self.env_override is not None:
            env.update(self.env_override)
        else:
            env.update(os.environ)

        if INTERNAL_ORIGINATOR_ENV not in env:
            env[INTERNAL_ORIGINATOR_ENV] = PYTHON_SDK_ORIGINATOR

        if args.base_url:
            env["OPENAI_BASE_URL"] = args.base_url

        if args.api_key:
            env["CODEX_API_KEY"] = args.api_key

        return env

    async def run(self, args: CodexExecArgs) -> AsyncIterator[str]:
        # Pre-aborted signals should fail deterministically before any work happens.
        if args.signal is not None and args.signal.aborted:
            raise AbortError(_format_abort_reason(args.signal.reason))

        command_args = self._build_command_args(args)
        env = self._build_env(args)

        proc = await asyncio.create_subprocess_exec(
            self.executable_path,
            *command_args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        if proc.stdin is None or proc.stdout is None:
            try:
                proc.kill()
            finally:
                raise CodexExecError("Child process missing stdin/stdout")

        stderr_task = asyncio.create_task(_read_all(proc.stderr))
        abort_waiter: Optional[asyncio.Task[None]] = None
        if args.signal is not None:
            abort_waiter = asyncio.create_task(args.signal.wait())

        try:
            proc.stdin.write(args.input.encode("utf-8"))
            await proc.stdin.drain()
            proc.stdin.close()

            while True:
                line_task: asyncio.Task[bytes] = asyncio.create_task(proc.stdout.readline())

                wait_set = {line_task}
                if abort_waiter is not None:
                    wait_set.add(abort_waiter)

                done, _pending = await asyncio.wait(wait_set, return_when=asyncio.FIRST_COMPLETED)

                if abort_waiter is not None and abort_waiter in done:
                    line_task.cancel()
                    await asyncio.gather(line_task, return_exceptions=True)
                    await _terminate_process(proc)
                    raise AbortError(_format_abort_reason(args.signal.reason if args.signal else None))

                line = line_task.result()
                if not line:
                    break

                yield line.decode("utf-8").rstrip("\n")

            returncode = await proc.wait()
            stderr = await stderr_task

            if returncode != 0:
                raise CodexExecError(
                    f"Codex Exec exited with code {returncode}: {stderr.decode('utf-8', errors='replace')}"
                )

        finally:
            if abort_waiter is not None:
                abort_waiter.cancel()
                await asyncio.gather(abort_waiter, return_exceptions=True)

            if proc.returncode is None:
                await _terminate_process(proc)

            stderr_task.cancel()
            await asyncio.gather(stderr_task, return_exceptions=True)


async def _read_all(stream: Optional[asyncio.StreamReader]) -> bytes:
    if stream is None:
        return b""
    chunks: List[bytes] = []
    while True:
        chunk = await stream.read(4096)
        if not chunk:
            break
        chunks.append(chunk)
    return b"".join(chunks)


async def _terminate_process(proc: asyncio.subprocess.Process) -> None:
    try:
        proc.kill()
    except ProcessLookupError:
        pass
    try:
        await proc.wait()
    except Exception:
        pass


def find_codex_path() -> str:
    """Resolve the packaged codex binary path.

    Mirrors the TypeScript SDK layout:
      <pkg>/vendor/<target-triple>/codex/<codex|codex.exe>
    """

    system = sys_platform()
    machine = platform.machine().lower()

    target_triple: Optional[str] = None
    if system in ("linux", "android"):
        if machine in ("x86_64", "amd64"):
            target_triple = "x86_64-unknown-linux-musl"
        elif machine in ("aarch64", "arm64"):
            target_triple = "aarch64-unknown-linux-musl"
    elif system == "darwin":
        if machine in ("x86_64", "amd64"):
            target_triple = "x86_64-apple-darwin"
        elif machine in ("aarch64", "arm64"):
            target_triple = "aarch64-apple-darwin"
    elif system == "win32":
        if machine in ("x86_64", "amd64"):
            target_triple = "x86_64-pc-windows-msvc"
        elif machine in ("aarch64", "arm64"):
            target_triple = "aarch64-pc-windows-msvc"

    if not target_triple:
        raise CodexExecError(f"Unsupported platform: {system} ({machine})")

    pkg_dir = Path(__file__).resolve().parent
    vendor_root = pkg_dir / "vendor"
    codex_binary = "codex.exe" if system == "win32" else "codex"
    binary_path = vendor_root / target_triple / "codex" / codex_binary
    return str(binary_path)


def sys_platform() -> str:
    # Keep behaviour aligned with Node's `process.platform` naming where possible.
    import sys

    return sys.platform
