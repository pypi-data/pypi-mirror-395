from __future__ import annotations

from typing import Any, Dict, List, Tuple, Union

from .types import Input, LocalImageInput, TextInput, UserInput


def normalize_input(input_: Input) -> Tuple[str, List[str]]:
    """Normalize input into a prompt string and a list of image paths."""

    if isinstance(input_, str):
        return input_, []

    prompt_parts: List[str] = []
    images: List[str] = []

    for entry in input_:
        item = _parse_user_input(entry)
        if item.type == "text":
            prompt_parts.append(item.text)
        elif item.type == "local_image":
            images.append(item.path)

    return "\n\n".join(prompt_parts), images


def _parse_user_input(entry: Union[UserInput, Dict[str, Any]]) -> UserInput:
    if isinstance(entry, (TextInput, LocalImageInput)):
        return entry

    if not isinstance(entry, dict):
        raise TypeError(f"Invalid input entry (expected dict): {entry!r}")

    t = entry.get("type")
    if t == "text":
        return TextInput.model_validate(entry)
    if t == "local_image":
        return LocalImageInput.model_validate(entry)

    raise TypeError(f"Invalid input entry type: {t!r}")
