from __future__ import annotations

from typing import Any


def build_recommendations(metrics: dict[str, Any]) -> list[dict[str, str]]:
    """
    Generate actionable, prioritised recommendations based on current metrics.
    Each recommendation is a dict with keys: priority (HIGH/MEDIUM/LOW),
    category, title, and action.
    """
    recs: list[dict[str, str]] = []
    cpu = metrics.get("cpu", {})
    ram = metrics.get("ram", {})
    gpu = metrics.get("gpu", {})
    disk = metrics.get("disk", {})
    thermal = metrics.get("thermal", {})
    network = metrics.get("network", {})

    cpu_util = cpu.get("utilization", 0)
    ram_pct = ram.get("used_percent", 0)
    swap_pct = ram.get("swap_percent", 0)
    disk_pct = disk.get("used_percent", 0)
    cpu_temp = thermal.get("cpu_temperature_c", 0)
    gpu_temp = gpu.get("temperature_c", 0)

    # CPU
    if cpu_util >= 95:
        recs.append({"priority": "HIGH", "category": "CPU", "title": "Critical CPU overload",
                     "action": "Kill or suspend non-essential processes immediately via Task Manager."})
    elif cpu_util >= 80:
        recs.append({"priority": "MEDIUM", "category": "CPU", "title": "High CPU usage",
                     "action": "Identify heavy background tasks; consider closing browser tabs, antivirus scans, or indexing jobs."})
    elif cpu_util >= 60:
        recs.append({"priority": "LOW", "category": "CPU", "title": "Elevated CPU load",
                     "action": "Monitor for sustained high load; review startup programs with Task Manager > Startup."})

    # Memory
    if ram_pct >= 90:
        recs.append({"priority": "HIGH", "category": "Memory", "title": "Memory critically exhausted",
                     "action": "Close all non-essential applications. Restart memory-heavy apps or add more RAM."})
    elif ram_pct >= 80:
        recs.append({"priority": "MEDIUM", "category": "Memory", "title": "Memory pressure",
                     "action": "Close idle browser tabs and heavy applications. Review services using Task Manager."})

    if swap_pct >= 70:
        recs.append({"priority": "HIGH", "category": "Memory", "title": "Heavy swap usage",
                     "action": "System is using disk as RAM — severely impacts performance. Free RAM immediately or upgrade RAM."})
    elif swap_pct >= 40:
        recs.append({"priority": "MEDIUM", "category": "Memory", "title": "Moderate swap usage",
                     "action": "Consider increasing virtual memory size in System Properties > Advanced > Performance."})

    # Thermal
    if thermal.get("temperature_monitoring_available"):
        if cpu_temp >= 90:
            recs.append({"priority": "HIGH", "category": "Thermal", "title": "CPU overheating",
                         "action": "Stop intensive tasks immediately. Clean dust from heatsink/fans. Reapply thermal paste if possible."})
        elif cpu_temp >= 80:
            recs.append({"priority": "MEDIUM", "category": "Thermal", "title": "CPU running hot",
                         "action": "Improve case airflow. Check that all fans are spinning. Reduce CPU-intensive workloads."})
        elif cpu_temp >= 70:
            recs.append({"priority": "LOW", "category": "Thermal", "title": "CPU temperature elevated",
                         "action": "Ensure adequate ventilation around the computer. Monitor trend over next few minutes."})
    else:
        recs.append({"priority": "LOW", "category": "Thermal", "title": "No temperature sensors detected",
                     "action": "Install a hardware monitor (e.g., HWiNFO64) for accurate thermal telemetry."})

    if thermal.get("thermal_throttling"):
        recs.append({"priority": "HIGH", "category": "Thermal", "title": "Thermal throttling active",
                     "action": "CPU is self-limiting performance to prevent damage. Reduce load and improve cooling immediately."})

    # Disk
    if disk_pct >= 95:
        recs.append({"priority": "HIGH", "category": "Disk", "title": "Disk critically full",
                     "action": "Delete temporary files (run Disk Cleanup), empty Recycle Bin, and move large files to external storage."})
    elif disk_pct >= 85:
        recs.append({"priority": "MEDIUM", "category": "Disk", "title": "Low disk space",
                     "action": "Run Disk Cleanup, uninstall unused applications, and check for large log or cache files."})

    # GPU
    if gpu.get("status") not in ("UNAVAILABLE", None):
        if gpu_temp >= 85:
            recs.append({"priority": "HIGH", "category": "GPU", "title": "GPU overheating",
                         "action": "Stop GPU-intensive workloads. Clean GPU fans and heatsink. Check driver for thermal profile settings."})
        elif gpu_temp >= 75:
            recs.append({"priority": "LOW", "category": "GPU", "title": "GPU temperature elevated",
                         "action": "Ensure case has good airflow. Consider a custom fan curve with MSI Afterburner or similar."})

    # Network
    net_err = network.get("errin", 0) + network.get("errout", 0)
    if net_err > 1000:
        recs.append({"priority": "MEDIUM", "category": "Network", "title": "Network errors detected",
                     "action": "Check Ethernet cable or Wi-Fi signal quality. Update NIC drivers. Disable/re-enable the adapter."})

    if not recs:
        recs.append({"priority": "LOW", "category": "General", "title": "System healthy",
                     "action": "No immediate action needed. All metrics are within normal operating parameters."})

    # Sort by priority
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    recs.sort(key=lambda r: priority_order.get(r["priority"], 3))
    return recs
