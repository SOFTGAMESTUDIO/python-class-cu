from __future__ import annotations


def detect_anomalies(metrics: dict) -> list[str]:
    anomalies: list[str] = []
    if metrics.get("thermal", {}).get("thermal_throttling"):
        anomalies.append("Thermal throttling detected")
    if metrics.get("ram", {}).get("used_percent", 0) > 90:
        anomalies.append("Possible memory pressure")
    if metrics.get("gpu", {}).get("status") == "UNAVAILABLE":
        anomalies.append("GPU telemetry unavailable")
    return anomalies
