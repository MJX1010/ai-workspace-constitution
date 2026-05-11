# Source-Derived Principles

本文件把本地 skill 经验与外部官方 guidance 做了 `principle extraction`，用于支撑顶层工作区治理。

## Local Skills -> Reusable Rules

### `et-code-guardian`

可复用原则：

- 先判断 `ownership boundary`
- 先判断依赖方向，再决定落点
- 生成代码受保护，修改 source of truth 而不是 output
- 目录结构本身就是 architecture contract

不直接上提的内容：

- ET/YIUI 专属装配层与目录细节
- lockstep、YIUI invoke、Luban editor 的具体规则

### `project-knowledge-base`

可复用原则：

- 只沉淀高价值 insight
- 按 domain 归档，不要做单体大文档
- 更新索引和入口文档
- 优先保存"为什么"和"如何做"

### `project-arch-writer`

可复用原则：

- 先分析代码，再写架构文档
- 文档要区分 human-facing 与 agent-facing audience
- 用结构化模板表达类、数据流、约束、模式

### `meta-skill-sync`

可复用原则：

- 结束一轮开发后，要把新规则同步回 skill
- 新知识需要做分类、去重、路由到正确文档
- UI/doc/rule 应保持同步

### `skill-creator`

可复用原则：

- 保持 `progressive disclosure`
- skill body 只写 workflow 和 trigger-critical 内容
- 详细原则放到 `references/`
- 新 skill 应初始化、编辑、验证、再迭代

## Official Guidance -> Governance Rules

## OpenAI Codex

来源：

- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/rules

提炼结果：

- 用 `AGENTS.md` 承载 repository-level instructions
- 使用最近规则优先，避免顶层规则压扁子目录语义
- 可把长规则拆成 `rules/*.md` 或 skill references，避免主文件膨胀
- 把通用操作变成 reusable skills，而不是反复重写 prompt

## Gemini

来源：

- https://ai.google.dev/gemini-api/docs/system-instructions
- https://ai.google.dev/guide/prompt_best_practices

提炼结果：

- system instructions 要稳定、清晰、直接
- prompt 要写清目标、约束、输入、输出格式
- 复杂任务要结构化，不要靠隐式猜测
- 限法要显式写出来，而不是假设模型会自己遵守

## Google AI Principles

来源：

- https://ai.google/principles/

提炼结果：

- 规范应服务于真实用户价值，而不是形式主义
- 自动化应可解释、可审计、可问责
- 对高风险或高影响操作必须增加 guardrail
- 优先减少误改、误判、误传播的系统性风险

## Google Cloud Agentic AI Design Patterns

来源：

- https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system?hl=zh-cn

提炼结果：

- 先选足够简单的 pattern，再谈多 agent
- 用 routing、tool-use、orchestration pattern 解决明确问题
- 避免没有边界和角色分工的"万能 agent"
- 每个 agent 或 skill 都应有明确 `scope`, `inputs`, `outputs`

## Community Practice: everything-claude-code

来源：

- https://github.com/affaan-m/everything-claude-code

提炼结果：

- 把 agent memory、rules、skills、commands 做体系化组织
- 统一多 agent 使用的 shared conventions
- 把经验沉淀为 discoverable artifacts，而不是散落在聊天记录里

## Top-Level Translation

综合以上来源，顶层工作区应长期保留这几条硬原则：

1. `closest rule wins`
2. `source of truth first`
3. `ownership before edits`
4. `minimal but complete changes`
5. `knowledge capture after discovery`
6. `progressive disclosure for long guidance`
