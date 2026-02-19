# sentientagent_v2 配置说明

## 配置来源与优先级

支持两种配置来源：

- 配置文件（推荐）：`~/.sentientagent_v2/config.json`
- 环境变量（覆盖配置文件）

建议日常只维护 `config.json`，环境变量仅用于临时覆盖。

## `config.json` 关键字段

- `agent.workspace` / `agent.builtinSkillsDir`
- `providers.<provider>.enabled / apiKey / model / apiBase / extraHeaders`
- `session.dbUrl`
- `channels.<name>.*`
- `web.enabled` / `web.search.*`
- `security.restrictToWorkspace / allowExec / allowNetwork / execAllowlist`
- `tools.mcpServers`
- `debug`

Provider 选择由 `enabled` 控制，建议保持“仅一个 provider 为 true”。

## 常用环境变量

### Provider / Runtime

- `GOOGLE_API_KEY`
- `OPENAI_API_KEY`
- `SENTIENTAGENT_V2_CHANNELS`
- `SENTIENTAGENT_V2_DEBUG`
- `SENTIENTAGENT_V2_DEBUG_MAX_CHARS`

### Session / Memory / Compaction

- `SENTIENTAGENT_V2_SESSION_DB_URL`
- `SENTIENTAGENT_V2_MEMORY_ENABLED`
- `SENTIENTAGENT_V2_MEMORY_BACKEND`
- `SENTIENTAGENT_V2_MEMORY_MARKDOWN_DIR`
- `SENTIENTAGENT_V2_COMPACTION_ENABLED`
- `SENTIENTAGENT_V2_COMPACTION_INTERVAL`
- `SENTIENTAGENT_V2_COMPACTION_OVERLAP`
- `SENTIENTAGENT_V2_COMPACTION_TOKEN_THRESHOLD`
- `SENTIENTAGENT_V2_COMPACTION_EVENT_RETENTION`

### WhatsApp Bridge

- `WHATSAPP_BRIDGE_URL`
- `WHATSAPP_BRIDGE_TOKEN`
- `SENTIENTAGENT_V2_WHATSAPP_BRIDGE_PRECHECK`
- `SENTIENTAGENT_V2_WHATSAPP_BRIDGE_SOURCE`

### Exec / MCP

- `SENTIENTAGENT_V2_EXEC_ALLOWLIST`
- `SENTIENTAGENT_V2_MCP_SERVERS_JSON`
- `SENTIENTAGENT_V2_MCP_REQUIRED_SERVERS`
- `SENTIENTAGENT_V2_MCP_PROBE_RETRY_ATTEMPTS`
- `SENTIENTAGENT_V2_MCP_PROBE_RETRY_BACKOFF_SECONDS`
- `SENTIENTAGENT_V2_MCP_DOCTOR_TIMEOUT_SECONDS`
- `SENTIENTAGENT_V2_MCP_GATEWAY_TIMEOUT_SECONDS`

## 配置样例

```json
{
  "agent": {
    "workspace": "~/.sentientagent_v2/workspace",
    "builtinSkillsDir": ""
  },
  "providers": {
    "google": {
      "enabled": true,
      "apiKey": "your_google_api_key",
      "model": "gemini-3-flash-preview"
    },
    "openai": {
      "enabled": false,
      "apiKey": "",
      "model": "openai/gpt-4.1-mini"
    }
  },
  "session": {
    "dbUrl": ""
  },
  "channels": {
    "local": {
      "enabled": false
    },
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "",
      "verificationToken": ""
    }
  },
  "web": {
    "enabled": true,
    "search": {
      "enabled": true,
      "provider": "brave",
      "apiKey": "your_brave_api_key",
      "maxResults": 5
    }
  },
  "security": {
    "restrictToWorkspace": false,
    "allowExec": true,
    "allowNetwork": true,
    "execAllowlist": []
  },
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": [
          "-y",
          "@modelcontextprotocol/server-filesystem",
          "/absolute/path/to/workspace"
        ]
      }
    }
  },
  "debug": false
}
```

## 平台说明

### Feishu

如果环境使用 SOCKS 代理，Feishu websocket 依赖 `python-socks`（默认依赖已包含）。

### WhatsApp

WhatsApp bridge 依赖 Node.js `>=20`，运行时目录位于 `~/.sentientagent_v2/bridge/`。
