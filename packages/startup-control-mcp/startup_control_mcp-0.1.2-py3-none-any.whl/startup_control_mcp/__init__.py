"""
开机启动项控制 MCP - 跨平台启动项管理工具
Startup Control MCP - Cross-platform startup item management tool

这个包提供了一个强大的跨平台启动项管理解决方案，支持：
- Windows、macOS 和 Linux 系统
- 自然语言交互控制
- 智能启动项分析和优化
- MCP (Model Context Protocol) 服务器支持
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# 导出主要组件
from .server import StartupItemManager, mcp_server

__all__ = [
    "StartupItemManager",
    "mcp_server",
    "__version__",
]