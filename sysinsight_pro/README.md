# SysInsight Pro

SysInsight Pro is a Python-based system diagnostics, health scoring, benchmarking, and optimization dashboard inspired by the design in the provided specification. Its Tkinter desktop dashboard presents live hardware metrics, health scoring, and alerts.

## Features

- CPU, RAM, disk, network, and GPU monitoring
- Temperature and fan analysis
- Built-in diagnostics and benchmark mode
- System health scoring and risk labeling
- Optimization recommendations and temp cleanup actions
- Local AI integration hooks for Ollama-compatible analysis
- SQLite-backed snapshot storage
- Tkinter desktop dashboard with automatic metric refresh

## Project structure

```text
sysinsight_pro/
├── main.py
├── requirements.txt
├── README.md
├── sysinsight/
│   ├── __init__.py
│   ├── __main__.py
│   ├── ai/
│   │   └── ollama.py
│   ├── analysis/
│   │   ├── anomaly.py
│   │   ├── baseline.py
│   │   ├── behavior.py
│   │   ├── health_score.py
│   │   └── rules.py
│   ├── core/
│   │   ├── collector.py
│   │   ├── config.py
│   │   └── database.py
│   ├── data/
│   │   └── .gitkeep
│   ├── diagnostics/
│   │   ├── cpu_test.py
│   │   ├── disk_test.py
│   │   ├── gpu_test.py
│   │   ├── memory_test.py
│   │   ├── network_test.py
│   │   └── thermal_test.py
│   ├── hardware/
│   │   ├── cpu.py
│   │   ├── disk.py
│   │   ├── fans.py
│   │   ├── gpu.py
│   │   ├── network.py
│   │   ├── ram.py
│   │   ├── sensors.py
│   │   └── __init__.py
│   ├── logs/
│   │   ├── log_analyzer.py
│   │   └── windows_logs.py
│   ├── optimization/
│   │   ├── recommendations.py
│   │   ├── startup.py
│   │   └── temp_cleanup.py
    └── ui/
        ├── benchmark.py
        ├── dashboard.py
        ├── diagnostics.py
        ├── gpu.py
        └── reports.py
```

## Quick start

```bash
cd sysinsight_pro
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

On Windows, run `python main.py` from the project folder to open the desktop window. The dashboard refreshes system readings every two seconds; use **Refresh** to request an immediate scan.

## Notes

- This is a functional starter prototype based on the requested design.
- GPU telemetry uses `nvidia-smi` when installed, otherwise it returns a safe placeholder.
- The app is intentionally modular so you can expand it with actual Windows APIs or local AI diagnostics later.
