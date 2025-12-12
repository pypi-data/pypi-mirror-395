"""Configuration helpers and constants for the PMini Zenoh SDK."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

# Key expressions / topics
COMMAND_KEYEXPR = "pmini/command/**"
POSITION_TOPIC = "pmini/position"
STATUS_TOPIC = "pmini/esp/status"
STATUS_TEXT_TOPIC = "pmini/status_text"
LOG_ROOT_TOPIC = "pmini/log"

# Default network configuration (align with firmware defaults)
DEFAULT_MODE = "client"
DEFAULT_ROUTER_ENDPOINT = "udp/192.168.4.2:7447"
DEFAULT_WAIT_SECONDS = 1.0


@dataclass
class PminiConfig:
    """
    Configuration for establishing Zenoh connectivity with a PMini drone.

    Attributes:
        mode: Zenoh mode, typically ``peer`` when connected directly to the drone.
        listen_endpoints: Optional list of listen endpoints (e.g. multicast locator).
        connect_endpoints: Optional list of router endpoints when running in client mode.
        iface: Optional network interface (used in locators via ``#iface`` suffix).
        command_keyexpr: Key expression used for command queries.
        position_topic: Topic for binary position telemetry.
        status_topic: Topic for JSON ESP status snapshots.
        status_text_topic: Topic for textual status updates.
        log_root_topic: Base key expression used for log streaming (``pmini/log``).
        wait_seconds: Delay after declaring a querier to allow discovery.
    """

    mode: str = DEFAULT_MODE
    listen_endpoints: Sequence[str] = field(default_factory=list)
    connect_endpoints: Sequence[str] = field(default_factory=lambda: [DEFAULT_ROUTER_ENDPOINT])
    iface: Optional[str] = None
    command_keyexpr: str = COMMAND_KEYEXPR
    position_topic: str = POSITION_TOPIC
    status_topic: str = STATUS_TOPIC
    status_text_topic: str = STATUS_TEXT_TOPIC
    log_root_topic: str = LOG_ROOT_TOPIC
    wait_seconds: float = DEFAULT_WAIT_SECONDS


DEFAULT_PMINI_CONFIG = PminiConfig()
