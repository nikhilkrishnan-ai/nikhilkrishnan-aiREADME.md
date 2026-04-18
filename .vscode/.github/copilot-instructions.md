# Project Guidelines

## Scope
This workspace currently contains editor-level configuration files under `.vscode` and no application source tree.

## Code Style
- Preserve existing JSON formatting style in configuration files (tabs in `mcp.json`, spaces in `settings.json`).
- Keep edits minimal and avoid reformatting unrelated keys.
- Use ASCII unless the file already requires Unicode.

## Build and Test
- Python test discovery is configured for unittest in `settings.json`.
- Use unittest when adding or updating tests:
  - Start directory: `./__pycache__`
  - Pattern: `*test.py`
- Do not assume pytest is available (`python.testing.pytestEnabled` is false).

## Conventions
- Treat `mcp.json` as the source of truth for MCP server definitions; preserve existing server IDs unless explicitly asked to rename them.
- When changing MCP server commands, keep `type`, `command`, and `args` aligned so server startup remains valid.
- Prefer additive updates over destructive rewrites for config files.

## Architecture
- Primary configuration surfaces:
  - `.vscode/mcp.json` for MCP server registration.
  - `.vscode/settings.json` for Python testing behavior.
- If project code/docs are added later, update these instructions to link to canonical docs instead of duplicating them.
