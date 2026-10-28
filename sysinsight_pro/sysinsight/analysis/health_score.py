from __future__ import annotations

import math
from typing import Any


# Risk thresholds
_THRESHOLDS = {
    "cpu_critical": 90,
    "cpu_high": 75,
    "cpu_moderate": 50,
    "ram_critical": 90,
    "ram_high": 80,
    "ram_moderate": 60,
    "temp_critical": 95,
    "temp_high": 80,
    "temp_moderate": 65,
    "disk_critical": 95,
    "disk_high": 85,
    "disk_moderate": 70,
    "network_high": 100,
}


def calculate_health_score(metrics: dict[str, Any]) -> dict[str, Any]:
    """
    Multi-dimensional health score engine.

    Returns score (0-100), status (GOOD/WATCH/CRITICAL/DANGER),
    a risk level (LOW/MEDIUM/HIGH/CRITICAL), per-component details,
    and a list of risk factors.
    """
    cpu = metrics.get("cpu", {})
    ram = metrics.get("ram", {})
    gpu = metrics.get("gpu", {})
    disk = metrics.get("disk", {})
    network = metrics.get("network", {})
    thermal = metrics.get("thermal", {})

    cpu_util = cpu.get("utilization", 0)
    ram_pct = ram.get("used_percent", 0)
    gpu_temp = thermal.get("gpu_temperature_c", gpu.get("temperature_c", 0))
    cpu_temp = thermal.get("cpu_temperature_c", 0)
    disk_pct = disk.get("used_percent", 0)
    gpu_util = gpu.get("utilization", 0)
    net_down = network.get("download_mbps", 0)

    # Component scores (0-100 each, penalised above thresholds)
    cpu_score = _score_component(cpu_util, 50, 75, 90)
    ram_score = _score_component(ram_pct, 60, 80, 90)
    gpu_score = _score_component(gpu_util, 60, 80, 95) if gpu.get("status") != "UNAVAILABLE" else 85
    disk_score = _score_component(disk_pct, 70, 85, 95)
    temp_score = _score_component(cpu_temp, 65, 80, 95) if thermal.get("temperature_monitoring_available") else 80
    network_score = 100 if net_down <= 100 else max(60, 100 - (net_down - 100) / 10)

    # Weighted average (CPU & RAM weighted heavier)
    weights = {"cpu": 0.25, "ram": 0.20, "gpu": 0.15, "disk": 0.15, "temp": 0.15, "network": 0.10}
    scores = {"cpu": cpu_score, "ram": ram_score, "gpu": gpu_score, "disk": disk_score, "temp": temp_score, "network": network_score}
    overall = round(sum(scores[k] * weights[k] for k in weights), 1)

    # Status tiers
    if overall >= 80:
        status = "GOOD"
    elif overall >= 65:
        status = "WATCH"
    elif overall >= 45:
        status = "CRITICAL"
    else:
        status = "DANGER"

    # Risk level
    risk_factors: list[str] = []
    if cpu_util >= _THRESHOLDS["cpu_critical"]:
        risk_factors.append(f"CPU critically overloaded ({cpu_util:.0f}%)")
    elif cpu_util >= _THRESHOLDS["cpu_high"]:
        risk_factors.append(f"CPU load is high ({cpu_util:.0f}%)")

    if ram_pct >= _THRESHOLDS["ram_critical"]:
        risk_factors.append(f"Memory critically full ({ram_pct:.0f}%)")
    elif ram_pct >= _THRESHOLDS["ram_high"]:
        risk_factors.append(f"Memory pressure detected ({ram_pct:.0f}%)")

    if thermal.get("temperature_monitoring_available") and cpu_temp >= _THRESHOLDS["temp_high"]:
        risk_factors.append(f"CPU temperature elevated ({cpu_temp:.0f}°C)")

    if disk_pct >= _THRESHOLDS["disk_high"]:
        risk_factors.append(f"Disk nearing capacity ({disk_pct:.0f}%)")

    if thermal.get("thermal_throttling"):
        risk_factors.append("Thermal throttling active – performance is being reduced")

    swap_pct = ram.get("swap_percent", 0)
    if swap_pct > 50:
        risk_factors.append(f"High swap usage ({swap_pct:.0f}%) – RAM may be exhausted")

    if len(risk_factors) >= 3 or overall < 45:
        risk_level = "CRITICAL"
    elif len(risk_factors) == 2 or overall < 65:
        risk_level = "HIGH"
    elif len(risk_factors) == 1 or overall < 80:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "score": overall,
        "status": status,
        "risk": risk_level,
        "risk_factors": risk_factors,
        "details": scores,
    }


def _score_component(value: float, moderate_at: float, high_at: float, critical_at: float) -> float:
    """Linear penalty scoring: 100 at 0, drops to 0 at critical_at."""
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        return 80.0
    if value <= moderate_at:
        return 100.0
    if value >= critical_at:
        return max(0.0, 100.0 - (value - moderate_at) * (100 / (critical_at - moderate_at + 0.001)))
    fraction = (value - moderate_at) / (critical_at - moderate_at)
    return round(max(0.0, 100.0 - fraction * 100), 1)
