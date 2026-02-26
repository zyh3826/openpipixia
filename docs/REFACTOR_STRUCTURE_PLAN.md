# Openheron Package Refactor Plan (Phase 1)

## Goal

Reorganize `openheron/` by domain boundaries while keeping behavior unchanged.
Phase 1 only introduces package skeleton and migration map.

## Target Packages

- `openheron/app/`: app entry, agent assembly, bootstrap wiring.
- `openheron/core/`: shared orchestration/domain logic.
- `openheron/tooling/`: tool definitions and tool adapters.
- `openheron/gui/`: GUI planning/execution runtime.
- `openheron/browser/`: browser runtime/services/routes/schema.
- Existing `openheron/runtime/`, `openheron/channels/`, `openheron/bridge/`, `openheron/bus/` remain as-is.

## Current -> Target Mapping

### App layer

- `openheron/agent.py` -> `openheron/app/agent.py`
- `openheron/cli.py` -> `openheron/app/cli.py`
- `openheron/gateway.py` -> `openheron/app/gateway.py`

### Tool layer

- `openheron/tools.py` -> `openheron/tooling/registry.py` (migrated, legacy shim kept)
- `openheron/skills.py` -> `openheron/tooling/skills_adapter.py` (migrated, legacy shim kept)

### GUI layer

- `openheron/gui_executor.py` -> `openheron/gui/executor.py`
- `openheron/gui_task_runner.py` -> `openheron/gui/task_runner.py`

### Browser layer

- `openheron/browser_playwright_runtime.py` -> `openheron/browser/playwright_runtime.py`
- `openheron/browser_runtime.py` -> `openheron/browser/runtime.py`
- `openheron/browser_service.py` -> `openheron/browser/service.py`
- `openheron/browser_routes.py` -> `openheron/browser/routes.py`
- `openheron/browser_schema.py` -> `openheron/browser/schema.py`

### Core/shared layer

- `openheron/config.py` -> `openheron/core/config.py` (migrated, legacy shim kept)
- `openheron/provider.py` -> `openheron/core/provider.py` (migrated, legacy shim kept)
- `openheron/provider_registry.py` -> `openheron/core/provider_registry.py` (migrated, legacy shim kept)
- `openheron/openai_codex_llm.py` -> `openheron/core/openai_codex_llm.py` (migrated, legacy shim kept)
- `openheron/mcp_registry.py` -> `openheron/core/mcp_registry.py` (migrated, legacy shim kept)
- `openheron/exec_policy.py` -> `openheron/core/exec_policy.py` (migrated, legacy shim kept)
- `openheron/security.py` -> `openheron/core/security.py` (migrated, legacy shim kept)
- `openheron/doctor_rules.py` -> `openheron/core/doctor_rules.py` (migrated, legacy shim kept)
- `openheron/install_rules.py` -> `openheron/core/install_rules.py` (migrated, legacy shim kept)
- `openheron/onboarding_adapters.py` -> `openheron/core/onboarding_adapters.py` (migrated, legacy shim kept)
- `openheron/logging_utils.py` -> `openheron/core/logging_utils.py` (migrated, legacy shim kept)
- `openheron/env_utils.py` -> `openheron/core/env_utils.py` (migrated, legacy shim kept)

## Execution Phases

1. Phase 1 (done in this change): create package skeleton and mapping doc.
2. Phase 2: split oversized files with compatibility imports to avoid breakage.
   Note: `openheron.tools` currently points to `tools.py`, so staged target package
   uses `openheron.tooling` first to avoid import shadowing.
   Progress:
   - App migration completed:
     - `openheron/agent.py` -> `openheron/app/agent.py` (legacy module alias shim kept)
     - `openheron/gateway.py` -> `openheron/app/gateway.py` (legacy module alias shim kept)
     - `openheron/cli.py` -> `openheron/app/cli.py` (legacy module alias shim kept)
   - Browser migration completed:
     - `openheron/browser_runtime.py` -> `openheron/browser/runtime.py` (legacy module alias shim kept)
     - `openheron/browser_playwright_runtime.py` -> `openheron/browser/playwright_runtime.py` (legacy module alias shim kept)
     - `openheron/browser_service.py` -> `openheron/browser/service.py` (legacy module alias shim kept)
     - `openheron/browser_routes.py` -> `openheron/browser/routes.py` (legacy module alias shim kept)
     - `openheron/browser_schema.py` -> `openheron/browser/schema.py` (legacy module alias shim kept)
   - GUI migration completed:
     - `openheron/gui_executor.py` -> `openheron/gui/executor.py` (legacy shim kept)
     - `openheron/gui_task_runner.py` -> `openheron/gui/task_runner.py` (legacy shim kept)
3. Phase 3: migrate call sites and tests to new import paths.
   Progress:
   - Internal package call sites now use new paths directly:
     - `openheron/tools.py` now imports from `openheron.browser.*` and `openheron.gui.*`
     - `openheron/__init__.py` now resolves `root_agent` from `openheron.app.agent`
     - `openheron/config.py`, `openheron/install_rules.py`, `openheron/app/agent.py`, `openheron/app/cli.py`
       now import provider modules from `openheron.core.*`
     - `openheron/app/agent.py` and `openheron/app/cli.py` now import MCP registry from `openheron.core.mcp_registry`
     - `openheron/core/provider.py` now imports Codex adapter from `openheron.core.openai_codex_llm`
     - `openheron/tools.py`, `openheron/exec_policy.py`, `openheron/app/gateway.py`, `openheron/app/cli.py`
       now import security APIs from `openheron.core.security`
     - `openheron/runtime/token_usage_store.py` now imports config APIs from `openheron.core.config`
     - `openheron/onboarding_adapters.py` now imports install rules from `openheron.core.install_rules`
     - `openheron/core/install_rules.py` now imports doctor rules from `openheron.core.doctor_rules`
     - `openheron/app/cli.py` now imports onboarding adapters from `openheron.core.onboarding_adapters`
     - `openheron/tools.py`, `openheron/skills.py`, `openheron/browser/runtime.py`, `openheron/app/cli.py`
       now import env/logging utilities from `openheron.core.env_utils` and `openheron.core.logging_utils`
     - `openheron/core/config.py`, `openheron/core/security.py`, `openheron/core/mcp_registry.py`
       now use `openheron.core.env_utils` internally
     - `openheron/app/agent.py` and `openheron/app/cli.py` now import skill registry APIs from
       `openheron.tooling.skills_adapter`
     - `openheron/app/agent.py` and `openheron/app/gateway.py` now import tool APIs from
       `openheron.tooling.registry`
4. Phase 4: remove temporary compatibility shims. (completed)
   Progress:
   - Removed all top-level compatibility shim modules under `openheron/`.
   - Updated package/tests/scripts import paths to new package layout.
   - Kept lightweight package-level compatibility exports in `openheron/__init__.py`:
     - `openheron.agent` -> `openheron.app.agent`
     - `openheron.cli` -> `openheron.app.cli`
     - `openheron.gateway` -> `openheron.app.gateway`

## Safety Rules

- Keep existing public imports working during migration.
- One domain at a time (GUI, then Browser, then Tool/Core).
- Run focused tests after each migration step.
