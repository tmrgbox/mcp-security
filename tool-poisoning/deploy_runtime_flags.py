"""Runtime flags readable from bridge or health endpoints after deploy."""

from __future__ import annotations

import os


def runtime_flags() -> dict[str, str | bool]:
    return {
        "mcp_transport": os.environ.get("MCP_TRANSPORT", "stdio"),
        "fastmcp_host": os.environ.get("FASTMCP_HOST", "127.0.0.1"),
        "port": os.environ.get("PORT") or os.environ.get("FASTMCP_PORT", "8000"),
        "railway_env": bool(os.environ.get("RAILWAY_ENVIRONMENT")),
    }


if __name__ == "__main__":
    for key, value in runtime_flags().items():
        print(f"{key}={value}")
