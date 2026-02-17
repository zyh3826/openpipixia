"""Gateway that bridges bus/channel traffic to ADK Runner."""

from __future__ import annotations

import asyncio
from typing import Any

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .bus.events import InboundMessage, OutboundMessage
from .bus.queue import MessageBus
from .channels.manager import ChannelManager
from .runtime.tool_context import route_context
from .tools import configure_outbound_publisher


def _extract_text(content: types.Content | None) -> str:
    if content is None or not content.parts:
        return ""
    chunks: list[str] = []
    for part in content.parts:
        text = getattr(part, "text", None)
        if text:
            chunks.append(text)
    return "\n".join(chunks).strip()


class Gateway:
    """Consumes inbound bus messages and routes them through ADK runner."""

    def __init__(
        self,
        *,
        agent: Any,
        app_name: str,
        bus: MessageBus,
        channel_manager: ChannelManager | None = None,
        session_service: Any | None = None,
    ) -> None:
        self.bus = bus
        self.channel_manager = channel_manager
        self.session_service = session_service or InMemorySessionService()
        self.runner = Runner(
            agent=agent,
            app_name=app_name,
            session_service=self.session_service,
            auto_create_session=True,
        )
        self._running = False
        self._inbound_task: asyncio.Task[None] | None = None
        self._session_locks: dict[str, asyncio.Lock] = {}

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        configure_outbound_publisher(self.bus.publish_outbound)
        if self.channel_manager:
            await self.channel_manager.start_all()
            await self.channel_manager.start_dispatcher()
        self._inbound_task = asyncio.create_task(self._consume_inbound())

    async def stop(self) -> None:
        self._running = False
        configure_outbound_publisher(None)
        if self._inbound_task:
            self._inbound_task.cancel()
            try:
                await self._inbound_task
            except asyncio.CancelledError:
                pass
            self._inbound_task = None
        if self.channel_manager:
            await self.channel_manager.stop_dispatcher()
            await self.channel_manager.stop_all()

    async def send_user_message(
        self,
        *,
        channel: str,
        sender_id: str,
        chat_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        await self.bus.publish_inbound(
            InboundMessage(
                channel=channel,
                sender_id=sender_id,
                chat_id=chat_id,
                content=content,
                metadata=metadata or {},
            )
        )

    async def process_message(self, msg: InboundMessage) -> OutboundMessage:
        lock = self._session_locks.setdefault(msg.session_key, asyncio.Lock())
        async with lock:
            request = types.UserContent(parts=[types.Part.from_text(text=msg.content)])
            final = ""
            with route_context(msg.channel, msg.chat_id):
                async for event in self.runner.run_async(
                    user_id=msg.sender_id,
                    session_id=msg.session_key,
                    new_message=request,
                ):
                    text = _extract_text(getattr(event, "content", None))
                    if text:
                        final = text
            if not final:
                final = "(no response)"
            return OutboundMessage(
                channel=msg.channel,
                chat_id=msg.chat_id,
                content=final,
                metadata=msg.metadata,
            )

    async def _consume_inbound(self) -> None:
        while self._running:
            try:
                msg = await asyncio.wait_for(self.bus.consume_inbound(), timeout=0.5)
            except asyncio.TimeoutError:
                continue
            response = await self.process_message(msg)
            await self.bus.publish_outbound(response)
