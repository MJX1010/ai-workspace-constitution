# D:\Projects 项目结构与 Agent 宪法方案

状态：建议稿  
适用范围：`D:\Projects` 工作区、`ai-workspace-constitution`、`ai_projects`、`DragonPow2`、`DragonPow1` 及其子目录。  
目标：让目录结构、规则来源、Agent 上下文发现、版本控制边界可复用、可迁移、可审查。

## 1. 总体结论

`D:\Projects` 应按“工作区本地层 + 可版本化宪法层 + 领域根 + 实际仓库 + 产物缓存层”管理，而不是在每个 Trunk、Branch、工具仓库里重复放一份个人 `AGENTS.md` / `CLAUDE.md`。

推荐原则：

- `D:\Projects\AGENTS.md` / `CLAUDE.md` 是个人工作区入口，可以进入个人治理 Git 仓库管理；默认不提交到业务/产品仓库。
- `D:\Projects\ai-workspace-constitution` 是可版本化的规则模板、安装器、文档和技能 source of truth。
- `D:\Projects\DragonPow2`、`D:\Projects\DragonPow1`、`D:\Projects\ai_projects` 是领域根，可以放本机个人域级规则，但不应向每个子仓库复制。
- 子仓库里只有团队共享、项目公有、明确要版本化的 Agent 规则才保留；个人规则若要版本化，应进 `ai-workspace-constitution` 这类个人治理仓库，而不是混入业务 SVN/Git。
- Agent 读取上下文时按路径自上而下发现规则，但提交时必须反向审查：确认是否把本地治理文件误放进版本控制。

## 2. 推荐目录分层

```text
D:\Projects\
  AGENTS.md                         # 本机工作区级规则，个人入口，可由个人治理仓库管理
  CLAUDE.md                         # 本机 Claude 工作区入口，可由个人治理仓库管理
  GEMINI.md                         # 可选，本机 Gemini 工作区入口
  README_AI_GOVERNANCE.md           # 可选，本机治理说明
  .agents\                          # 本机共享 skills / agent 资源
  .codex\                           # Codex 本机配置、skills、脚本、缓存
  .claude\                          # Claude 本机配置、skills、设置
  .constitution-state.json           # constitution 安装状态

  ai-workspace-constitution\         # 可版本化宪法仓库：模板、manifest、安装器、文档
  ai_projects\                       # AI 工具/研究/插件/训练项目领域根
  DragonPow2\                        # DragonPow2 多工作副本领域根
  DragonPow1\                        # DragonPow1 历史/维护工作副本领域根
  lqs_automation\                    # 自动化构建/发布仓库
  specs\                             # 跨仓库活跃功能规格与任务状态

  _outputs\                          # 输出物、报告、临时交付
  _research\                         # 调研资料、一次性采样
  _codex_tmp\ / _tmp_*\              # 临时工作区
  __Android\ / __Unity\ / __GitRepo\ # 平台 SDK、镜像、归档类资源
```

目录按职责分类：

