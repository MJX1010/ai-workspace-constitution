## 语言与描述

- 首要使用中文沟通和记录设计结论；除非用户明确要求英文，客户端相关说明、注释、README、review 结论优先使用中文。
- 保留类名、协议名、字段名、路径、命令原文；解释这些名称的职责和边界时使用中文。
- C# 代码注释默认使用中文；说明遗留链路、禁止新增路径、迁移边界或兼容原因时也必须使用中文，不写英文占位注释。
- 更新 docs、skills、AGENTS.md、CLAUDE.md 等治理内容时，规则标题和可复用规范必须使用中性表述，例如“项目规则”“Editor Excel 工具按能力分层”“MetaTools 内部公共层”；不要把可迁移规则写成“Dragon2/DragonPow2 项目规则”。只有描述确实项目专有的架构、目录、业务背景或迁移对象时，才保留项目名。
- 修改局外/Meta/YIUI/MockStore/LocalPrefs 相关 Unity C# 代码前，必须先读取 `client/Unity/docs/architecture/meta-client-coding-performance-standards.md`，再按任务读取对应专项 docs / skills；本轮已读取且上下文未变化时可以复用，但最终说明要写明采用了哪些关键规范入口。

## 客户端小改动流程收敛

- 单文件、低风险的 Unity/YIUI 业务改动，先检查目标文件、精确符号、直接数据来源和唯一显示/消费出口；没有跨模块证据时，不扩大到全客户端搜索，不对通用重名回调执行全库 codegraph impact。
- 必读架构文档和被触发 skill 仍需完整读取，但同一会话已读取且未变化时直接复用；只跟进当前子任务路由明确要求的 references，不因相邻模块或可选能力继续追读。
- 此类改动的默认验证闭环是当前 Unity 编译、目标文件及必要直接相关文件的 `cr_local.ps1` review；未改变 Prefab、生成源、协议、宏、生命周期或平台依赖时，不额外运行代码生成、Prefab 检查、测试框架恢复或平台矩阵。
- 阶段说明保持简短，只报告改动位置、关键判断、编译/review 结果和真实阻塞；不得用规则读取清单、宽泛搜索日志或重复工具输出代替有效进度。

## 飞书文档与 UIDoc 归档

- 客户端 UI、YIUI、WorldExplore、Task 等需求引用飞书交互稿、策划案或视觉稿时，先使用 `<客户端根>/Unity/.skills/feishu-doc-reader/SKILL.md` 完整读取；命令参数以 `lark-cli skills read lark-doc` 及其 references 为准。
- 抓取快照放在 `<客户端根>/Unity/Temp/UI_AutoGen/<module>_lark/` 或当前 skill 指定的更细目录，至少记录来源链接、标题、revision 或读取时间、执行命令、Markdown/XML、媒体/表格清单和未读项。
- 若交互稿包含 GIF、录屏或动图，必须下载原始媒体、抽关键帧/条带图，并在快照摘要和 UIDoc 中记录动效结论；客户端 UI 实现不能只按静态首帧还原。
- `Temp/UI_AutoGen/*_lark/` 是证据缓存，不是 source of truth，也不默认提交。稳定结论必须同步进模块 `UIFeatureDoc.asset`、导出的模块 Markdown 或对应 docs/specs。
- 用户说明飞书文档更新时，必须重新读取并生成新快照或明确覆盖策略；不能沿用旧缓存继续实现。

## 编码设计原则

