from __future__ import annotations

from typing import List
import time
from math import radians, sin, cos, pi

from .engine import CanMessageTemplate


# ============================================================
# General simulator settings
# ============================================================

SA = 0x00  # Default source address for this simulator ECU


# ============================================================
# Live “knobs” (updated by GUI)
# ============================================================

# GNSS / vehicle motion
LAT_DEG = 46.810000
LON_DEG = -96.810000
COG_DEG = 123.0        # degrees (0°=north, 90°=east)
SOG_MS = 4.2           # speed over ground (m/s)
ALT_M = 299.0
HDOP = 0.9
VDOP = 1.1

# Engine / fuel
ENGINE_HOURS = 1234.5
FUEL_PERCENT = 45.0
FUEL_RATE_LPH = 18.0
FUEL_ECON_KM_PER_L = 1.8
ENGINE_LOAD_PCT = 72.0
TOTAL_FUEL_USED_L = 4567.0
ENGINE_COOLANT_TEMP_C = 82.0

# Temps / pressures
OIL_TEMP_C = 90.0
OIL_PRESS_KPA = 350.0
FUEL_TEMP_C = 40.0
COOLANT_PRESS_KPA = 120.0

# Transmission
TRANS_TEMP_C = 75.0
TRANS_PRESS_KPA = 250.0

# Combine yield demo
YIELD_KG_PER_S = 15.0
MOISTURE_PCT = 16.5


# ============================================================
# GNSS motion integrator state
# ============================================================

SIM_START_TIME: float | None = None
EARTH_RADIUS_M = 6_371_000.0


def reset_motion_origin(start_time: float | None = None) -> None:
    """
    Reset the base time used to compute moving GNSS position.
    Called whenever the simulator starts or the user changes profile.
    """
    global SIM_START_TIME
    SIM_START_TIME = start_time if start_time is not None else time.time()


def compute_moving_lat_lon(now: float) -> tuple[float, float]:
    """
    Dead-reckoning:
      - Start from LAT_DEG, LON_DEG
      - Move at SOG_MS
      - Heading COG_DEG
    Small-angle approximation is plenty accurate for this simulator.
    """
    global SIM_START_TIME

    if SIM_START_TIME is None:
        SIM_START_TIME = now

    dt = max(0.0, now - SIM_START_TIME)
    distance = SOG_MS * dt

    heading_rad = radians(COG_DEG)
    d_north = distance * cos(heading_rad)
    d_east = distance * sin(heading_rad)

    lat0_rad = radians(LAT_DEG)

    dlat_rad = d_north / EARTH_RADIUS_M
    dlon_rad = d_east / (EARTH_RADIUS_M * cos(lat0_rad))

    lat = LAT_DEG + (dlat_rad * 180.0 / pi)
    lon = LON_DEG + (dlon_rad * 180.0 / pi)
    return lat, lon


# ============================================================
# Encoding helpers
# ============================================================

def encode_lat_lon(deg: float) -> int:
    """1e-7 deg J1939/NMEA2000 format."""
    return int(deg * 1e7)


def encode_double(value: float, resolution: float) -> int:
    return int(value / resolution)


def pack_u32(value: int) -> list[int]:
    return [
        (value >> 0) & 0xFF,
        (value >> 8) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 24) & 0xFF,
    ]


def pack_u16(value: int) -> list[int]:
    return [(value >> 0) & 0xFF, (value >> 8) & 0xFF]


def pack_u8(value: int) -> list[int]:
    return [value & 0xFF]


# ============================================================
# Core PGN builders (NMEA2k + J1939 style)
# ============================================================

def pgn_129025_position_rapid(lat_deg: float, lon_deg: float) -> list[int]:
    lat = encode_lat_lon(lat_deg)
    lon = encode_lat_lon(lon_deg)
    return pack_u32(lat) + pack_u32(lon)


def pgn_129026_cog_sog(cog_deg: float, sog_ms: float) -> list[int]:
    cog_rad = radians(cog_deg)
    cog_raw = int(cog_rad / 1e-4)
    sog_raw = int(sog_ms / 0.01)
    return pack_u16(cog_raw) + pack_u16(sog_raw) + [0xFF] * 4


def pgn_129029_gnss_detailed(lat_deg, lon_deg, alt_m, hdop, vdop) -> list[int]:
    """
    Returns a 32-byte GNSS full payload (stubbed into 8 bytes later).
    This simulates a simplified NMEA2000 fast-packet block.
    """
    lat = encode_lat_lon(lat_deg)
    lon = encode_lat_lon(lon_deg)
    alt = int(alt_m * 100)

    return (
        pack_u32(lat)
        + pack_u32(lon)
        + pack_u32(alt)
        + pack_u16(int(hdop * 100))
        + pack_u16(int(vdop * 100))
        + [0] * 10
    )[:32]


