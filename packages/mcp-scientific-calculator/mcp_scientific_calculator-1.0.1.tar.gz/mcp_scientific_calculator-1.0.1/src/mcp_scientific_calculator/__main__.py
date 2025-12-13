"""
Entry point for running the MCP server directly as a module.
Usage: python -m mcp_scientific_calculator
"""

import sys
from .mcp_server import main

if __name__ == "__main__":
    sys.exit(main())
