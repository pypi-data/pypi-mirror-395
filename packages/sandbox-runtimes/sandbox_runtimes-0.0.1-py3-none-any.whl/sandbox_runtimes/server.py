# Copyright (c) 2023-2024 Datalayer, Inc.
#
# BSD 3-Clause License

from fastmcp import FastMCP


mcp = FastMCP("Demo 🚀")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


if __name__ == "__main__":
    mcp.run()
