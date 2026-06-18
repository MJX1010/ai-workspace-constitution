# Claude Code Plugins & Skills Inventory

> 最后更新: 2026-04-01

## 已安装插件

### 1. claude-mem (v10.5.2)

- **功能**: 持久化记忆插件，自动捕获 coding session 中的决策、bugfix、架构变更等
- **来源**: `thedotmack/claude-mem` (GitHub marketplace)
- **Web UI**: http://localhost:37777
- **配置文件**: `~/.claude-mem/settings.json`
- **数据目录**: `~/.claude-mem/`（含 SQLite DB、ChromaDB、日志）

#### 安装命令

```bash
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

#### 关键配置

```json
{
  "CLAUDE_MEM_MODEL": "claude-sonnet-4-5",
  "CLAUDE_MEM_WORKER_PORT": "37777",
  "CLAUDE_MEM_WORKER_HOST": "127.0.0.1",
  "CLAUDE_MEM_PROVIDER": "claude",
  "CLAUDE_MEM_CLAUDE_AUTH_METHOD": "cli",
  "CLAUDE_MEM_CHROMA_ENABLED": "true",
  "CLAUDE_MEM_CHROMA_MODE": "local",
  "CLAUDE_MEM_DATA_DIR": "C:\\Users\\Admin\\.claude-mem"
}
```

---

### 2. memsearch (v0.1.16)

- **功能**: 基于 Milvus 的语义搜索记忆系统，Markdown 为 source of truth
- **来源**: `zilliztech/memsearch` (GitHub marketplace)
- **依赖**: Docker Desktop + Milvus v2.5.27+
- **配置文件**: `~/.memsearch/config.toml`
- **记忆目录**: 各项目 `.memsearch/memory/`

#### 安装命令

```bash
# 1. CLI 安装
pip install memsearch
# 或: uv tool install memsearch

# 2. Milvus 容器
docker run -d --name milvus-standalone \
  -e ETCD_USE_EMBED=true \
  -e COMMON_STORAGETYPE=local \
  -e COMMON_SECURITY_AUTHORIZATIONENABLED=true \
  -p 127.0.0.1:19530:19530 \
  -v milvus_data:/var/lib/milvus \
  --restart unless-stopped \
  milvusdb/milvus:v2.5.27 \
  milvus run standalone

# 3. Claude Code plugin
/plugin marketplace add zilliztech/memsearch
/plugin install memsearch@memsearch-plugins
```

#### 配置 (`~/.memsearch/config.toml`)

```toml
[embedding]
provider = "local"
model = "sentence-transformers/all-MiniLM-L6-v2"

[milvus]
uri = "http://localhost:19530"
token = "root:<password>"
```

#### Windows 兼容补丁

详见 Skill: `${WORKSPACE_ROOT}\DragonPow2\DragonPow2_Trunk\client\Unity\.claude\skills\memsearch-windows-setup`

补丁文件需覆盖到:
```
~/.claude/plugins/cache/memsearch-plugins/memsearch/<VERSION>/hooks/
```

---

### 3. superpowers (待安装)

- **功能**: 完整软件开发工作流框架，含 brainstorming、planning、TDD、code review、debugging 等 skills
- **来源**: `obra/superpowers` (GitHub)

#### 安装命令

```bash
# 方式 1: 如果在官方 marketplace 中
/plugin install superpowers@claude-plugins-official

# 方式 2: 从 GitHub 添加 marketplace
/plugin marketplace add obra/superpowers
/plugin install superpowers@superpowers-marketplace
```

---

## 插件注册文件位置

| 文件 | 路径 |
|------|------|
| 已安装插件 | `~/.claude/plugins/installed_plugins.json` |
| 已知 marketplace | `~/.claude/plugins/known_marketplaces.json` |
| 插件代码缓存 | `~/.claude/plugins/cache/` |
| 插件黑名单 | `~/.claude/plugins/blocklist.json` |

## Skills

| Skill | 位置 | 用途 |
|-------|------|------|
| memsearch-windows-setup | `${WORKSPACE_ROOT}\DragonPow2\...\Unity\.claude\skills\memsearch-windows-setup` | memsearch Windows 兼容性修复 |
| workspace-governance | `${WORKSPACE_ROOT}\.codex\skills\workspace-governance` | 工作区治理规范 |
| skill-factory-playbook | `${WORKSPACE_ROOT}\.codex\skills\skill-factory-playbook` | Skill 创建工厂流程 |
