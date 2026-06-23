# AI 环境备份与新机器恢复说明

状态：建议稿
适用范围：Claude Code、Codex、MCP、plugins、skills、agents、superpowers，以及 `D:\Projects` 工作区治理。

## 1. 备份边界

本仓库备份的是可复用配置和恢复清单，不备份真实凭证。

会进入 Git：

- Codex 全局 agents：`governance/global/codex/agents/`
- Codex 非 `.system` skills：`governance/global/codex/skills/`
- Codex/Claude MCP 模板：`governance/global/{codex,claude}/mcp/mcp-servers.json`
- Claude 插件安装清单和 marketplace 清单：`governance/global/claude/plugins/*.redacted.json`
- Claude/Codex 脱敏配置快照：`governance/global/{claude,codex}/`
- superpowers 版本和 skill 列表：`governance/global/superpowers/`
- 当前机器摘要：`governance/environment-inventory/current-windows.redacted.json`

不会进入 Git：

- `auth.json`、`cap_sid`、`.credentials.json`
- `settings.json` 中真实 token、key、secret、password
- session、history、logs、cache、SQLite、插件缓存
- Codex bundled `.system` skills
- Claude plugin cache 整包

## 2. 新机器恢复顺序

```powershell
git clone https://github.com/MJX1010/ai-workspace-constitution.git D:\Projects\ai-workspace-constitution
cd D:\Projects\ai-workspace-constitution
$env:WORKSPACE_ROOT = "D:\Projects"
.\scripts\install.ps1 --workspace-root $env:WORKSPACE_ROOT --yes
.\scripts\verify.ps1 --workspace-root $env:WORKSPACE_ROOT
```

`--workspace-root` 控制工作区目标；全局 Codex/Claude 目标默认写入当前用户 HOME。若只是演练或测试，必须同时覆盖 `--user-home`：

```powershell
$tmp = Join-Path $env:TEMP "ai-constitution-smoke"
.\scripts\install.ps1 --workspace-root $tmp --user-home (Join-Path $tmp "home") --yes --verbose
.\scripts\verify.ps1 --workspace-root $tmp
```

安装器会恢复：

- `D:\Projects` 工作区治理入口
- workspace skills 到 `.agents` / `.codex` / `.claude`
- Codex 全局 agents
- Codex 全局非 `.system` skills
- Codex/Claude MCP placeholder 配置
- Claude env 恢复说明
- `skills-lock.json`

## 3. 需要手动完成的内容

### Claude Code

1. 重新登录或重新配置 provider token。
2. 参考 `governance/global/claude/settings/settings.redacted.json` 恢复模型名、hooks、插件启用状态。
3. 参考 `governance/global/claude/plugins/known_marketplaces.redacted.json` 添加 marketplace。
4. 参考 `governance/global/claude/plugins/installed_plugins.redacted.json` 安装插件。

示例：

```text
/plugin marketplace add <marketplace>
/plugin install <plugin>@<marketplace>
```

不要复制旧机器的 `settings.json` 原文；其中可能包含真实鉴权 token。

### Codex

1. 重新登录 Codex。
2. 按 `governance/global/codex/config/config.redacted.toml` 复核模型 provider、MCP server、plugin 启用状态。
3. machine-specific runtime 路径、native pipe、hook trusted hash 不跨机器复用。

### MCP

`mcp-servers.json` 中的 `YOUR_*_HERE` 是占位符。新机器需要按实际账号填入环境变量或本机 secret manager，不要把真实值写回 Git。

### superpowers

`governance/global/superpowers/codex-superpowers-package.json` 记录 Codex 侧 superpowers 版本；`codex-superpowers-skills.txt` 记录当前 skill 列表。恢复时优先使用官方安装方式，再应用工作区规则里的 whitelist。

## 4. 验证

恢复后运行：

```powershell
.\scripts\verify.ps1 --workspace-root D:\Projects
```

再检查：

```powershell
codex mcp list
```

Claude Code 侧用插件命令查看 marketplace 和已安装插件；如果某个插件需要账号授权，先完成登录或 OAuth。

## 5. 安全检查

提交前运行：

```powershell
rg -n "tp-[A-Za-z0-9]|sk-[A-Za-z0-9]|api[_-]?key\s*[=:]|secret\s*[=:]|password\s*[=:]|authorization\s*[=:]" governance docs manifests
```

命中示例、占位符或安全说明可以保留；真实 token、key、cookie、session 必须删除并轮换。
