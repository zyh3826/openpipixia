"""Channel factory and env-driven bootstrap helpers."""

from __future__ import annotations

import os
from typing import Callable

from ..bus.queue import MessageBus
from .feishu import FEISHU_AVAILABLE, FeishuChannel
from .local import LocalChannel
from .manager import ChannelManager


def parse_enabled_channels(channels: str | None) -> list[str]:
    """Parse channel list from CLI arg or env."""
    raw = channels if channels is not None else os.getenv("SENTIENTAGENT_V2_CHANNELS", "local")
    names = [item.strip().lower() for item in raw.split(",") if item.strip()]
    if not names:
        return ["local"]
    # Keep input order but deduplicate.
    return list(dict.fromkeys(names))


def validate_channel_setup(channel_names: list[str]) -> list[str]:
    issues: list[str] = []
    supported = {"local", "feishu"}
    unknown = [name for name in channel_names if name not in supported]
    if unknown:
        issues.append(f"Unsupported channels: {', '.join(unknown)}")

    if "feishu" in channel_names:
        if not FEISHU_AVAILABLE:
            issues.append("Feishu channel requires `lark-oapi` (pip install lark-oapi).")
        if not os.getenv("FEISHU_APP_ID", "").strip():
            issues.append("Missing FEISHU_APP_ID for feishu channel.")
        if not os.getenv("FEISHU_APP_SECRET", "").strip():
            issues.append("Missing FEISHU_APP_SECRET for feishu channel.")
    return issues


def build_channel_manager(
    *,
    bus: MessageBus,
    channel_names: list[str],
    local_writer: Callable[[str], None] | None = None,
) -> tuple[ChannelManager, LocalChannel | None]:
    """Build channel manager and register selected channels."""
    manager = ChannelManager(bus)
    local_channel: LocalChannel | None = None

    for name in channel_names:
        if name == "local":
            local_channel = LocalChannel(bus=bus, writer=local_writer)
            manager.register(local_channel)
            continue

        if name == "feishu":
            manager.register(
                FeishuChannel(
                    bus=bus,
                    app_id=os.getenv("FEISHU_APP_ID", "").strip(),
                    app_secret=os.getenv("FEISHU_APP_SECRET", "").strip(),
                    encrypt_key=os.getenv("FEISHU_ENCRYPT_KEY", "").strip(),
                    verification_token=os.getenv("FEISHU_VERIFICATION_TOKEN", "").strip(),
                )
            )
            continue

    return manager, local_channel
