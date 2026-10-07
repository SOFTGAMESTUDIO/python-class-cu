from __future__ import annotations


def get_recent_system_events(limit: int = 10) -> list[str]:
    return [
        f"System event {idx}: Normal health check completed" for idx in range(1, limit + 1)
    ]
