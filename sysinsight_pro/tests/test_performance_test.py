from __future__ import annotations

import threading
import time
import unittest

from unittest.mock import patch

from sysinsight.diagnostics.performance_test import (
    MAX_DURATION_SECONDS,
    assess_test_risk,
    run_cpu_benchmark,
)


class PerformanceTestTests(unittest.TestCase):
    def test_high_cpu_load_blocks_test(self) -> None:
        risk = assess_test_risk(
            {
                "cpu": {"utilization": 90},
                "ram": {"used_percent": 40},
                "thermal": {"cpu_temperature_c": 50, "temperature_monitoring_available": True},
            }
        )

        self.assertEqual(risk["level"], "HIGH")
        self.assertTrue(any("CPU" in reason for reason in risk["reasons"]))

    def test_unavailable_temperature_sensor_requires_caution(self) -> None:
        risk = assess_test_risk(
            {
                "cpu": {"utilization": 10},
                "ram": {"used_percent": 30},
                "thermal": {"cpu_temperature_c": 0, "temperature_monitoring_available": False},
            }
        )

        self.assertEqual(risk["level"], "CAUTION")
        self.assertFalse(risk["temperature_monitored"])

    def test_benchmark_rejects_duration_above_maximum(self) -> None:
        with self.assertRaises(ValueError):
            run_cpu_benchmark(MAX_DURATION_SECONDS + 1, threading.Event())

    def test_benchmark_honors_stop_before_start(self) -> None:
        stop_event = threading.Event()
        stop_event.set()

        result = run_cpu_benchmark(1, stop_event)

        self.assertEqual(result["status"], "cancelled")
        self.assertEqual(result["operations"], 0)

    def test_benchmark_honors_stop_during_run(self) -> None:
        stop_event = threading.Event()
        result_holder: list[dict] = []

        def run_test() -> None:
            result_holder.append(run_cpu_benchmark(5, stop_event))

        worker = threading.Thread(target=run_test)
        worker.start()
        time.sleep(0.1)
        stop_event.set()
        worker.join(timeout=2)

        self.assertFalse(worker.is_alive())
        self.assertEqual(result_holder[0]["status"], "cancelled")

    def test_short_benchmark_returns_measurement(self) -> None:
        with patch(
            "sysinsight.diagnostics.performance_test.get_thermal_metrics",
            return_value={"cpu_temperature_c": 0},
        ):
            result = run_cpu_benchmark(1, threading.Event())

        self.assertEqual(result["status"], "completed")
        self.assertGreater(result["operations_per_second"], 0)


if __name__ == "__main__":
    unittest.main()
