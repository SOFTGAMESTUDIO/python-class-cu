from __future__ import annotations


def default_baseline() -> dict:
    return {
        "cpu": {"utilization": 18, "frequency_mhz": 1800},
        "ram": {"used_percent": 52},
        "gpu": {"temperature_c": 50, "utilization": 15},
        "disk": {"used_percent": 45},
        "network": {"download_mbps": 5},
    }
