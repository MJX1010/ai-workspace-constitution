# DragonPow2 项目 Overlay

本 overlay 用于版本化 DragonPow2 仓库自有的 AI 治理文件，避免把
DragonPow2 专用的 Unity、协议、Mock 等规则混入通用工作区治理层。

## 安装目标

- `root/AGENTS.md.tmpl` -> `${DRAGONPOW2_ROOT}/AGENTS.md`
- `root/CLAUDE.md.tmpl` -> `${DRAGONPOW2_ROOT}/CLAUDE.md`
- `agent-docs/` -> `${DRAGONPOW2_ROOT}/governance/agent-docs/`
- `scripts/` -> `${DRAGONPOW2_ROOT}/scripts/`

`${DRAGONPOW2_ROOT}` 默认是 `${WORKSPACE_ROOT}/DragonPow2`。如果某台机器使用不同 checkout 路径，在
`manifests/machine.local.yaml` 中覆盖 `paths.dragonpow2_root`。

## 更新流程

1. 修改 `agent-docs/` 下的源模板。
2. 在 DragonPow2 checkout 中运行 `${DRAGONPOW2_ROOT}/scripts/sync-agent-docs.ps1` 物化到目标工作副本。
3. 从生成后的 `${DRAGONPOW2_ROOT}/AGENTS.md` 和 `${DRAGONPOW2_ROOT}/CLAUDE.md` 回灌更新
   `root/AGENTS.md.tmpl` 和 `root/CLAUDE.md.tmpl`。
4. 运行 `${DRAGONPOW2_ROOT}/scripts/check-agent-docs.ps1 -IncludeRoot` 验证托管块同步状态。
