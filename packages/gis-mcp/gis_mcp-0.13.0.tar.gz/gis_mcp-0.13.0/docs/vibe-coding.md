# Vibe Coding

If you develop agents via vibe coding, keep these context files open in your editor so the LLM understands the GIS MCP server:

- `llms.txt`: summarized context for smaller windows.
- `llms-full.txt`: full context when your model has a larger window.

Where to find them:

- In the repository root alongside this documentation:
  - [`llms.txt` (summary)](https://github.com/mahdin75/gis-mcp/blob/main/llms.txt)
  - [`llms-full.txt` (full)](https://github.com/mahdin75/gis-mcp/blob/main/llms-full.txt)

How to use:

- Pin or open one of these files in your MCP-aware editor (Cursor, Claude Desktop, etc.) so it can be fed as context while coding.
- Use `llms.txt` for quick, lightweight context; switch to `llms-full.txt` when your model can handle more detail.
