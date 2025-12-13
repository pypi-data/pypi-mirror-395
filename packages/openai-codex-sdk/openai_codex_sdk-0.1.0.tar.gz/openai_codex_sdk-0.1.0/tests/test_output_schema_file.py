from __future__ import annotations

import os
import pytest

from openai_codex_sdk.output_schema_file import create_output_schema_file
from openai_codex_sdk.errors import CodexSdkError


@pytest.mark.asyncio
async def test_create_output_schema_file_requires_dict():
    with pytest.raises(CodexSdkError):
        await create_output_schema_file(["not", "a", "dict"])  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_create_output_schema_file_writes_and_cleans_up():
    schema = {"type": "object", "properties": {"answer": {"type": "string"}}}
    schema_file = await create_output_schema_file(schema)
    assert schema_file.schema_path is not None
    assert os.path.exists(schema_file.schema_path)

    await schema_file.cleanup()
    assert not os.path.exists(schema_file.schema_path)
