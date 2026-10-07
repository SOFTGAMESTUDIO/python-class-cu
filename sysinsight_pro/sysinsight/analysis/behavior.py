from __future__ import annotations


def compare_to_baseline(current: dict, baseline: dict) -> dict:
    deviations = {}
    for key in ("cpu", "ram", "gpu", "disk", "network"):
        current_value = current.get(key, {})
        baseline_value = baseline.get(key, {})
        if isinstance(current_value, dict):
            for subkey, value in current_value.items():
                if isinstance(value, (int, float)):
                    base = baseline_value.get(subkey, value)
                    deviations[f"{key}.{subkey}"] = round(value - base, 2)
    return {"deviations": deviations, "status": "STABLE" if not deviations else "CHANGED"}
