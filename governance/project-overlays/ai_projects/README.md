# ai_projects overlay

本目录维护 `${WORKSPACE_ROOT}/ai_projects` 子工作区的本地 AI 规则入口。

同步范围：

- `root/AGENTS.md.tmpl` -> `${AI_PROJECTS_ROOT}/AGENTS.md`
- `root/CLAUDE.md.tmpl` -> `${AI_PROJECTS_ROOT}/CLAUDE.md`

只放 `ai_projects` 根层的多仓库约束、skills 路由和稳定入口说明。更深层具体项目，例如 `__gamedev_ai/dragonpow2-wulin/`，默认不在本 overlay 中创建，避免在没有该项目的新机器上生成空目录。若某个子项目需要跨机器治理，单独新增命名 overlay。
