## 语言与文档

- 首要使用中文与用户沟通；除非用户明确要求英文，最终回复、阶段性说明、设计分析和 review 结论都使用中文。
- 新增或修改文档、代码注释、XML summary、README、架构说明时，优先使用中文描述。保留 API 名称、类型名、路径、命令和协议字段原文。
- 面向团队沉淀的设计规范、迁移规则和边界说明必须写清楚中文上下文，避免只留下英文占位描述。
- 长期维护型技术文档，包括 `docs/architecture/`、guides、README、skills 及其 references，默认只维护 Markdown，不自动生成或提交同内容 HTML。只有需求开发阶段确实需要人工审核、验收、演示、复杂对比或交互阅读时，才同时生成 Markdown 和自包含 HTML；HTML 放在对应 specs、评审产物目录或用户指定位置，不进入长期架构文档目录。用户明确要求 HTML 时按要求生成。
- 更新 docs、skills、AGENTS.md、CLAUDE.md 等治理内容时，规则标题和可复用规范必须使用中性表述，例如“项目规则”“Editor Excel 工具按能力分层”“MetaTools 内部公共层”；不要把可迁移规则写成“Dragon2/DragonPow2 项目规则”。只有描述确实项目专有的架构、目录、业务背景或迁移对象时，才保留项目名。
- 在 `AGENTS.md`、`CLAUDE.md`、skills、README 和架构文档中引用路径时，只使用相对路径或 `<工作区根>`、`<DragonPow2根目录>`、`<项目根目录>` 等语义占位符，不写入盘符、个人用户名或本机绝对路径。用户回复中如需可点击本地链接，在运行时解析实际路径，不把解析结果回写到治理文档。

## 跨目录协作上下文发现

