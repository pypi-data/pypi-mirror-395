"""Common data classes shared by the PMini Zenoh SDK."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Position:
    """Position expressed in meters."""

    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Velocity:
    """Velocity expressed in meters per second."""

    v_x: float
    v_y: float
    v_z: float


@dataclass(frozen=True)
class Attitude:
    """Attitude angles expressed in radians."""

    roll: float
    pitch: float
    yaw: float


@dataclass(frozen=True)
class AngularVelocity:
    """Angular velocity expressed in radians per second."""

    roll_rate: float
    pitch_rate: float
    yaw_rate: float


@dataclass(frozen=True)
class Acceleration:
    """Linear acceleration expressed in m/s^2."""

    ax: float
    ay: float
    az: float


@dataclass(frozen=True)
class BatteryStatus:
    """Battery telemetry."""

    voltage: float
    current: float
    remaining_percent: float


@dataclass(frozen=True)
class LidarRange:
    """Simple lidar measurement."""

    distance_m: float
    quality: int
    sensor_id: int


class FlightMode(str, Enum):
    """Placeholder flight mode enumeration."""

    STABILIZE = "STABILIZE"
    GUIDED = "GUIDED"
    LOITER = "LOITER"
    LAND = "LAND"
    RTL = "RTL"
    AUTO = "AUTO"
    ACRO = "ACRO"
    ALT_HOLD = "ALT_HOLD"


@dataclass
class CommandResult:
    """Response from a command query."""

    status: str
    message: str = ""
    data: Optional[Dict[str, Any]] = None

    @property
    def ok(self) -> bool:
        return self.status.lower() == "success"
