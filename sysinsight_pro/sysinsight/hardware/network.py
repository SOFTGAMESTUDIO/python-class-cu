from __future__ import annotations

import time
import psutil


# Track previous counters and timestamp for bandwidth calculation
_prev_counters: psutil._common.snetio | None = None
_prev_time: float = 0.0


def get_network_metrics() -> dict:
    global _prev_counters, _prev_time

    counters = psutil.net_io_counters()
    now = time.monotonic()

    download_mbps = 0.0
    upload_mbps = 0.0

    if _prev_counters is not None:
        elapsed = now - _prev_time
        if elapsed > 0:
            recv_delta = max(0, counters.bytes_recv - _prev_counters.bytes_recv)
            sent_delta = max(0, counters.bytes_sent - _prev_counters.bytes_sent)
            download_mbps = round(recv_delta / elapsed / (1024 * 1024), 3)
            upload_mbps = round(sent_delta / elapsed / (1024 * 1024), 3)

    _prev_counters = counters
    _prev_time = now

    # Collect active interface info
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    active_interfaces = [
        name for name, st in stats.items() if st.isup and name != "lo"
    ]

    return {
        "bytes_sent": counters.bytes_sent,
        "bytes_recv": counters.bytes_recv,
        "packets_sent": counters.packets_sent,
        "packets_recv": counters.packets_recv,
        "download_mbps": download_mbps,
        "upload_mbps": upload_mbps,
        "active_interfaces": active_interfaces[:4],  # cap at 4
        "errin": counters.errin,
        "errout": counters.errout,
        "dropin": counters.dropin,
        "dropout": counters.dropout,
        "status": "HIGH" if download_mbps > 100 or upload_mbps > 100 else "NORMAL",
    }
