## 语言与描述

- 首要使用中文沟通和记录设计结论；除非用户明确要求英文，服务端相关说明、注释、README、review 结论优先使用中文。
- 保留包名、协议名、字段名、路径、命令原文；解释职责、流程和边界时使用中文。

## 编码设计原则

- 服务端编码应遵循设计模式和面向对象/模块化设计原则，优先保证单一职责、依赖倒置、接口隔离和开放封闭。
- handler、service、repository、protocol model、生成代码之间职责要清晰；handler 保持薄入口，复杂业务下沉到明确的服务或领域模块。
- 当同一流程存在多种实现或运行模式时，优先通过接口、factory、registry 或 strategy 组织，不在业务入口堆叠具体实现分支。
- 抽象必须服务于真实变化点，避免为了套模式增加无必要的层级。
- 跨层状态队列、ledger、projection、presentation request 必须区分“领域事实 / 事件快照”和“界面表现细节”。Model、协议、持久化、ledger 层只保存可复现的领域事实、状态快照和通用表现事实，例如 `OldState`、`NewState`、`WasTracked`、`Version`、`Sequence`、`RewardItems`、`DialogId`、`TipsType`；不得保存具体 UI 控件、动画、扫光、Toast、Panel、颜色、Icon 高光等 View / ModelView 细节开关。
- 表现层需要动画或 UI 判断时，必须在 ModelView、YIUI、UI 播放入口根据事件快照、task policy 或 view policy 推导；不要把 `ShowXxxSweep`、`ShowXxxTip`、`ShowXxxIcon` 这类命名的字段塞进 Model 层。异步队列消费时，事件发生瞬间无法事后可靠推导的信息必须在入队时快照；当前状态只能作为校验或补充，不能替代事件快照。
- Review 新增跨层字段时必须先判断三点：它是领域事实还是 UI 表现；延迟消费后能否从当前状态可靠重建；字段名是否暴露具体 UI 控件或动画。任一不满足，就下沉到表现层或改成 policy 推导。

## 协议与生成代码

- 新增或修改 CS/SS 协议时，先更新 `server/meta/models/*` 中的模型定义，再运行协议生成命令，不能手改生成产物。
- `.gen.go`、生成 proto、生成 C# pb 等自动生成文件只允许由生成脚本更新。
- 服务端 handler 应负责协议入口与错误返回，复杂业务规则和持久化操作应下沉到 service/repository 或清晰的领域模块。
