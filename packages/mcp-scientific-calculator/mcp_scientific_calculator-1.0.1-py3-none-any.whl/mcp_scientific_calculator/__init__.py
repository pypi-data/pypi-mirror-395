"""
MCP Scientific Calculator - A production-ready Model Context Protocol server.

Provides advanced mathematical calculation capabilities including:
- Symbolic mathematics (SymPy)
- Numerical computing (NumPy/SciPy)
- Data analysis (pandas)
- Image processing

Version: 1.0.1
"""

__version__ = "1.0.1"
__author__ = "MCP Calculator Team"
__license__ = "MIT"

from .calculator import CALCULATOR_TOOLS, symbolic_tool, numpy_tool, scipy_tool

__all__ = [
    "CALCULATOR_TOOLS",
    "symbolic_tool",
    "numpy_tool",
    "scipy_tool",
    "__version__",
]
