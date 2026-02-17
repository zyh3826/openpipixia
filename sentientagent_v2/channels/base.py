"""Base channel interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..bus.events import InboundMessage, OutboundMessage
from ..bus.queue import MessageBus


class BaseChannel(ABC):
    """Base interface for all channel adapters."""

    name: str = "base"

    def __init__(self, bus: MessageBus):
        self.bus = bus
        self._running = False

    @abstractmethod
    async def start(self) -> None:
        """Start channel workers/connections."""

    @abstractmethod
    async def stop(self) -> None:
        """Stop channel workers/connections."""

    @abstractmethod
    async def send(self, msg: OutboundMessage) -> None:
        """Send outbound message to channel."""

    async def publish_inbound(
        self,
        *,
        sender_id: str,
        chat_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        await self.bus.publish_inbound(
            InboundMessage(
                channel=self.name,
                sender_id=sender_id,
                chat_id=chat_id,
                content=content,
                metadata=metadata or {},
            )
        )

    @property
    def is_running(self) -> bool:
        return self._running
