from __future__ import annotations

import psutil


def get_network_metrics() -> dict:
    counters = psutil.net_io_counters()
    return {
        "bytes_sent": counters.bytes_sent,
        "bytes_recv": counters.bytes_recv,
        "packets_sent": counters.packets_sent,
        "packets_recv": counters.packets_recv,
        "download_mbps": 0.0,
        "upload_mbps": 0.0,
        "status": "NORMAL",
    }
