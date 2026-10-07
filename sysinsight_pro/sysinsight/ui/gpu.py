from __future__ import annotations

from sysinsight.hardware.gpu import get_gpu_metrics


def show_gpu_panel() -> dict:
    return get_gpu_metrics()
