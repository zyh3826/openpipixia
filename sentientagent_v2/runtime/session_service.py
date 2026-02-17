"""Session service factory for ADK runner."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from google.adk.sessions import DatabaseSessionService, InMemorySessionService


@dataclass(slots=True)
class SessionBackendConfig:
    """Runtime session backend configuration."""

    backend: str
    db_url: str | None = None


def load_session_backend_config() -> SessionBackendConfig:
    backend = os.getenv("SENTIENTAGENT_V2_SESSION_BACKEND", "memory").strip().lower()
    db_url = os.getenv("SENTIENTAGENT_V2_SESSION_DB_URL", "").strip() or None
    return SessionBackendConfig(backend=backend, db_url=db_url)


def _default_sqlite_db_url() -> str:
    workspace_env = os.getenv("SENTIENTAGENT_V2_WORKSPACE")
    workspace = Path(workspace_env).expanduser().resolve() if workspace_env else Path.cwd().resolve()
    db_path = workspace / ".sentientagent_v2" / "sessions.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+aiosqlite:///{db_path}"


def create_session_service(config: SessionBackendConfig | None = None) -> Any:
    """Create ADK session service using env-configured backend."""
    cfg = config or load_session_backend_config()

    if cfg.backend in {"memory", "inmemory", "in-memory"}:
        return InMemorySessionService()

    if cfg.backend in {"sqlite", "db", "database"}:
        db_url = cfg.db_url or _default_sqlite_db_url()
        return DatabaseSessionService(db_url)

    raise ValueError(
        "Unsupported session backend. Use SENTIENTAGENT_V2_SESSION_BACKEND="
        "'memory' or 'sqlite'."
    )
