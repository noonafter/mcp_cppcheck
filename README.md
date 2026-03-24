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
    "cppcheck": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp_cppcheck", "mcp_cppcheck"]
    }
  }
}
```

### Tools

- `check_code(target_path, mode="quick")` - Check code
- `check_with_config(target_path, config_file)` - Check with config
- `get_project_context(target_path)` - Get project info

## Requirements

- Python >= 3.10
- cppcheck (must be installed separately)
