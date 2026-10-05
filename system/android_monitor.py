from typing import Optional

from system.linux_monitor import LinuxMonitor


class AndroidMonitor(LinuxMonitor):
    """Android is Linux underneath; the battery lives at a fixed sysfs path."""

    BATTERY_PATH = "/sys/class/power_supply/battery/capacity"

    def battery_percent(self) -> Optional[float]:
        try:
            with open(self.BATTERY_PATH) as f:
                return float(f.read().strip())
        except OSError:
            return super().battery_percent()

    def gpu_available(self) -> bool:
        return False  # mobile GPUs are not targeted by the heavy model
