from __future__ import annotations

import math
from typing import Any


def detect_anomalies(metrics: dict[str, Any]) -> list[str]:
    """
    Detect anomalous system conditions that rule-based thresholds might miss.
    Returns a list of anomaly description strings.
    """
    anomalies: list[str] = []
    cpu = metrics.get("cpu", {})
    ram = metrics.get("ram", {})
    gpu = metrics.get("gpu", {})
    disk = metrics.get("disk", {})
    thermal = metrics.get("thermal", {})
    network = metrics.get("network", {})

    # Thermal throttling
    if thermal.get("thermal_throttling"):
        anomalies.append("Thermal throttling detected — CPU is being clock-limited by heat")

    # Sensor absent but high load
    cpu_util = cpu.get("utilization", 0)
    if not thermal.get("temperature_monitoring_available") and cpu_util > 80:
        anomalies.append("High CPU load with no temperature monitoring — cannot assess thermal risk")

    # Memory exhaustion
    if ram.get("used_percent", 0) > 90:
        anomalies.append("Severe memory pressure — system may become unstable")

    # Swap pressure while RAM still available
    if ram.get("swap_percent", 0) > 60 and ram.get("used_percent", 0) < 70:
        anomalies.append("Unexpectedly high swap usage despite moderate RAM — investigate memory fragmentation")

    # GPU telemetry absent
    if gpu.get("status") == "UNAVAILABLE":
        anomalies.append("GPU telemetry unavailable — discrete GPU may not be present or driver is missing")

    # Network error burst
    errs = network.get("errin", 0) + network.get("errout", 0)
    drops = network.get("dropin", 0) + network.get("dropout", 0)
    if errs > 5000:
        anomalies.append(f"High network error count ({errs:,}) — check NIC driver or cable quality")
    if drops > 2000:
        anomalies.append(f"High packet drop count ({drops:,}) — possible network congestion or NIC issue")

    # Disk critically near full
    for part in disk.get("partitions", []):
        if part.get("used_percent", 0) >= 95:
            anomalies.append(f"Partition {part['mountpoint']} is {part['used_percent']:.0f}% full — immediate action required")

    # Per-core imbalance (one core burning while others idle)
    per_core = cpu.get("per_core_percent", [])
    if len(per_core) >= 2:
        max_c = max(per_core)
        avg_c = sum(per_core) / len(per_core)
        if max_c >= 95 and avg_c < 50:
            anomalies.append(f"Single core hotspot detected (core at {max_c:.0f}% while average is {avg_c:.0f}%)")

    return anomalies
