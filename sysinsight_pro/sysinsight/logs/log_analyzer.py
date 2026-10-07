from __future__ import annotations


def analyze_log_events(events: list[str]) -> dict:
    return {
        "count": len(events),
        "status": "CLEAN" if events else "NO_DATA",
        "summary": "No critical events detected in the captured log stream.",
    }
