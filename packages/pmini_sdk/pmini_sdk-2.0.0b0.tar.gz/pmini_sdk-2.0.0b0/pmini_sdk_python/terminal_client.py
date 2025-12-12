"""Interactive terminal client for controlling a PMini drone."""

from __future__ import annotations

import cmd
import logging
import shlex
import sys
import time
from typing import Callable, Optional

from .common import Position
from .config import PminiConfig
from .pmini import Pmini


class PminiTerminal(cmd.Cmd):
    intro = "PMini Zenoh Terminal\n" "====================\n" "Type 'help' for a list of commands. Use 'quit' to exit.\n"
    prompt = "pmini> "

    def __init__(self):
        super().__init__()
        self._client: Optional[Pmini] = None
        self._position_callback: Optional[Callable[[Position], None]] = None
        self._status_text_callback: Optional[Callable[[dict], None]] = None

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------
    def do_connect(self, arg: str) -> None:
        """
        connect [mode=peer] [listen=udp/... ] [connect=tcp/...] [iface=wlan0]

        Establish a Zenoh session with the drone.
        """

        if self._client:
            print("Already connected. Use 'disconnect' first if needed.")
            return

        config = PminiConfig()
        tokens = [token.strip() for token in arg.split() if token.strip()]
        for token in tokens:
            key, _, value = token.partition("=")
            if key == "mode" and value:
                config.mode = value
            elif key == "listen" and value:
                config.listen_endpoints = [value]
            elif key == "connect" and value:
                config.connect_endpoints = [value]
            elif key == "iface" and value:
                config.iface = value
        try:
            self._client = Pmini(config=config)
            self._client.connect()
            print("Connected successfully.")
            status = self._client.get_status()
            if status:
                print(f"Status: {status.get('system', {}).get('uptime_ms', 0)} ms uptime")
        except Exception as exc:  # pragma: no cover - CLI convenience
            self._client = None
            print(f"Failed to connect: {exc}")

    def do_disconnect(self, arg: str) -> None:
        """Disconnect from the drone."""
        if not self._client:
            print("Not connected.")
            return
        self._stop_monitoring()
        self._client.disconnect()
        self._client = None
        print("Disconnected.")

    def do_status(self, arg: str) -> None:
        """Display ESP status information."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        status = client.get_status()
        if not status:
            print("No status data available yet.")
            return
        print(status)

    def do_status_text(self, arg: str) -> None:
        """Display last status_text message (severity and text)."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        st = client.get_status_text()
        if not st:
            print("No status_text available yet.")
            return
        severity = st.get("severity", "INFO")
        text = st.get("text", "")
        print(f"[{severity}] {text}")

    def do_position(self, arg: str) -> None:
        """Print the latest position sample."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        position = client.get_position()
        if not position:
            print("No position data available yet.")
            return
        self._print_position(position)

    def do_takeoff(self, arg: str) -> None:
        """takeoff [altitude_m]"""
        if not self._ensure_client():
            return
        try:
            altitude = float(arg.strip()) if arg.strip() else 1.0
        except ValueError:
            print("Invalid altitude.")
            return
        client = self._client
        assert client is not None
        result = client.takeoff(altitude)
        self._print_command_result("Takeoff", result)

    def do_land(self, arg: str) -> None:
        """Land the drone."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        result = client.land()
        self._print_command_result("Land", result)

    def do_mode(self, arg: str) -> None:
        """mode <name>"""
        if not self._ensure_client():
            return
        mode_name = arg.strip()
        if not mode_name:
            print("Usage: mode <name>")
            return
        client = self._client
        assert client is not None
        result = client.set_mode(mode_name.upper())
        self._print_command_result("Mode", result)

    def do_arm(self, arg: str) -> None:
        """Arm the drone."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        result = client.arm()
        self._print_command_result("Arm", result)

    def do_disarm(self, arg: str) -> None:
        """Disarm the drone."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        result = client.disarm()
        self._print_command_result("Disarm", result)

    def do_emergency_stop(self, arg: str) -> None:
        """Execute emergency stop."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        result = client.emergency_stop()
        self._print_command_result("Emergency stop", result)

    def do_reboot(self, arg: str) -> None:
        """Reboot the drone."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        result = client.reboot()
        self._print_command_result("Reboot", result)

    def do_goto(self, arg: str) -> None:
        """goto x y z [yaw] [frame]

        Send a goto command to move to a position.

        Frame can be:
          - Numeric: 1 (local), 7 (local_offset), 8 (body), 9 (body_offset, default)
          - String: "local", "local_offset", "body", "body_offset"

        Examples:
          goto 0 0 0
          goto 0 0 0 0 1
          goto 0 0 0 0 local
          goto 0 0 0 0 body_offset"""
        if not self._ensure_client():
            return
        tokens = [token for token in arg.split() if token]
        if len(tokens) < 3:
            print("Usage: goto x y z [yaw] [frame]")
            return
        try:
            x, y, z = (float(tokens[i]) for i in range(3))
            yaw = 0.0
            frame = None

            # Parse optional yaw and frame
            # Format: goto x y z [yaw] [frame]
            if len(tokens) == 4:
                # Could be yaw (float) or frame (string/int)
                try:
                    yaw = float(tokens[3])
                except ValueError:
                    # Token 3 is not a float, treat as frame
                    frame = tokens[3]
            elif len(tokens) >= 5:
                # Both yaw and frame provided
                yaw = float(tokens[3])
                frame = tokens[4]
        except (ValueError, IndexError) as e:
            print(f"Invalid parameters: {e}")
            print("Usage: goto x y z [yaw] [frame]")
            return

        client = self._client
        assert client is not None

        # Convert frame string to int if needed, or pass as-is
        if frame is not None:
            try:
                # Try to parse as integer first
                frame_int = int(frame)
                result = client.goto(x, y, z, yaw, frame=frame_int)
            except ValueError:
                # It's a string frame name
                result = client.goto(x, y, z, yaw, frame=frame)
        else:
            result = client.goto(x, y, z, yaw)

        self._print_command_result("Goto", result)

    def do_velocity(self, arg: str) -> None:
        """velocity vx vy vz [yaw]

        Send a body-frame velocity command (m/s, Z up)."""
        if not self._ensure_client():
            return
        tokens = [token for token in arg.split() if token]
        if len(tokens) < 3:
            print("Usage: velocity vx vy vz [yaw]")
            return
        try:
            vx, vy, vz = (float(tokens[i]) for i in range(3))
            yaw = float(tokens[3]) if len(tokens) >= 4 else 0.0
        except ValueError:
            print("All parameters must be numeric.")
            return
        client = self._client
        assert client is not None
        result = client.set_velocity_local_ned(vx, vy, vz, yaw)
        self._print_command_result("Velocity", result)

    def do_log_list(self, arg: str) -> None:
        """log_list

        Fetch and print metadata for available vehicle logs."""
        if arg.strip():
            print("Usage: log_list")
            return
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        result = client.log_list()
        if not result.ok:
            self._print_command_result("Log list", result)
            return

        payload = result.data or {}
        entries = payload.get("data") if isinstance(payload, dict) else None
        if not entries:
            print("No logs available.")
            return

        print(f"Found {len(entries)} log(s):")
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            log_id = entry.get("id", "?")
            size = entry.get("size", "?")
            timestamp = entry.get("time_utc", "?")
            print(f"  - id={log_id} size={size} bytes time_utc={timestamp}")

    def do_log_download(self, arg: str) -> None:
        """log_download <id> [limit_bytes] [> filename]

        Start a log download. Provide ``> file.bin`` to save locally, otherwise
        the command prints the chunk/meta topics so you can subscribe manually."""
        if not self._ensure_client():
            return

        try:
            tokens = shlex.split(arg)
        except ValueError as exc:
            print(f"Failed to parse arguments: {exc}")
            return

        if not tokens:
            print("Usage: log_download <id> [limit_bytes] [> filename]")
            return

        output_path: Optional[str] = None
        if ">" in tokens:
            redirect_index = tokens.index(">")
            if redirect_index == len(tokens) - 1:
                print("Usage: log_download <id> [limit_bytes] [> filename]")
                return
            output_path = tokens[redirect_index + 1]
            tokens = tokens[:redirect_index]

        if not tokens:
            print("Usage: log_download <id> [limit_bytes] [> filename]")
            return

        try:
            log_id = int(tokens[0])
        except ValueError:
            print("Log id must be an integer.")
            return

        limit_bytes = None
        if len(tokens) >= 2:
            try:
                limit_bytes = int(tokens[1])
                if limit_bytes <= 0:
                    limit_bytes = None
            except ValueError:
                print("Limit must be an integer.")
                return

        client = self._client
        assert client is not None

        if output_path:
            progress_state = {"start_time": time.monotonic(), "total": limit_bytes, "progress_active": False}

            def progress(meta: dict) -> None:
                self._render_download_progress(meta, progress_state, limit_bytes)

            result = client.log_download_to_file(
                log_id,
                output_path,
                max_bytes=limit_bytes,
                progress_callback=progress,
            )
            self._print_command_result("Log download", result)
            if not result.ok and self._is_log_download_busy(result):
                self._print_log_busy_hint()
            return

        result = client.log_download(log_id, max_bytes=limit_bytes)
        if not result.ok:
            self._print_command_result("Log download", result)
            if self._is_log_download_busy(result):
                self._print_log_busy_hint()
            return

        self._print_command_result("Log download", result)
        payload = result.data or {}
        data_field = payload.get("data") if isinstance(payload, dict) else None
        chunk_topic = data_field.get("chunks") if isinstance(data_field, dict) else None
        meta_topic = data_field.get("meta") if isinstance(data_field, dict) else None
        if meta_topic and chunk_topic:
            print("Subscribe to these topics to receive the stream:")
            print(f"  Meta updates : {meta_topic}")
            print(f"  Chunk payloads: {chunk_topic}/** (raw binary)")
            print("Re-run with '> filename.bin' to save automatically.")
        else:
            print("Log topics were not provided in the reply.")

    def do_log_clear(self, arg: str) -> None:
        """log_clear

        Erase all logs on the vehicle (same as Mission Planner's 'Erase All Logs')."""
        if arg.strip():
            print("Usage: log_clear")
            return
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        result = client.log_clear()
        self._print_command_result("Log clear", result)

    def do_log_delete(self, arg: str) -> None:
        """Alias for log_clear."""
        return self.do_log_clear(arg)

    def do_monitor(self, arg: str) -> None:
        """Start printing position updates as they arrive."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        if self._position_callback:
            print("Monitoring already active.")
            return

        def callback(position: Position) -> None:
            self._print_position(position)

        self._position_callback = callback
        client.add_position_callback(callback)
        print("Monitoring started. Use 'stop_monitor' to stop.")

    def do_monitor_status(self, arg: str) -> None:
        """Start printing status_text messages as they arrive."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        if getattr(self, "_status_text_callback", None):
            print("StatusText monitoring already active.")
            return

        def st_callback(payload: dict) -> None:
            severity = payload.get("severity", "INFO")
            text = payload.get("text", "")
            print(f"[{severity}] {text}")

        self._status_text_callback = st_callback
        client.add_status_text_callback(st_callback)
        print("StatusText monitoring started. Use 'stop_monitor_status' to stop.")

    def do_stop_monitor_status(self, arg: str) -> None:
        """Stop status_text monitoring."""
        if not self._ensure_client():
            return
        client = self._client
        assert client is not None
        if getattr(self, "_status_text_callback", None):
            assert self._status_text_callback is not None
            client.remove_status_text_callback(self._status_text_callback)
            self._status_text_callback = None
        print("StatusText monitoring stopped.")

    def do_stop_monitor(self, arg: str) -> None:
        """Stop position monitoring."""
        if not self._ensure_client():
            return
        self._stop_monitoring()
        print("Monitoring stopped.")

    def do_quit(self, arg: str) -> bool:
        """Exit the terminal."""
        self._cleanup()
        print("Goodbye!")
        return True

    def do_exit(self, arg: str) -> bool:  # alias
        return self.do_quit(arg)

    def do_EOF(self, arg: str) -> bool:  # Ctrl+D
        print()
        return self.do_quit(arg)

    def default(self, line: str) -> None:
        if line.startswith("connect="):
            # Allow shorthand usage: typing "connect=udp/..." instead of "connect connect=udp/..."
            self.do_connect(line)
        else:
            print(f"Unknown command: {line}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _ensure_client(self) -> bool:
        if not self._client:
            print("Not connected. Use 'connect' first.")
            return False
        return True

    def _stop_monitoring(self) -> None:
        if self._client and self._position_callback:
            self._client.remove_position_callback(self._position_callback)
            self._position_callback = None
        if self._client and getattr(self, "_status_text_callback", None):
            assert self._status_text_callback is not None
            self._client.remove_status_text_callback(self._status_text_callback)
            self._status_text_callback = None

    def _print_position(self, position: Position) -> None:
        print(f"Position → x={position.x:.2f} y={position.y:.2f} z={position.z:.2f}")

    def _print_command_result(self, name: str, result) -> None:
        icon = "✅" if result.ok else "❌"
        message = result.message or result.status
        print(f"{icon} {name}: {message}")

    def _is_log_download_busy(self, result) -> bool:
        message = (result.message or result.status or "").lower()
        return "log download already running" in message or "log download mutex busy" in message

    def _print_log_busy_hint(self) -> None:
        print(
            "A log download is already running. Wait for its meta topic to report "
            "'done' or 'error' before starting another download.",
            flush=True,
        )

    def _render_download_progress(
        self,
        meta: dict,
        state: dict,
        limit_bytes: Optional[int],
    ) -> None:
        now = time.monotonic()
        transferred = int(meta.get("transferred", 0))
        total = state.get("total")
        meta_size = meta.get("size")
        if isinstance(meta_size, (int, float)) and meta_size > 0:
            total = int(meta_size)
        if limit_bytes is not None and limit_bytes > 0:
            total = limit_bytes if total is None else min(total, limit_bytes)
        state["total"] = total

        elapsed = max(now - state["start_time"], 1e-3)
        speed = transferred / elapsed
        percent = (transferred / total * 100) if total else None
        bar = self._render_progress_bar(percent)
        speed_str = self._format_bytes(speed) + "/s"
        total_str = self._format_bytes(total) if total else "?"
        line = f"{bar} "
        if percent is not None:
            line += f"{percent:6.2f}% "
        line += f"{self._format_bytes(transferred)} / {total_str}  {speed_str}"
        if speed > 0 and total:
            eta = max((total - transferred) / speed, 0.0)
            line += f"  ETA {self._format_duration(eta)}"
        state["progress_active"] = True
        sys.stdout.write("\r" + line)
        sys.stdout.flush()

        if (meta.get("state") or "").lower() in {"done", "error"}:
            sys.stdout.write("\n")
            sys.stdout.flush()
            state["progress_active"] = False
            message = meta.get("message")
            if message:
                print(f"  message: {message}")

    @staticmethod
    def _format_bytes(value: Optional[float]) -> str:
        if value is None or value < 0:
            return "?"
        units = ["B", "KiB", "MiB", "GiB", "TiB"]
        idx = 0
        while value >= 1024 and idx < len(units) - 1:
            value /= 1024
            idx += 1
        if idx == 0:
            return f"{value:.0f} {units[idx]}"
        return f"{value:.1f} {units[idx]}"

    @staticmethod
    def _format_duration(seconds: float) -> str:
        seconds = max(seconds, 0.0)
        if seconds >= 3600:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        if seconds >= 60:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        return f"{int(seconds)}s"

    @staticmethod
    def _render_progress_bar(percent: Optional[float], width: int = 28) -> str:
        if percent is None:
            return "[" + "." * width + "]"
        percent = max(0.0, min(percent, 100.0))
        filled = int((percent / 100.0) * width)
        return "[" + "#" * filled + "." * (width - filled) + "]"

    def _cleanup(self) -> None:
        self._stop_monitoring()
        if self._client:
            self._client.disconnect()
            self._client = None


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    terminal = PminiTerminal()
    try:
        terminal.cmdloop()
    except KeyboardInterrupt:  # pragma: no cover - CLI convenience
        terminal._cleanup()
        print("\nInterrupted.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
