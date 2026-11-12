"""Summarize synthetic Torq leak dataset from the local JSONL file."""

from __future__ import annotations

import json
from pathlib import Path


def summarize_leak_file(path: Path | None = None) -> dict[str, int | str]:
    path = path or Path(__file__).with_name("simulated_torq_fat_leak.jsonl")
    records = 0
    total_bytes = path.stat().st_size if path.exists() else 0
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            records += 1
            try:
                json.loads(line)
            except json.JSONDecodeError:
                pass
    return {
        "path": str(path),
        "file_bytes": total_bytes,
        "record_count": records,
    }


if __name__ == "__main__":
    import json as json_mod

    print(json_mod.dumps(summarize_leak_file(), indent=2))
