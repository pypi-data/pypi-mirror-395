from fastmcp import FastMCP
from mcp_server_stdio.middleware.Authentication_middleware import AuthMiddleware
from mcp_server_stdio.tools.loader import load_tools


def run():
    mcp = FastMCP(
        "mcp-service",
        middleware=[
            AuthMiddleware()
        ]
    )

    load_tools(mcp)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
