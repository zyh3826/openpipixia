"""Tests for bus and gateway skeleton."""

from __future__ import annotations

import asyncio
import types as pytypes
import unittest
from unittest.mock import patch

from sentientagent_v2.bus.events import InboundMessage, OutboundMessage
from sentientagent_v2.bus.queue import MessageBus
from sentientagent_v2.gateway import Gateway


class MessageBusTests(unittest.IsolatedAsyncioTestCase):
    async def test_roundtrip(self) -> None:
        bus = MessageBus()
        inbound = InboundMessage(channel="local", sender_id="u1", chat_id="c1", content="ping")
        outbound = OutboundMessage(channel="local", chat_id="c1", content="pong")

        await bus.publish_inbound(inbound)
        await bus.publish_outbound(outbound)

        got_inbound = await bus.consume_inbound()
        got_outbound = await bus.consume_outbound()

        self.assertEqual(got_inbound.content, "ping")
        self.assertEqual(got_outbound.content, "pong")


class GatewayTests(unittest.TestCase):
    def test_process_message_collects_final_text(self) -> None:
        fake_event_1 = pytypes.SimpleNamespace(content=pytypes.SimpleNamespace(parts=[]))
        fake_event_2 = pytypes.SimpleNamespace(
            content=pytypes.SimpleNamespace(parts=[pytypes.SimpleNamespace(text="gateway answer")])
        )

        class _FakeRunner:
            def __init__(self, **kwargs):
                pass

            async def run_async(self, **kwargs):
                yield fake_event_1
                yield fake_event_2

        fake_agent = pytypes.SimpleNamespace(name="sentientagent_v2")
        with patch("sentientagent_v2.gateway.Runner", _FakeRunner):
            gateway = Gateway(agent=fake_agent, app_name="sentientagent_v2", bus=MessageBus())
            inbound = InboundMessage(channel="local", sender_id="u1", chat_id="c1", content="hello")
            outbound = asyncio.run(gateway.process_message(inbound))

        self.assertEqual(outbound.channel, "local")
        self.assertEqual(outbound.chat_id, "c1")
        self.assertEqual(outbound.content, "gateway answer")


if __name__ == "__main__":
    unittest.main()
