# main.py
from mcp_tools.dp_tools import *
from fastmcp import FastMCP

mcp = FastMCP("Jarvis Brain DrissionPage mcp")

# 根据环境变量加载模块
enabled_modules = os.getenv("MCP_MODULES", "DrissionPage").split(",")

if "DrissionPage" in enabled_modules:
    register_visit_url(mcp)


# if "api" in enabled_modules:
#     register_api_tools(mcp)

def main():
    mcp.run()
