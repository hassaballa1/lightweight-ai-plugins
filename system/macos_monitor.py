import os
import re
import subprocess
from typing import Optional

from interfaces.monitor_interface import MonitorInterface
from system import _common


def _cmd(*args) -> str:
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


class MacMonitor(MonitorInterface):
    """Reads psutil when installed, otherwise load average, vm_stat and pmset."""

    def cpu_percent(self) -> float:
        value = _common.psutil_cpu_percent()
        if value is not None:
            return value
        return min(100.0, 100.0 * os.getloadavg()[0] / (os.cpu_count() or 1))

    def available_ram_gb(self) -> float:
        value = _common.psutil_ram_gb()
        if value is not None:
            return value
        out = _cmd("vm_stat")
        page = re.search(r"page size of (\d+)", out)
        pages = sum(int(m) for m in re.findall(r"Pages (?:free|inactive|speculative):\s+(\d+)", out))
        return pages * int(page.group(1)) / 1024 ** 3 if page else 0.0

    def battery_percent(self) -> Optional[float]:
        value = _common.psutil_battery()
        if value is not None:
            return value
        match = re.search(r"(\d+)%", _cmd("pmset", "-g", "batt"))
        return float(match.group(1)) if match else None

    def gpu_available(self) -> bool:
        # Apple Silicon GPU via Metal is usable by ONNX Runtime's CoreML provider.
        return os.uname().machine == "arm64"
