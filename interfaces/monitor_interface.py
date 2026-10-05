from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class SystemStatus:
    cpu_percent: float
    available_ram_gb: float
    battery_percent: Optional[float]  # None when there is no battery
    gpu_available: bool


class MonitorInterface(ABC):
    """Contract for platform-specific resource monitors."""

    @abstractmethod
    def cpu_percent(self) -> float: ...

    @abstractmethod
    def available_ram_gb(self) -> float: ...

    @abstractmethod
    def battery_percent(self) -> Optional[float]: ...

    @abstractmethod
    def gpu_available(self) -> bool: ...

    def status(self) -> SystemStatus:
        return SystemStatus(
            cpu_percent=self.cpu_percent(),
            available_ram_gb=self.available_ram_gb(),
            battery_percent=self.battery_percent(),
            gpu_available=self.gpu_available(),
        )
