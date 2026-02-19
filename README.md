# sentientagent_v2

`sentientagent_v2` is a lightweight, skills-first agent runtime built on Google ADK.

It focuses on:

- Multi-channel gateway execution
- Local skill loading (`SKILL.md`)
- Built-in action tools (file/shell/web/message/cron/subagent)
- Persistent session + optional long-term memory

Compared with larger systems, this project keeps the core runtime compact and easy to iterate.

## Quick Start

```bash
cd sentientagent_v2_root
pip install -e .
sentientagent_v2 onboard
python -m sentientagent_v2.cli -m "Describe what you can do"
```

## Common Commands

```bash
# local gateway
python -m sentientagent_v2.cli gateway-local

# multi-channel gateway
sentientagent_v2 gateway --channels local,feishu --interactive-local

# diagnostics
sentientagent_v2 doctor
sentientagent_v2 skills
```

## Core Capabilities

- Runtime: Google ADK (`LlmAgent` + tools + callbacks)
- Session: SQLite-backed ADK session service
- Memory backends: `in_memory` / `markdown`
- Context compaction: ADK `EventsCompactionConfig`
- Slash commands: `/help` and `/new`
- Channel bridge: local + mainstream chat connectors

## Project Layout

```text
sentientagent_v2_root/
├── README.md
├── docs/
├── sentientagent_v2/
├── tests/
└── scripts/
```

## Documentation

Detailed docs are in [`docs/`](./docs/):

- [`docs/PROJECT_OVERVIEW.md`](./docs/PROJECT_OVERVIEW.md)
- [`docs/OPERATIONS.md`](./docs/OPERATIONS.md)
- [`docs/CONFIGURATION.md`](./docs/CONFIGURATION.md)
- [`docs/MCP_SECURITY.md`](./docs/MCP_SECURITY.md)
- [`docs/README.md`](./docs/README.md)

## Testing

```bash
source .venv/bin/activate
pytest -q
```

## Acknowledgements

This project is inspired by and partially adapted from [nanobot](https://github.com/HKUDS/nanobot).
