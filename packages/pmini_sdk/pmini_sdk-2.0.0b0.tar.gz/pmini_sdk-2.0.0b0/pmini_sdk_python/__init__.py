"""
PMini Zenoh SDK
================

High-level Python utilities for interacting with a PMini drone entirely over
Zenoh.  The package exposes the `Pmini` client, configuration helpers, and
common data classes representing telemetry samples.
"""

from .common import (
    Acceleration,
    AngularVelocity,
    Attitude,
    BatteryStatus,
    CommandResult,
    FlightMode,
    LidarRange,
    Position,
    Velocity,
)
from .config import DEFAULT_PMINI_CONFIG, PminiConfig
from .pmini import Pmini

__all__ = [
    "Pmini",
    "PminiConfig",
    "DEFAULT_PMINI_CONFIG",
    "Acceleration",
    "AngularVelocity",
    "Attitude",
    "BatteryStatus",
    "CommandResult",
    "FlightMode",
    "LidarRange",
    "Position",
    "Velocity",
]
