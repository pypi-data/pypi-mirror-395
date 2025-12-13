#!/usr/bin/env python3
"""
MCP Server for Mobile App Development
Tools for building Login, Home, and Settings pages

Install: pip install mcp-mobile-app
Usage: uvx mcp-mobile-app
"""

from .server import mcp, main

__version__ = "0.1.0"
__all__ = ["mcp", "main"]
