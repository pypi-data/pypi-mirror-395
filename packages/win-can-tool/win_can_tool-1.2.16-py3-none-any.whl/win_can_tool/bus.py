from __future__ import annotations
import can
from typing import Any, Dict, Union

def open_bus(interface: str, channel: Union[str, int], bitrate: int | None = None) -> can.BusABC:
    """
    Opens a CAN bus using python-can.

    Automatically casts the channel to an int when appropriate,
    since some python-can backends (like Kvaser/PCAN) expect channel=1
    while others (like socketcan) expect channel='can0'.

    Parameters:
        interface: python-can interface name ('neovi', 'kvaser', 'pcan', 'socketcan', etc.)
        channel: channel identifier, may be '1', 1, 'can0', etc.
        bitrate: bus bitrate (ignored by some interfaces)

    Returns:
        A python-can BusABC instance.

    Raises:
        RuntimeError: if the bus fails to open.
    """

    # Auto-convert numeric strings to int (e.g., "1" → 1)
    if isinstance(channel, str) and channel.isdigit():
        channel = int(channel)

    kwargs: Dict[str, Any] = {
        "interface": interface,
        "channel": channel,
    }

    if bitrate is not None:
        kwargs["bitrate"] = bitrate

    try:
        return can.Bus(**kwargs)  # type: ignore
    except Exception as e:
        raise RuntimeError(f"Failed to open CAN bus ({interface}, {channel}, {bitrate}): {e}")
