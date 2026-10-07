from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any

from sysinsight.hardware.cpu import get_cpu_metrics
from sysinsight.hardware.disk import get_disk_metrics
from sysinsight.hardware.gpu import get_gpu_metrics
from sysinsight.hardware.network import get_network_metrics
from sysinsight.hardware.ram import get_ram_metrics
from sysinsight.hardware.sensors import get_thermal_metrics


@dataclass
class SystemSnapshot:
    captured_at: str
    cpu: dict[str, Any]
    ram: dict[str, Any]
    gpu: dict[str, Any]
    disk: dict[str, Any]
    network: dict[str, Any]
    health: dict[str, Any]
    thermal: dict[str, Any]


class Collector:
    def collect(self) -> SystemSnapshot:
        cpu = get_cpu_metrics()
        ram = get_ram_metrics()
        gpu = get_gpu_metrics()
        disk = get_disk_metrics()
        network = get_network_metrics()
        thermal = get_thermal_metrics()
        health = {
            "score": 82,
            "status": "GOOD",
            "risk": "LOW",
        }
        return SystemSnapshot(
            captured_at=datetime.utcnow().isoformat(timespec="seconds"),
            cpu=cpu,
            ram=ram,
            gpu=gpu,
            disk=disk,
            network=network,
            health=health,
            thermal=thermal,
        )

    def serialize(self, snapshot: SystemSnapshot) -> dict[str, Any]:
        return asdict(snapshot)
