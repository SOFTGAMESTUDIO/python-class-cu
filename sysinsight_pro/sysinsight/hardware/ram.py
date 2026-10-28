from __future__ import annotations

import psutil


def get_ram_metrics() -> dict:
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    if memory.percent >= 90:
        status = "CRITICAL"
    elif memory.percent >= 80:
        status = "HIGH"
    elif memory.percent >= 60:
        status = "MODERATE"
    else:
        status = "NORMAL"

    return {
        "total_gb": round(memory.total / (1024 ** 3), 2),
        "used_gb": round(memory.used / (1024 ** 3), 2),
        "available_gb": round(memory.available / (1024 ** 3), 2),
        "cached_gb": round(getattr(memory, "cached", 0) / (1024 ** 3), 2),
        "used_percent": round(memory.percent, 1),
        "swap_total_gb": round(swap.total / (1024 ** 3), 2),
        "swap_used_gb": round(swap.used / (1024 ** 3), 2),
        "swap_percent": round(swap.percent, 1),
        "status": status,
    }
