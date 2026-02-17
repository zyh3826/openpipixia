"""Tests for session service backend factory."""

from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch

from google.adk.sessions import InMemorySessionService

from sentientagent_v2.runtime.session_service import (
    SessionBackendConfig,
    create_session_service,
    load_session_backend_config,
)


class SessionServiceFactoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self._env_backup = dict(os.environ)

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._env_backup)

    def test_load_backend_defaults_to_memory(self) -> None:
        os.environ.pop("SENTIENTAGENT_V2_SESSION_BACKEND", None)
        cfg = load_session_backend_config()
        self.assertEqual(cfg.backend, "memory")
        self.assertIsNone(cfg.db_url)

    def test_create_memory_backend(self) -> None:
        svc = create_session_service(SessionBackendConfig(backend="memory"))
        self.assertIsInstance(svc, InMemorySessionService)

    def test_create_sqlite_backend_uses_db_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_url = f"sqlite+aiosqlite:///{tmp}/sessions.db"
            with patch("sentientagent_v2.runtime.session_service.DatabaseSessionService") as mocked:
                mocked.return_value = object()
                out = create_session_service(SessionBackendConfig(backend="sqlite", db_url=db_url))
                self.assertIsNotNone(out)
                mocked.assert_called_once_with(db_url)


if __name__ == "__main__":
    unittest.main()
