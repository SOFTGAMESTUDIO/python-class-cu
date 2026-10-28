from __future__ import annotations

from collections import deque
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any

from sysinsight.hardware.cpu import get_cpu_metrics
from sysinsight.hardware.disk import get_disk_metrics
from sysinsight.hardware.gpu import get_gpu_metrics
from sysinsight.hardware.network import get_network_metrics
from sysinsight.hardware.ram import get_ram_metrics
from sysinsight.hardware.sensors import get_thermal_metrics
from sysinsight.analysis.health_score import calculate_health_score
from sysinsight.analysis.rules import evaluate_rules
from sysinsight.analysis.anomaly import detect_anomalies
from sysinsight.optimization.recommendations import build_recommendations


@dataclass
class SystemSnapshot:
    captured_at: str
    cpu: dict[str, Any]
    ram: dict[str, Any]
    gpu: dict[str, Any]
    disk: dict[str, Any]
    network: dict[str, Any]
    thermal: dict[str, Any]
    health: dict[str, Any]
    alerts: list[str]
    anomalies: list[str]
    recommendations: list[dict[str, str]]


class Collector:
    """
    Central system data collector.

    Collects all hardware metrics, runs health scoring, alert evaluation,
    anomaly detection, and recommendation generation in one atomic call.
    Also maintains a rolling history of the last N snapshots for trend analysis.
    """

    HISTORY_SIZE = 120  # ~4 minutes at 2-second interval

    def __init__(self) -> None:
        # Rolling history: deque of (timestamp, score) pairs
        self._score_history: deque[tuple[str, float]] = deque(maxlen=self.HISTORY_SIZE)
        self._cpu_history: deque[float] = deque(maxlen=self.HISTORY_SIZE)
        self._ram_history: deque[float] = deque(maxlen=self.HISTORY_SIZE)
        self._temp_history: deque[float] = deque(maxlen=self.HISTORY_SIZE)
        self._net_down_history: deque[float] = deque(maxlen=self.HISTORY_SIZE)

    def collect(self) -> SystemSnapshot:
        """Collect all metrics and compute derived values in one call."""
        cpu = get_cpu_metrics()
        ram = get_ram_metrics()
        gpu = get_gpu_metrics()
        disk = get_disk_metrics()
        network = get_network_metrics()
        thermal = get_thermal_metrics()

        metrics = {
            "cpu": cpu,
            "ram": ram,
            "gpu": gpu,
            "disk": disk,
            "network": network,
            "thermal": thermal,
        }

        health = calculate_health_score(metrics)
        alerts = evaluate_rules(metrics)
        anomalies = detect_anomalies(metrics)
        recommendations = build_recommendations(metrics)

        # Update rolling history
        ts = datetime.now().strftime("%H:%M:%S")
        self._score_history.append((ts, health["score"]))
        self._cpu_history.append(cpu.get("utilization", 0))
        self._ram_history.append(ram.get("used_percent", 0))
        self._temp_history.append(thermal.get("cpu_temperature_c", 0))
        self._net_down_history.append(network.get("download_mbps", 0))

        return SystemSnapshot(
            captured_at=datetime.now().isoformat(timespec="seconds"),
            cpu=cpu,
            ram=ram,
            gpu=gpu,
            disk=disk,
            network=network,
            thermal=thermal,
            health=health,
            alerts=alerts,
            anomalies=anomalies,
            recommendations=recommendations,
        )

    # ------------------------------------------------------------------
    # History accessors
    # ------------------------------------------------------------------

    @property
    def score_history(self) -> list[tuple[str, float]]:
        return list(self._score_history)

    @property
    def cpu_history(self) -> list[float]:
        return list(self._cpu_history)

    @property
    def ram_history(self) -> list[float]:
        return list(self._ram_history)

    @property
    def temp_history(self) -> list[float]:
        return list(self._temp_history)

    @property
    def net_down_history(self) -> list[float]:
        return list(self._net_down_history)

    def trend_summary(self) -> dict[str, Any]:
        """Return min/max/avg trend data for each key metric."""
        return {
            "health_score": _trend(v for _, v in self._score_history),
            "cpu_util": _trend(self._cpu_history),
            "ram_pct": _trend(self._ram_history),
            "cpu_temp": _trend(self._temp_history),
            "net_down_mbps": _trend(self._net_down_history),
        }

    def serialize(self, snapshot: SystemSnapshot) -> dict[str, Any]:
        return asdict(snapshot)


def _trend(values) -> dict[str, float]:
    lst = [v for v in values if isinstance(v, (int, float))]
    if not lst:
        return {"min": 0.0, "max": 0.0, "avg": 0.0, "latest": 0.0}
    return {
        "min": round(min(lst), 1),
        "max": round(max(lst), 1),
        "avg": round(sum(lst) / len(lst), 1),
        "latest": round(lst[-1], 1),
    }
