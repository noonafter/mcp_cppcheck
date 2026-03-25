"""Project configuration detection module"""
from pathlib import Path
from typing import Optional


class ProjectContext:
    """Project context information"""
    def __init__(self, target_path: str):
        self.target_path = Path(target_path).resolve()
        self.is_project_file = self._is_project_file()
        self.project_root = self._find_project_root()

        # Only search for compile_commands.json if target is project file or project root
        # 后续优化中智能提取编译参数，这里需要改动一下，在else中，也可以找compile_commands.json，只不过是用来优化-I选项，而不是设置self.compile_commands
        if self.is_project_file or (self.target_path.is_dir() and self.target_path == self.project_root):
            self.compile_commands = self._find_file("compile_commands.json")
        else:
            self.compile_commands = None

        self.cppcheck_config = self._find_file(".cppcheck")

    def _is_project_file(self) -> bool:
        """Check if target is a project file"""
        if not self.target_path.is_file():
            return False
        return self.target_path.suffix in [".sln", ".vcxproj", ".cbp"] or \
               self.target_path.name in ["compile_commands.json", ".cppcheck"]

    def _find_project_root(self) -> Optional[Path]:
        """Find project root directory"""
        # If target is a project file, use its parent as root
        if self.is_project_file:
            return self.target_path.parent

        current = self.target_path if self.target_path.is_dir() else self.target_path.parent

        # Primary markers (more reliable)
        primary_markers = [".git", "Makefile", ".cppcheck", "meson.build", "configure.ac", ".project", "*.sln"]

        # Check for primary markers first
        while current != current.parent:
            for marker in primary_markers:
                if "*" in marker:
                    if list(current.glob(marker)):
                        return current
                elif (current / marker).exists():
                    return current
            current = current.parent

        # If no primary marker found, look for topmost CMakeLists.txt
        current = self.target_path if self.target_path.is_dir() else self.target_path.parent
        last_cmake_dir = None
        while current != current.parent:
            if (current / "CMakeLists.txt").exists():
                last_cmake_dir = current
            current = current.parent

        if last_cmake_dir:
            return last_cmake_dir

        # 如果没有找到任何项目标志的文件，直接将最底层目录当做项目root目录
        return self.target_path if self.target_path.is_dir() else self.target_path.parent

    def _find_file(self, filename: str) -> Optional[Path]:
        """Find file in project root or build directories"""
        if not self.project_root:
            return None

        # Check project root first
        file_path = self.project_root / filename
        if file_path.exists():
            return file_path

        # For compile_commands.json, search in directories starting with common build prefixes
        if filename == "compile_commands.json":
            for item in self.project_root.iterdir():
                if item.is_dir() and any(item.name.lower().startswith(prefix) for prefix in ["build", "cmake-build", "out"]):
                    build_path = item / filename
                    if build_path.exists():
                        return build_path

        return None

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "is_project_file": self.is_project_file,
            "project_root": str(self.project_root) if self.project_root else None,
            "compile_commands": str(self.compile_commands) if self.compile_commands else None,
            "cppcheck_config": str(self.cppcheck_config) if self.cppcheck_config else None,
        }
