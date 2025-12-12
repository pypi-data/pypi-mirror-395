"""Low-level Zenoh client used by the PMini SDK."""

from __future__ import annotations

import json
import logging
import os
import struct
import threading
import time
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence

from .common import CommandResult, Position
from .config import DEFAULT_PMINI_CONFIG, PminiConfig

logger = logging.getLogger(__name__)

try:
    import zenoh  # type: ignore
except ImportError as exc:  # pragma: no cover - dependency missing at runtime
    zenoh = None  # type: ignore
    _ZENOH_IMPORT_ERROR: Optional[ImportError] = exc
else:
    _ZENOH_IMPORT_ERROR = None


PayloadCallback = Callable[[bytes], None]
PositionCallback = Callable[[Position], None]


def _extract_payload_bytes(payload_obj) -> Optional[bytes]:
    if payload_obj is None:
        return None
    if hasattr(payload_obj, "to_bytes"):
        try:
            return payload_obj.to_bytes()
        except Exception:
            return None
    if isinstance(payload_obj, bytes):
        return payload_obj
    if hasattr(payload_obj, "get_bytes"):
        try:
            return payload_obj.get_bytes()
        except Exception:
            return None
    if hasattr(payload_obj, "__bytes__"):
        try:
            return bytes(payload_obj)
        except Exception:
            return None
    return None


