from __future__ import annotations

from pathlib import Path


def cleanup_temp_files(root: str = ".") -> dict:
    base = Path(root)
    temp_dirs = [base / "__pycache__", base / ".pytest_cache", base / ".mypy_cache"]
    removed = []
    for folder in temp_dirs:
        if folder.exists():
            for child in folder.rglob("*"):
                removed.append(str(child))
    return {"removed": removed, "count": len(removed), "status": "OK" if removed else "NO_ACTION"}
