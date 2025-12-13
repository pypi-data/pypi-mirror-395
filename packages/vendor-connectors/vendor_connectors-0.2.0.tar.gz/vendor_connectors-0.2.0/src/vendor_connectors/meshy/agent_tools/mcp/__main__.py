"""Run the mesh-toolkit MCP server.

Usage:
    python -m vendor_connectors.meshy.agent_tools.mcp

Environment:
    MESHY_API_KEY - Required for API access
"""

from __future__ import annotations

import os


def main():
    # Check for API key
    if not os.environ.get("MESHY_API_KEY"):
        msg = "MESHY_API_KEY environment variable is required for API access."
        raise RuntimeError(msg)

    from vendor_connectors.meshy.agent_tools.mcp import run_server

    run_server()


if __name__ == "__main__":
    main()
