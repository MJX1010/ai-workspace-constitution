# Skill Creation Workflow

本流程适用于在仓库里创建 `production-grade skill`，尤其是从既有子工作区经验中抽取通用规范。

## Workflow

### 1. Understand the ask

确认用户要的是：

- 新 skill
- 更新现有 skill
- 上提顶层规范
- skill 审计
- 多 agent 规则统一

### 2. Find reusable inputs

优先看这些输入：

- 现有 skill frontmatter 和 workflow
- 共享文档、知识库、架构图
- 官方 vendor docs
- 项目里的成熟实践

### 3. Score each candidate rule

按这四项打分：

- `Generality`
- `Stability`
- `Actionability`
- `Discovery value`

低分内容不要塞进顶层 skill。

### 4. Decide the artifact split

- 短硬规则 -> `AGENTS.md`
- 可执行流程 -> `SKILL.md`
- 长解释/来源/模板 -> `references/*.md`
- 需要自动化的固定动作 -> `scripts/`

### 5. Create and prune

先初始化，再删除无用样板。

常见要删除的内容：

- `example.py`
- `example_asset.txt`
- 占位 API reference
- 没写完的 TODO 段落

### 6. Verify trigger quality

frontmatter `description` 要保证：

- 用户自然语言能命中
- 范围不过宽
- 包含"何时使用"
- 不把 body 才能看到的触发信息藏起来

### 7. Publish and maintain

发布后要把后续经验继续回写，不要让 skill 再次过时。

## Anti-Patterns

- 把 skill 写成 README
- 把背景故事写得比 workflow 还长
- 把所有细节都塞进主文件
- 不区分顶层规则和子工作区规则
- 创建 skill 但不做验证
