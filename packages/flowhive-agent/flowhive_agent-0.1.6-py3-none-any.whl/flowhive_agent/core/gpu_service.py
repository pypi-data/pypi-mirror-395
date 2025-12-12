"""Simple façade around the GPU monitor singleton."""

from __future__ import annotations

from threading import Lock
from typing import List, Optional

from .gpu_monitor import GPUStats, GPUMonitor


class GPUService:
    """Shared accessor for GPU monitoring capabilities."""

    _instance: Optional["GPUService"] = None
    _lock = Lock()

    def __init__(self, monitor: Optional[GPUMonitor] = None) -> None:
        self._monitor = monitor or GPUMonitor()

    @property
    def monitor(self) -> GPUMonitor:
        return self._monitor

    @classmethod
    def instance(cls) -> "GPUService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def snapshot(self) -> List[GPUStats]:
        return self._monitor.snapshot()

    def history(self) -> List[List[GPUStats]]:
        return self._monitor.history()

    def refresh(self) -> None:
        self._monitor.refresh()

    def shutdown(self) -> None:
        self._monitor.shutdown()


