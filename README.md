# MCP Cppcheck

MCP plugin for cppcheck static analysis tool with project awareness and output optimization.

## Installation

```bash
uv pip install -e .
```

## Usage

### With MCP Client

Add to your MCP config:

```json
{
  "mcpServers": {
    "type": "stdio",
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/mcp_cppcheck",
      "run",
      "-m",
      "mcp_cppcheck"
    ]
  }
}
```

### Tools

- `check_code(target_path, mode="quick")` - Check code (use absolute paths)
- `get_project_context(target_path)` - Get project info

**Important**: Always use absolute paths for `target_path`. The MCP server cannot resolve relative paths from the client's working directory.

## Requirements

- Python >= 3.10
- cppcheck (must be installed separately)
