from __future__ import annotations

import psutil


def get_cpu_metrics() -> dict:
    freq = psutil.cpu_freq()
    return {
        "cores": psutil.cpu_count(logical=True),
        "physical_cores": psutil.cpu_count(logical=False),
        "utilization": round(psutil.cpu_percent(interval=None), 1),
        "frequency_mhz": round(freq.current, 1) if freq else 0.0,
        "temperature_c": 0.0,
        "status": "NORMAL",
    }
