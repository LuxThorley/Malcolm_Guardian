from __future__ import annotations

import logging
import threading
import time
from typing import Callable, Dict, Any, List

import psutil

from .events import SecurityEvent

logger = logging.getLogger(__name__)


class SecurityWatchdog:
    def __init__(
        self,
        interval_seconds: int,
        suspicious_cpu_threshold: float,
        suspicious_names: List[str],
        on_event: Callable[[SecurityEvent], None],
    ) -> None:
        self.interval_seconds = interval_seconds
        self.suspicious_cpu_threshold = suspicious_cpu_threshold
        self.suspicious_names = suspicious_names
        self.on_event = on_event
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._stop_flag = threading.Event()

    def start(self) -> None:
        logger.info("SecurityWatchdog starting.")
        self._thread.start()

    def stop(self) -> None:
        logger.info("SecurityWatchdog stopping.")
        self._stop_flag.set()

    def _run(self) -> None:
        while not self._stop_flag.is_set():
            try:
                self._scan_processes()
            except Exception as e:
                logger.exception("Error during security scan: %s", e)
            time.sleep(self.interval_seconds)

    def _scan_processes(self) -> None:
        for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "exe"]):
            try:
                info = proc.info
                pid = info.get("pid")
                name = (info.get("name") or "").strip()
                name_lower = name.lower()
                cpu = info.get("cpu_percent") or 0.0
                exe = (info.get("exe") or "").lower()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

            # Ignore the Windows "System Idle Process" and PID 0, which can report nonsense CPU.
            if pid == 0 or name_lower == "system idle process":
                continue

            for pattern in self.suspicious_names:
                if pattern.lower() in name_lower or pattern.lower() in exe:
                    evt = SecurityEvent(
                        event_type="suspicious_process_name",
                        description=f"Suspicious process '{name}' (PID {pid}).",
                        severity="warning",
                        data={"pid": pid, "name": name, "exe": exe},
                    )
                    logger.warning(evt.description)
                    self.on_event(evt)
                    break

            if cpu >= self.suspicious_cpu_threshold:
                evt = SecurityEvent(
                    event_type="high_cpu_process",
                    description=f"Process '{name}' (PID {pid}) is using high CPU: {cpu:.1f}%.",
                    severity="info",
                    data={"pid": pid, "name": name, "cpu": cpu},
                )
                logger.info(evt.description)
                self.on_event(evt)
