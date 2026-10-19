"""Deploy smoke test: verify MCP tool module imports after deploy."""

from __future__ import annotations


def smoke_test_imports() -> dict[str, bool]:
    results: dict[str, bool] = {}
    try:
        from tool_poisoning import mcp  # noqa: F401

        results["tool_poisoning"] = True
        results["mcp_name"] = mcp.name == "Demo"
    except ImportError:
        results["tool_poisoning"] = False
        results["mcp_name"] = False
    return results


if __name__ == "__main__":
    print(smoke_test_imports())
