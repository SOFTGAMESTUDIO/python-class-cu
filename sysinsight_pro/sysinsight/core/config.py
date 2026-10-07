from __future__ import annotations

from pathlib import Path

APP_NAME = "SysInsight Pro"
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "sysinsight.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_BENCHMARKS = {
    "cpu": 0,
    "ram": 0,
    "gpu": 0,
    "disk": 0,
    "network": 0,
}
