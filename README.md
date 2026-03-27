# MCP Cppcheck

MCP plugin for cppcheck static analysis tool with project awareness and output optimization.

## Installation

1. Install dependencies:
```bash
cd /path/to/mcp_cppcheck
uv pip install -e .
```

2. Install cppcheck (if not already installed):
   - Windows: `choco install cppcheck` or download from [cppcheck.net](http://cppcheck.net/)
   - Linux: `sudo apt install cppcheck`
   - macOS: `brew install cppcheck`

## Configuration

### MCP Server

Add to your MCP config:

```json
{
  "mcpServers": {
    "cppcheck": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp_server", "run", "mcp_cppcheck"]
    }
  }
}
```




## Tools

- `check_code(target_path, mode="quick")` - Check code files or directories
- `get_project_context(target_path)` - Get project configuration info

## Requirements

- Python >= 3.10
- uv package manager
- cppcheck (must be installed separately)
