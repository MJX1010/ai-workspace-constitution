---
name: skill-factory-playbook
description: "创建、迁移、升级或审计工作区 skill 的通用工厂流程。适用于用户要求把子工作区 skill 规则上提到顶层、融合 Codex/Claude/Gemini 官方或社区准则、整理 skill 创建流程、建立统一 skill catalog、或把一次性经验沉淀成长期可复用 skill 时。"
---

# Skill Factory Playbook

## Overview

使用这个 skill 把一次性的经验抽取工作，变成可重复执行的 `skill creation pipeline`。它特别适合处理"从子工作区提炼规则，再升级为顶层 skill"的场景。

## Pipeline

### Step 1: Inventory

盘点这些输入源：

- 现有 `skills/`
- `AGENTS.md`
- 架构文档和知识库
- 其他 agent 配置，如 `.claude`, `.skills`, `.agent`
- 官方文档和社区实践

为每个输入源记录：

- `scope`
- `stability`
- `reuse value`
- `target audience`

### Step 2: Extract

把内容拆成三层：

- `rule`: 必须遵守的硬约束
- `workflow`: 重复执行的操作步骤
- `reference`: 长文说明、来源映射、背景原则

仅当某条内容可跨任务、跨模块、跨会话复用时，才值得放入 skill。

### Step 3: Normalize

做规范化处理：

- 去掉 feature-specific 细节
- 去掉短期 workaround
- 去掉纯聊天式表述
- 保留 trigger words、decision points、hard constraints

目标是从"经验描述"转成"可触发、可执行、可维护的 skill"。

### Step 4: Design Artifact Shape

默认结构：

```text
<skill-name>/
  SKILL.md
  references/
    *.md
```

仅在确实需要 deterministic automation 时再增加 `scripts/`。
没有用途的 `assets/`、示例脚本、占位参考文档要删除。

### Step 5: Initialize

新 skill 优先使用初始化脚本创建骨架，再手工精简。

推荐命令模式：

```powershell
python -X utf8 <skill-creator>/scripts/init_skill.py <skill-name> --path <skills-root>
```

Windows 环境优先使用 `-X utf8`，避免控制台编码导致脚本初始化失败。

### Step 6: Author

写 `SKILL.md` 时遵守这些规则：

- frontmatter description 要写清楚"做什么 + 什么时候触发"
- 主体只写 workflow 与 decision logic
- 详细原则放进 `references/`
- 用简体中文为主，搭配 English technical terms

### Step 7: Validate

至少验证：

1. YAML frontmatter 合法
2. description 能准确触发
3. body 没有占位 TODO
4. references 与主体没有重复污染
5. 不再保留无用示例文件

如果有验证脚本，运行它；如果没有，做人工结构检查。

## Migration Pattern

当要把 `child workspace skill` 上提到 `top-level workspace skill` 时：

1. 先抽象出稳定原则
2. 再分离 child-specific 细节
3. 最后把稳定原则写到顶层，把具体细节留在子 skill

不要把子工作区的内部 API 直接复制到顶层 skill。

## Output Standard

每次创建或升级 skill，至少输出：

- 新 skill 的用途
- 触发方式
- 关键 workflow
- 引用的规则来源
- 后续维护方式

## Reference Routing

按需读取：

- `references/skill-creation-workflow.md`: 创建流程与检查清单
- `references/source-map.md`: 本次技能工厂使用的来源和映射