| 类型 | 示例 | 是否应进产品仓库 | 说明 |
|---|---|---:|---|
| 工作区本地层 | `D:\Projects\AGENTS.md`、`.codex\`、`.claude\` | 否 | 个人环境、工具配置、默认行为规则 |
| 宪法 source of truth | `ai-workspace-constitution\governance\`、`manifests\`、`docs\` | 是，进 constitution 仓库 | 可复用模板、安装器、策略文档 |
| 领域根 | `DragonPow2\`、`DragonPow1\`、`ai_projects\` | 通常否 | 本机组织层，用来聚合多个 repo / working copy |
| 实际仓库 | `DragonPow2_Trunk\`、`lqs_automation\build_dragon2\`、`ai_projects\paseo\` | 视仓库而定 | 业务代码或工具代码的真实版本控制边界 |
| 临时/产物层 | `_outputs\`、`_research\`、Unity `Library\` | 否 | 可再生成、一次性或机器状态 |

## 3. Source of Truth 分层

### 3.1 个人规则

个人规则只应该存在于：

- `D:\Projects\AGENTS.md`
- `D:\Projects\CLAUDE.md`
- `D:\Projects\<领域根>\AGENTS.md`
- `D:\Projects\<领域根>\CLAUDE.md`
- constitution 中对应模板，例如 `governance/workspace/` 或未来的 `governance/domain-overlays/`

这些规则描述个人协作偏好、编码门禁、本机路径、工具约束、提交授权规则。它们可以由 constitution 生成到本机，也可以在个人治理 Git 仓库中版本化，但不应该被提交到业务/产品 SVN/Git。

### 3.2 团队共享规则

团队共享规则可以存在于实际仓库中，但必须满足所有条件：

- 内容对所有使用者成立，不依赖个人本机路径。
- 规则是项目公共契约，而不是某个 AI 工具的个人偏好。
- 仓库 owner 接受它作为版本化文件。
- 提交前明确列出并确认该文件属于本次提交范围。

示例：

- 服务端仓库内的协议生成规则。
- Unity 项目内团队统一的资源导入、构建、测试门禁。
- CI 仓库内构建脚本和发布目录约定。

### 3.3 constitution 仓库

`ai-workspace-constitution` 应作为可复用治理层，负责：

- 保存可版本化模板、脚本、skills、manifest。
- 记录哪些目标文件可以被安装器写入。
- 记录哪些目标文件绝对不能同步或提交。
- 提供跨机器迁移、验证、漂移检测能力。
- 保存本方案这类结构文档和 ADR。

它不负责：

- 存储密钥、会话、缓存、构建产物。
- 替代各产品仓库自己的 README、CI、业务规范。
- 把个人 `AGENTS.md` / `CLAUDE.md` 批量写入每个子仓库。

## 4. Agent 规格宪法

### 4.1 规则优先级

Agent 必须按以下优先级解释规则：

1. system / developer / 当前用户要求
2. 当前会话中用户的最新指令
3. 最近目录的 `AGENTS.md` / `CLAUDE.md`
4. 父级目录的 `AGENTS.md` / `CLAUDE.md`
5. 被当前任务触发的 skills / docs / specs
6. 默认模型行为

但“提交、上传、发布、删除、回退”类操作有额外门禁：即使下级文件允许，也不能覆盖上级个人安全规则和当前用户授权要求。

### 4.2 上下文发现算法

Agent 进入任意任务前应执行：

```text
1. 确认 cwd、实际目标路径、VCS 类型。
2. 从 D:\Projects 开始读取工作区级规则。
3. 进入领域根，例如 DragonPow2 / DragonPow1 / ai_projects，读取域级规则。
4. 进入实际仓库，读取仓库公开规则、README、docs、specs。
5. 进入模块目录，读取最近的局部规则和 source of truth。
6. 识别当前任务的验证路径、构建平台、提交边界。
7. 修改前列出将触碰的文件类型：源码、模板、生成物、缓存、治理文件。
```

### 4.3 Agent 规则文件规格

每个 `AGENTS.md` / `CLAUDE.md` 应尽量短，并固定包含以下信息：

```text
# <范围> Agent 规则

## 适用范围
说明本文件覆盖哪个目录树，是否是个人本地文件，是否允许提交。

## Source of Truth
说明真正应修改的源码、模板、manifest、生成流程在哪里。

## 操作门禁
说明禁止操作、需要用户确认的操作、编码和提交规则。

## 验证方式
说明本目录最小可行的 test / build / review gate。

