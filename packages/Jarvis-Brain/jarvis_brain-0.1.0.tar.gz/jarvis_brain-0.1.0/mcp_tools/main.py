# main.py
from mcp_tools.dp_tools import *
from fastmcp import FastMCP

mcp = FastMCP("Jarvis Brain DrissionPage mcp")

# 根据环境变量加载模块
enabled_modules = os.getenv("MCP_MODULES", "DrissionPage").split(",")

if "DrissionPage" in enabled_modules:
    register_visit_url(mcp)
    register_close_tab(mcp)
    register_switch_tab(mcp)
    register_get_html(mcp)
    register_get_new_tab(mcp)
    register_check_selector(mcp)


def main():
    mcp.run()
