# Workspace Vibe Coding Guardrails

本文件定义整个顶层工作区的 `AI Vibe Coding` 限法。目标是保留 agentic coding 的速度，同时压住误改、乱改、过度抽象和跨模块污染。

## Golden Rule

`Fast is good. Blind is forbidden.`

## Hard Guardrails

### 1. No owner, no edit

在没有确认 owner module、owner folder、owner build surface 之前，不允许直接写代码。

### 2. No source-of-truth, no patch

在没有确认当前文件是：

- hand-written source
- generated output
- config definition
- template
- derived cache

之前，不允许直接 patch。

### 3. No sweep without blast-radius estimate

大范围替换、批量重命名、自动生成、跨目录迁移前，必须先说明 `blast radius`：

- 影响哪些项目或程序集
- 是否会触发重新生成
- 是否会影响 child workspace 规则
- 如何验证

### 4. No abstraction before repetition

没有看到至少两个到三个稳定重复场景，不要新建 framework、helper layer、base class、manager、facade。

### 5. No silent rule drift

当修复暴露出稳定的新规则时，必须同步到：

- 最近的 skill
- 或顶层 `AGENTS.md`
- 或对应参考文档

不能只停留在当前对话里。

## Preferred Behaviors

### Prefer

- nearby pattern matching
- explicit assumptions
- narrow-scope edits
- verification-oriented execution
- bilingual docs with English technical terms

### Avoid

- rewriting architecture from scratch
- mixing generated code with manual code
- hidden dependency inversion
- "顺手"修改无关模块
- 只给概念，不给可执行 constraint

## Required Pre-Edit Checklist

开始 substantial edit 前，至少完成下面四项：

1. `Owner`: 我改的是谁负责的模块
2. `Boundary`: 它和上下游的依赖边界是什么
3. `Truth`: 真正应该修改的 source 在哪里
4. `Verify`: 改完如何确认没有回归

## Escalation Conditions

遇到以下情况，应先停下并补充上下文，而不是继续"vibe"：

- 两个以上目录都可能是正确落点
- 代码看起来像 generated output
- 需要跨 `Unity` / `.NET` / `Config` 同步
- 修改会影响 build pipeline 或 codegen
- 现有模式彼此冲突

## Review Standard

任何 AI 产出的 patch，都至少要能回答：

- 为什么这里是正确的落点
- 为什么这不是 generated code
- 为什么这次改动没有破坏依赖方向
- 为什么验证足以覆盖风险

## Encoding Guardrail

在 Windows 工作区处理中文文本时，先区分 `文件编码错误` 和 `终端显示乱码`，不要看到 mojibake 就直接认定文件被写坏。

### Required Checks

- 涉及中文注释、`LabelText`、文档、规则文件时，默认按 `UTF-8` 写入。
- 在 PowerShell 里检查中文内容时，优先使用 `Get-Content -Encoding UTF8`；直接 `Get-Content` 的显示乱码不能单独作为结论。
- 如果需要通过 shell 回写文件，必须显式指定 `UTF-8` 编码，避免落回系统默认代码页。
- 修复"乱码"前，先确认是磁盘文件真的损坏，还是只是当前终端的解码方式不对。

### Why This Exists

Codex/agent 在 Windows 环境里经常会遇到：文件本身是正常 UTF-8，但 PowerShell 直接读取时中文显示异常。这个场景如果误判成"写文件编码坏了"，很容易引发二次错误修复和无效重写。
