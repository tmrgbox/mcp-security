"""Version stamp for deploy verification in logs and health checks."""

from __future__ import annotations

DEPLOY_BUILD = "2026-10-19-railway-test-13"
DEPLOY_COMPONENT = "tool-poisoning-bridge"


def version_info() -> dict[str, str]:
    return {
        "build": DEPLOY_BUILD,
        "component": DEPLOY_COMPONENT,
    }


if __name__ == "__main__":
    print(version_info())
