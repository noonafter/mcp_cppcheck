"""Cppcheck runner and output cleaner"""
import subprocess
import xml.etree.ElementTree as ET
from typing import Optional
from .project_detector import ProjectContext


class CppcheckRunner:
    """Run cppcheck and clean output"""

    def __init__(self, context: ProjectContext):
        self.context = context

    def run(self, mode: str = "quick") -> str:
        """Run cppcheck and return cleaned XML output"""
        cmd = self._build_command(mode)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return self._clean_xml(result.stderr)

    def _build_command(self, mode: str) -> list:
        """Build cppcheck command"""
        cmd = ["cppcheck", "--xml", "--xml-version=2"]

        if mode == "full":
            cmd.append("--enable=all")
        else:
            cmd.append("--enable=warning")

        if self.context.is_project_file:
            cmd.append(f"--project={self.context.target_path}")
        elif self.context.compile_commands:
            cmd.append(f"--project={self.context.compile_commands}")
        else:
            # For regular files/dirs, add project root as include path
            if self.context.project_root:
                cmd.append(f"-I{self.context.project_root}")
            cmd.append(str(self.context.target_path))

        return cmd

    def _clean_xml(self, xml_output: str) -> str:
        """Clean XML output by removing verbose and column attributes"""
        try:
            root = ET.fromstring(xml_output)
            for error in root.findall(".//error"):
                error.attrib.pop("verbose", None)
                for location in error.findall("location"):
                    location.attrib.pop("column", None)
            return ET.tostring(root, encoding="unicode")
        except ET.ParseError:
            return xml_output

