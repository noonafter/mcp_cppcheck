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
        target_path: File or directory path to check
        mode: Check mode - 'quick' (default) or 'full'
    """
    context = ProjectContext(target_path)
    runner = CppcheckRunner(context)
    return runner.run(mode)


@mcp.tool()
def get_project_context(target_path: str) -> str:
    """Get project context information

    Args:
        target_path: File or directory path
    """
    context = ProjectContext(target_path)
    return json.dumps(context.to_dict(), indent=2)

