from __future__ import annotations

import math
import threading
import time
from collections.abc import Callable
from typing import Any

from sysinsight.hardware.sensors import get_thermal_metrics

MAX_DURATION_SECONDS = 15
THERMAL_STOP_C = 85.0


def assess_test_risk(metrics: dict[str, Any]) -> dict[str, Any]:
    """Assess whether current load and available sensor readings make a short CPU test inadvisable."""
    reasons: list[str] = []
    cpu = metrics.get("cpu", {})
    ram = metrics.get("ram", {})
    thermal = metrics.get("thermal", {})
    cpu_load = cpu.get("utilization", 0)
    memory_load = ram.get("used_percent", 0)
    cpu_temperature = thermal.get("cpu_temperature_c", 0)
    monitored = bool(thermal.get("temperature_monitoring_available", cpu_temperature > 0))

    if _is_number(cpu_load) and cpu_load >= 85:
        reasons.append(f"CPU is already heavily loaded ({cpu_load:.0f}%).")
    if _is_number(memory_load) and memory_load >= 90:
        reasons.append(f"Memory use is already very high ({memory_load:.0f}%).")
    if _is_number(cpu_temperature) and cpu_temperature >= 80:
        reasons.append(f"CPU temperature is elevated ({cpu_temperature:.0f}°C).")
    if not monitored:
        reasons.append("CPU temperature sensor is unavailable, so automatic thermal cut-off cannot be verified.")

    level = "HIGH" if (
        (_is_number(cpu_load) and cpu_load >= 85)
        or (_is_number(memory_load) and memory_load >= 90)
        or (_is_number(cpu_temperature) and cpu_temperature >= 80)
    ) else "CAUTION" if not monitored or (
        (_is_number(cpu_load) and cpu_load >= 70)
        or (_is_number(memory_load) and memory_load >= 80)
        or (_is_number(cpu_temperature) and cpu_temperature >= 75)
    ) else "LOW"

    return {"level": level, "reasons": reasons, "temperature_monitored": monitored}


def run_cpu_benchmark(
    duration_seconds: int,
    stop_event: threading.Event,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Run a bounded, single-threaded CPU benchmark; this is not a full-system stress test."""
    if not 1 <= duration_seconds <= MAX_DURATION_SECONDS:
        raise ValueError(f"Duration must be between 1 and {MAX_DURATION_SECONDS} seconds.")

    started = time.monotonic()
    deadline = started + duration_seconds
    last_update = started
    operations = 0
    thermal_stop = False
    checksum = 0

    while not stop_event.is_set() and time.monotonic() < deadline:
        for value in range(1, 10_001):
            checksum = (checksum * 33 + value) % 1_000_000_007
        operations += 10_000

        now = time.monotonic()
        if now - last_update >= 1:
            temperature = get_thermal_metrics().get("cpu_temperature_c", 0)
            if _is_number(temperature) and temperature >= THERMAL_STOP_C:
                thermal_stop = True
                stop_event.set()
            elapsed = min(now - started, float(duration_seconds))
            if progress_callback:
                progress_callback(
                    {
                        "elapsed_seconds": elapsed,
                        "duration_seconds": duration_seconds,
                        "cpu_temperature_c": temperature,
                    }
                )
            last_update = now

    elapsed = max(time.monotonic() - started, 0.001)
    status = "thermal_stop" if thermal_stop else "cancelled" if stop_event.is_set() else "completed"
    return {
        "status": status,
        "duration_seconds": round(elapsed, 2),
        "operations_per_second": round(operations / elapsed),
        "operations": operations,
        "checksum": checksum,
    }


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)
