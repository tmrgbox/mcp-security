"""HTTP-style response helpers for bridge /health and /rpc smoke tests."""

from __future__ import annotations

import json
from typing import Any


def json_response(body: dict[str, Any], status: int = 200) -> dict[str, Any]:
    return {
        "status": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def health_response() -> dict[str, Any]:
    return json_response({"status": "ok", "endpoint": "/health"})


def rpc_ack(request_id: int | str | None) -> dict[str, Any]:
    return json_response(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"message": "deploy test ack"},
        }
    )


if __name__ == "__main__":
    print(json.dumps(health_response(), indent=2))
