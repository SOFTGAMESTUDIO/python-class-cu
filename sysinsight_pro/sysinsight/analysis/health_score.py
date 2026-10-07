from __future__ import annotations


def calculate_health_score(metrics: dict) -> dict:
    cpu = max(0, 100 - max(metrics.get("cpu", {}).get("utilization", 0) - 50, 0))
    ram = max(0, 100 - max(metrics.get("ram", {}).get("used_percent", 0) - 40, 0))
    gpu = max(0, 100 - max(metrics.get("gpu", {}).get("temperature_c", 0) - 60, 0))
    disk = max(0, 100 - max(metrics.get("disk", {}).get("used_percent", 0) - 35, 0))
    network = 92
    overall = round((cpu + ram + gpu + disk + network) / 5, 1)
    status = "GOOD" if overall >= 75 else "WATCH" if overall >= 55 else "CRITICAL"
    return {"score": overall, "status": status, "details": {"cpu": cpu, "ram": ram, "gpu": gpu, "disk": disk, "network": network}}
