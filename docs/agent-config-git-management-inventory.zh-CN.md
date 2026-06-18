# D:\Projects Agent 配置与文档 Git 管理清单

状态：建议稿  
盘点范围：`D:\Projects` 顶层 Agent 入口、`.agents`、`.codex`、`.claude`、`ai-workspace-constitution` 中的治理源。  
结论：可版本化的 source of truth 应进入 `D:\Projects\ai-workspace-constitution` Git 仓库；`D:\Projects` 下已经渲染出来的 live 配置可以被个人治理仓库管理，但默认不作为业务/产品仓库提交物。

## 1. 管理原则

Agent 相关文件分三类：

| 分类 | 处理方式 | 判断标准 |
|---|---|---|
| 可直接 Git 管理 | 放入 `ai-workspace-constitution` | 用户自写、可复用、无密钥、跨机器稳定 |
| 间接 Git 管理 | live 文件不提交，只提交模板或 manifest | 当前文件是 installer 渲染目标、软链接目标、机器本地配置 |
| 禁止 Git 管理 | 保持本地或忽略 | 密钥、会话、缓存、状态、备份、插件安装产物、生成物 |

关键约束：

- 不把 live 的 `D:\Projects\AGENTS.md` / `CLAUDE.md` 作为业务/产品仓库提交物；若要版本化，放进个人治理仓库或 constitution 模板/快照。
- 不提交 `D:\Projects\.codex`、`.claude`、`.agents` 下的备份、缓存、运行状态。
- 能通过模板生成的文件，提交模板，不提交渲染结果。
- 外部来源 skill 优先提交 lock/manifest，不直接 vendor，除非需要固定快照且带来源说明。

## 2. 当前已适合放入 Git 的内容

这些内容已经在 `ai-workspace-constitution` 中，适合继续作为 Git 管理对象：

| constitution 路径 | 管理内容 | 目标 |
|---|---|---|
| `governance/workspace/AGENTS.md.tmpl` | 工作区 Codex/Agent 入口模板 | `D:\Projects\AGENTS.md` |
| `governance/workspace/CLAUDE.md.tmpl` | 工作区 Claude 入口模板 | `D:\Projects\CLAUDE.md` |
| `governance/workspace/GEMINI.md.tmpl` | 工作区 Gemini 入口模板 | `D:\Projects\GEMINI.md` |
| `governance/workspace/README_AI_GOVERNANCE.md.tmpl` | 人读治理说明模板 | `D:\Projects\README_AI_GOVERNANCE.md` |
| `governance/global/codex/AGENTS.md.partial.tmpl` | HOME 级 Codex marker section | `~\.codex\AGENTS.md` 局部区域 |
| `governance/global/claude/CLAUDE.md.partial.tmpl` | HOME 级 Claude marker section | `~\.claude\CLAUDE.md` 局部区域 |
| `governance/workspace-config/codex.config.toml.tmpl` | Codex 工作区配置模板 | `D:\Projects\.codex\config.toml` |
| `governance/workspace-config/claude.settings.local.json.tmpl` | Claude 项目设置模板 | `D:\Projects\.claude\settings.local.json` |
| `governance/workspace-skills/shared/workspace-governance/` | 工作区治理 skill 源 | `.agents` / `.codex` / `.claude` 镜像 |
| `governance/workspace-skills/shared/skill-factory-playbook/` | skill 创建流程源 | `.agents` / `.codex` / `.claude` 镜像 |
| `governance/workspace-skills/shared/feature-spec-workflow/` | specs 工作流源 | `.agents` / `.codex` / `.claude` 镜像 |
| `governance/workspace-skills/shared/github-sync-commit/` | GitHub 同步提交 skill 源 | `.agents` / `.codex` / `.claude` 镜像 |
| `governance/workspace-skills/codex-only/manage-superpowers-whitelist/` | Codex 专用 skill 源 | `D:\Projects\.codex\skills` |
| `governance/workspace-scripts/codex/manage-superpowers.*` | Codex helper 脚本源 | `D:\Projects\.codex\scripts` |
| `governance/project-overlays/DragonPow2/` | DragonPow2 overlay 源 | `D:\Projects\DragonPow2` 相关目标 |
| `manifests/default.yaml` | 默认安装清单 | installer source of truth |
| `manifests/machine.example.yaml` | 本机覆盖示例 | 可提交示例，不提交真实 local |
| `scripts/` | install/update/verify/upstream-watch 实现 | constitution 工具链 |
| `tests/` | 渲染与 smoke test | constitution 验证 |
| `docs/` | 架构、同步范围、策略、ADR、当前盘点文档 | 治理知识库 |

