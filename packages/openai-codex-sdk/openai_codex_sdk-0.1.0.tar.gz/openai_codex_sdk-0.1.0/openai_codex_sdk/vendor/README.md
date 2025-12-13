# Bundled Codex CLI binaries

The Python SDK resolves the `codex` executable from the package at:

```
openai_codex_sdk/vendor/<target-triple>/codex/codex
openai_codex_sdk/vendor/<target-triple>/codex/codex.exe
```

This mirrors the layout used by the TypeScript SDK.

Packaging the actual binaries is out of scope for this repository snapshot, but the SDK
supports overriding the path via `CodexOptions.codex_path_override`.
