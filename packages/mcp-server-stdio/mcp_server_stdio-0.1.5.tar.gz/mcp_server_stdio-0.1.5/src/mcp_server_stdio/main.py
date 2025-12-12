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

    print("=" * 70)
    print("Starting MCP Service Server")
    print("=" * 70)
    print("Transport: stdio (MCP over stdin/stdout)")
    print("=" * 70)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
