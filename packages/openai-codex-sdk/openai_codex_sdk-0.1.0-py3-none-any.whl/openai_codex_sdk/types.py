from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from .abort import AbortSignal

# === Thread options ===

ApprovalMode = Literal["never", "on-request", "on-failure", "untrusted"]
SandboxMode = Literal["read-only", "workspace-write", "danger-full-access"]
ModelReasoningEffort = Literal["minimal", "low", "medium", "high"]


class CodexOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        protected_namespaces=(),
    )

    codex_path_override: Optional[str] = Field(default=None, alias="codexPathOverride")
    base_url: Optional[str] = Field(default=None, alias="baseUrl")
    api_key: Optional[str] = Field(default=None, alias="apiKey")
    # When provided, the SDK will NOT inherit variables from os.environ.
    env: Optional[Dict[str, str]] = None


class ThreadOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        protected_namespaces=(),
    )

    model: Optional[str] = None
    sandbox_mode: Optional[SandboxMode] = Field(default=None, alias="sandboxMode")
    working_directory: Optional[str] = Field(default=None, alias="workingDirectory")
    skip_git_repo_check: Optional[bool] = Field(default=None, alias="skipGitRepoCheck")
    model_reasoning_effort: Optional[ModelReasoningEffort] = Field(
        default=None,
        alias="modelReasoningEffort",
    )
    network_access_enabled: Optional[bool] = Field(default=None, alias="networkAccessEnabled")
    web_search_enabled: Optional[bool] = Field(default=None, alias="webSearchEnabled")
    approval_policy: Optional[ApprovalMode] = Field(default=None, alias="approvalPolicy")
    additional_directories: Optional[List[str]] = Field(default=None, alias="additionalDirectories")


class TurnOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        arbitrary_types_allowed=True,
        protected_namespaces=(),
    )

    output_schema: Optional[Dict[str, Any]] = Field(default=None, alias="outputSchema")
    signal: Optional[AbortSignal] = None


# === User input ===

class TextInput(BaseModel):
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    type: Literal["text"]
    text: str


class LocalImageInput(BaseModel):
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    type: Literal["local_image"]
    path: str


UserInput = Union[TextInput, LocalImageInput]
Input = Union[str, List[Union[UserInput, Dict[str, Any]]]]  # accepts dicts for convenience


# === Thread items ===
CommandExecutionStatus = Literal["in_progress", "completed", "failed"]


class CommandExecutionItem(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    id: str
    type: Literal["command_execution"]
    command: str
    aggregated_output: str
    exit_code: Optional[int] = None
    status: CommandExecutionStatus


PatchChangeKind = Literal["add", "delete", "update"]


class FileUpdateChange(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    path: str
    kind: PatchChangeKind


PatchApplyStatus = Literal["completed", "failed"]


class FileChangeItem(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    id: str
    type: Literal["file_change"]
    changes: List[FileUpdateChange]
    status: PatchApplyStatus


McpToolCallStatus = Literal["in_progress", "completed", "failed"]


class McpToolCallResult(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    # MCP content blocks are modelled as JSON objects for forward-compatibility.
    content: List[Dict[str, Any]]
    structured_content: Any


class McpToolCallError(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    message: str


class McpToolCallItem(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    id: str
    type: Literal["mcp_tool_call"]
    server: str
    tool: str
    arguments: Any
    result: Optional[McpToolCallResult] = None
    error: Optional[McpToolCallError] = None
    status: McpToolCallStatus


class AgentMessageItem(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    id: str
    type: Literal["agent_message"]
    text: str


class ReasoningItem(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    id: str
    type: Literal["reasoning"]
    text: str


class WebSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    id: str
    type: Literal["web_search"]
    query: str


class ErrorItem(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    id: str
    type: Literal["error"]
    message: str


class TodoItem(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    text: str
    completed: bool


class TodoListItem(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    id: str
    type: Literal["todo_list"]
    items: List[TodoItem]


class UnknownThreadItem(BaseModel):
    """Fallback for forward-compatible parsing."""

    model_config = ConfigDict(extra="allow", protected_namespaces=())

    id: str
    type: str


ThreadItem = Union[
    AgentMessageItem,
    ReasoningItem,
    CommandExecutionItem,
    FileChangeItem,
    McpToolCallItem,
    WebSearchItem,
    TodoListItem,
    ErrorItem,
    UnknownThreadItem,
]


# === Events ===

class Usage(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    input_tokens: int
    cached_input_tokens: int
    output_tokens: int


class ThreadError(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    message: str


class ThreadStartedEvent(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    type: Literal["thread.started"]
    thread_id: str


class TurnStartedEvent(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    type: Literal["turn.started"]


class TurnCompletedEvent(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    type: Literal["turn.completed"]
    usage: Usage


class TurnFailedEvent(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    type: Literal["turn.failed"]
    error: ThreadError


class ItemStartedEvent(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    type: Literal["item.started"]
    item: ThreadItem


class ItemUpdatedEvent(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    type: Literal["item.updated"]
    item: ThreadItem


class ItemCompletedEvent(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    type: Literal["item.completed"]
    item: ThreadItem


class ThreadErrorEvent(BaseModel):
    model_config = ConfigDict(extra="allow", protected_namespaces=())

    type: Literal["error"]
    message: str


class UnknownThreadEvent(BaseModel):
    """Fallback for forward-compatible parsing."""

    model_config = ConfigDict(extra="allow", protected_namespaces=())

    type: str


ThreadEvent = Union[
    ThreadStartedEvent,
    TurnStartedEvent,
    TurnCompletedEvent,
    TurnFailedEvent,
    ItemStartedEvent,
    ItemUpdatedEvent,
    ItemCompletedEvent,
    ThreadErrorEvent,
    UnknownThreadEvent,
]
