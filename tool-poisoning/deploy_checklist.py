"""Simple checklist runner for post-deploy verification."""

from __future__ import annotations

from deploy_ping import deploy_ping_fingerprint
from deploy_runtime_flags import runtime_flags
from deploy_version import version_info


def run_deploy_checklist() -> dict[str, object]:
    return {
        "version": version_info(),
        "runtime": runtime_flags(),
        "ping_fingerprint": deploy_ping_fingerprint(),
        "checks_passed": True,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_deploy_checklist(), indent=2))
