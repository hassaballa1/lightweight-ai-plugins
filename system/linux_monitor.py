import glob
import os
import time
from typing import Optional

from interfaces.monitor_interface import MonitorInterface
from system import _common


class LinuxMonitor(MonitorInterface):
    """Reads psutil when installed, otherwise /proc and /sys."""

    def cpu_percent(self) -> float:
        value = _common.psutil_cpu_percent()
        if value is not None:
            return value
        idle1, total1 = self._cpu_times()
        time.sleep(0.5)
        idle2, total2 = self._cpu_times()
        total = total2 - total1
        return 100.0 * (1 - (idle2 - idle1) / total) if total else 0.0

    @staticmethod
    def _cpu_times():
        with open("/proc/stat") as f:
            fields = [int(x) for x in f.readline().split()[1:]]
        return fields[3] + fields[4], sum(fields)  # idle + iowait, total

    def available_ram_gb(self) -> float:
        value = _common.psutil_ram_gb()
        if value is not None:
            return value
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) / 1024 ** 2
        return 0.0

    def battery_percent(self) -> Optional[float]:
        value = _common.psutil_battery()
        if value is not None:
            return value
        for path in glob.glob("/sys/class/power_supply/BAT*/capacity"):
            with open(path) as f:
                return float(f.read().strip())
        return None

    def gpu_available(self) -> bool:
        return _common.nvidia_gpu_present() or os.path.exists("/dev/nvidia0") or os.path.exists("/dev/dri/renderD128")
