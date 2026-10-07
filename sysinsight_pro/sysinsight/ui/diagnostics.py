from __future__ import annotations

from sysinsight.diagnostics.cpu_test import run_cpu_test
from sysinsight.diagnostics.disk_test import run_disk_test
from sysinsight.diagnostics.gpu_test import run_gpu_test
from sysinsight.diagnostics.memory_test import run_memory_test
from sysinsight.diagnostics.network_test import run_network_test
from sysinsight.diagnostics.thermal_test import run_thermal_test


class DiagnosticsCenter:
    def run(self) -> dict:
        tests = [
            run_cpu_test(),
            run_memory_test(),
            run_gpu_test(),
            run_disk_test(),
            run_network_test(),
            run_thermal_test(),
        ]
        return {"tests": tests, "passed": sum(1 for item in tests if item["status"] == "PASS")}
