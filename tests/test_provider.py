"""Tests for provider helpers."""

from __future__ import annotations

import unittest

from sentientagent_v2.provider import normalize_model_name, validate_provider_runtime


class ProviderTests(unittest.TestCase):
    def test_openai_model_is_prefixed_when_missing_provider(self) -> None:
        self.assertEqual(normalize_model_name("openai", "gpt-4.1-mini"), "openai/gpt-4.1-mini")

    def test_openai_model_keeps_existing_provider_prefix(self) -> None:
        self.assertEqual(normalize_model_name("openai", "openai/gpt-4.1"), "openai/gpt-4.1")

    def test_openrouter_is_supported_by_runtime(self) -> None:
        issue = validate_provider_runtime("openrouter")
        self.assertIsNone(issue)

    def test_deepseek_model_is_prefixed_when_missing_provider(self) -> None:
        self.assertEqual(normalize_model_name("deepseek", "deepseek-chat"), "deepseek/deepseek-chat")

    def test_openai_codex_is_oauth_only_for_now(self) -> None:
        issue = validate_provider_runtime("openai_codex")
        self.assertIsNotNone(issue)
        self.assertIn("OAuth login is available", str(issue))


if __name__ == "__main__":
    unittest.main()
