"""Small ADK helpers shared across CLI and gateway."""

from __future__ import annotations

from google.genai import types


def extract_text(content: types.Content | None) -> str:
    """Join text parts from an ADK content payload."""
    if content is None or not content.parts:
        return ""
    chunks: list[str] = []
    for part in content.parts:
        text = getattr(part, "text", None)
        if text:
            chunks.append(text)
    return "\n".join(chunks).strip()
