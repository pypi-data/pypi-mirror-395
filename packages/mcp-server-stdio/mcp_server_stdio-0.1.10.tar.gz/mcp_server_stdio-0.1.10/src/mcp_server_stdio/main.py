from fastmcp import FastMCP
from mcp_server_stdio.tools.loader import load_tools


def run():
    mcp = FastMCP(
        "mcp-service"
    )

    load_tools(mcp)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
