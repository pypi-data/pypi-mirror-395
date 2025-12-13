from __future__ import annotations

import pytest

from openai_codex_sdk.utils import normalize_input


def test_normalize_input_string():
    prompt, images = normalize_input("hello")
    assert prompt == "hello"
    assert images == []


def test_normalize_input_combines_text_and_collects_images():
    prompt, images = normalize_input(
        [
            {"type": "text", "text": "Describe file changes"},
            {"type": "text", "text": "Focus on impacted tests"},
            {"type": "local_image", "path": "./ui.png"},
            {"type": "local_image", "path": "./diagram.jpg"},
        ]
    )
    assert prompt == "Describe file changes\n\nFocus on impacted tests"
    assert images == ["./ui.png", "./diagram.jpg"]


def test_normalize_input_rejects_unknown_entry_type():
    with pytest.raises(TypeError):
        normalize_input([{"type": "wat", "x": 1}])  # type: ignore[arg-type]
