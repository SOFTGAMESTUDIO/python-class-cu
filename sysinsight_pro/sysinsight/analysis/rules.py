from __future__ import annotations


def evaluate_rules(metrics: dict) -> list[str]:
    alerts: list[str] = []
    if metrics.get("cpu", {}).get("utilization", 0) > 85:
        alerts.append("High CPU load detected")
    if metrics.get("ram", {}).get("used_percent", 0) > 80:
        alerts.append("Memory pressure detected")
    if metrics.get("gpu", {}).get("temperature_c", 0) > 80:
        alerts.append("GPU temperature elevated")
    if metrics.get("disk", {}).get("used_percent", 0) > 85:
        alerts.append("Disk nearing capacity")
    if metrics.get("network", {}).get("download_mbps", 0) > 100:
        alerts.append("High network throughput")
    return alerts
