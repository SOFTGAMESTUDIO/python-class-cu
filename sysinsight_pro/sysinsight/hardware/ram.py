from __future__ import annotations

import psutil


def get_ram_metrics() -> dict:
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "total_gb": round(memory.total / (1024**3), 2),
        "used_gb": round(memory.used / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2),
        "used_percent": memory.percent,
        "swap_total_gb": round(swap.total / (1024**3), 2),
        "swap_used_gb": round(swap.used / (1024**3), 2),
        "status": "NORMAL" if memory.percent < 80 else "HIGH",
    }
