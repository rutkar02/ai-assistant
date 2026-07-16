from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b:int) -> int:
    """Add two numbers."""
    return a+b

# At the bottom of your server.py:
if __name__ == "__main__":
    # If using FastMCP (the most common modern wrapper):
    mcp.run(transport="stdio")