class ZenohClient:
    """Thin wrapper around zenoh-python providing PMini-specific utilities."""

    def __init__(self, config: Optional[PminiConfig] = None):
        if zenoh is None:
            raise RuntimeError(
                "zenoh package is not available. Install with `pip install eclipse-zenoh`"
            ) from _ZENOH_IMPORT_ERROR

        self._config = config or DEFAULT_PMINI_CONFIG
        self._session: Optional[Any] = None
        self._position: Optional[Position] = None
        self._position_lock = threading.Lock()
        self._position_callbacks: List[PositionCallback] = []
        self._status_json: Optional[dict] = None
        self._status_lock = threading.Lock()
        self._status_callbacks: List[Callable[[dict], None]] = []
        self._status_text_json: Optional[dict] = None
        self._status_text_lock = threading.Lock()
        self._status_text_callbacks: List[Callable[[dict], None]] = []
        self._subscribers: List[Any] = []
        self._connection_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------
    def connect(self) -> None:
        """Open a Zenoh session and start telemetry subscriptions."""
        with self._connection_lock:
            if self._session is not None:
                logger.debug("Zenoh session already active.")
                return

            conf = zenoh.Config()
            conf.insert_json5("mode", json.dumps(self._config.mode))

            listen_endpoints = self._decorate_endpoints(self._config.listen_endpoints)
            connect_endpoints = self._decorate_endpoints(self._config.connect_endpoints)
            if listen_endpoints:
                conf.insert_json5("listen/endpoints", json.dumps(listen_endpoints))
            if connect_endpoints:
                conf.insert_json5("connect/endpoints", json.dumps(connect_endpoints))

            logger.info(
                "Opening Zenoh session (mode=%s, listen=%s, connect=%s)",
                self._config.mode,
                listen_endpoints or None,
                connect_endpoints or None,
            )
            self._session = zenoh.open(conf)

            if self._config.wait_seconds > 0:
                time.sleep(self._config.wait_seconds)

            self._start_subscriptions()

    def disconnect(self) -> None:
        """Stop subscriptions and close the Zenoh session."""
        with self._connection_lock:
            for subscriber in self._subscribers:
                try:
                    subscriber.undeclare()
                except Exception:  # pragma: no cover - best-effort cleanup
                    logger.debug("Failed to undeclare subscriber", exc_info=True)
            self._subscribers.clear()

            if self._session:
                try:
                    self._session.close()
                finally:
                    self._session = None

    # ------------------------------------------------------------------
    # Command helpers
    # ------------------------------------------------------------------
    def send_command(
        self,
        command: str,
        args: Optional[Sequence[object]] = None,
        timeout: Optional[float] = None,
        extra_payload: Optional[dict] = None,
    ) -> CommandResult:
        """
        Send a command via Zenoh queryable.

        Args:
            command: Name of the command (e.g. ``takeoff``).
            args: Optional numeric arguments.
            timeout: Optional timeout in seconds.
            extra_payload: Additional JSON payload fields.
        """
        session = self._require_session()

        payload: Dict[str, Any] = {"command": command}
        if args:
            payload["args"] = list(args)
        if extra_payload:
            payload.update(extra_payload)

        payload_bytes = json.dumps(payload).encode("utf-8")

        key_expr = self._command_keyexpr_for(command)
        logger.debug("Sending command %s via %s", command, key_expr)

        with session.declare_querier(key_expr, timeout=timeout) as querier:
            replies: Iterable[zenoh.Reply] = querier.get(payload=payload_bytes)

            for reply in replies:
                if reply.ok is None:
                    continue
                raw_bytes = _extract_payload_bytes(reply.ok.payload)
                if not raw_bytes:
                    continue
                try:
                    response = json.loads(raw_bytes.decode("utf-8"))
                    return CommandResult(
                        status=response.get("status", "error"),
                        message=response.get("message", ""),
                        data=response,
                    )
                except json.JSONDecodeError:
                    logger.warning("Command reply was not valid JSON: %r", raw_bytes)
                    return CommandResult(status="error", message="invalid reply", data=None)

        return CommandResult(status="error", message="no reply", data=None)

    def publish_general_command(
        self,
        command: str,
        payload: Optional[dict] = None,
    ) -> None:
        """
        Broadcast a command to every drone via ``pmini/all/command/<name>``.

        Args:
            command: Command name (e.g. ``takeoff``).
            payload: Optional JSON payload (e.g. ``{\"altitude\": 1.0}``).
        """
        session = self._require_session()
        suffix = command.strip().lower()
        if not suffix:
            raise ValueError("Command name is required")
        topic = f"pmini/all/command/{suffix}"
        body = json.dumps(payload or {}, separators=(",", ":")).encode("utf-8") if payload else b""
        logger.debug("Broadcasting general command %s via %s", command, topic)
        session.put(topic, body)

    def clear_logs(self) -> CommandResult:
        """Delete all logs on the vehicle."""
        return self.send_command("log_clear")

    def download_log_to_file(
        self,
        log_id: int,
        path: str,
        *,
        max_bytes: Optional[int] = None,
        timeout: float = 120.0,
        progress_callback: Optional[Callable[[dict], None]] = None,
    ) -> CommandResult:
        """
        Request a log download and stream the resulting chunks into a file.

        Args:
            log_id: Vehicle log identifier from ``log_list``.
            path: Destination path for the binary log.
            max_bytes: Optional upper bound if only a prefix is needed.
            timeout: Maximum time (seconds) to wait for completion.
            progress_callback: Optional callable receiving parsed meta payloads.
        """
        if not self._session:
            raise RuntimeError("Zenoh session not connected.")

        log_id_int = int(log_id)
        chunk_prefix = self._log_chunk_prefix(log_id_int)
        meta_topic = self._log_meta_keyexpr(log_id_int)
        chunk_subscription = f"{chunk_prefix}/**"

        done_event = threading.Event()
        file_lock = threading.Lock()
        bytes_written = 0
        expected_offset = 0
        error_message: Optional[str] = None
        preserve_file = False
        session = self._session
        buffered_chunks: Dict[int, bytes] = {}

        fp = open(path, "wb")

        def flush_ready_chunks_locked() -> None:
            nonlocal bytes_written, expected_offset
            while True:
                chunk = buffered_chunks.pop(expected_offset, None)
                if chunk is None:
                    break
                fp.seek(expected_offset)
                fp.write(chunk)
                expected_offset += len(chunk)
            bytes_written = max(bytes_written, expected_offset)

        def chunk_callback(sample) -> None:
            if done_event.is_set():
                return
            payload = _extract_payload_bytes(sample.payload)
            if not payload:
                return
            offset = self._extract_chunk_offset(sample, chunk_prefix)
            if offset is None:
                offset = expected_offset
            with file_lock:
                if offset < expected_offset:
                    return
                chunk_data = payload
                if max_bytes is not None:
                    remaining = max_bytes - offset
                    if remaining <= 0:
                        return
                    if len(chunk_data) > remaining:
                        chunk_data = chunk_data[:remaining]
                buffered_chunks[offset] = chunk_data
                flush_ready_chunks_locked()

        def meta_callback(sample) -> None:
            nonlocal error_message
            payload = _extract_payload_bytes(sample.payload)
            if not payload:
                return
            try:
                meta = json.loads(payload.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                logger.warning("Failed to parse log meta payload: %r", payload)
                return
            if progress_callback:
                try:
                    progress_callback(meta)
                except Exception:  # pragma: no cover - defensive logging
                    logger.exception("Log progress callback raised an exception")
            state = (meta.get("state") or "").lower()
            if state in {"done", "error"}:
                if state == "error":
                    error_message = meta.get("message") or "log download failed"
                done_event.set()

        chunk_sub = None
        meta_sub = None
        args: List[object] = [log_id_int]
        if max_bytes is not None:
            limit = int(max_bytes)
            if limit > 0:
                args.append(limit)

        try:
            chunk_sub = session.declare_subscriber(chunk_subscription, chunk_callback)
            meta_sub = session.declare_subscriber(meta_topic, meta_callback)

            command_result = self.send_command("log_download", args=args)
            if not command_result.ok:
                return command_result

            if not done_event.wait(timeout):
                return CommandResult(status="error", message="log download timed out", data=command_result.data)

            if error_message:
                return CommandResult(status="error", message=error_message, data=command_result.data)

            try:
                fp.flush()
                os.fsync(fp.fileno())
            except OSError:
                logger.debug("Failed to fsync log file '%s'", path, exc_info=True)
            preserve_file = True
            message = f"Saved log {log_id_int} ({bytes_written} bytes) to {path}"
            return CommandResult(status="success", message=message, data=command_result.data)
        finally:
            if chunk_sub is not None:
                try:
                    chunk_sub.undeclare()
                except Exception:
                    logger.debug("Failed to undeclare log chunk subscriber", exc_info=True)
            if meta_sub is not None:
                try:
                    meta_sub.undeclare()
                except Exception:
                    logger.debug("Failed to undeclare log meta subscriber", exc_info=True)
            fp.close()
            if not preserve_file:
                try:
                    os.remove(path)
                except OSError:
                    pass

    def _extract_chunk_offset(self, sample, chunk_prefix: str) -> Optional[int]:
        keyexpr_obj = getattr(sample, "key_expr", None)
        key_str: Optional[str] = None
        if keyexpr_obj is None:
            return None
        for attr in ("to_string", "name", "keyexpr", "keyexpr_as_string"):
            candidate = getattr(keyexpr_obj, attr, None)
            if callable(candidate):
                try:
                    key_str = candidate()
                except TypeError:
                    key_str = None
            elif candidate:
                key_str = candidate
            if isinstance(key_str, str):
                break
        if key_str is None:
            key_str = str(keyexpr_obj)
        if not key_str:
            return None
        suffix = key_str
        if key_str.startswith(chunk_prefix):
            suffix = key_str[len(chunk_prefix) :]
        suffix = suffix.strip("/")
        if "/" in suffix:
            suffix = suffix.split("/")[-1]
        try:
            return int(suffix, 10)
        except ValueError:
            return None

    # ------------------------------------------------------------------
    # Telemetry accessors
    # ------------------------------------------------------------------
    def get_position(self) -> Optional[Position]:
        with self._position_lock:
            return self._position

    def add_position_callback(self, callback: PositionCallback) -> None:
        self._position_callbacks.append(callback)

    def remove_position_callback(self, callback: PositionCallback) -> None:
        if callback in self._position_callbacks:
            self._position_callbacks.remove(callback)

    def get_status(self) -> Optional[dict]:
        with self._status_lock:
            return self._status_json

    def add_status_callback(self, callback: Callable[[dict], None]) -> None:
        self._status_callbacks.append(callback)

    def remove_status_callback(self, callback: Callable[[dict], None]) -> None:
        if callback in self._status_callbacks:
            self._status_callbacks.remove(callback)

    # ------------------------------------------------------------------
    # Subscription wiring
    # ------------------------------------------------------------------
    def _start_subscriptions(self) -> None:
        assert self._session is not None

        self._subscribers.append(self._session.declare_subscriber(self._config.position_topic, self._on_position_sample))
        self._subscribers.append(self._session.declare_subscriber(self._config.status_topic, self._on_status_sample))
        self._subscribers.append(self._session.declare_subscriber(self._config.status_text_topic, self._on_status_text_sample))

    def _on_position_sample(self, sample) -> None:
        raw_bytes = _extract_payload_bytes(sample.payload)
        if not raw_bytes:
            return
        if len(raw_bytes) < 12:
            logger.warning("Position payload too small (%d bytes). Expected 12 bytes.", len(raw_bytes))
            return
        try:
            x, y, z = struct.unpack("<fff", raw_bytes[:12])
            position = Position(x=x, y=y, z=z)
        except struct.error:
            logger.warning("Failed to unpack position payload: size=%d", len(raw_bytes))
            return

        with self._position_lock:
            self._position = position

        for callback in list(self._position_callbacks):
            try:
                callback(position)
            except Exception:  # pragma: no cover - user callback errors
                logger.exception("Position callback raised an exception")

    def _on_status_sample(self, sample) -> None:
        raw_bytes = _extract_payload_bytes(sample.payload)
        if not raw_bytes:
            return
        try:
            payload_str = raw_bytes.decode("utf-8")
            status_json = json.loads(payload_str)
        except (UnicodeDecodeError, json.JSONDecodeError):
            logger.warning("Failed to parse status JSON payload: %r", raw_bytes)
            return

        with self._status_lock:
            self._status_json = status_json

        for callback in list(self._status_callbacks):
            try:
                callback(status_json)
            except Exception:  # pragma: no cover
                logger.exception("Status callback raised an exception")

    def _on_status_text_sample(self, sample) -> None:
        raw_bytes = _extract_payload_bytes(sample.payload)
        if not raw_bytes:
            return
        try:
            payload_str = raw_bytes.decode("utf-8")
            status_text_json = json.loads(payload_str)
        except (UnicodeDecodeError, json.JSONDecodeError):
            logger.warning("Failed to parse status_text JSON payload: %r", raw_bytes)
            return

        with self._status_text_lock:
            self._status_text_json = status_text_json

        for callback in list(self._status_text_callbacks):
            try:
                callback(status_text_json)
            except Exception:  # pragma: no cover
                logger.exception("StatusText callback raised an exception")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _decorate_endpoints(self, endpoints: Sequence[str]) -> List[str]:
        result: List[str] = []
        for endpoint in endpoints:
            if not endpoint:
                continue
            endpoint = endpoint.strip()
            if self._config.iface and "#iface=" not in endpoint:
                endpoint = f"{endpoint}#iface={self._config.iface}"
            result.append(endpoint)
        return result

    def _require_session(self):
        if not self._session:
            raise RuntimeError("Zenoh session not connected.")
        return self._session

    def _command_keyexpr_for(self, command: str) -> str:
        base = self._config.command_keyexpr.split("*", 1)[0]
        base = base.rstrip("/")
        return f"{base}/{command}"

    def _log_root_prefix(self) -> str:
        root = getattr(self._config, "log_root_topic", "pmini/log") or "pmini/log"
        return root.rstrip("/")

    def _log_base_topic(self, log_id: int) -> str:
        return f"{self._log_root_prefix()}/{log_id}"

    def _log_chunk_prefix(self, log_id: int) -> str:
        return f"{self._log_base_topic(log_id)}/chunk"

    def _log_meta_keyexpr(self, log_id: int) -> str:
        return f"{self._log_base_topic(log_id)}/meta"

    # ------------------------------------------------------------------
    # Status text accessors
    # ------------------------------------------------------------------
    def get_status_text(self) -> Optional[dict]:
        with self._status_text_lock:
            return self._status_text_json

    def add_status_text_callback(self, callback: Callable[[dict], None]) -> None:
        self._status_text_callbacks.append(callback)

    def remove_status_text_callback(self, callback: Callable[[dict], None]) -> None:
        if callback in self._status_text_callbacks:
            self._status_text_callbacks.remove(callback)
