from __future__ import annotations


def build_recommendations(metrics: dict) -> list[str]:
    recommendations: list[str] = []
    if metrics.get("cpu", {}).get("utilization", 0) > 80:
        recommendations.append("Reduce background processes and close unnecessary apps.")
    if metrics.get("ram", {}).get("used_percent", 0) > 75:
        recommendations.append("Close memory-heavy applications and review startup services.")
    if metrics.get("gpu", {}).get("temperature_c", 0) > 75:
        recommendations.append("Improve airflow and consider a lower power cap or fan tuning.")
    if not recommendations:
        recommendations.append("No immediate action needed; system appears stable.")
    return recommendations
