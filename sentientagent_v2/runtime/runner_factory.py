"""Runner construction helpers shared by CLI and gateway."""

from __future__ import annotations

from typing import Any

from google.adk.runners import Runner

from .session_service import create_session_service


def create_runner(
    *,
    agent: Any,
    app_name: str,
    session_service: Any | None = None,
) -> tuple[Runner, Any]:
    """Create a runner with a shared session service contract."""
    service = session_service or create_session_service()
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=service,
        auto_create_session=True,
    )
    return runner, service