## 子目录覆盖
列出哪些子目录有更近规则，或者说明子目录默认继承。
```

不要在规则文件里放长背景、聊天记录、一次性方案、完整构建日志、临时排障过程。

### 4.4 版本控制规则

默认禁止提交到业务/产品仓库：

- 任意个人 `AGENTS.md` / `CLAUDE.md`
- `.codex\`、`.claude\`、`.agents\` 下的本机状态
- `machine.local.yaml`
- 密钥、cookie、session、日志、缓存
- Unity `Library\`、`Temp\`、全量导入缓存
- `_outputs\`、`_research\`、`_tmp_*\` 下的一次性产物

允许提交：

- 个人治理仓库中的 `AGENTS.md` / `CLAUDE.md` 模板、快照或 overlay。
- constitution 仓库中的模板、manifest、安装脚本、验证脚本、docs、ADR。
- 实际产品仓库中团队明确共享的项目规则。
- 与业务改动同属 source of truth 的源码、配置、测试。

任何提交前必须做三件事：

```text
1. 查看 VCS 状态，只提交本次任务相关文件。
2. 单独确认是否包含 AGENTS.md / CLAUDE.md；默认排除。
3. 中文提交日志用 UTF-8 文件和明确编码提交，提交后验证中文无乱码。
```

## 5. constitution 推荐结构

当前仓库已有 `workspace`、`global`、`project-overlays`、`workspace-skills`、`workspace-config` 等层。建议逐步演进为更清晰的三类 overlay：

```text
ai-workspace-constitution\
  governance\
    workspace\                         # D:\Projects 顶层通用规则
    global\                            # 用户 HOME 级 Claude/Codex marker section
    domain-overlays\                   # 领域根本机规则，目标不是产品仓库
      DragonPow2\
      DragonPow1\
      ai_projects\
    project-overlays\                  # 明确团队共享、可进入实际 repo 的项目规则
      <repo-name>\
    workspace-skills\
    workspace-config\
    workspace-scripts\
  manifests\
    default.yaml
    machine.example.yaml
    machine.local.yaml                 # gitignored，本机路径覆盖
  docs\
    workspace-structure-agent-constitution.zh-CN.md
    workspace-structure-agent-constitution.zh-CN.html
