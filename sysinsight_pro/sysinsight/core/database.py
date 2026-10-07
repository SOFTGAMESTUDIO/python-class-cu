from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any

from sysinsight.core.config import DB_PATH


class Database:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or str(DB_PATH)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    captured_at TEXT NOT NULL,
                    cpu TEXT,
                    ram TEXT,
                    gpu TEXT,
                    disk TEXT,
                    network TEXT,
                    health TEXT
                )
                """
            )
            conn.commit()

    def save_snapshot(self, snapshot: dict[str, Any]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO snapshots (captured_at, cpu, ram, gpu, disk, network, health)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.utcnow().isoformat(timespec="seconds"),
                    str(snapshot.get("cpu", {})),
                    str(snapshot.get("ram", {})),
                    str(snapshot.get("gpu", {})),
                    str(snapshot.get("disk", {})),
                    str(snapshot.get("network", {})),
                    str(snapshot.get("health", {})),
                ),
            )
            conn.commit()

    def get_recent_snapshots(self, limit: int = 10) -> list[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT captured_at, cpu, ram, gpu, disk, network, health
                FROM snapshots ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [
            {
                "captured_at": captured_at,
                "cpu": cpu,
                "ram": ram,
                "gpu": gpu,
                "disk": disk,
                "network": network,
                "health": health,
            }
            for captured_at, cpu, ram, gpu, disk, network, health in rows
        ]