def pgn_65253_engine_hours(hours: float) -> list[int]:
    raw = int(hours / 0.05)
    return pack_u32(raw) + [0xFF] * 4


def pgn_65276_fuel_level(percent: float) -> list[int]:
    raw = int(percent / 0.4)
    return [raw & 0xFF] + [0xFF] * 7


def pgn_65262_engine_temp(temp_c: float) -> list[int]:
    raw = int(temp_c + 40)
    return [raw & 0xFF] + [0xFF] * 7


def pgn_65267_vehicle_position(lat_deg: float, lon_deg: float) -> list[int]:
    """
    PGN 65267 - Vehicle Position
    Encodes lat/lon (1e-7 deg) into 8 bytes total.
    """
    lat = encode_lat_lon(lat_deg)
    lon = encode_lat_lon(lon_deg)
    return pack_u32(lat)[:4] + pack_u32(lon)[:4]


def pgn_65266_fuel_rate_economy(rate_lph, econ_km_per_l) -> list[int]:
    rate_raw = int(rate_lph / 0.1)
    econ_raw = int(econ_km_per_l / 0.01)
    return pack_u16(rate_raw) + pack_u16(econ_raw) + [0xFF] * 4


def pgn_61443_engine_load(load_pct: float) -> list[int]:
    raw = max(0, min(250, int(load_pct)))
    return [raw] + [0xFF] * 7


def pgn_65257_total_fuel_used(total_l: float) -> list[int]:
    raw = int(total_l / 0.5)
    return pack_u32(raw) + [0xFF] * 4


def pgn_65263_engine_pressures_temps(
    oil_temp_c, oil_press_kpa, fuel_temp_c, coolant_press_kpa, coolant_temp_c
) -> list[int]:
    return [
        int(oil_temp_c + 40) & 0xFF,
        int(oil_press_kpa / 4) & 0xFF,
        int(fuel_temp_c + 40) & 0xFF,
        int(coolant_press_kpa / 4) & 0xFF,
        int(coolant_temp_c + 40) & 0xFF,
        0xFF,
        0xFF,
        0xFF,
    ]


def pgn_65272_transmission_temp_pressure(temp_c, press_kpa) -> list[int]:
    return [
        int(temp_c + 40) & 0xFF,
        int(press_kpa / 4) & 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF
    ]


def pgn_yield_basic(yield_kg_per_s, moisture_pct) -> list[int]:
    flow_raw = int(yield_kg_per_s / 0.1)
    moist_raw = int(moisture_pct / 0.1)
    return pack_u16(flow_raw) + pack_u16(moist_raw) + [0xFF] * 4


# ============================================================
# J1939 ID builder
# ============================================================

def build_j1939_id(priority: int, pgn: int, sa: int) -> int:
    return (priority << 26) | (pgn << 8) | sa


# ============================================================
# Profiles
# ============================================================

