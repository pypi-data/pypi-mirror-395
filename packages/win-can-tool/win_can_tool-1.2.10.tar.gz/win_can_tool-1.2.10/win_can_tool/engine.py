from __future__ import annotations

import time
import threading
from dataclasses import dataclass, field
from typing import Callable, Optional, List
import can

# ------------------------------------------------------------
# Type alias: function(now) -> payload bytes
# ------------------------------------------------------------
PayloadFunc = Callable[[float], bytes]

# Minimum sane period to avoid CPU spin (ms)
MIN_PERIOD_MS = 5


# ------------------------------------------------------------
# CAN Message Template Model
# ------------------------------------------------------------
@dataclass
class CanMessageTemplate:
    """
    Represents one scheduled CAN message.
    Contains ID, DLC, timing, and payload generator.
    """

    name: str
    arbitration_id: int
    is_extended_id: bool
    dlc: int
    payload_func: PayloadFunc
    period_ms: int
    start_delay_ms: int = 0
    max_count: Optional[int] = None  # None = repeat forever
    enabled: bool = True

    # For GUI-created raw messages
    raw_data: bytes | None = None

    # Runtime fields
    _next_due: float = field(default_factory=time.time, init=False)
    _sent_count: int = field(default=0, init=False)


# ------------------------------------------------------------
# Build python-can Message
# ------------------------------------------------------------
def build_can_message(tmpl: CanMessageTemplate, now: float) -> can.Message:
    data = tmpl.payload_func(now)
    return can.Message(
        arbitration_id=tmpl.arbitration_id,
        is_extended_id=tmpl.is_extended_id,
        dlc=tmpl.dlc,
        data=data,
    )


# ------------------------------------------------------------
# Scheduler Engine
# ------------------------------------------------------------
class CanSimEngine:
    """
    Background thread scheduler that fires CAN messages based on
    timestamp-driven scheduling.
    """

    def __init__(self, bus: can.BusABC):
        self.bus = bus
        self.messages: List[CanMessageTemplate] = []
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

    # --------------------------------------------------------
    # Set messages list and initialize timing
    # --------------------------------------------------------
    def set_messages(self, templates: List[CanMessageTemplate]) -> None:
        self.messages = templates

        now = time.time()
        for tmpl in self.messages:
            tmpl._sent_count = 0

            # Enforce minimum period to avoid runaway spin
            if tmpl.period_ms < MIN_PERIOD_MS:
                tmpl.period_ms = MIN_PERIOD_MS

            tmpl._next_due = now + tmpl.start_delay_ms / 1000.0

    # --------------------------------------------------------
    # Start scheduling thread
    # --------------------------------------------------------
    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    # --------------------------------------------------------
    # Stop safely
    # --------------------------------------------------------
    def stop(self) -> None:
        self._stop.set()

        if self._thread:
            self._thread.join()
            self._thread = None

    # --------------------------------------------------------
    # Main scheduler loop
    # --------------------------------------------------------
    def _run(self) -> None:
        """
        Evaluate all templates, send due messages, sleep until next event.
        Responsive to stop via Event.wait().
        """
        while not self._stop.is_set():
            now = time.time()
            next_wake = now + 1.0  # upper bound

            for tmpl in self.messages:
                if not tmpl.enabled:
                    continue

                if tmpl.max_count is not None and tmpl._sent_count >= tmpl.max_count:
                    continue

                # Due?
                if now >= tmpl._next_due:
                    try:
                        msg = build_can_message(tmpl, now)
                        self.bus.send(msg)
                    except Exception as err:
                        print(f"[ERROR] Failed to send {tmpl.name}: {err}")

                    tmpl._sent_count += 1
                    tmpl._next_due = now + (tmpl.period_ms / 1000.0)

                next_wake = min(next_wake, tmpl._next_due)

            # Sleep until next event or stop
            sleep_time = max(0.001, next_wake - time.time())
            self._stop.wait(timeout=sleep_time)
