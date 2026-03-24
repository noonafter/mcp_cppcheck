"""Test script for MCP Cppcheck"""
from mcp_cppcheck.project_detector import ProjectContext
from mcp_cppcheck.cppcheck_runner import CppcheckRunner

# Test project detection
print("Testing project detection...")
context = ProjectContext("D:\\alc\\c\\g33ddc\\src\\app")
print(f"Project root: {context.project_root}")
print(f"Is project file: {context.is_project_file}")
print(f"Compile commands: {context.compile_commands}")

print("\nProject context works!")


runner = CppcheckRunner(context)
xml_result = runner.run(mode="quick")
print(context.to_dict())
