from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from .errors import CodexSdkError


@dataclass(frozen=True)
class OutputSchemaFile:
    schema_path: Optional[str]
    _dir: Optional[str]

    async def cleanup(self) -> None:
        if not self._dir:
            return
        # Best-effort cleanup; suppress errors like the TS SDK.
        try:
            for root, dirs, files in os.walk(self._dir, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except OSError:
                        pass
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except OSError:
                        pass
            try:
                os.rmdir(self._dir)
            except OSError:
                pass
        except OSError:
            pass


async def create_output_schema_file(schema: Optional[Dict[str, Any]]) -> OutputSchemaFile:
    if schema is None:
        return OutputSchemaFile(schema_path=None, _dir=None)

    if not isinstance(schema, dict):
        raise CodexSdkError("output_schema must be a plain JSON object (Python dict)")

    schema_dir = tempfile.mkdtemp(prefix="codex-output-schema-")
    schema_path = str(Path(schema_dir) / "schema.json")

    try:
        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(schema, f, ensure_ascii=False)
    except Exception:
        # Ensure no temp dirs leak on error.
        try:
            await OutputSchemaFile(schema_path=None, _dir=schema_dir).cleanup()
        finally:
            raise

    return OutputSchemaFile(schema_path=schema_path, _dir=schema_dir)
