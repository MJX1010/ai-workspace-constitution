# D:\Projects 当前结构、配置同步与 AI 读取顺序

状态：当前快照
核对日期：2026-06-23
适用范围：`D:\Projects` 工作区、`D:\Projects\ai-workspace-constitution`、顶层 `AGENTS.md` / `CLAUDE.md`、workspace skills、DragonPow2 overlay。

## 1. 结论

`D:\Projects\ai-workspace-constitution` 已经覆盖工作区治理的主要 source of truth：顶层 Agent 模板、workspace skills 源、DragonPow2 overlay、Codex / Claude 全局快照、安装清单、安装脚本和文档。

但截至本次核对，不能说“当前 Projects 工程目录结构、配置和文档已经完全同步到 constitution 的已提交状态”。原因有三类：

1. constitution Git 工作树存在未提交改动和未跟踪快照，例如 `governance/global/`、`governance/environment-inventory/`、`docs/ai-environment-restore.zh-CN.*` 等仍处于待审查状态。
2. live 的 `.agents/skills`、`.codex/skills`、`.claude/skills` 当前内容不完全一致；`.claude/skills/lark-*` 是 junction，`.agents/skills` 中存在外部 skill 源。
3. DragonPow2 Unity 本地 skill 使用 SVN externals 的规则已经写入 DragonPow2 overlay，但这属于 DragonPow2 领域规则，不等同于顶层 workspace skills 的同步机制。

本次已完成的同步点：

- `D:\Projects\AGENTS.md` 和 `D:\Projects\CLAUDE.md` 已增加新 session / 指定工程根时的 codegraph 初始化或索引更新规则。
- constitution 的 `governance/workspace/AGENTS.md.tmpl` 和 `governance/workspace/CLAUDE.md.tmpl` 已同步同一规则。
- constitution 根目录已执行 `codegraph init`，状态为 up to date；`.codegraph/` 已加入 `.gitignore`，作为本地索引状态处理。
- 本文档新增 `.md` 与自包含 `.html` 两个版本。

## 2. D:\Projects 当前顶层结构

`D:\Projects` 是多仓库工作区，不是单一工程根。顶层目录按职责分为以下几类。