这些文件的特点是：没有真实密钥，能跨机器复用，是当前治理体系的 source of truth。

## 3. 当前 live 文件的处理方式

以下文件存在于 `D:\Projects` live 工作区，建议只通过 constitution 模板间接管理，不直接把 live 文件提交进 Git：

| live 路径 | 推荐处理 | 原因 |
|---|---|---|
| `D:\Projects\AGENTS.md` | 推荐提交 `governance/workspace/AGENTS.md.tmpl`；需要精确追踪 live 时可放 constitution 快照 | 渲染目标，可能含本机路径和临时规则 |
| `D:\Projects\CLAUDE.md` | 推荐提交 `governance/workspace/CLAUDE.md.tmpl`；需要精确追踪 live 时可放 constitution 快照 | 渲染目标 |
| `D:\Projects\GEMINI.md` | 推荐提交 `governance/workspace/GEMINI.md.tmpl`；需要精确追踪 live 时可放 constitution 快照 | 渲染目标 |
| `D:\Projects\README_AI_GOVERNANCE.md` | 推荐提交模板；需要精确追踪 live 时可放 constitution 快照 | 渲染目标 |
| `D:\Projects\.codex\config.toml` | 不直接提交；提交 `codex.config.toml.tmpl` | 本机 live 配置 |
| `D:\Projects\.claude\settings.local.json` | 不直接提交；提交 `claude.settings.local.json.tmpl` | 本机 live 配置，可能随工具变化 |
| `D:\Projects\.codex\scripts\manage-superpowers.*` | 不直接提交 live；提交 constitution 源脚本 | 已有源脚本 |
| `D:\Projects\.codex\skills\*` | 不直接提交 live；提交 workspace skill 源 | 镜像目标 |
| `D:\Projects\.claude\skills\*` | 不直接提交 live；提交 workspace skill 源或 lock | 镜像目标或 junction |
| `D:\Projects\.agents\skills\*` | 视来源处理；用户自写 skill 可迁入 constitution | 混合了源、镜像、外部安装内容 |

## 4. 本次已迁入 constitution 管理的内容

这些内容原本在 `D:\Projects` live 目录下，本次已迁入 constitution 的稳定 source of truth，并通过 `manifests/default.yaml` 进入安装清单。

### 4.1 `skills-lock.json`

当前路径：

```text
D:\Projects\skills-lock.json
```

处理：

- 已迁到 `ai-workspace-constitution\manifests\skills-lock.json`。
- 当前内容只记录 `lark-doc`、`lark-shared` 的来源和 hash，没有真实密钥，适合版本化。
- 已通过 `workspace_skills_lock` 组件安装回 `D:\Projects\skills-lock.json`。

原因：外部 skill 更适合用 lock 固定来源和 hash，而不是直接复制安装结果。

### 4.2 `.agents\skills\browser-doc-crawler`

当前路径：

```text
D:\Projects\.agents\skills\browser-doc-crawler
```

处理：

- 已迁入 `governance\workspace-skills\shared\browser-doc-crawler\`。
- 已改用 `${WORKSPACE_ROOT}` 写法，避免固定 `D:\Projects` 路径。
- 已通过 manifest 同步到 `.agents` / `.codex` / `.claude`。
- 脚本说明里提到复用已登录浏览器会话，不读取 cookie 数据库；盘点未发现真实密钥。

注意：迁入前应保留脚本依赖、Node 版本要求和输出目录约束。

### 4.3 `.agents\skills\karpathy-guidelines`

当前路径：

```text
D:\Projects\.agents\skills\karpathy-guidelines
```

处理：

- 已迁入 `governance\workspace-skills\shared\karpathy-guidelines\`。
- `SKILL.md` frontmatter 保留 `license: MIT` 和来源链接；后续若要更严格追踪上游，可再补 upstream 快照。

### 4.4 `.claude\env`

当前路径：

```text
D:\Projects\.claude\env
```

包含：

- `README.md`
- `plugins-inventory.md`
- `settings-reference.json`
- `restore-settings.sh`

处理：

- 已迁入 `governance\workspace-config\claude-env\`。
- 已通过 `workspace_config_claude_env` 组件逐文件安装回 `D:\Projects\.claude\env\`。
- `settings-reference.json` 可提交，因为它没有 env/model 和真实密钥。
- `plugins-inventory.md` 里有 `root:<password>` 占位符，不是真实密钥。

用途：这是 Claude 插件恢复说明和恢复脚本，属于可复用环境知识。

### 4.5 后续候选：领域根 overlay

建议新增 constitution 目录：

```text
governance\domain-overlays\
  DragonPow2\
  DragonPow1\
  ai_projects\
