"""
Memory Hub MCP Server

A local memory hub for AI agents with MCP integration.
Supports both HTTP (FastAPI) and stdio transports.
"""

__version__ = "0.1.0"
__author__ = "Matt"

from .cli import main as cli_main

__all__ = ["cli_main"] 