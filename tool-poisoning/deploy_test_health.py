"""Small deploy smoke-test module for Railway verification."""

from __future__ import annotations

import json
from datetime import datetime, timezone


def build_health_payload() -> dict[str, str]:
    """Return a JSON-serializable health check payload."""
    return {
        "status": "ok",
        "service": "tool-poisoning",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def render_health_json() -> str:
    return json.dumps(build_health_payload(), indent=2)


if __name__ == "__main__":
    print(render_health_json())
