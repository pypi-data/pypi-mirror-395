"""High-level Pmini client that exposes convenient drone control helpers."""

from __future__ import annotations

import logging
from typing import Callable, Optional, Sequence

from .common import CommandResult, FlightMode, Position
from .config import DEFAULT_PMINI_CONFIG, PminiConfig
from .zenoh_client import ZenohClient

logger = logging.getLogger(__name__)

# MAV_FRAME constants
MAV_FRAME_LOCAL_NED = 1
MAV_FRAME_LOCAL_OFFSET_NED = 7
MAV_FRAME_BODY_NED = 8
MAV_FRAME_BODY_OFFSET_NED = 9  # Default


def _parse_frame(frame: str | int | None) -> int:
    """
    Convert frame string or number to MAV_FRAME numeric value.

    Args:
        frame: Frame as string ("local", "body", "local_offset", "body_offset")
               or integer (1, 7, 8, 9), or None for default.

    Returns:
        MAV_FRAME numeric value (defaults to 9 = BODY_OFFSET_NED).
    """
    if frame is None:
        return MAV_FRAME_BODY_OFFSET_NED

    if isinstance(frame, int):
        # Validate numeric frame values
        if frame in (1, 7, 8, 9):
            return frame
        raise ValueError(f"Invalid frame value: {frame}. Must be 1, 7, 8, or 9.")

    if isinstance(frame, str):
        frame_lower = frame.lower()
        frame_map = {
            "local": MAV_FRAME_LOCAL_NED,
            "local_offset": MAV_FRAME_LOCAL_OFFSET_NED,
            "body": MAV_FRAME_BODY_NED,
            "body_offset": MAV_FRAME_BODY_OFFSET_NED,
        }
        if frame_lower in frame_map:
            return frame_map[frame_lower]
        # Try to parse as integer string
        try:
            frame_int = int(frame_lower)
            if frame_int in (1, 7, 8, 9):
                return frame_int
        except ValueError:
            pass
        raise ValueError(
            f"Invalid frame name: {frame}. Must be one of: local, body, local_offset, body_offset, or 1, 7, 8, 9."
        )

    raise TypeError(f"Frame must be str, int, or None, got {type(frame).__name__}")


class Pmini:
    """High-level synchronous client built on top of :class:`ZenohClient`."""

    def __init__(self, config: Optional[PminiConfig] = None):
        self._config = config or DEFAULT_PMINI_CONFIG
        self._zenoh = ZenohClient(self._config)

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------
    def connect(self) -> None:
        """Open the underlying Zenoh session and start telemetry subscriptions."""
        logger.info("Connecting to PMini via Zenoh...")
        self._zenoh.connect()

    def disconnect(self) -> None:
        """Disconnect from the drone."""
        logger.info("Disconnecting from PMini...")
        self._zenoh.disconnect()

    # ------------------------------------------------------------------
    # Telemetry accessors
    # ------------------------------------------------------------------
    def get_position(self) -> Optional[Position]:
        """Return the latest position sample (if available)."""
        return self._zenoh.get_position()

    def add_position_callback(self, callback: Callable[[Position], None]) -> None:
        self._zenoh.add_position_callback(callback)

    def remove_position_callback(self, callback: Callable[[Position], None]) -> None:
        self._zenoh.remove_position_callback(callback)

    def get_status(self) -> Optional[dict]:
        return self._zenoh.get_status()

    def get_status_text(self) -> Optional[dict]:
        return self._zenoh.get_status_text()

    def add_status_text_callback(self, callback: Callable[[dict], None]) -> None:
        self._zenoh.add_status_text_callback(callback)

    def remove_status_text_callback(self, callback: Callable[[dict], None]) -> None:
        self._zenoh.remove_status_text_callback(callback)

    # ------------------------------------------------------------------
    # Command helpers
    # ------------------------------------------------------------------
    def takeoff(self, altitude_m: float = 1.0) -> CommandResult:
        return self._zenoh.send_command("takeoff", args=[altitude_m])

    def land(self) -> CommandResult:
        return self._zenoh.send_command("land")

    def arm(self) -> CommandResult:
        return self._zenoh.send_command("arm")

    def disarm(self) -> CommandResult:
        return self._zenoh.send_command("disarm")

    def set_mode(self, mode: FlightMode | str) -> CommandResult:
        mode_name = mode.value if isinstance(mode, FlightMode) else str(mode)
        return self._zenoh.send_command("mode", extra_payload={"args": [mode_name]})

    def emergency_stop(self) -> CommandResult:
        return self._zenoh.send_command("emergency_stop")

    def reboot(self) -> CommandResult:
        return self._zenoh.send_command("reboot")

    def goto_local_ned(self, x: float, y: float, z: float, yaw: float | None = 0.0) -> CommandResult:
        """Legacy method: goto with BODY_OFFSET_NED frame (default)."""
        return self.goto(x, y, z, yaw, frame=MAV_FRAME_BODY_OFFSET_NED)

    def goto(
        self,
        x: float,
        y: float,
        z: float,
        yaw: float | None = 0.0,
        frame: str | int | None = None,
    ) -> CommandResult:
        """
        Send a goto command to move to a position.

        Args:
            x: X coordinate (meters)
            y: Y coordinate (meters)
            z: Z coordinate (meters, up is positive)
            yaw: Optional yaw angle (radians). Defaults to 0.0.
            frame: Frame type as string ("local", "body", "local_offset", "body_offset")
                   or integer (1, 7, 8, 9). Defaults to 9 (BODY_OFFSET_NED).

        Returns:
            CommandResult with status and message.
        """
        frame_value = _parse_frame(frame)
        args = [x, y, z]
        if yaw is not None:
            args.append(yaw)
        args.append(frame_value)
        return self._zenoh.send_command("goto", args=args)

    def set_velocity_local_ned(self, v_x: float, v_y: float, v_z: float, yaw: float | None = 0.0) -> CommandResult:
        args = [v_x, v_y, v_z]
        if yaw is not None:
            args.append(yaw)
        return self._zenoh.send_command("velocity", args=args)

    def log_list(self) -> CommandResult:
        return self._zenoh.send_command("log_list")

    def log_download(self, log_id: int, max_bytes: int | None = None) -> CommandResult:
        args = [int(log_id)]
        if max_bytes is not None:
            limit = int(max_bytes)
            if limit > 0:
                args.append(limit)
        return self._zenoh.send_command("log_download", args=args)

    def log_download_to_file(
        self,
        log_id: int,
        path: str,
        *,
        max_bytes: int | None = None,
        timeout: float = 120.0,
        progress_callback: Optional[Callable[[dict], None]] = None,
    ) -> CommandResult:
        return self._zenoh.download_log_to_file(
            log_id,
            path,
            max_bytes=max_bytes,
            timeout=timeout,
            progress_callback=progress_callback,
        )

    def log_clear(self) -> CommandResult:
        """Erase all logs stored on the vehicle."""
        return self._zenoh.clear_logs()

    def custom_command(
        self, command: str, args: Optional[Sequence[float]] = None, extra_payload: Optional[dict] = None
    ) -> CommandResult:
        """Send a custom command not covered by helpers."""
        return self._zenoh.send_command(command, args=args, extra_payload=extra_payload)