```

短期可以不立刻重命名现有 `project-overlays/DragonPow2`，但语义上建议拆开：

- 写到 `D:\Projects\DragonPow2\AGENTS.md` / `CLAUDE.md` 的内容，属于 `domain-overlays/DragonPow2`。
- 写到 `D:\Projects\DragonPow2\DragonPow2_Trunk\...` 或实际 SVN/Git 仓库里的内容，才属于 `project-overlays/<repo>`。

这样可以避免“本机个人规则”和“项目公共规则”混在同一个 overlay 中。

## 6. 重点目录落地策略

### 6.1 D:\Projects

定位：个人工作区根。

保留：

- 顶层 `AGENTS.md` / `CLAUDE.md`，作为所有 agent 的默认入口。
- `.codex\`、`.claude\`、`.agents\`，作为本机工具配置和 skills 入口。
- `specs\`，记录跨仓库活跃功能。

避免：

- 把具体项目细节写进顶层规则。
- 在顶层规则里复制所有子项目说明。
- 把临时构建产物、下载包、报告混入 source of truth。

### 6.2 ai-workspace-constitution

定位：个人 AI 工作区宪法的版本化仓库。

建议：

- 所有通用规则先写模板，再由 installer 渲染到本机。
- manifest 明确列出每个目标路径。
- docs 记录结构、同步范围、更新策略和 ADR。
- 新增 domain overlay 前先判断目标是否只是本机规则；如果是，不要放进 project overlay。

### 6.3 ai_projects

定位：AI 工具、插件、训练、研究项目集合。

建议：

- `D:\Projects\ai_projects\AGENTS.md` / `CLAUDE.md` 作为域级本机入口。
- 每个真实 Git 项目自己保留最小项目规则；个人偏好不复制进去。
- 对 fork、vendor、示例仓库，默认不改它们的 `AGENTS.md` / `CLAUDE.md`，除非任务目标就是维护该仓库。
- 研究产物放 `docs\` 或 `_research\`，不要散落在工具源码目录。

### 6.4 DragonPow2

定位：DragonPow2 多 working copy 与配套工具的领域根。

建议：

- `D:\Projects\DragonPow2\AGENTS.md` / `CLAUDE.md` 是本机域级入口，统一描述 Unity、SVN、Jenkins、补丁、构建、中文提交日志等门禁。
- `DragonPow2_Trunk`、`DragonPow2_Trunk_Leaning`、`DragonPow2_Trunk_Windows*` 等子工作副本不再复制个人规则。
- 子工作副本里的 `server\AGENTS.md` / `CLAUDE.md` 只有在确认为服务端团队共享规则时才保留并提交。
- 构建自动化规则属于 `lqs_automation\build_dragon2`；不要混写进 Unity 客户端规则。

### 6.5 DragonPow1

定位：历史项目和维护分支集合。

建议：

- 默认继承 `D:\Projects`，只有频繁维护时才新增 `DragonPow1\AGENTS.md` / `CLAUDE.md`。
- 保持只读/低变更策略，避免把 DragonPow2 的构建、补丁、YooAsset 规则默认套用到 DragonPow1。
- 每次进入具体旧分支，先确认 Unity 版本、SVN/Git 边界和可用验证方式。

## 7. 迁移与清理步骤

建议按低风险顺序执行：

```text
1. 盘点现有 AGENTS.md / CLAUDE.md 分布。
2. 标注每个文件：个人本地、域级本地、团队共享、第三方示例、无效重复。
3. 个人本地规则上移到 D:\Projects 或领域根。
4. 团队共享规则保留在实际仓库，但删掉本机路径和个人偏好。
5. constitution 中把 workspace、domain overlay、project overlay 分开。
6. manifest 只写明确目标，不做“递归写入所有子目录”。
7. 提交前用 VCS 状态确认没有误提交个人治理文件。
```

盘点命令示例：

```powershell
rg --files -g AGENTS.md -g CLAUDE.md D:\Projects
```

重复内容检查建议：

```powershell
rg -n "禁止提交|svn commit|Unity|Jenkins|YooAsset" D:\Projects\DragonPow2 -g AGENTS.md -g CLAUDE.md
```

## 8. 审查清单

新增或调整任何 Agent 规则前，先问：

- 这个规则是个人规则、团队规则，还是一次性任务说明？
- 它应该放在工作区、领域根、实际仓库，还是 specs？
- 它是否依赖本机路径、账号、Jenkins 地址、FTP 地址？
- 它是否会被另一个使用者错误继承？
- 它是否需要进入 SVN/Git？如果需要，是否已有明确授权？
- 它是否能用更短的规则引用已有 source of truth？

提交或发布前，必须检查：

- 是否包含 `AGENTS.md` / `CLAUDE.md`。
- 是否包含缓存、产物、临时文件、密钥。
- 中文日志是否使用 UTF-8 且提交后可读。
- 多平台构建或补丁任务是否完成 Android/iOS 等受影响平台验证。
- 当前任务是否修改了实际 source of truth，而不是派生产物。

## 9. 推荐决策

本工作区推荐采用以下决策：

1. `D:\Projects` 保存个人工作区入口，作为所有 agent 的默认上下文。
2. `ai-workspace-constitution` 保存可版本化模板和安装逻辑。
3. `DragonPow2`、`DragonPow1`、`ai_projects` 作为领域根，必要时放本机域级入口。
4. 不再在每个 Trunk、Branch、工具仓库里复制个人 `AGENTS.md` / `CLAUDE.md`。
5. `project-overlays` 只用于实际仓库里团队共享的规则；本机域级规则应拆到 `domain-overlays` 或保持当前 overlay 但明确其本机语义。
6. 所有提交、上传、发布默认需要单独确认；`AGENTS.md` / `CLAUDE.md` 可以进个人治理仓库，但默认不提交到业务/产品仓库。

这样设计后，Agent 有稳定上下文，个人规则不会污染产品仓库，constitution 仍然能跨机器复用，子项目也保留必要的自治空间。
