# Claude Code Environment Configuration

CC switch 切换 API Key 时会覆盖 `~/.claude/settings.json`，本目录记录所有插件、MCP、Skill 的安装配置，方便快速恢复。

## 快速恢复

切换 API Key 后，执行以下操作恢复完整环境：

```bash
# 1. 恢复 settings.json（合并插件配置到当前 settings.json）
bash D:/Projects/.claude/env/restore-settings.sh

# 2. 如果插件缓存被清除，需重新安装（通常不会）
# 在 Claude Code 交互中执行：
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
/plugin marketplace add obra/superpowers
/plugin install superpowers@superpowers-marketplace
```

## 目录结构

```
env/
  README.md                    # 本文件
  plugins-inventory.md         # 所有插件清单与安装命令
  settings-reference.json      # settings.json 完整参考配置
  restore-settings.sh          # 自动恢复脚本
```

## CC Switch 影响范围分析

| 文件 | 是否被覆盖 | 说明 |
|------|-----------|------|
| `~/.claude/settings.json` | **YES** | env + model 被替换 |
| `~/.claude/plugins/installed_plugins.json` | NO | 插件注册独立存储 |
| `~/.claude/plugins/known_marketplaces.json` | NO | marketplace 独立存储 |
| `~/.claude/plugins/cache/` | NO | 插件代码缓存不受影响 |
| `~/.claude-mem/settings.json` | NO | claude-mem 独立配置 |
| `~/.memsearch/config.toml` | NO | memsearch 独立配置 |
| 项目级 `.claude/settings.local.json` | NO | 不受影响 |

> **结论**: CC switch 只覆盖 `settings.json` 的 `env`/`model` 字段。如果 settings.json 中有 `enabledPlugins`、`hooks`、`mcpServers` 等字段，切换时可能被丢失。建议将这些配置放入项目级 `settings.local.json` 或使用恢复脚本。
