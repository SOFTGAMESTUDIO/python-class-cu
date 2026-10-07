from __future__ import annotations


def generate_report(metrics: dict) -> str:
    summary = [
        "SysInsight Pro Summary",
        "======================",
        f"CPU utilization: {metrics.get('cpu', {}).get('utilization', 0)}%",
        f"RAM utilization: {metrics.get('ram', {}).get('used_percent', 0)}%",
        f"GPU status: {metrics.get('gpu', {}).get('status', 'UNKNOWN')}",
        f"Disk usage: {metrics.get('disk', {}).get('used_percent', 0)}%",
    ]
    return "\n".join(summary)
