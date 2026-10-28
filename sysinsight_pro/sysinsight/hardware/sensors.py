from __future__ import annotations

import psutil


def get_thermal_metrics() -> dict:
    cpu_temperature = 0.0
    gpu_temperature = 0.0
    all_sensors: list[dict] = []

    try:
        sensor_groups = psutil.sensors_temperatures()
    except (AttributeError, NotImplementedError, OSError):
        sensor_groups = {}

    for sensor_name, readings in sensor_groups.items():
        for reading in readings:
            temperature = reading.current
            if temperature is None:
                continue
            label = f"{sensor_name} {reading.label}".lower()
            all_sensors.append({
                "name": sensor_name,
                "label": reading.label or sensor_name,
                "current": round(temperature, 1),
                "high": round(reading.high, 1) if reading.high else None,
                "critical": round(reading.critical, 1) if reading.critical else None,
            })
            if "cpu" in label or "package" in label or "tctl" in label or "core" in label:
                cpu_temperature = max(cpu_temperature, temperature)
            elif "gpu" in label or "graphics" in label:
                gpu_temperature = max(gpu_temperature, temperature)

    available = cpu_temperature > 0 or gpu_temperature > 0

    # Fan sensors
    fan_speeds: list[dict] = []
    try:
        fan_groups = psutil.sensors_fans()
        for fan_name, fan_readings in fan_groups.items():
            for fr in fan_readings:
                fan_speeds.append({
                    "name": fan_name,
                    "label": fr.label or fan_name,
                    "rpm": fr.current,
                })
    except (AttributeError, NotImplementedError, OSError):
        pass

    # Thermal throttling detection (basic heuristic)
    thermal_throttling = (
        available and cpu_temperature >= 95
    )

    # Determine status
    if available:
        if cpu_temperature >= 95:
            status = "CRITICAL"
        elif cpu_temperature >= 80:
            status = "HOT"
        elif cpu_temperature >= 65:
            status = "WARM"
        else:
            status = "COOL"
    else:
        status = "UNAVAILABLE"

    return {
        "cpu_temperature_c": round(cpu_temperature, 1),
        "gpu_temperature_c": round(gpu_temperature, 1),
        "all_sensors": all_sensors,
        "fan_speeds": fan_speeds,
        "thermal_throttling": thermal_throttling,
        "status": status,
        "temperature_monitoring_available": available,
    }
