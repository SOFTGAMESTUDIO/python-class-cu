from __future__ import annotations

import psutil


def get_disk_metrics() -> dict:
    usage = psutil.disk_usage('/')
    return {
        "total_gb": round(usage.total / (1024**3), 2),
        "used_gb": round(usage.used / (1024**3), 2),
        "free_gb": round(usage.free / (1024**3), 2),
        "used_percent": round((usage.used / usage.total) * 100, 1),
        "status": "HEALTHY" if usage.percent < 80 else "WARNING",
    }
