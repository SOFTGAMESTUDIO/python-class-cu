from __future__ import annotations

import shutil
import subprocess


def get_gpu_metrics() -> dict:
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        try:
            cmd = [
                nvidia_smi,
                "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw,driver_version",
                "--format=csv,noheader,nounits",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            line = result.stdout.strip().splitlines()[0]
            parts = [item.strip() for item in line.split(",")]
            if len(parts) >= 7:
                return {
                    "name": parts[0],
                    "utilization": float(parts[1]) if parts[1] else 0.0,
                    "memory_used_gb": float(parts[2]) / 1024 if parts[2] else 0.0,
                    "memory_total_gb": float(parts[3]) / 1024 if parts[3] else 0.0,
                    "temperature_c": float(parts[4]) if parts[4] else 0.0,
                    "power_w": float(parts[5]) if parts[5] else 0.0,
                    "driver": parts[6],
                    "status": "NORMAL",
                }
        except (subprocess.CalledProcessError, IndexError, ValueError):
            pass
    return {
        "name": "GPU not detected",
        "utilization": 0.0,
        "memory_used_gb": 0.0,
        "memory_total_gb": 0.0,
        "temperature_c": 0.0,
        "power_w": 0.0,
        "driver": "unknown",
        "status": "UNAVAILABLE",
    }
