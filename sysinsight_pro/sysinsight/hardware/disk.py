from __future__ import annotations

import psutil


def get_disk_metrics() -> dict:
    """Collect disk usage for all mounted, fixed-drive partitions."""
    partitions = []
    primary_used_percent = 0.0
    primary_free_gb = 0.0
    primary_total_gb = 0.0
    primary_used_gb = 0.0

    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue
        entry = {
            "device": part.device,
            "mountpoint": part.mountpoint,
            "fstype": part.fstype,
            "total_gb": round(usage.total / (1024 ** 3), 2),
            "used_gb": round(usage.used / (1024 ** 3), 2),
            "free_gb": round(usage.free / (1024 ** 3), 2),
            "used_percent": round(usage.percent, 1),
        }
        partitions.append(entry)

    if partitions:
        # Use the first (typically system) partition as the primary
        p = partitions[0]
        primary_used_percent = p["used_percent"]
        primary_free_gb = p["free_gb"]
        primary_total_gb = p["total_gb"]
        primary_used_gb = p["used_gb"]

    # Disk I/O counters
    try:
        io = psutil.disk_io_counters()
        read_mb = round(io.read_bytes / (1024 ** 2), 1) if io else 0.0
        write_mb = round(io.write_bytes / (1024 ** 2), 1) if io else 0.0
    except (AttributeError, OSError):
        read_mb = write_mb = 0.0

    status = "CRITICAL" if primary_used_percent >= 95 else "WARNING" if primary_used_percent >= 80 else "HEALTHY"

    return {
        "total_gb": primary_total_gb,
        "used_gb": primary_used_gb,
        "free_gb": primary_free_gb,
        "used_percent": primary_used_percent,
        "partitions": partitions,
        "total_read_mb": read_mb,
        "total_write_mb": write_mb,
        "status": status,
    }
