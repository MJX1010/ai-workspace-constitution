## 语言与描述

- 首要使用中文沟通和记录设计结论；除非用户明确要求英文，客户端相关说明、注释、README、review 结论优先使用中文。
- 保留类名、协议名、字段名、路径、命令原文；解释这些名称的职责和边界时使用中文。

## 编码设计原则

- 客户端编码应遵循设计模式和面向对象设计原则，优先保证单一职责、依赖倒置、接口隔离和开放封闭。
- 当 Hotfix、NetworkMock、正式协议、mock 协议之间存在实现切换时，优先通过接口、adapter、factory、registry 或 strategy 组织，不让调用方直接依赖具体实现。
- UI、客户端缓存投影、协议适配、mock 服务端逻辑必须分层清楚；通用组件不承载模块特化副作用。
- 抽象只围绕真实扩展点建立，避免为了套模式增加无必要的类和跳转。

## 协议与 Mock 边界

- Hotfix 侧 Adapter 只能依赖接口，不直接依赖 mock/formal 具体实现。
- mock 与正式协议通过接口、registry 或 factory 选择；具体实现类型只能出现在 registry/factory 这类组合根中，不能出现在 Adapter、PropComponent、通用网络层或业务调用方。
- `#if MOCK_CLIENT`、`Mock.Csp`、`Mock.Datap` 等依赖必须集中在 mock 实现或 `NetworkMock` 内；关闭 `MOCK_CLIENT` 时，mock 实现类不应被编译，registry/factory 中也不应创建 mock 实现对象。
- `NetworkMock/Client/MockStore` 负责模拟服务端存档、业务校验、权威写入和协议返回；Hotfix 组件只消费协议结果并更新客户端缓存。
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

- 修改或迭代开发不属于单一、低风险、小范围改动的客户端功能时，默认需要在 `Unity.Tests` 增加或更新对应测试用例，覆盖核心成功路径、失败/边界条件以及受影响的协议、mock、缓存投影或 UI 状态路径；完成前必须按本节命令全量跑测 `Unity.Tests` 并报告结果。
- 需要全量验证 `Unity.Tests` 项目测试程序集时，从项目根目录运行：

```powershell
uloop run-tests --project-path client/Unity --test-mode PlayMode --filter-type assembly --filter-value Unity.Tests
```

- 若 uLoop 提示 Unity Editor 未启动或 CLI Loop server 不可用，先按共享 Unity 编译验证规则执行 `uloop fix`、重试，再用 `uloop launch client/Unity` 启动 Unity Editor 后重跑测试。
- 若测试被未保存的场景/Prefab 阻断，或 Unity 报 `Assets/Scenes/Init.unity` 等场景存在未保存改动并导致测试数为 0，必须按共享 uLoop 规则保存后继续：追加 `--save-before-run true` 重跑同一条测试命令，并报告阻断路径与重跑后的测试结果；除非用户明确要求丢弃改动，不得通过 revert / checkout 场景来绕过验证。例如：

```powershell
uloop run-tests --project-path client/Unity --test-mode PlayMode --filter-type assembly --filter-value Unity.Tests --save-before-run true
```
