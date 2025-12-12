import argparse
import time

from .bus import open_bus
from .engine import CanSimEngine
from .profiles import (
    PROFILE_BUILDERS,
    DEFAULT_PROFILE_NAME,
    build_default_profile,
    reset_motion_origin,
)


def main():
    print("CLI main() started")

    parser = argparse.ArgumentParser(description="CAN Simulator (CLI Mode)")
    parser.add_argument("--interface", default="neovi", help="python-can interface name")
    parser.add_argument("--channel", default="1", help="CAN channel (e.g., 1, 'can0')")
    parser.add_argument("--bitrate", type=int, default=250000, help="CAN bitrate")
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE_NAME,
        choices=list(PROFILE_BUILDERS.keys()),
        help="Select which message profile to use",
    )

    args = parser.parse_args()

    print(f"Connecting to CAN... interface={args.interface}, channel={args.channel}, bitrate={args.bitrate}")
    print(f"Using profile: {args.profile}")

    # Load profile
    profile_builder = PROFILE_BUILDERS.get(args.profile, build_default_profile)
    messages = profile_builder()

    # Reset heading/lat/lon timer whenever CLI runs
    reset_motion_origin()

    # Open bus
    try:
        bus = open_bus(args.interface, args.channel, args.bitrate)
    except Exception as e:
        print(f"ERROR: Failed to open bus: {e}")
        return

    # Start engine
    engine = CanSimEngine(bus)
    engine.set_messages(messages)

    print(f"Starting engine with {len(messages)} messages:")
    for m in messages:
        print(f"  - {m.name} (ID 0x{m.arbitration_id:08X}, period {m.period_ms} ms)")

    engine.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")

    # Clean shutdown
    try:
        engine.stop()
    except Exception:
        pass

    try:
        bus.shutdown()
    except Exception:
        pass

    print("CLI simulator stopped cleanly.")


if __name__ == "__main__":
    main()