```

用途：

- 管理写到 `D:\Projects\DragonPow2`、`D:\Projects\DragonPow1`、`D:\Projects\ai_projects` 的本机域级规则。
- 与 `project-overlays` 区分：domain overlay 是个人本机领域入口，project overlay 才是实际仓库公共规则。

当前 `project-overlays\DragonPow2` 语义偏混合，后续建议拆分。

## 5. 不建议或禁止 Git 管理的内容

以下内容不要放入 Git：

| 路径或模式 | 原因 |
|---|---|
| `D:\Projects\.constitution-state.json` | installer 状态文件，机器本地 hash 和时间戳 |
| `*.backup.*` | 安装器或手工备份产物 |
| `D:\Projects\.codex\config.toml` live 文件 | 渲染目标，应提交模板 |
| `D:\Projects\.claude\settings.local.json` live 文件 | 渲染目标，可能随本机工具变化 |
| `D:\Projects\.claude\skills\lark-doc`、`lark-shared` junction | 软链接目标，不直接提交链接结果 |
| `.claude\settings.local.json.backup.*` | 备份 |
| `.codex\config.toml.backup.*` | 备份 |
| `.agents\skills\*\*.backup.*` | skill 备份 |
| 插件缓存、session、history、log、auth、credentials | 机器状态或密钥风险 |
| `.memsearch\`、`.omc\`、`.hermes\` 等运行状态目录 | 插件或工具状态，不是治理源 |
| `_codex_tmp\`、`_outputs\`、`_research\` 中的一次性产物 | 临时产物或调研输出 |

## 6. 推荐 Git 管理落点

建议所有可管理内容统一放进：

```text
D:\Projects\ai-workspace-constitution
```

不要新建多个散落的 git 仓库来分别管理 `.codex`、`.claude`、`.agents`。推荐落点：

| 内容 | 推荐 constitution 路径 |
|---|---|
| 工作区入口规则 | `governance\workspace\*.tmpl` |
| HOME marker section | `governance\global\claude\`、`governance\global\codex\` |
| Codex / Claude 配置模板 | `governance\workspace-config\` |
| Claude 插件恢复资料 | `governance\workspace-config\claude-env\` 或 `docs\claude-environment-recovery\` |
| 共享 skills | `governance\workspace-skills\shared\` |
| Codex 专用 skills | `governance\workspace-skills\codex-only\` |
| 外部 skill 锁定 | `manifests\skills-lock.json` |
| 领域根规则 | `governance\domain-overlays\<domain>\` |
| 实际仓库公共规则 | `governance\project-overlays\<repo>\` |
| 安装、更新、验证脚本 | `scripts\` |
| 治理说明和决策 | `docs\` |

## 7. 后续建议迁移顺序

已完成 `skills-lock.json`、`.claude\env`、`browser-doc-crawler`、`karpathy-guidelines` 的迁入。后续低风险顺序：

```text
1. 提交 constitution 里已有模板、docs、scripts、tests 和本次新增源。
2. 新建 domain-overlays，拆分 DragonPow2 等领域根本机规则。
3. 若需要更严格追踪外部来源，为 karpathy-guidelines 补 upstream 快照或来源 hash。
4. 删除或忽略 live 目录中的备份文件，避免误提交。
```

迁移时每一步都应运行：

```powershell
git status --short
rg -n "\x{FFFD}|\x{95C2}|api[_-]?key|secret|password|cookie|authorization|credential|private[_-]?key" <候选目录>
```

命中说明文字或占位符可以保留，但真实密钥、账号 token、cookie、session 不能进入 Git。

## 8. 最终建议

当前最合理的管理方式是：

1. `ai-workspace-constitution` 继续作为唯一 Git 管理仓库。
2. `D:\Projects` 下 live 的 `AGENTS.md` / `CLAUDE.md` 可以进个人治理 Git，但推荐以 constitution 模板为主；`.codex` / `.claude` live 配置仍以模板和 manifest 管理。
3. `skills-lock.json`、`.claude\env`、`browser-doc-crawler`、`karpathy-guidelines` 已迁入 constitution 管理。
4. `lark-doc` / `lark-shared` 这类外部 skill 优先通过 lock 管理；除非需要固定离线快照，否则不 vendor。
5. `DragonPow2` 这类领域根应走 `domain-overlays`，不要把个人域级规则混入产品仓库提交。

这样可以让 Agent 配置可复用、可审查、可恢复，同时避免把本机状态和个人规则污染产品仓库。
