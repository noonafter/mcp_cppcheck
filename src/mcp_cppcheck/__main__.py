#!/usr/bin/env python3
"""MCP Cppcheck entry point"""
from mcp_cppcheck.server import mcp


def main():
    mcp.run()


if __name__ == "__main__":
    main()