- 客户端编码应遵循设计模式和面向对象设计原则，优先保证单一职责、依赖倒置、接口隔离和开放封闭。
- ET 框架下新增或移动 Handler 时默认一类一文件，文件名与 Handler 类名一致；`ProtoMessageHandler`、`MemorypackMessageHandler`、`FiberCrossMessageHandler`、事件 Handler 等不要混写在 `*ComponentSystem.cs` 中。
- Handler 使用的 `FiberCrossRequest` 参数类型可以按模块或方向聚合到 `*FiberCrossMessages.cs` 等 Model 文件；不要为了参数 DTO 强制一类一文件。
- `*Component.cs` 默认只放组件实体和组件持有的数据字段；`FiberCrossRequest` 等跨 fiber 消息参数 DTO 不要混在 Component 文件中。
- `*ComponentSystem.cs` 只保留组件生命周期、组件扩展方法和本组件私有辅助逻辑；消息/事件分发入口放到独立 Handler 文件，便于检索、注册和 review。
- `A2NetClient_Message.cs` 中的 Memorypack 桥接类型属于旧 Actor -> ClientNet 转发链路遗留；后续客户端内部跨 fiber 消息应使用 `FiberCrossRequest` 类型，参数定义按模块聚合，Handler 独立建文件。
- 当 Hotfix、NetworkMock、正式协议、mock 协议之间存在实现切换时，优先通过接口、adapter、factory、registry 或 strategy 组织，不让调用方直接依赖具体实现。
- UI、客户端缓存投影、协议适配、mock 服务端逻辑必须分层清楚；通用组件不承载模块特化副作用。
- 跨层状态队列、ledger、projection、presentation request 必须区分“领域事实 / 事件快照”和“界面表现细节”。Model、协议、持久化、ledger 层只保存可复现的领域事实、状态快照和通用表现事实，例如 `OldState`、`NewState`、`WasTracked`、`Version`、`Sequence`、`RewardItems`、`DialogId`、`TipsType`；不得保存具体 UI 控件、动画、扫光、Toast、Panel、颜色、Icon 高光等 View / ModelView 细节开关。
- 表现层需要动画或 UI 判断时，必须在 ModelView、YIUI、UI 播放入口根据事件快照、task policy 或 view policy 推导；不要把 `ShowXxxSweep`、`ShowXxxTip`、`ShowXxxIcon` 这类命名的字段塞进 Model 层。异步队列消费时，事件发生瞬间无法事后可靠推导的信息必须在入队时快照；当前状态只能作为校验或补充，不能替代事件快照。
- Review 新增跨层字段时必须先判断三点：它是领域事实还是 UI 表现；延迟消费后能否从当前状态可靠重建；字段名是否暴露具体 UI 控件或动画。任一不满足，就下沉到表现层或改成 policy 推导。
- 运行时本地 IO 必须只做必要写入：涉及 `LocalPrefs`、`FileSaveSystem`、MockStore 本地快照、局外本地偏好或非权威缓存时，禁止在心跳、Update、轮询、频繁 notify、UI 高频刷新等热路径每次直接落盘；应优先内存缓存，并通过节流、批量、脏标记、生命周期节点（登录、前后台切换、退出、显式保存）或业务事务完成点写入。
- 新增局外本地存档或非权威缓存时，必须说明写入触发点、最坏丢失窗口、异常 kill 误差、是否受设备时间修改影响，以及 mock/formal 两种运行模式下是否只执行必要 IO。
- 抽象只围绕真实扩展点建立，避免为了套模式增加无必要的类和跳转。

## 协议与 Mock 边界

- Hotfix 侧 Adapter 只能依赖接口，不直接依赖 mock/formal 具体实现。
- mock 与正式协议通过接口、registry 或 factory 选择；具体实现类型只能出现在 registry/factory 这类组合根中，不能出现在 Adapter、PropComponent、通用网络层或业务调用方。
- `#if MOCK_CLIENT`、`Mock.Csp`、`Mock.Datap` 等依赖必须集中在 mock 实现或 `NetworkMock` 内；关闭 `MOCK_CLIENT` 时，mock 实现类不应被编译，registry/factory 中也不应创建 mock 实现对象。
- `NetworkMock/Client/MockStore` 负责模拟服务端存档、业务校验、权威写入和协议返回；Hotfix 组件只消费协议结果并更新客户端缓存。
- NetworkMock 协议开关配置的唯一手写源是 `client/Unity/Assets/Resources/NetworkMock/NetworkMockSettings.json`；Editor、Player 和校验脚本读取同一文件，不再维护 `Assets/Scripts/NetworkMock/Editor/NetworkMockSettings.json`、`NetworkMockDefaultSettings.g.cs` 或其它可手改/生成副本作为配置源。
- 客户端需求默认先消费现有 `LoginResp`、`Notify`、`Heartbeat` 等协议数据并完成本地投影；不得默认修改 Go server、协议生成源、RoleDelta/Notify 触发语义或服务端持久化行为。
- 对“`LoginResp` 初始化 + 后续 `Notify` 增量同步”这类契约，不能为了客户端实现方便改成“登录时强制补发增量 `Notify`”；只有用户明确要求改变服务端契约，或 source of truth 明确生产方缺字段/缺语义时，才允许改生产方。
- 新增或修改客户端协议测试时，必须先标注被验证的是现有契约还是新契约；若测试需要服务端新行为才能通过，必须先回到需求确认，不得用测试驱动无授权的 server 行为变化。
- mock 关闭且正式协议缺失时，返回明确 `NotSupported`，不得静默回退到客户端本地改存档。
- 通用网络发送层保持通用，不加入 Prop、Meta 或其他业务模块的投影副作用。
- 具体业务写入必须使用模块级 adapter，例如 `JobProtocolAdapter`、`MapProtocolAdapter`、`SkillProtocolAdapter`、`LootProtocolAdapter`、`DigestProtocolAdapter`、`GuideProtocolAdapter`、`TaskProtocolAdapter`。
- 禁止新增大而全的 `MetaBusinessProtocolAdapter` 或类似业务总线；`MetaDataProtocolAdapter` 只处理 Meta 加载/清理。
- 命名必须表达真实角色：协议接口使用 `I...Protocol`，mock 实现使用 `...MockProtocol`，正式实现使用 `...FormalProtocol`；只有无状态工具方法集合才使用 `Helper` 或 `Support`。
- review 此类改动时必须检查四项：调用方是否只依赖接口、具体实现是否只在组合根出现、mock 关闭后是否完全走正式路径、正式协议缺失时是否显式返回 `NotSupported`。

## 迁移原则

