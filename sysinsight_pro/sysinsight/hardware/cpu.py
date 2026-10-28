from __future__ import annotations

import psutil


def get_cpu_metrics() -> dict:
    freq = psutil.cpu_freq()
    per_core = psutil.cpu_percent(percpu=True, interval=None)
    utilization = round(psutil.cpu_percent(interval=None), 1)

    # Determine status based on utilization
    if utilization >= 90:
        status = "CRITICAL"
    elif utilization >= 75:
        status = "HIGH"
    elif utilization >= 50:
        status = "MODERATE"
    else:
        status = "NORMAL"

    return {
        "cores": psutil.cpu_count(logical=True),
        "physical_cores": psutil.cpu_count(logical=False),
        "utilization": utilization,
        "per_core_percent": per_core,
        "frequency_mhz": round(freq.current, 1) if freq else 0.0,
        "frequency_max_mhz": round(freq.max, 1) if freq and freq.max else 0.0,
        "temperature_c": 0.0,  # filled by sensors
        "status": status,
    }
