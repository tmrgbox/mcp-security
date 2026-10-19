"""Lightweight deploy ping endpoint helpers for manual verification."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone


def deploy_ping(version: str = "1") -> str:
    """Return a stable JSON ping payload for deploy checks."""
    payload = {
        "ping": "pong",
        "version": version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(payload, sort_keys=True)


def deploy_ping_fingerprint(version: str = "1") -> str:
    """Short hash of the ping payload for quick log comparison."""
    return hashlib.sha256(deploy_ping(version).encode()).hexdigest()[:12]


if __name__ == "__main__":
    print(deploy_ping())
    print(deploy_ping_fingerprint())
