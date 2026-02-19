"""Tests for Mochat channel adapter behavior."""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, patch

from sentientagent_v2.bus.events import OutboundMessage
from sentientagent_v2.bus.queue import MessageBus
from sentientagent_v2.channels.mochat import MochatChannel


class MochatChannelTests(unittest.IsolatedAsyncioTestCase):
    async def test_send_session_target_calls_session_api(self) -> None:
        bus = MessageBus()
        channel = MochatChannel(
            bus=bus,
            base_url="https://mochat.io",
            claw_token="claw-token",
        )

        with patch.object(channel, "_post_json", new=AsyncMock()) as post_json:
            await channel.send(
                OutboundMessage(
                    channel="mochat",
                    chat_id="session_123",
                    content="hello session",
                )
            )

        post_json.assert_awaited_once_with(
            "/api/claw/sessions/send",
            {"sessionId": "session_123", "content": "hello session"},
        )

    async def test_send_panel_target_calls_panel_api(self) -> None:
        bus = MessageBus()
        channel = MochatChannel(
            bus=bus,
            base_url="https://mochat.io",
            claw_token="claw-token",
        )

        with patch.object(channel, "_post_json", new=AsyncMock()) as post_json:
            await channel.send(
                OutboundMessage(
                    channel="mochat",
                    chat_id="panel:group_123",
                    content="hello panel",
                    metadata={"group_id": "workspace_1"},
                )
            )

        post_json.assert_awaited_once_with(
            "/api/claw/groups/panels/send",
            {"panelId": "group_123", "content": "hello panel", "groupId": "workspace_1"},
        )


if __name__ == "__main__":
    unittest.main()
