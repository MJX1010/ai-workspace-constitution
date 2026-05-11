---
name: workspace-governance
description: "为整个上层工作区建立或维护通用治理规则、AGENTS.md、跨子工作区协作规范、AI coding guardrails、知识沉淀约束与维护 playbook。适用于用户要求抽取子工作区 skill 规则上提、统一 Codex/Claude/Gemini 风格约束、创建 workspace-level 通用 skill、整理最上层工作区维护规范、或设计 AI Vibe Coding 限法时。"
---

# Workspace Governance

## Overview

使用这个 skill 为整个顶层工作区建立统一的 `workspace governance`，把子工作区的有效规则、官方文档里的稳定原则、以及团队自己的维护习惯收敛成可复用的上层规范。

目标不是复制所有细节，而是提炼出可以跨 `Unity`、`.NET`、`Tools`、`Config`、`Share` 复用的治理规则。

## Core Workflow

### Phase 1: 定义治理边界

先判断这次需求属于哪一种：

- `workspace bootstrap`: 首次给顶层工作区建立规则
- `rule consolidation`: 从子工作区 skill、prompt、指南中抽取上层规则
- `guardrail design`: 设计 AI Vibe Coding 限法
- `governance refactor`: 统一多套 agent 规则，减少冲突
- `maintenance sync`: 把新的经验回写到顶层规范

只把满足下面条件的内容上提为顶层规则：

- 跨模块复用
- 与业务 feature 解耦
- 长期稳定
- 对新 agent 有明显 onboarding 价值

### Phase 2: 盘点现有约束

优先检查：

1. 最近的 `AGENTS.md`
2. 顶层和子目录的 `.codex/skills`
3. 其他 agent 体系，如 `.claude`、`.skills`、`.agent`
4. 架构文档、知识库、生成规则、代码放置约束

从现有 skill 中重点提取这几类规则：

- `instruction hierarchy`
- `ownership boundary`
- `generated-code protection`
- `knowledge capture`
- `documentation sync`
- `cross-workspace handoff`

不要上提以下内容：

- 单一业务模块专属逻辑
- 只对某一个 UI framework 有意义的具体 API 细节
- 频繁变化的临时 workaround
- 只能在某个 package 内成立的局部命名习惯

### Phase 3: 融合官方原则

把本地经验与官方 guidance 对齐，优先吸收这些稳定原则：

- OpenAI Codex: `AGENTS.md` 的最近规则优先、仓库级 rules file、可复用 skill
- Gemini: `system instructions`、清晰任务边界、结构化 prompt、显式约束
- Google Cloud Agentic AI: 按复杂度选择 `single-agent` 或 `multi-agent` pattern，避免过度设计
- Google AI Principles: 有益、可解释、可问责、避免不必要风险

如果官方建议与本地习惯冲突：

1. 优先保留对当前仓库更安全的约束
2. 记录冲突点
3. 把 vendor-specific 细节放进 `references/`，不要把易变内容写死在主 skill 里

详细原则见：

- `references/source-derived-principles.md`
- `references/workspace-vibe-coding-guardrails.md`

### Phase 4: 产出治理工件

默认产物：

1. 顶层 `AGENTS.md`
2. 一个通用治理 skill
3. 必要的参考文档 `references/*.md`

推荐职责分工：

- `AGENTS.md`: 高优先级、短小、全局适用的硬规则
- `SKILL.md`: 可执行 workflow、决策步骤、更新流程
- `references/*.md`: 长文原则、来源映射、checklist、template

### Phase 5: 写入 AI Vibe Coding 限法

限法要强调 `guardrails over slogans`。

至少覆盖：

- 先找 owner，再写代码
- 先判断 source of truth，再改文件
- 禁止手改 generated output
- 禁止无归属的大范围 sweep
- 禁止凭感觉新建 abstraction layer
- 发现新 invariant 时必须沉淀到文档或 skill

不要写成空泛口号，例如"保持高质量""注意架构一致性"。
要写成可执行约束，例如"修改前必须确认 owner module / dependency direction / verification surface"。

### Phase 6: 验证一致性

完成后执行这三个检查：

1. 顶层规则是否覆盖整个 workspace，而不是只覆盖 `Unity/`
2. 顶层规则是否与更近的子工作区规则冲突
3. skill frontmatter 是否明确说明触发场景

## Extraction Heuristics

把子工作区规则分成三类：

### A. 可直接上提

- 规则层级
- 生成代码保护
- 知识沉淀机制
- 文档同步责任
- 顶层工作区维护流程

### B. 需要抽象后上提

- 代码放置规则
- 分层依赖方向
- 模块协作方式
- 工具链同步流程

这类内容要先去掉框架私货，再转成 top-level guideline。

### C. 不应上提

- 具体业务系统实现
- 某个组件或 prefab 的使用方式
- 某个包的专用命名表
- 高频变动的临时流程

## Output Pattern

推荐输出结构：

```text
client/
  AGENTS.md
  .codex/
    skills/
      workspace-governance/
        SKILL.md
        references/
          source-derived-principles.md
          workspace-vibe-coding-guardrails.md
```

## Maintenance Rules

- 发现新的跨工作区规则时，优先更新顶层 skill，而不是复制到多个子 skill
- 子工作区规则更具体时，保留"closest rule wins"
- 只保留 high-signal 内容；把长解释移到 `references/`
- 使用简体中文撰写，夹带必要的 English technical terms
