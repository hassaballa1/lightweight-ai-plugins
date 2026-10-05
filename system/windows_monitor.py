import ctypes
from typing import Optional

from interfaces.monitor_interface import MonitorInterface
from system import _common


class _MemoryStatusEx(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


class _SystemPowerStatus(ctypes.Structure):
    _fields_ = [
        ("ACLineStatus", ctypes.c_byte), ("BatteryFlag", ctypes.c_byte),
        ("BatteryLifePercent", ctypes.c_byte), ("SystemStatusFlag", ctypes.c_byte),
        ("BatteryLifeTime", ctypes.c_ulong), ("BatteryFullLifeTime", ctypes.c_ulong),
    ]


class WindowsMonitor(MonitorInterface):
    """Reads psutil when installed, otherwise the Win32 API via ctypes."""

    def cpu_percent(self) -> float:
        value = _common.psutil_cpu_percent()
        return value if value is not None else 0.0  # no cheap ctypes fallback

    def available_ram_gb(self) -> float:
        value = _common.psutil_ram_gb()
        if value is not None:
            return value
        stat = _MemoryStatusEx()
        stat.dwLength = ctypes.sizeof(stat)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        return stat.ullAvailPhys / 1024 ** 3

    def battery_percent(self) -> Optional[float]:
        value = _common.psutil_battery()
        if value is not None:
            return value
        status = _SystemPowerStatus()
        if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
            return None
        percent = status.BatteryLifePercent & 0xFF
        return None if percent == 255 else float(percent)  # 255 = no battery

    def gpu_available(self) -> bool:
        return _common.nvidia_gpu_present()
