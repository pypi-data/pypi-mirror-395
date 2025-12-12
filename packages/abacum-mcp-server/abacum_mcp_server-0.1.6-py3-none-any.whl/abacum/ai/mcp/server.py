"""
Abacum MCP Server
Initializes the FastMCP server and provides the main entry point.
"""

from fastmcp import FastMCP
import sys
import asyncio
from .api import get_api_credentials, ApiError

# Initialize the MCP server FIRST
mcp = FastMCP("Abacum MCP Server")

# THEN import tools and resources modules (they need mcp to be defined)
from . import tools
from . import resources


# Register resources
mcp.resource("abacum://models")(resources.get_models_resource)
mcp.resource("abacum://scenarios")(resources.get_scenarios_resource)
mcp.resource("abacum://variables")(resources.get_variables_resource)


def main():
    """
    Main entry point for the MCP server.
    Validates credentials, loads resources at startup, and runs the server.
    """
    try:
        # Validate credentials before starting
        get_api_credentials()
        print("✅ Credentials validated", file=sys.stderr)

        # Load resources at startup
        print("⏳ Loading resources...", file=sys.stderr)
        success = asyncio.run(resources.load_all_resources())

        if success:
            print("✅ Resources loaded: models, scenarios, variables", file=sys.stderr)
        else:
            print("⚠️  Warning: Resources failed to load (cached error state)", file=sys.stderr)

        print("✅ MCP server initialized", file=sys.stderr)

    except ApiError as e:
        print(f"❌ ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Run with stdio transport for Claude Desktop
    mcp.run()

if __name__ == "__main__":
    main()

