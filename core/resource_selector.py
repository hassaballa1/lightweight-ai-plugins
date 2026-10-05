import os
from typing import Optional

from interfaces.monitor_interface import SystemStatus
from system import get_monitor

# Thresholds can be overridden with environment variables.
MIN_BATTERY_PERCENT = float(os.environ.get("MIN_BATTERY_PERCENT", 30))
MIN_RAM_GB = float(os.environ.get("MIN_RAM_GB", 2))
MAX_CPU_PERCENT = float(os.environ.get("MAX_CPU_PERCENT", 80))
HEAVY_MIN_RAM_GB = float(os.environ.get("HEAVY_MIN_RAM_GB", 4))
HEAVY_MAX_CPU_PERCENT = float(os.environ.get("HEAVY_MAX_CPU_PERCENT", 50))


def decide(status: SystemStatus) -> str:
    """Pure decision logic: map a system snapshot to a model tier."""
    if status.battery_percent is not None and status.battery_percent < MIN_BATTERY_PERCENT:
        return "light"
    if status.available_ram_gb < MIN_RAM_GB:
        return "light"
    if status.cpu_percent > MAX_CPU_PERCENT:
        return "light"
    if (status.gpu_available
            and status.available_ram_gb >= HEAVY_MIN_RAM_GB
            and status.cpu_percent <= HEAVY_MAX_CPU_PERCENT):
        return "heavy"
    return "medium"


def select_model_type(status: Optional[SystemStatus] = None) -> str:
    forced = os.environ.get("FORCE_MODEL")
    if forced:
        return forced
    return decide(status or get_monitor().status())
