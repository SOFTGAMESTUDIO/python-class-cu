from __future__ import annotations


def get_thermal_metrics() -> dict:
    return {
        "cpu_temperature_c": 0.0,
        "gpu_temperature_c": 0.0,
        "fan_rpm": 0,
        "thermal_throttling": False,
        "status": "NORMAL",
    }
