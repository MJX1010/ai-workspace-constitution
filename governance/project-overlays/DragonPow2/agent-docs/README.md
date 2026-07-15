# DragonPow2 Agent 文档统一管理

本目录是多个 DragonPow2 工作区共享的 `AGENTS.md` / `CLAUDE.md` 模板源。

## 文件

- `common.md`：所有项目顶层共享规则。
- `client.md`：客户端 `client/` 子层规则。
- `server.md`：服务端 `server/` 子层规则。

## 同步

从 `<DragonPow2根目录>` 运行：

```powershell
.\scripts\sync-agent-docs.ps1
.\scripts\check-agent-docs.ps1
```

只同步当前多项目根和指定项目：

```powershell
.\scripts\sync-agent-docs.ps1 -IncludeRoot -Project DragonPow2_Trunk_Leaning
.\scripts\check-agent-docs.ps1 -IncludeRoot -Project DragonPow2_Trunk_Leaning
```

同步脚本只更新托管块，托管块之外的项目本地说明会保留。
