---
name: dragonpow2-overlay-sync
description: "同步 DragonPow2 live 治理规则与 ai-workspace-constitution 中 DragonPow2 overlay 的工作流。适用于用户要求把 DragonPow2 的 AGENTS/CLAUDE/agent-docs 回灌到 constitution、刷新 project overlay、同步本地 review gate 规则，或从 constitution 重新物化 DragonPow2 agent 文档时使用。"
---

# DragonPow2 Overlay 同步

这个 skill 管理 DragonPow2 live 工作区与 `ai-workspace-constitution` 中 DragonPow2 overlay 的双向同步。目标是让 constitution 成为可版本化 source of truth，同时避免把其他工作副本里的未提交改动混入本次同步。

## 适用场景

- 用户要求“同步 DragonPow2 规则到 constitution”。
- 用户要求“更新 ai-workspace-constitution 的 DragonPow2 overlay”。
- 用户刚在 DragonPow2 live 工作区调整了 `governance/agent-docs/`、`AGENTS.md`、`CLAUDE.md`、`scripts/sync-agent-docs.ps1` 或 `scripts/check-agent-docs.ps1`。
- 用户要求把 constitution 中的 DragonPow2 overlay 重新安装/物化到 live 工作区。

## 路径约定

- constitution 根目录：当前 Git 仓库根，通常是 `${WORKSPACE_ROOT}\ai-workspace-constitution`。
- DragonPow2 live 根目录：默认 `${WORKSPACE_ROOT}\DragonPow2`，也可能由 `manifests/machine.local.yaml` 的 `paths.dragonpow2_root` 覆盖。
- constitution overlay 目录：`governance/project-overlays/DragonPow2/`。
- live 模板源：`${DRAGONPOW2_ROOT}\governance\agent-docs\`。

不要在 skill 正文里写固定本机盘符路径；对话中报告实际路径时再使用已解析的完整路径。

## 从 DragonPow2 live 回灌到 constitution

1. **确认两个仓库状态**
   - 在 constitution 根目录运行 `git status --short --branch`。
   - 在 DragonPow2 live 根目录确认 VCS 状态；SVN 工作副本用 `svn status`，Git 工作副本用 `git status --short --branch`。
   - 标出无关未提交改动，后续只暂存/提交本次 overlay 同步相关文件。

2. **确认 live 规则已同步**
   - 在 DragonPow2 live 根目录运行：

```powershell
.\scripts\check-agent-docs.ps1 -IncludeRoot -Project DragonPow2_Trunk_Leaning
```

   - 如果目标项目不是 `DragonPow2_Trunk_Leaning`，替换为当前实际项目名。
   - 若 check 失败，先在 live 侧运行对应 `sync-agent-docs.ps1` 修正托管块，再回灌到 constitution。

3. **回灌 overlay 源文件**
   - 从 live 复制到 constitution：
     - `${DRAGONPOW2_ROOT}\governance\agent-docs\common.md` -> `governance/project-overlays/DragonPow2/agent-docs/common.md`
     - 必要时同步 `client.md`、`server.md`、`README.md`
     - 必要时同步 `scripts/sync-agent-docs.ps1`、`scripts/check-agent-docs.ps1`
   - 使用 UTF-8 写入，保留中文可读；不要把乱码、`�`、`??` 写入治理文件。

4. **刷新 root 模板**
   - 按 `governance/project-overlays/DragonPow2/README.md` 的流程，从 live 生成后的 `${DRAGONPOW2_ROOT}\AGENTS.md` 和 `${DRAGONPOW2_ROOT}\CLAUDE.md` 回灌：
     - `governance/project-overlays/DragonPow2/root/AGENTS.md.tmpl`
     - `governance/project-overlays/DragonPow2/root/CLAUDE.md.tmpl`
   - 若只改了 `common.md`，也可以用相同 managed block marker 重新生成 root 模板，但必须保证 marker 与 live 文件一致。

5. **更新 manifest**
   - 新增 workspace shared skill 时，必须同时更新 `manifests/default.yaml` 中 `.codex`、`.claude`、`.agents` 三个 shared skill mirror。
   - 只同步 DragonPow2 overlay 规则时，通常不需要改 manifest。

6. **验证**
   - constitution 根目录运行：

```powershell
.\tests\run.ps1
git diff --check -- governance/project-overlays/DragonPow2
```

   - 如涉及 manifest 或 installer，额外检查安装 smoke test 是否覆盖新增 source。

7. **提交边界**
   - 只暂存本次 overlay 同步相关文件，不使用 `git add .`。
   - 仓库里已有无关改动时必须保留，不纳入本次提交。
   - commit / push 前必须得到用户单独确认。

## 从 constitution 物化到 DragonPow2 live

1. 在 constitution 根目录确认 overlay 源文件已经是目标版本。
2. 运行 constitution install/update 或按 `governance/project-overlays/DragonPow2/README.md` 的安装目标复制到 `${DRAGONPOW2_ROOT}`。
3. 在 DragonPow2 live 根目录运行：

```powershell
.\scripts\sync-agent-docs.ps1 -IncludeRoot -Project DragonPow2_Trunk_Leaning
.\scripts\check-agent-docs.ps1 -IncludeRoot -Project DragonPow2_Trunk_Leaning
```

4. 检查 live 侧 VCS 状态，只确认目标托管块和模板源发生预期变化。

## Review Checklist

- 是否明确了同步方向：live -> constitution，还是 constitution -> live。
- 是否只处理 DragonPow2 overlay 文件，没有混入 constitution 里的其他脏改动。
- `agent-docs/common.md`、`root/AGENTS.md.tmpl`、`root/CLAUDE.md.tmpl` 的 managed block 内容是否一致。
- `cr_local.ps1`、codegraph、review gate 等规则是否只维护一份 source of truth。
- 新增 shared skill 是否加入 `.codex` / `.claude` / `.agents` 三个 manifest mirror。
- 所有新增或修改的治理文档是否为中文，必要技术名词保留英文。
