"""MCP Cppcheck Server"""
import json
from mcp.server.fastmcp import FastMCP
from .project_detector import ProjectContext
from .cppcheck_runner import CppcheckRunner

mcp = FastMCP("cppcheck")


@mcp.tool()
def check_code(target_path: str, mode: str = "quick") -> str:
    """Check code with cppcheck
    Args:
        target_path: ABSOLUTE path to file, directory, compile_commands.json, or .cppcheck file
        mode: Check mode - 'quick' (default) or 'full'

    Important: target_path must be an absolute path. Relative paths cannot be resolved.
    """
    try:
        context = ProjectContext(target_path)
        runner = CppcheckRunner(context)
        return runner.run(mode)
    except ValueError as e:
        return f"Error: {e}"


@mcp.tool()
def get_project_context(target_path: str) -> str:
    """Get project context information

    Args:
        target_path: File or directory path
    """
    context = ProjectContext(target_path)
    return json.dumps(context.to_dict(), indent=2)