| 类别 | 当前示例 | 说明 |
|---|---|---|
| 工作区入口规则 | `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`README_AI_GOVERNANCE.md` | 顶层默认规则；更近目录规则优先 |
| AI harness 配置 | `.agents/`、`.codex/`、`.claude/`、`.qoder/`、`.trae/`、`.windsurf/` | 本机 AI 工具配置、skills、插件状态或缓存 |
| 治理 source of truth | `ai-workspace-constitution/` | 可版本化的模板、manifest、skills 源、安装脚本和文档 |
| AI 工具与研究域 | `ai_projects/`、`aime_workspace/`、`trae_workspace/`、`cli-history-analysis/` | AI 工具、自动化、实验项目集合 |
| 业务项目域 | `DragonPow2/`、`DragonPow1/`、`ET_Main/`、`ET_Main_Unity2022/`、`lqs_automation/`、`Main_YIUI_Odin/` | 真实业务工作副本、历史项目和自动化仓库 |
| 跨仓库规格 | `specs/` | 非平凡改动的跨仓库 spec / plan / tasks |
| 临时与产物 | `_outputs/`、`_research/`、`_tmp_paseo/`、`__Android/`、`__Unity/`、`__GitRepo/` | 报告、调研、临时 worktree、SDK、归档或缓存 |
| 机器状态 | `.constitution-state.json`、`skills-lock.json`、各类 backup | 本机安装状态或外部 skill 锁定信息 |

处理原则：

- 顶层只放跨仓库通用规则，不写具体项目实现细节。
- 进入具体任务后，以用户声明的工程路径为目标根，不从 `D:\Projects` 猜测其它工程。
- 产物、缓存、临时目录默认不是 source of truth。

## 3. constitution 当前配置布局

`D:\Projects\ai-workspace-constitution` 是工作区治理的 Git source of truth。当前主要目录如下。

| constitution 路径 | 管理内容 | 目标位置 |
|---|---|---|
| `governance/workspace/` | 顶层 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`README_AI_GOVERNANCE.md` 模板 | `${WORKSPACE_ROOT}` |
| `governance/workspace-skills/shared/` | harness 共享 skills 源 | `${WORKSPACE_ROOT}/.agents/skills`、`.codex/skills`、`.claude/skills` |
| `governance/workspace-skills/codex-only/` | Codex 专用 skill | `${WORKSPACE_ROOT}/.codex/skills` |
| `governance/workspace-config/` | workspace 级 Codex / Claude 配置模板和 Claude env 恢复资料 | `${WORKSPACE_ROOT}/.codex`、`${WORKSPACE_ROOT}/.claude` |
| `governance/workspace-scripts/` | workspace helper 脚本 | `${WORKSPACE_ROOT}/.codex/scripts` 等 |
| `governance/project-overlays/DragonPow2/` | DragonPow2 领域规则、agent-doc 模板和同步脚本 | `${DRAGONPOW2_ROOT}` |
| `governance/global/codex/` | 用户 HOME 级 Codex 规则、agents、skills、MCP 配置快照 | `${USER_HOME}/.codex` |
| `governance/global/claude/` | 用户 HOME 级 Claude 规则、MCP、插件和 settings 快照 | `${USER_HOME}/.claude` |
| `governance/environment-inventory/` | 本机环境盘点快照 | constitution 文档化输入 |
| `manifests/default.yaml` | 默认安装清单 | installer source of truth |
| `manifests/skills-lock.json` | 外部 skill 锁定信息 | `${WORKSPACE_ROOT}/skills-lock.json` |
| `scripts/` | install / verify / sync 实现 | constitution 工具链 |
| `tests/` | smoke tests 和渲染检查 | constitution 验证 |
| `docs/` | 架构、同步范围、恢复、盘点和当前说明 | 人读知识库 |

`manifests/default.yaml` 是安装路径的统一入口；新增或调整同步目标时，优先更新 manifest 和 governance 源，不直接手改 live 目录里的镜像文件。

## 4. Live skills 当前状态

当前顶层 skills 不是完全同构状态，需要按来源理解。

| live 路径 | 当前观察 | 管理建议 |
|---|---|---|
| `D:\Projects\.agents\skills` | 包含 `browser-doc-crawler`、`feature-spec-workflow`、`github-sync-commit`、`karpathy-guidelines`、`lark-doc`、`lark-shared`、`skill-factory-playbook`、`workspace-governance`、`yiui-uidoc-workflow` | harness-neutral 入口；外部 skill 通过 lock 或明确来源管理 |
| `D:\Projects\.codex\skills` | 包含 `feature-spec-workflow`、`github-sync-commit`、`manage-superpowers-whitelist`、`skill-factory-playbook`、`workspace-governance`、`yiui-uidoc-workflow` | Codex 优先读取；缺失共享 skill 时应通过 installer/manifest 同步，而不是手工复制 |
| `D:\Projects\.claude\skills` | 包含 `feature-spec-workflow`、`github-sync-commit`、`skill-factory-playbook`、`workspace-governance`、`yiui-uidoc-workflow`，`lark-doc` / `lark-shared` 为 junction | Claude 优先读取；junction 只提交 lock/说明，不提交链接结果 |
| `DragonPow2/client/Unity/.skills` | DragonPow2 Unity 本地 skill canonical 位置 | `.codex/skills` 和 `.claude/skills` 通过 SVN externals 指向它时，只改 `.skills` 源 |

如果需要把 live skills 与 constitution 完全对齐，推荐顺序：

1. 先确认 `manifests/default.yaml` 中的 `workspace_skills_*` 源和目标是否符合预期。
2. 运行 constitution installer 或 verify，而不是手动复制目录。
3. 对外部 skill 用 `manifests/skills-lock.json` 固定来源。
4. 对 DragonPow2 Unity 本地 skill，遵守 SVN externals 规则，只改 canonical `.skills`。

## 5. 新 session 的工程根与 codegraph 规则

当用户在新 session 或当前对话中声明目标路径时，AI 必须先判断它是否是工程根。

工程根判断优先级：

1. VCS 根：`.git` 或 `.svn`。
2. Unity 根：同时存在 `Assets/` 和 `ProjectSettings/`。
3. C# / .NET 根：存在 `.sln` 或主要 `.csproj`。
4. Node / Python / Rust 等包根：`package.json`、`pyproject.toml`、`Cargo.toml` 等。
5. 若输入是子目录，向上寻找最近的真实工程根；找不到时明确说明只能按当前目录降级处理。

确认是工程根后：

1. codegraph 可用且未初始化：执行 `codegraph init <工程根>`。
2. 已有 codegraph 索引：执行 `codegraph sync <工程根>` 或 `codegraph index <工程根>`，按工具实际能力选择。
3. 只有 MCP 查询工具可用：用 `codegraph_status` / `codegraph_explore` 确认索引状态和目标文件可见。
4. codegraph 不可用、过期或不支持当前语言：说明降级，使用 `rg`、语言服务、编译/测试、本地 review gate 补足影响面。

codegraph 是影响面和 caller/callee 上下文工具，不是 diff source of truth。实际改动范围仍以 Git/SVN diff、cr_local packet、构建脚本和项目 source of truth 为准。

## 6. AI 读取配置、文档和 skills 的顺序

推荐读取顺序如下，越靠近目标目录的规则优先。

1. 最高优先级指令：system / developer / 当前用户要求。
2. 用户声明的目标路径：规范化绝对路径，判断工程根，必要时初始化或更新 codegraph。
3. 工作区入口：读取 `D:\Projects\AGENTS.md` / `CLAUDE.md`，以及当前 harness 需要的顶层配置。
4. 工作区共享 skills：Codex 优先 `.codex/skills`，Claude 优先 `.claude/skills`，通用能力可参考 `.agents/skills`；只加载与当前任务匹配的 skill。
5. 路径逐层下钻：从 `D:\Projects` 到领域根，再到实际仓库和模块目录，查找更近的 `AGENTS.md` / `CLAUDE.md`。
6. 项目文档：读取目标仓库的 README、docs、references、specs、构建说明、测试说明。
7. 本地项目 skills：优先于顶层共享 skill；若 DragonPow2 Unity 的 `.codex/skills` / `.claude/skills` 由 SVN externals 指向 `.skills`，以 `.skills` 正文为准。
8. source of truth 判断：区分手写源码、模板、manifest、生成物、缓存、构建参数和部署配置。
9. 验证与 review：按最近规则运行构建、测试、本地 review gate；修改代码后在完成回复前带回结果。

冲突处理：

- 当前用户要求高于文档规则。
- 更近目录规则高于父级规则。
- 触发的本地 skill 高于泛用共享 skill。
- 提交、上传、发布、删除、回退类操作仍受顶层安全门禁约束，不能被下级规则静默放宽。

## 7. 同步完整性判断

可以把同步状态分成三档。

| 状态 | 判断标准 | 当前结论 |
|---|---|---|
| 已进入 constitution 管理 | 有 governance 源、manifest 或文档说明，并且不含密钥/缓存 | 顶层入口模板、DragonPow2 overlay、workspace skills 源、部分 global 快照已进入 |
| 已在工作树但未完成提交/审查 | `git status` 显示 modified 或 untracked，尚未确认是否全部可版本化 | 当前存在多处，例如 `governance/global/*`、`governance/environment-inventory/`、部分 docs 和 scripts |
| live 与 constitution 不一致 | live 目录存在额外 skill、junction、机器状态或未同步镜像 | 当前 `.agents` / `.codex` / `.claude` skills 内容不完全一致 |

因此，严格说当前不是“完全同步”。要达到完全同步，应完成：

1. 对 constitution 当前 dirty / untracked 内容逐项审查，确认可提交范围。
2. 用 installer/verify 重新渲染或校验 workspace live 目标。
3. 对 `.agents`、`.codex`、`.claude` skills 差异明确来源：constitution 源、external lock、junction、或本地未管理内容。
4. 更新文档后运行测试，并只提交本次确认范围。

## 8. 推荐核对命令

在 `D:\Projects` 顶层确认环境：

```powershell
ai-env-probe
Get-ChildItem -Force -Name D:\Projects
```

在 constitution 根目录确认 Git 和 codegraph：

```powershell
git status --short --branch
codegraph status D:\Projects\ai-workspace-constitution
```

检查 workspace 模板与 live 入口差异：

```powershell
rg -n "codegraph|工程根|当前对话 session" D:\Projects\AGENTS.md D:\Projects\CLAUDE.md
rg -n "codegraph|工程根|当前对话 session" governance\workspace\AGENTS.md.tmpl governance\workspace\CLAUDE.md.tmpl
```

检查 skills 来源和链接：

```powershell
Get-ChildItem -Force D:\Projects\.agents\skills
Get-ChildItem -Force D:\Projects\.codex\skills
Get-ChildItem -Force D:\Projects\.claude\skills | Select-Object Name,Mode,LinkType,Target
```

constitution 变更验证：

```powershell
git diff --check
.\tests\run.ps1
```
