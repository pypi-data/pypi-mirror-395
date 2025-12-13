from fastmcp import FastMCP
from src.tools.karini_tools import KariniTools

mcp = FastMCP(
    name="karini-mcp-server",
    version="0.1.1",
)

def setup_server():
    karini_tools = KariniTools()
    karini_tools.register_copilot_tools(mcp)
    karini_tools.register_webhook_tools(mcp)
    karini_tools.register_dataset_tools(mcp)
    karini_tools.register_tracing_tools(mcp)
    return mcp

server = setup_server()