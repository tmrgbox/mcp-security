"""Log line formatter for deploy verification in Railway logs."""

from __future__ import annotations

from datetime import datetime, timezone


def format_deploy_log(event: str, detail: str = "") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    base = f"[deploy] {ts} {event}"
    return f"{base} {detail}".strip() if detail else base


def startup_banner() -> str:
    return format_deploy_log("startup", "tool-poisoning bridge ready")


if __name__ == "__main__":
    print(startup_banner())
    print(format_deploy_log("smoke", "ok"))