- 当从 `<DragonPow2根目录>` 对 `DragonPow2_Trunk_Leaning/`、`DragonPow2_Trunk_Leaning/client/` 等子目录项目开展 AI agent 对话协作时，必须按“顶层目录 -> 项目根目录 -> 子模块目录 -> 目标文件所在目录”的顺序逐层查找上下文。
- 每一层优先检查 `AGENTS.md`、`CLAUDE.md`、`.skills\`、`.agents\skills\`、`.codex\skills\`、`.agents\docs\`、`docs\`、`reference\`、`references\`、`README.md` 等；任务涉及特定模块时，继续向下检查该模块附近的同类说明、脚本和模板。
- 发现可用 skill 时，先读取对应 `SKILL.md` 的触发条件和工作流；若 skill 引用 `docs`、`reference`、模板或脚本，按相对路径从该 skill 所在目录解析，只加载与当前任务直接相关的资料。
- 子目录局部规则用于补充或收窄上层规则；如出现冲突，以更靠近目标项目或目标文件的说明为准，但不得违反 DragonPow2 顶层共享的语言、安全、协议边界和验证规则。
- 阶段性说明或最终回复中应简要说明已采用的关键层级、skill 或 docs/reference；若某层不存在相关资料，记录后继续向下查找，不要因为顶层已有规则就跳过子项目局部说明。

## 任务规模与流程收敛

- 先按改动风险决定调查和验证深度。单文件或少量文件、可用一句 diff 描述、不改变公共接口、协议/schema、持久化、生命周期、构建链路或平台语义的任务，按小改动处理；触及上述边界或影响面不明时再升级流程。
- 小改动只加载完成任务所需的最小上下文：最近规则、直接相关源码、被触发 skill 的完整正文及其明确要求的直接引用。同一会话已完整读取且文件未变化时直接复用；`AGENTS.md` 与 `CLAUDE.md` 的托管块若确认同源同版，不重复展开相同正文。
- 搜索从目标文件、精确符号和直接 caller/callee 开始；只有发现跨模块证据时才扩大范围。codegraph 查询使用可区分的完整符号、文件或模块范围，不对通用重名符号直接执行全库 impact 并把海量结果当成有效审查。
- 小改动仍执行仓库规定的必要编译和 review gate，但验证应取能覆盖改动的最小闭环；没有明确触发条件时，不额外创建 specs/docs、补测试框架、展开平台矩阵、派发 SubAgent 或追读无关 references。
- 阶段说明与工具输出按信息价值收敛：开工时说明范围和验证入口，长任务或阻塞时更新，结束时报告结果；不逐项播报规则读取、重复搜索和无结论的工具过程。达到 source of truth、直接影响面和必要门禁三项证据闭环后停止扩展调查。

## 主 Agent、SubAgent 与会话隔离

- 所有用户沟通只由主 Agent 完成；SubAgent 不直接向用户提问、请求授权或交付最终结果，阻塞统一回报主 Agent。
- 创建 SubAgent 时默认显式使用 `fork_turns="none"`，不得继承完整主会话；主 Agent 必须提供包含绝对工程根、目标、范围、事实、验收标准和返回格式的自包含短任务书。
- 每个 SubAgent 一次只负责一个工程根，自行读取该工程最近的规则、skills、source of truth 和验证入口；不得继续创建子代理。
- SubAgent 只返回结论、关键证据路径、修改文件、验证结果、风险和阻塞，不回传完整日志、大段源码或无关背景；默认控制在约 1200 个中文字符以内。
- 功能或主工程切换前，把稳定状态写入最近的 specs 或 `ai-handoff` 交接文件；使用 `/new` 开启新 Chat，或用 `/clear` 清屏并开启新 Chat。
- `codex resume` 和 `codex fork` 会保留旧历史，不用于上下文隔离。新 Chat 第一条消息必须声明主工程根、交接文件、当前目标和排除项。
- Agent 结果只作为证据输入；主 Agent 负责复核文件修改、验证结果、跨工程契约和最终交付。

## AI 临时产物与版本控制边界

- AI agent 在分析、调试、review、抓取、索引或会话交接过程中生成的临时产物只允许保留在本地受控临时目录，不得执行 `svn add`、`git add`、`svn import`、`svn copy`、commit 或 push。包括但不限于日志、截图、证据快照、review packet、提示词或对话导出、索引与 memory 目录、一次性脚本、中间报告和工具缓存。
- 用户明确要求交付且已确认归属、source of truth 和维护方式的源码、测试、配置、正式 specs/docs 不属于临时产物；不能仅因文件由 AI 生成就排除，也不能把临时分析材料改名后当作正式文档提交。
- AI 临时产物优先放入项目约定的 `Temp/`、本地 artifacts 或已忽略目录；不得为了方便提交而移入源码、docs、specs、skills、资源或构建目录。
- 准备 changelist 或提交前必须检查 `svn status` / `git status` 和实际 diff，逐项排除 AI 临时产物。发现已登记为新增、修改或待提交时，先撤销其版本控制登记并保留必要的本地证据，再继续验证；不能把清理临时产物与业务改动拆成侥幸提交。

## Skill 编写与维护约束

- 新增或修改 DragonPow2 项目内 skill 时，`SKILL.md` frontmatter 的 `description` 必须使用中文描述能力、触发条件和适用场景；正文中的触发条件、工作流、注意事项也必须优先使用中文，不写英文触发语句。
- 新增项目本地或 Unity 本地 skill 时，优先放在距离使用场景最近的 `.skills\` 目录；不要默认放到 `.agents\skills\`，除非当前工具链明确只扫描该目录。
- 共享或跨项目 skill 命名必须按能力、框架或工作流命名，不写 `DragonPow2` 等项目名前缀；项目限定条件写入触发场景或更近的项目本地 skill。
- skill 内引用工程文件、脚本、模板、docs、reference、assets 时，只使用相对 skill 目录、相对项目根目录或明确占位变量路径；不得写入 Windows 盘符开头路径、个人用户名目录或其他本机绝对工程路径。
- 若必须举路径示例，使用 `<项目根目录>/client/...`、`<工作区根>/DragonPow2/...` 或 `references/foo.md` 这类可迁移写法；保留 API 名称、命令名、字段名、目录名原文。
- 更新 skill 后，需要检查 `agents/openai.yaml` 等界面元数据是否仍与 `SKILL.md` 中文描述一致；若触发语义变化，必须同步更新对应元数据。

## 飞书文档与 lark-cli

- 遇到飞书、Lark、豆包文档链接，先查找目标目录最近的 `feishu-doc-reader` 或同类 skill，并以 `lark-cli` 内置 skill 文档作为命令参数 source of truth。
- 用户要求完整读取时，正文、结构、图片/附件/表格线索未确认前不得进入实现；读取失败必须说明授权、应用配置、用户登录或文档权限缺口。
- 抓取内容必须归档在目标项目内的临时证据目录，包含来源元数据、原始 Markdown/XML、媒体/表格清单和未读项；不要把聊天记录、历史缓存或截图局部当成唯一证据。
- 交互稿包含 GIF、录屏或其它动图时，必须下载原始媒体并抽关键帧或条带图，记录动效触发、阶段、停留、隐藏/移除条件和实现映射；只看首帧或静态预览不算完整读取。
- 临时归档不保存 App Secret、user token、refresh token，不默认提交；稳定结论同步到 UIDoc、docs 或 specs。用户说明文档更新时，必须重新抓取或明确使用的快照版本。

## 编码设计原则

- 编码应遵循设计模式和面向对象设计原则，优先保证单一职责、依赖倒置、接口隔离和开放封闭。
- 当同一调用点需要切换多种实现时，优先使用接口配合 strategy、adapter、factory、registry 等模式，不在业务调用方直接分支依赖具体实现。
- 抽象必须服务于真实变化点，避免为了“看起来规范”引入无实际收益的过度设计。
- 业务规则、存档权威、协议投影、UI 展示等职责需要清晰分层，禁止把多个层级的副作用塞进同一个通用方法。
- 跨层状态队列、ledger、projection、presentation request 必须区分“领域事实 / 事件快照”和“界面表现细节”。Model、协议、持久化、ledger 层只保存可复现的领域事实、状态快照和通用表现事实，例如 `OldState`、`NewState`、`WasTracked`、`Version`、`Sequence`、`RewardItems`、`DialogId`、`TipsType`；不得保存具体 UI 控件、动画、扫光、Toast、Panel、颜色、Icon 高光等 View / ModelView 细节开关。
- 表现层需要动画或 UI 判断时，必须在 ModelView、YIUI、UI 播放入口根据事件快照、task policy 或 view policy 推导；不要把 `ShowXxxSweep`、`ShowXxxTip`、`ShowXxxIcon` 这类命名的字段塞进 Model 层。异步队列消费时，事件发生瞬间无法事后可靠推导的信息必须在入队时快照；当前状态只能作为校验或补充，不能替代事件快照。
- Review 新增跨层字段时必须先判断三点：它是领域事实还是 UI 表现；延迟消费后能否从当前状态可靠重建；字段名是否暴露具体 UI 控件或动画。任一不满足，就下沉到表现层或改成 policy 推导。

## 需求边界与防漂移

- 实现前必须先写清本次需求的 source of truth、协议契约和改动侧：是在消费现有数据、补客户端投影，还是需要改变服务端、生成源、持久化或 notify 生产语义。
- 跨 client/server、mock/formal、生成协议、持久化状态的需求，未确认生产方契约前默认只做消费端兼容和投影，不主动改变生产方行为。
- 不得为了让测试通过反向制造新行为；测试只能验证已经确认的契约，不能把猜测出的 notify、flush、登录、登出或存档语义写成事实。
- 若实现过程中发现必须改变协议字段、服务端触发时机、RoleDelta/Notify 语义、持久化权威、mock/formal 边界或登录流程，必须暂停说明证据、影响面和备选方案，等用户确认后再改。
- Review 时必须专门检查是否出现需求实现漂移：新增改动是否超出用户点名范围，是否把“客户端消费已有数据”做成“服务端新增行为”，是否修改了无关测试、生产方或契约。

## 配置 source of truth

- 手写配置文件必须有且只有一个 source of truth；不要为 Editor/Runtime、脚本/构建、客户端/工具各维护一份可手改副本。
- 需要跨环境消费时，优先让各环境读取同一配置；若平台限制必须生成派生快照或代码，派生产物必须自动生成、不可手改、可校验同步，并在 docs / skills 中声明权威配置路径。

## 协议与 Mock 边界

- Adapter 只能依赖接口或抽象选择器，不直接依赖 mock/formal 具体实现类型。
- mock 与正式协议通过接口、registry 或 factory 切换；具体实现类型只能出现在 registry/factory 这类组合根中，不能出现在 Adapter、ComponentSystem、通用网络层或业务调用方。
- mock 宏和 mock 协议字段依赖必须收敛在 mock 实现文件或 NetworkMock 模块内；关闭 mock 编译宏时，不应编译 mock 实现类，也不应存在创建 mock 实现对象的代码路径。
- mock 关闭时不得走客户端本地权威写入兜底；正式协议缺失时返回明确的 `NotSupported`，由调用方决定提示、降级读取缓存或阻断流程。
- 通用网络调用层不得塞入具体业务投影逻辑；Meta/Prop 等缓存投影应放在对应协议投影器或模块适配层。
- 业务写入入口必须按具体模块拆分，例如 `JobProtocolAdapter`、`SkillProtocolAdapter`、`TaskProtocolAdapter`；禁止新增大而全的 `MetaBusinessProtocolAdapter` 或类似业务总线。
- `MetaDataProtocolAdapter` 只保留 Meta 加载/清理，不承载具体玩法写入；具体玩法写入必须走具体业务协议。
- 命名必须表达真实角色：接口使用能力名，具体实现使用 `Formal`/`Mock` 等实现名，只有纯辅助方法集合才使用 `Helper`/`Support`，避免把协议实现误命名成辅助类。
- 完成此类改动前必须做设计边界检查：调用方是否只依赖抽象、组合根是否唯一持有具体实现、mock 关闭时是否完全走正式路径、缺失正式协议是否显式失败。

## Unity 编译验证

- 修改 Unity C# 代码、生成代码、asmdef 引用或可能影响编译的 Unity 资源后，完成前必须检查 Unity 编译错误。
- 从当前项目根目录运行：

```powershell
uloop compile --project-path client/Unity --wait-for-domain-reload true
```

- 必须读取并报告 uLoop 返回的编译错误。若有错误，修复后重新运行，直到没有编译错误。
- 若 uLoop 无法连接（提示 Unity Editor 未打开或 CLI Loop server 未运行）：先用 `uloop fix` 清理 stale lock 后重试；仍失败时用 `uloop launch client/Unity` 启动该项目的 Unity Editor，待加载完成后重新运行原 uLoop 命令。
- 若 uLoop 编译、测试或运行命令被未保存的场景/Prefab 阻断，默认应保存未保存改动后继续验证：在原命令追加 `--save-before-run true` 重跑。若用户已明确要求继续验证、只处理该场景/Prefab、重跑测试或保存后继续，视为已授权保存；除非用户明确要求丢弃改动，不得默认 revert / checkout 场景或 Prefab。
- 若用户未授权保存且语义不明确，必须先询问；测试命令因未保存场景/Prefab 被阻断且测试数为 0 时，不得视为测试通过，必须按保存后重跑或等待用户决策处理。
- 若 Unity 启动或连接最终仍失败，保底使用 `dotnet build` 进行编译验证，并在最终说明中写明已降级为 dotnet、降级原因及 uLoop 不可用的事实。
- 正常情况下 `dotnet build` 仅作额外检查，不能替代 uLoop 的 Editor 编译状态。

## 本地全面 Review Gate

- 对 agent 来说，code review 是代码交付的默认自动行为；只要实际修改代码、Unity 资源、配置、脚本或可能影响行为的项目文档，就必须主动执行本地全面 Review Gate，不依赖用户额外提醒或显式输入 review 关键词；详细步骤以本节规则和 `cr_local.ps1` 输出的 review packet 为准。
- 纯咨询、只读分析、无行为影响的低风险文本修改不触发完整 review gate；若后续进入代码或行为相关改动，立即按本节执行。
- `cr_local.ps1` 只负责生成本地 diff review packet 和统一审查提示，不能替代当前对话内的全面 review。
- 完整顺序：刷新或确认 codegraph 索引 -> 运行项目编译 / 测试门禁 -> 运行 `cr_local.ps1` 生成 packet -> 在当前对话内基于 diff、codegraph caller / callee / impact、references、受影响平台/Profile 和生命周期风险做全面 review -> 修复 RED / YELLOW 后重新跑完整闭环。
- “检查平台/Profile/宏矩阵”默认指静态识别受影响范围，不等同于实际构建所有组合。只有新增、删除或重命名宏，修改 `#if` / `[Conditional]` 条件，改变宏产生链路、构建 Profile、平台专用依赖或分支输出语义时，才扩展到对应构建矩阵；仅修改现有条件分支内部的普通业务代码时，先跑当前 Unity 编译，若当前环境未覆盖该分支，再补一次 owner assembly 的最小目标宏编译。
- 不得把项目依赖链重复拆成 Core / Loader / Hotfix 等多项目与多个宏组合做笛卡尔积构建；单个上层项目已传递编译依赖时，只构建能覆盖改动的最小项目。预计需要 3 个及以上组合、明显超过常规 Unity 编译成本，或必须做 Android/iOS/Jenkins 实际构建时，先向用户说明触发依据、组合数和预计收益并取得确认；用户明确要求发布/提交门禁或全矩阵验证时除外。
- codegraph 是上下文和影响面工具，不是 diff source of truth；若当前环境提供 codegraph refresh / index 命令，必须先执行；若只提供查询工具，则用 `codegraph_status` / `codegraph_explore` 确认索引可用且目标文件可见；若 codegraph 更新不可用或索引明显过期，必须说明降级，并用 `rg` + `csharp-ls` / `uloop compile` 补足引用和编译检查。
- 非平凡代码改动或涉及启动/退出、生命周期、构建宏、平台矩阵、持久化状态、发布链路等高风险面时，若当前工具链支持 agent，应优先启动只读 reviewer subagent 复审 `cr_local` packet；最终 RED / YELLOW / GREEN 结论仍必须回到当前对话，由主 agent 复核、修复并重跑闭环。
- 从 client 工作副本根目录运行 `cr_local.ps1`（脚本自动识别 SVN/Git diff，用 `-Path` 收窄到本次改动文件和必要直接相关文件）：