def build_default_profile() -> List[CanMessageTemplate]:
    """
    Tractor-style default simulator profile.
    Includes GNSS, engine, fuel, and diagnostics PGNs.
    """
    messages: List[CanMessageTemplate] = []

    # ----- GNSS: 65267 -----
    def payload_65267(now):
        lat, lon = compute_moving_lat_lon(now)
        return bytes(pgn_65267_vehicle_position(lat, lon))

    messages.append(
        CanMessageTemplate(
            name="PGN 65267 - Vehicle Position",
            arbitration_id=build_j1939_id(6, 65267, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=payload_65267,
            period_ms=200,
        )
    )

    # ----- 129025 -----
    def payload_129025(now):
        lat, lon = compute_moving_lat_lon(now)
        return bytes(pgn_129025_position_rapid(lat, lon))

    messages.append(
        CanMessageTemplate(
            name="PGN 129025 - Position Rapid",
            arbitration_id=build_j1939_id(6, 129025, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=payload_129025,
            period_ms=200,
        )
    )

    # ----- 129026 -----
    messages.append(
        CanMessageTemplate(
            name="PGN 129026 - COG & SOG Rapid",
            arbitration_id=build_j1939_id(6, 129026, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_129026_cog_sog(COG_DEG, SOG_MS)),
            period_ms=200,
        )
    )

    # ----- 129029 (stubbed) -----
    def payload_129029(now):
        lat, lon = compute_moving_lat_lon(now)
        full = pgn_129029_gnss_detailed(lat, lon, ALT_M, HDOP, VDOP)
        return bytes(full[:8])  # stubbed

    messages.append(
        CanMessageTemplate(
            name="PGN 129029 - GNSS Position (stubbed)",
            arbitration_id=build_j1939_id(6, 129029, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=payload_129029,
            period_ms=1000,
        )
    )

    # ----- Fuel Level -----
    messages.append(
        CanMessageTemplate(
            name="PGN 65276 - Fuel Level",
            arbitration_id=build_j1939_id(6, 65276, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_65276_fuel_level(FUEL_PERCENT)),
            period_ms=200,
        )
    )

    # ----- Fuel Rate/Economy -----
    messages.append(
        CanMessageTemplate(
            name="PGN 65266 - Fuel Rate / Economy",
            arbitration_id=build_j1939_id(6, 65266, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_65266_fuel_rate_economy(FUEL_RATE_LPH, FUEL_ECON_KM_PER_L)),
            period_ms=1000,
        )
    )

    # ----- Engine Load -----
    messages.append(
        CanMessageTemplate(
            name="PGN 61443 - Engine Load",
            arbitration_id=build_j1939_id(3, 61443, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_61443_engine_load(ENGINE_LOAD_PCT)),
            period_ms=200,
        )
    )

    # ----- Engine Hours -----
    messages.append(
        CanMessageTemplate(
            name="PGN 65253 - Engine Hours",
            arbitration_id=build_j1939_id(6, 65253, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_65253_engine_hours(ENGINE_HOURS)),
            period_ms=2000,
        )
    )

    # ----- Total Fuel Used -----
    messages.append(
        CanMessageTemplate(
            name="PGN 65257 - Total Fuel Used",
            arbitration_id=build_j1939_id(6, 65257, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_65257_total_fuel_used(TOTAL_FUEL_USED_L)),
            period_ms=5000,
        )
    )

    # ----- Coolant Temp (basic) -----
    messages.append(
        CanMessageTemplate(
            name="PGN 65262 - Engine Coolant Temp (basic)",
            arbitration_id=build_j1939_id(6, 65262, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_65262_engine_temp(ENGINE_COOLANT_TEMP_C)),
            period_ms=200,
        )
    )

    # ----- Pressures & Temps -----
    messages.append(
        CanMessageTemplate(
            name="PGN 65263 - Engine Pressures & Temps",
            arbitration_id=build_j1939_id(6, 65263, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(
                pgn_65263_engine_pressures_temps(
                    OIL_TEMP_C,
                    OIL_PRESS_KPA,
                    FUEL_TEMP_C,
                    COOLANT_PRESS_KPA,
                    ENGINE_COOLANT_TEMP_C,
                )
            ),
            period_ms=500,
        )
    )

    # ----- Transmission -----
    messages.append(
        CanMessageTemplate(
            name="PGN 65272 - Transmission Temp/Pressure",
            arbitration_id=build_j1939_id(6, 65272, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_65272_transmission_temp_pressure(TRANS_TEMP_C, TRANS_PRESS_KPA)),
            period_ms=1000,
        )
    )

    return messages


def build_gnss_only_profile() -> List[CanMessageTemplate]:
    """
    Minimal GNSS-only simulator profile.
    """
    messages: List[CanMessageTemplate] = []

    messages.append(
        CanMessageTemplate(
            name="PGN 65267 - Vehicle Position",
            arbitration_id=build_j1939_id(6, 65267, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_65267_vehicle_position(LAT_DEG, LON_DEG)),
            period_ms=200,
        )
    )

    messages.append(
        CanMessageTemplate(
            name="PGN 129025 - Position Rapid",
            arbitration_id=build_j1939_id(6, 129025, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_129025_position_rapid(LAT_DEG, LON_DEG)),
            period_ms=200,
        )
    )

    messages.append(
        CanMessageTemplate(
            name="PGN 129026 - COG & SOG Rapid",
            arbitration_id=build_j1939_id(6, 129026, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_129026_cog_sog(COG_DEG, SOG_MS)),
            period_ms=200,
        )
    )

    messages.append(
        CanMessageTemplate(
            name="PGN 129029 - GNSS Position (stubbed)",
            arbitration_id=build_j1939_id(6, 129029, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(
                pgn_129029_gnss_detailed(LAT_DEG, LON_DEG, ALT_M, HDOP, VDOP)[:8]
            ),
            period_ms=1000,
        )
    )

    return messages


def build_combine_profile() -> List[CanMessageTemplate]:
    """
    Combine profile:
      - Includes all tractor messages
      - Adds simple yield message (demo)
    """
    messages = build_default_profile()

    yield_pgn = 0xFDD2  # demo PGN placeholder

    messages.append(
        CanMessageTemplate(
            name=f"Yield Demo - PGN 0x{yield_pgn:04X}",
            arbitration_id=build_j1939_id(6, yield_pgn, SA),
            is_extended_id=True,
            dlc=8,
            payload_func=lambda now: bytes(pgn_yield_basic(YIELD_KG_PER_S, MOISTURE_PCT)),
            period_ms=200,
        )
    )

    return messages


# Profile registry
PROFILE_BUILDERS = {
    "Tractor (default)": build_default_profile,
    "GNSS only": build_gnss_only_profile,
    "Combine with yield demo": build_combine_profile,
}

DEFAULT_PROFILE_NAME = "Tractor (default)"
