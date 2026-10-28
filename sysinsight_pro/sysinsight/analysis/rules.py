from __future__ import annotations

from typing import Any


def evaluate_rules(metrics: dict[str, Any]) -> list[str]:
    """
    Rule-based alert engine.  Returns human-readable alert strings
    ordered from most to least severe.
    """
    alerts: list[str] = []
    cpu = metrics.get("cpu", {})
    ram = metrics.get("ram", {})
    gpu = metrics.get("gpu", {})
    disk = metrics.get("disk", {})
    network = metrics.get("network", {})
    thermal = metrics.get("thermal", {})

    # CPU
    cpu_util = cpu.get("utilization", 0)
    if cpu_util >= 95:
        alerts.append(f"🔴 CPU critically overloaded at {cpu_util:.0f}%")
    elif cpu_util >= 85:
        alerts.append(f"🟠 High CPU load detected ({cpu_util:.0f}%)")
    elif cpu_util >= 70:
        alerts.append(f"🟡 CPU load is elevated ({cpu_util:.0f}%)")

    # Memory
    ram_pct = ram.get("used_percent", 0)
    if ram_pct >= 95:
        alerts.append(f"🔴 Memory critically exhausted ({ram_pct:.0f}%)")
    elif ram_pct >= 85:
        alerts.append(f"🟠 Severe memory pressure ({ram_pct:.0f}% used)")
    elif ram_pct >= 75:
        alerts.append(f"🟡 Memory usage is high ({ram_pct:.0f}%)")

    swap_pct = ram.get("swap_percent", 0)
    if swap_pct >= 80:
        alerts.append(f"🟠 High swap usage ({swap_pct:.0f}%) — RAM may be exhausted")
    elif swap_pct >= 50:
        alerts.append(f"🟡 Swap is in use ({swap_pct:.0f}%)")

    # Thermal
    cpu_temp = thermal.get("cpu_temperature_c", 0)
    if thermal.get("temperature_monitoring_available"):
        if cpu_temp >= 95:
            alerts.append(f"🔴 CPU temperature critically high ({cpu_temp:.0f}°C) — shutdown risk")
        elif cpu_temp >= 85:
            alerts.append(f"🟠 CPU temperature dangerously elevated ({cpu_temp:.0f}°C)")
        elif cpu_temp >= 75:
            alerts.append(f"🟡 CPU temperature is high ({cpu_temp:.0f}°C)")

    if thermal.get("thermal_throttling"):
        alerts.append("🟠 Thermal throttling active — CPU performance is being reduced")

    # GPU
    if gpu.get("status") not in ("UNAVAILABLE", None, ""):
        gpu_temp = gpu.get("temperature_c", 0)
        gpu_util = gpu.get("utilization", 0)
        if gpu_temp >= 90:
            alerts.append(f"🔴 GPU temperature critically high ({gpu_temp:.0f}°C)")
        elif gpu_temp >= 80:
            alerts.append(f"🟠 GPU temperature elevated ({gpu_temp:.0f}°C)")
        if gpu_util >= 95:
            alerts.append(f"🟡 GPU fully saturated ({gpu_util:.0f}% utilization)")

    # Disk
    disk_pct = disk.get("used_percent", 0)
    if disk_pct >= 95:
        alerts.append(f"🔴 Disk critically full ({disk_pct:.0f}%) — system instability risk")
    elif disk_pct >= 85:
        alerts.append(f"🟠 Disk nearing capacity ({disk_pct:.0f}% used)")
    elif disk_pct >= 75:
        alerts.append(f"🟡 Disk space getting low ({disk_pct:.0f}%)")

    # Network errors
    net_err = network.get("errin", 0) + network.get("errout", 0)
    net_drop = network.get("dropin", 0) + network.get("dropout", 0)
    if net_err > 1000:
        alerts.append(f"🟠 Significant network errors detected ({net_err:,})")
    if net_drop > 500:
        alerts.append(f"🟡 Network packet drops detected ({net_drop:,})")

    if network.get("download_mbps", 0) > 100:
        alerts.append(f"🟡 High network throughput ({network['download_mbps']:.1f} MB/s down)")

    return alerts
