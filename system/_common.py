import shutil
from typing import Optional

try:
    import psutil
except ImportError:  # psutil is optional; monitors fall back to platform APIs
    psutil = None


def psutil_cpu_percent() -> Optional[float]:
    return psutil.cpu_percent(interval=0.5) if psutil else None


def psutil_ram_gb() -> Optional[float]:
    return psutil.virtual_memory().available / 1024 ** 3 if psutil else None


def psutil_battery() -> Optional[float]:
    if not psutil or not hasattr(psutil, "sensors_battery"):
        return None
    battery = psutil.sensors_battery()
    return float(battery.percent) if battery else None


def nvidia_gpu_present() -> bool:
    return shutil.which("nvidia-smi") is not None