- 玩法数据一旦属于服务端权威，真实模式归 Go 服务端持久化，mock 模式归 MockStore 持久化。
- 已进入 MockStore 迁移范围的模块，不保留客户端本地权威写入过渡策略；正式协议缺失时显式失败，mock 模式下由 MockStore 持久化。

## Unity 测试验证

- 排查 Unity Editor PlayMode / 运行态问题时，优先读取当前 Unity 工程内文件日志：`client/Unity/Logs/YYYY-MM-DD/HH-mm-ss-fff/`，重点看 `All.log` 及对应模块日志如 `Login.log`、`Network.log`、`OpenSvr.log`、`Default.log`。不要默认把 `client/Unity/Temp/log.txt` 当作当前 Editor 现场；它可能是 Android 包、旧运行或其它工具残留日志，只有用户明确指定时才作为该次证据。
- 修改或迭代开发不属于单一、低风险、小范围改动的客户端功能时，应优先在被测模块自有测试目录和测试程序集内增加或更新用例，覆盖核心成功路径、失败/边界条件及受影响状态；不要把新测试继续挂到历史聚合程序集 `Unity.Tests`。
- DragonPow2 当前基线已主动排除 Unity Test Framework/Performance 包并停用 `Unity.Tests`。不得仅为单个功能恢复这些包、修改旧 `Unity.Tests.asmdef` 引用或生成 `Unity.Tests`；确需恢复项目级 Test Runner 时，必须作为独立工具链变更评估编译面后再实施。
- 当目标工作副本已经存在模块自有 Editor 测试程序集时，允许它显式引用被测模块的 Runtime 与 Editor 程序集；测试程序集必须限制为 Editor，生产程序集不得反向引用测试程序集。是否新增测试程序集由目标项目测试策略单独决定，不能因本规则自动生成。
- 当前基线没有可用 Unity Test Runner 时，使用模块已有测试入口、uLoop dynamic-code 回归或不落 Scene/Prefab 的 Editor 烟测，并同时执行 Unity 编译验证。测试数为 0、测试命令不受支持或程序集未生成均不得报告为测试通过。
- 若 uLoop 提示 Unity Editor 未启动或 CLI Loop server 不可用，先按共享 Unity 编译验证规则执行 `uloop fix`、重试，再用 `uloop launch client/Unity` 启动 Unity Editor 后重跑验证。

## YooAsset 资源发布

- YooAsset 运行时发布源只认 `DefaultPackage/<PackageVersion>`，例如 `DefaultPackage/1.0`；其中 `1.0` 是 YooAsset `PackageVersion`，不是 SVN revision，不要改成 `r<SVN>` 或写进入口文件。
- `OutputCache` 是 YooAsset 管线输出和增量缓存，只能进入本地诊断归档；启用 YooAsset `EncryptionServices` 时，`OutputCache/*.bundle` 是加固前原始 bundle，`*.bundle.encrypt` 是加固中间文件，最终运行时文件以 `DefaultPackage/<PackageVersion>` 为准。
- FTP/CDN runtime 散文件、runtime ZIP 和校验 manifest 必须来自同一份 `DefaultPackage/<PackageVersion>` 输出。默认发布散文件支持 YooAsset 差异更新；ZIP 仅用于归档、校验、后台可视化、外网 CDN 二次分发或显式 archive 导入。
- 常规 FTP/SFTP 发布不假设服务端 unzip 能力。需要 ZIP 解压发布时，必须由构建后台受控解压并校验解压结果，不能让客户端在只存在 ZIP 的远端目录上期望散文件差异更新。

## 客户端提交与上传

- SVN/Git 提交日志、构建说明和变更摘要中禁止出现乱码、问号占位或无法确认编码的中文；中文日志必须在 UTF-8 环境中确认可读后再传给 `svn commit -m`、TortoiseSVN、Jenkins 或其它工具。
- Windows/PowerShell 下准备包含中文的 SVN 日志时，先确认 `chcp 65001`、`$OutputEncoding = [System.Text.UTF8Encoding]::new($false)`；必要时把日志写入 UTF-8 文本文件再由工具读取，避免 GBK/UTF-8 混用导致历史记录乱码。
- Windows/PowerShell 下提交中文 SVN 日志时，优先把日志写入 UTF-8 文本文件并使用 `svn commit -F <日志文件> --encoding utf-8`；避免直接用 `svn commit -m "中文..."`，除非已在当前终端确认编码不会被转换。
- 任何 `svn commit`、`git commit`、`svn import`、`svn copy`、push、上传制品、发布构建、触发线上/后台提交类操作，执行前必须单独询问用户并得到明确确认；不能把“继续”“修复”“帮我处理”理解为提交或上传授权。
- 涉及客户端多平台构建、补丁、CDN、Jenkins 或发布入口的改动，提交前必须明确 Android/iOS 等受影响平台矩阵并完成本地可行的 Unity 编译/测试；提交后必须触发并确认受影响平台构建通过，失败则继续修复，不能把未验证或未通过状态写成已完成。
