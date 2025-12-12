"""
ICSC Ava Upload MCP Server
檔案上傳和處理 MCP Server，支援工具鏈設計
"""

from .server import mcp, download_and_upload

__version__ = "0.1.0"
__all__ = ["mcp", "download_and_upload"]
