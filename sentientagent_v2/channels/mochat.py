"""Mochat channel adapter (minimal outbound API integration)."""

from __future__ import annotations

import asyncio
import functools
import json
import logging
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..bus.events import OutboundMessage
from .base import BaseChannel

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class MochatTarget:
    """Resolved Mochat outbound target."""

    id: str
    is_panel: bool


class MochatChannel(BaseChannel):
    """Minimal Mochat adapter with HTTP outbound support."""

    name = "mochat"

    def __init__(
        self,
        bus,
        *,
        base_url: str,
        claw_token: str,
        allow_from: list[str] | None = None,
    ) -> None:
        super().__init__(bus, allow_from=allow_from)
        self.base_url = base_url.strip().rstrip("/")
        self.claw_token = claw_token.strip()

    async def start(self) -> None:
        if not self.base_url:
            raise RuntimeError("Missing MOCHAT_BASE_URL for mochat channel.")
        if not self.claw_token:
            raise RuntimeError("Missing MOCHAT_CLAW_TOKEN for mochat channel.")
        self._running = True

    async def stop(self) -> None:
        self._running = False

    async def send(self, msg: OutboundMessage) -> None:
        content = (msg.content or "").strip()
        if not content:
            return

        target = self.resolve_target(msg.chat_id)
        if not target.id:
            logger.warning("Skip Mochat send: empty target chat_id.")
            return

        payload: dict[str, Any]
        if target.is_panel:
            payload = {"panelId": target.id, "content": content}
            group_id = self._read_group_id(msg.metadata)
            if group_id:
                payload["groupId"] = group_id
            if msg.reply_to:
                payload["replyTo"] = msg.reply_to
            await self._post_json("/api/claw/groups/panels/send", payload)
            return

        payload = {"sessionId": target.id, "content": content}
        if msg.reply_to:
            payload["replyTo"] = msg.reply_to
        await self._post_json("/api/claw/sessions/send", payload)

    @staticmethod
    def resolve_target(raw: str) -> MochatTarget:
        """Resolve target id/type from user chat_id string."""
        text = (raw or "").strip()
        if not text:
            return MochatTarget(id="", is_panel=False)

        lowered = text.lower()
        cleaned = text
        forced_panel = False
        for prefix in ("mochat:", "group:", "channel:", "panel:"):
            if lowered.startswith(prefix):
                cleaned = text[len(prefix):].strip()
                forced_panel = prefix in {"group:", "channel:", "panel:"}
                break
        if not cleaned:
            return MochatTarget(id="", is_panel=False)
        return MochatTarget(id=cleaned, is_panel=forced_panel or not cleaned.startswith("session_"))

    def _post_json_sync(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        req = Request(
            f"{self.base_url}{path}",
            data=body,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "X-Claw-Token": self.claw_token,
            },
            method="POST",
        )
        try:
            with urlopen(req, timeout=30) as response:
                raw = response.read().decode("utf-8")
            parsed = json.loads(raw) if raw else {}
        except HTTPError as exc:
            raise RuntimeError(f"Mochat API HTTP error ({path}): {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError(f"Mochat API network error ({path}): {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Mochat API invalid JSON ({path}): {exc}") from exc

        if not isinstance(parsed, dict):
            return {}
        if isinstance(parsed.get("code"), int):
            code = int(parsed.get("code", 0))
            if code != 200:
                message = str(parsed.get("message", "request failed"))
                raise RuntimeError(f"Mochat API error ({path}): {message} (code={code})")
            data = parsed.get("data")
            return data if isinstance(data, dict) else {}
        return parsed

    async def _post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        loop = asyncio.get_running_loop()
        call = functools.partial(self._post_json_sync, path, payload)
        return await loop.run_in_executor(None, call)

    @staticmethod
    def _read_group_id(metadata: dict[str, Any]) -> str | None:
        if not isinstance(metadata, dict):
            return None
        value = metadata.get("group_id") or metadata.get("groupId")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None
