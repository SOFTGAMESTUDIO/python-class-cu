from __future__ import annotations


def get_fan_status() -> dict:
    return {
        "cpu_fan_rpm": 0,
        "gpu_fan_rpm": 0,
        "system_fan_rpm": 0,
        "control_supported": False,
    }