```powershell
.\Tools\codereview\cr_local.ps1 -Path @('Unity\Assets\Scripts\...\Changed.cs')
```

- 见到 `LOCAL_REVIEW_PACKET: READY` 后，在当前对话内 review 该 diff；RED 必须修复后才算完成，YELLOW 默认修复或说明风险和不修原因，GREEN 可作为后续建议；不发送飞书通知，不归档报告，不自动提交。

## Unity Skill 与 SVN Externals

- `client\Unity\.codex\skills` 和 `client\Unity\.claude\skills` 通过 SVN externals 指向同一份 `../.skills skills`，维护 Unity 本地 skill 时只改 `client\Unity\.skills`，不要在 `.codex\skills` 或 `.claude\skills` 下复制正文。
- 新建或初始化 Unity 本地 skill 时，明确把 source root 写成 `.skills`（例如 `python .skills/skill-creator/scripts/init_skill.py <skill-name> --path .skills`），不要使用未定义的 `<SkillRoot>` 占位符，也不要把 `.codex/skills` 或 `.claude/skills` 当作创建目标。
- 本地全面 Review Gate 是 agent 默认交付规则，不维护单独 skill，也不维护 `.agents\skills` 薄入口；只有工具链实测只能通过 skill 执行且用户明确要求时，才新增薄入口，并且只引用本节规则，不复制 checklist。
- 修改 review gate 规则时，先更新 `governance\agent-docs\` 模板并运行同步脚本，避免各级 `AGENTS.md` / `CLAUDE.md` 漂移。

## 最终输出与提交日志

- 禁止在 SVN/Git 提交日志、构建说明、变更摘要中写入乱码、问号占位或无法确认编码的中文；中文日志必须先在当前 UTF-8 终端或文件中确认可读，再交给 `svn commit -m`、TortoiseSVN、Jenkins 或其它提交/发布工具。
- 在 Windows/PowerShell 下准备包含中文的 SVN/Git 日志时，先确认 `chcp 65001`、`$OutputEncoding = [System.Text.UTF8Encoding]::new($false)`，必要时把日志写入 UTF-8 文本文件再由工具读取，避免 GBK/UTF-8 混用导致历史记录乱码。
- Windows/PowerShell 下提交中文 SVN 日志时，优先把日志写入 UTF-8 文本文件并使用 `svn commit -F <日志文件> --encoding utf-8`；避免直接用 `svn commit -m "中文..."`，除非已在当前终端确认编码不会被转换。
- 任何 `svn commit`、`git commit`、`svn import`、`svn copy`、push、上传制品、发布构建、触发线上/后台提交类操作，执行前必须单独询问用户并得到明确确认；不能把“继续”“修复”“帮我处理”理解为提交或上传授权。
- 涉及 Unity 客户端、多平台构建、补丁、CDN、Jenkins 或发布入口的改动，提交前必须明确受影响平台矩阵并完成本地可行的编译/测试；提交后必须触发并确认 Android/iOS 等受影响平台构建通过，失败则继续修复，不能把未验证或未通过状态写成已完成。
- 每次实际修改代码、Unity 资源、生成代码、配置或项目文档后，最终回复必须提供一段可直接复制使用的建议 commit 日志，便于用户手动提交。
- 建议 commit 日志至少包含一行提交标题、要点式变更摘要和已执行的验证命令/结果；若有验证未执行或失败，必须在 commit 日志旁明确说明原因与风险。
- 建议 commit 日志的正文、变更摘要和验证结果必须使用简体中文描述；提交标题可保留约定式英文类型和 scope，例如 `fix(gsdk): ...`，但标题说明部分优先使用中文，避免整段英文提交说明。
- 提交标题应简洁表达真实改动范围，例如 `fix(client): handle prop protocol fallback`、`docs(agent): update uloop test rule`；不要夸大范围，不把未完成或未验证的内容写成已完成。

## Agent 文档统一管理

- 多项目共享规范以 `governance/agent-docs/` 为唯一模板源。
- 修改 `AGENTS.md` / `CLAUDE.md` 的共享规则时，先改模板，再从 `<DragonPow2根目录>` 运行 `./scripts/sync-agent-docs.ps1` 同步。
- 提交或备份前从 `<DragonPow2根目录>` 运行 `./scripts/check-agent-docs.ps1` 检查各项目托管块是否漂移。
- 脚本只管理 `<!-- BEGIN DRAGONPOW2 ... -->` 到 `<!-- END DRAGONPOW2 ... -->` 之间的内容；项目本地补充必须写在托管块之外。
- `<DragonPow2根目录>` 下的具体工程目录是多人共享仓库工作区，禁止在更深层随意新增 `AGENTS.md` / `CLAUDE.md` 入口文件，例如 `Trunk/client/Unity/AGENTS.md` 或同级工程目录。只有用户明确指定目标工作副或模块需要局部入口时才新增；否则优先改 `governance/agent-docs/` 模板并同步，或写入最近合适的 `.skills/`、docs、references。
