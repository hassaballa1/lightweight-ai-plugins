import platform

from interfaces.monitor_interface import MonitorInterface


def is_android() -> bool:
    import os
    return "ANDROID_ROOT" in os.environ or "ANDROID_DATA" in os.environ


def get_monitor() -> MonitorInterface:
    """Return the resource monitor for the current platform."""
    if is_android():
        from system.android_monitor import AndroidMonitor
        return AndroidMonitor()
    if platform.system() == "Windows":
        from system.windows_monitor import WindowsMonitor
        return WindowsMonitor()
    if platform.system() == "Darwin":
        from system.macos_monitor import MacMonitor
        return MacMonitor()
    from system.linux_monitor import LinuxMonitor
    return LinuxMonitor()
