from __future__ import annotations

import json
from typing import Any, Dict, Type

from .errors import EventParseError
from .types import (
    AgentMessageItem,
    CommandExecutionItem,
    ErrorItem,
    FileChangeItem,
    ItemCompletedEvent,
    ItemStartedEvent,
    ItemUpdatedEvent,
    McpToolCallItem,
    ReasoningItem,
    ThreadErrorEvent,
    ThreadEvent,
    ThreadItem,
    ThreadStartedEvent,
    TodoListItem,
    TurnCompletedEvent,
    TurnFailedEvent,
    TurnStartedEvent,
    UnknownThreadEvent,
    UnknownThreadItem,
    WebSearchItem,
)


_ITEM_MODELS: Dict[str, Type[object]] = {
    "agent_message": AgentMessageItem,
    "reasoning": ReasoningItem,
    "command_execution": CommandExecutionItem,
    "file_change": FileChangeItem,
    "mcp_tool_call": McpToolCallItem,
    "web_search": WebSearchItem,
    "todo_list": TodoListItem,
    "error": ErrorItem,
}

_EVENT_MODELS: Dict[str, Type[object]] = {
    "thread.started": ThreadStartedEvent,
    "turn.started": TurnStartedEvent,
    "turn.completed": TurnCompletedEvent,
    "turn.failed": TurnFailedEvent,
    "item.started": ItemStartedEvent,
    "item.updated": ItemUpdatedEvent,
    "item.completed": ItemCompletedEvent,
    "error": ThreadErrorEvent,
}


def parse_thread_item(data: Any) -> ThreadItem:
    if not isinstance(data, dict):
        raise EventParseError(f"Invalid item payload (expected object): {data!r}")

    item_type = data.get("type")
    if not isinstance(item_type, str):
        raise EventParseError(f"Invalid item payload (missing type): {data!r}")

    model = _ITEM_MODELS.get(item_type)
    if model is None:
        return UnknownThreadItem.model_validate(data)
    return model.model_validate(data)  # type: ignore[attr-defined]


def parse_thread_event_line(line: str) -> ThreadEvent:
    try:
        data = json.loads(line)
    except Exception as exc:  # noqa: BLE001
        raise EventParseError(f"Failed to parse JSONL event line: {line!r}") from exc
    return parse_thread_event(data)


def parse_thread_event(data: Any) -> ThreadEvent:
    if not isinstance(data, dict):
        raise EventParseError(f"Invalid event payload (expected object): {data!r}")

    event_type = data.get("type")
    if not isinstance(event_type, str):
        raise EventParseError(f"Invalid event payload (missing type): {data!r}")

    model = _EVENT_MODELS.get(event_type)
    if model is None:
        return UnknownThreadEvent.model_validate(data)

    if event_type.startswith("item."):
        item = parse_thread_item(data.get("item"))
        event_data = dict(data)
        event_data["item"] = item
        return model.model_validate(event_data)  # type: ignore[attr-defined]

    return model.model_validate(data)  # type: ignore[attr-defined]
