# sentientagent_v2 运行与操作指南

## 安装

```bash
cd sentientagent_v2
pip install -e .
```

## 初始化（推荐）

```bash
sentientagent_v2 onboard
```

初始化后会生成：

- `~/.sentientagent_v2/config.json`
- `~/.sentientagent_v2/workspace`

## 运行方式

### 单轮调用

```bash
python -m sentientagent_v2.cli -m "Describe what you can do"
```

可显式指定会话标识：

```bash
python -m sentientagent_v2.cli -m "Describe what you can do" --user-id local --session-id demo001
```

### ADK CLI 模式

```bash
adk run sentientagent_v2
```

### Wrapper CLI

```bash
sentientagent_v2 run
```

### 常用工具命令

```bash
sentientagent_v2 skills
sentientagent_v2 doctor
sentientagent_v2 provider list
sentientagent_v2 provider status
sentientagent_v2 provider status --json
sentientagent_v2 provider login github-copilot
sentientagent_v2 provider login openai-codex
sentientagent_v2 provider login codex
sentientagent_v2 channels login
sentientagent_v2 channels bridge start
sentientagent_v2 channels bridge status
sentientagent_v2 channels bridge stop
```

## Gateway 模式

### 本地通道

```bash
python -m sentientagent_v2.cli gateway-local
```

### 多通道模式（含 Feishu）

```bash
sentientagent_v2 gateway --channels local,feishu --interactive-local
```

也可通过环境变量指定默认通道：

```bash
export SENTIENTAGENT_V2_CHANNELS=feishu
sentientagent_v2 gateway
```

## WhatsApp Bridge

`sentientagent_v2` 使用本地 Node.js Bridge（Baileys + WebSocket）完成 WhatsApp 登录和消息收发。

```bash
# 前台扫码登录
sentientagent_v2 channels login

# 后台 bridge 生命周期
sentientagent_v2 channels bridge start
sentientagent_v2 channels bridge status
sentientagent_v2 channels bridge stop
```

快速自检：

```bash
scripts/whatsapp_bridge_e2e.sh full
scripts/whatsapp_bridge_e2e.sh smoke
```

## Cron 调度

`sentientagent_v2` 的 cron 是进程内调度器，不写系统 crontab。只有网关运行时任务才会执行。

- 存储文件：`SENTIENTAGENT_V2_WORKSPACE/.sentientagent_v2/cron_jobs.json`
- 支持调度：`every`、`cron`（可配 `tz`）、`at`

常用命令：

```bash
sentientagent_v2 cron list
sentientagent_v2 cron add --name weather --message "check weather and summarize" --every 300
sentientagent_v2 cron add --name daily --message "daily report" --cron "0 9 * * 1-5" --tz Asia/Shanghai
sentientagent_v2 cron add --name reminder --message "remind me to review PR" --at 2026-02-19T09:30:00
sentientagent_v2 cron add --name push --message "send update" --every 600 --deliver --channel feishu --to ou_xxx
sentientagent_v2 cron run <job_id>
sentientagent_v2 cron enable <job_id>
sentientagent_v2 cron enable <job_id> --disable
sentientagent_v2 cron remove <job_id>
sentientagent_v2 cron status
```

## 测试

```bash
source .venv/bin/activate
pytest -q
```

## 示例

```bash
python -m sentientagent_v2.cli -m "search for the latest research progress today, and create a PPT for me."
python -m sentientagent_v2.cli -m "download all PDF files from this page: https://bbs.kangaroo.study/forum.php?mod=viewthread&tid=467"
```
