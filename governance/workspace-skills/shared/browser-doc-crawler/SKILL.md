---
name: browser-doc-crawler
description: 从已登录浏览器会话抓取内部文档站点并导出本地 HTML/Markdown 的工作流和脚本。用于需要通过 Chrome DevTools Protocol 读取登录态页面、整理 Feishu/Lark/GDev/Docusaurus/React SPA 等浏览器可访问文档、批量生成 html/、md/、index、all、manifest artifacts，或用户要求“通过当前浏览器整理全部文档”“减少 token 消耗，用脚本落地文档内容”的场景。
---

# Browser Doc Crawler

## 核心原则

使用 `scripts/crawl-browser-docs.mjs` 连接已经登录的 Chromium/Chrome DevTools 端口，从起始页递归收集同源同路径范围内的文档链接，输出到本地文件。不要把大段正文贴进聊天；让脚本写入 artifacts 后只汇报路径、页数和失败项。

脚本不读取浏览器 cookie 数据库，也不绕过权限；它只复用用户已经登录并打开的浏览器页面。

## 启动浏览器

如果没有现成 CDP 端口，先启动一个专用浏览器窗口并在里面登录目标站点：

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --remote-debugging-port=9222 `
  --user-data-dir="${WORKSPACE_ROOT}\.codex_tmp\browser-doc-profile" `
  --new-window "<start-url>"
```

保持这个窗口打开。若公司 SSO 需要人工确认，让用户在该窗口完成登录后再运行脚本。

## 运行脚本

脚本路径：

```text
${WORKSPACE_ROOT}\.agents\skills\browser-doc-crawler\scripts\crawl-browser-docs.mjs
```

通用命令：

```powershell
node ${WORKSPACE_ROOT}\.agents\skills\browser-doc-crawler\scripts\crawl-browser-docs.mjs `
  --start-url "<logged-in-doc-url>" `
  --output-dir "${WORKSPACE_ROOT}\_outputs\<export-name>" `
  --scope-prefix "/docs/path/prefix/" `
  --max-pages 200 `
  --clean
```

GDev UnityNew 示例：

```powershell
node ${WORKSPACE_ROOT}\.agents\skills\browser-doc-crawler\scripts\crawl-browser-docs.mjs `
  --start-url "https://gdev.nvsgames.cn/doc/Global/UnityNew/CoreModules/SDKSetupandProjectConfiguration/Documentation" `
  --output-dir "${WORKSPACE_ROOT}\_outputs\gdev-unitynew-docs" `
  --scope-prefix "/doc/Global/UnityNew/CoreModules/SDKSetupandProjectConfiguration/" `
  --clean
```

常用参数：

- `--scope-prefix`：限定抓取路径，只接受路径前缀；可重复传多个。
- `--extra-seed`：补充入口 URL；用于目录里没有普通 `<a>` 链接的隐藏页面。
- `--max-pages`：限制最多保存页数，smoke test 用 2 到 5。
- `--no-react-seeds`：关闭 React fiber 目录种子提取。
- `--tab-label`、`--service-item-selector`、`--tab-selector`：调整 React/Docusaurus/GDev 式点击目录的提取规则。
- `--no-combined`：跳过 `all.md` 和 `all.html`，适合超大文档树。
- `--md-bom`：给 Markdown 输出添加 UTF-8 BOM，兼容 Windows PowerShell 5.1、旧版记事本等默认按 ANSI 打开的工具。
- `--no-encoding-scan`：关闭可疑中文乱码 token 扫描；默认开启。

## 输出结构

输出目录包含：

- `html/*.html`：每页独立 HTML。
- `md/*.md`：每页独立 Markdown。
- `index.html`、`index.md`：页面索引。
- `all.html`、`all.md`：合并阅读版，除非传 `--no-combined`。
- `manifest.json`：配置、URL、文件名、失败项和文本长度。

图片和附件默认保留原始远程 URL，不下载离线资产。

## 中文编码

脚本所有文件按 UTF-8 写入，HTML 带 `<meta charset="utf-8">`，JSON 不加 BOM。Markdown 默认不加 BOM；如果后续要在 Windows PowerShell 5.1 或旧工具里直接打开中文 Markdown，运行时加 `--md-bom`。

PowerShell 5.1 查看无 BOM 的 UTF-8 Markdown 时要显式指定编码：

```powershell
Get-Content -Raw -Encoding UTF8 ${WORKSPACE_ROOT}\_outputs\<export-name>\index.md
```

脚本默认会扫描标题和 Markdown 正文里的典型 mojibake token，例如 Unicode replacement character 和常见 GBK/UTF-8 错解片段。发现后会在控制台输出 `encoding-warn`，并把 `encodingWarnings` 写入 `manifest.json`。这类告警表示源页面或提取结果需要人工复核，不要直接用聊天上下文猜测修复。

## 验证

先做语法检查：

```powershell
node --check ${WORKSPACE_ROOT}\.agents\skills\browser-doc-crawler\scripts\crawl-browser-docs.mjs
```

再做小范围 smoke test：

```powershell
node ${WORKSPACE_ROOT}\.agents\skills\browser-doc-crawler\scripts\crawl-browser-docs.mjs `
  --start-url "<logged-in-doc-url>" `
  --output-dir "${WORKSPACE_ROOT}\_outputs\browser-doc-crawler-smoke" `
  --scope-prefix "<path-prefix>" `
  --max-pages 3 `
  --clean
```

检查 `manifest.json` 的 `pages` 数量和 `error` 项。若 CDP 未启动、页面未登录、scope 过窄或站点需要人工点击展开，先修正这些条件再扩大页数。
