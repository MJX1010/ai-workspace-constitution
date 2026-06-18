#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

const defaults = {
  port: 9222,
  maxPages: 600,
  settleMs: 700,
  outputDir: "browser-doc-export",
  tabLabels: ["移动端", "PC端"],
  serviceItemSelector: ".c2ec2",
  tabSelector: ".arco-tabs-header-title, [role='tab']",
  collectReactSeeds: true,
  combined: true,
  clean: false,
  markdownBom: false,
  encodingScan: true,
};

const UTF8_BOM = "\uFEFF";
const mojibakePattern = /\uFFFD|\u95C2.|\u9225.|\u9286|\u9346|\u7F02|\u93C2|\u7039|\u6960\u5C83|\u74BA|\u68F0|\u6748|\u9A9E[\u8235\u6735]|\u7ED4|\u93C8|\u93B4|\u9436\u52F0|\u6D93\u20AC|\u65BA|\u6522/g;

function usage() {
  return `Usage:
  node crawl-browser-docs.mjs --start-url <url> --output-dir <dir> [options]

Required:
  --start-url <url>              Logged-in documentation page to start from.
  --output-dir <dir>             Output directory for html/, md/, index, all, manifest.

Options:
  --port <number>                Chrome DevTools port. Default: ${defaults.port}
  --scope-prefix <path>          Allowed URL path prefix. Repeat for multiple scopes.
  --extra-seed <url>             Additional seed URL. Repeatable.
  --max-pages <number>           Stop after this many saved pages. Default: ${defaults.maxPages}
  --settle-ms <number>           Wait after page ready before extraction. Default: ${defaults.settleMs}
  --tab-label <text>             Tab label for React seed extraction. Repeatable.
  --service-item-selector <css>  React service item selector. Default: ${defaults.serviceItemSelector}
  --tab-selector <css>           Tab selector. Default: ${defaults.tabSelector}
  --no-react-seeds               Disable React fiber service-list seed extraction.
  --no-combined                  Skip all.md and all.html generation.
  --md-bom                       Prefix Markdown files with UTF-8 BOM for legacy Windows tools.
  --no-encoding-scan             Skip suspicious mojibake warning scan.
  --clean                        Delete output directory before writing.
  --help                         Show this help.

Example:
  node crawl-browser-docs.mjs \\
    --start-url "https://docs.example.internal/handbook/start" \\
    --output-dir "D:/Projects/_outputs/internal-handbook" \\
    --scope-prefix "/handbook/" \\
    --clean
`;
}

function parseArgs(argv) {
  const args = {
    scopePrefixes: [],
    extraSeeds: [],
    tabLabels: [],
  };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }
    const [rawKey, inlineValue] = token.slice(2).split(/=(.*)/s, 2);
    const key = rawKey.trim();
    const nextValue = () => {
      if (inlineValue !== undefined) return inlineValue;
      if (i + 1 >= argv.length || argv[i + 1].startsWith("--")) {
        throw new Error(`Missing value for --${key}`);
      }
      i += 1;
      return argv[i];
    };
    switch (key) {
      case "help":
        args.help = true;
        break;
      case "start-url":
        args.startUrl = nextValue();
        break;
      case "output-dir":
        args.outputDir = nextValue();
        break;
      case "port":
        args.port = Number(nextValue());
        break;
      case "scope-prefix":
        args.scopePrefixes.push(nextValue());
        break;
      case "extra-seed":
        args.extraSeeds.push(nextValue());
        break;
      case "max-pages":
        args.maxPages = Number(nextValue());
        break;
      case "settle-ms":
        args.settleMs = Number(nextValue());
        break;
      case "tab-label":
        args.tabLabels.push(nextValue());
        break;
      case "service-item-selector":
        args.serviceItemSelector = nextValue();
        break;
      case "tab-selector":
        args.tabSelector = nextValue();
        break;
      case "no-react-seeds":
        args.collectReactSeeds = false;
        break;
      case "react-seeds":
        args.collectReactSeeds = true;
        break;
      case "no-combined":
        args.combined = false;
        break;
      case "combined":
        args.combined = true;
        break;
      case "md-bom":
      case "markdown-bom":
        args.markdownBom = true;
        break;
      case "no-md-bom":
      case "no-markdown-bom":
        args.markdownBom = false;
        break;
      case "encoding-scan":
        args.encodingScan = true;
        break;
      case "no-encoding-scan":
        args.encodingScan = false;
        break;
      case "clean":
        args.clean = true;
        break;
      default:
        throw new Error(`Unknown option: --${key}`);
    }
  }
  return args;
}

function buildConfig(argv) {
  const parsed = parseArgs(argv);
  if (parsed.help) {
    console.log(usage());
    process.exit(0);
  }
  const startUrl = parsed.startUrl || process.env.BROWSER_DOC_START_URL;
  if (!startUrl) throw new Error("--start-url is required");
  const start = new URL(startUrl);
  const outputDir = path.resolve(parsed.outputDir || process.env.BROWSER_DOC_OUTPUT_DIR || defaults.outputDir);
  const inferredScope = start.pathname.endsWith("/")
    ? start.pathname
    : start.pathname.replace(/\/[^/]*$/, "/");
  const scopePrefixes = parsed.scopePrefixes.length ? parsed.scopePrefixes : [inferredScope];
  return {
    port: parsed.port || Number(process.env.BROWSER_DOC_CDP_PORT || defaults.port),
    startUrl: start.toString(),
    startOrigin: start.origin,
    outputDir,
    scopePrefixes: scopePrefixes.map(normalizePrefix),
    extraSeeds: parsed.extraSeeds,
    maxPages: parsed.maxPages || Number(process.env.BROWSER_DOC_MAX_PAGES || defaults.maxPages),
    settleMs: parsed.settleMs || Number(process.env.BROWSER_DOC_SETTLE_MS || defaults.settleMs),
    tabLabels: parsed.tabLabels.length ? parsed.tabLabels : defaults.tabLabels,
    serviceItemSelector: parsed.serviceItemSelector || defaults.serviceItemSelector,
    tabSelector: parsed.tabSelector || defaults.tabSelector,
    collectReactSeeds: parsed.collectReactSeeds ?? defaults.collectReactSeeds,
    combined: parsed.combined ?? defaults.combined,
    clean: parsed.clean ?? defaults.clean,
    markdownBom: parsed.markdownBom ?? defaults.markdownBom,
    encodingScan: parsed.encodingScan ?? defaults.encodingScan,
  };
}

function normalizePrefix(prefix) {
  if (!prefix.startsWith("/")) return `/${prefix}`;
  return prefix;
}

const config = buildConfig(process.argv.slice(2));
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}: ${url}`);
  }
  return response.json();
}

async function writeUtf8(filePath, content, options = {}) {
  const text = options.bom && !String(content).startsWith(UTF8_BOM) ? UTF8_BOM + content : content;
  await fs.writeFile(filePath, text, "utf8");
}

function scanEncodingWarnings(label, text) {
  if (!config.encodingScan || !text) return [];
  const matches = [...new Set(String(text).match(mojibakePattern) || [])];
  return matches.slice(0, 8).map((token) => `${label}: suspicious token "${token}"`);
}

function collectEncodingWarnings(pageData) {
  return [
    ...scanEncodingWarnings("title", pageData.title),
    ...scanEncodingWarnings("markdown", pageData.markdown),
  ];
}

async function getOrCreateTarget() {
  const targets = await fetchJson(`http://127.0.0.1:${config.port}/json/list`);
  const scopedTarget =
    targets.find((item) => item.type === "page" && item.url && isInScope(item.url)) ||
    targets.find((item) => item.type === "page" && item.url?.startsWith(config.startOrigin)) ||
    targets.find((item) => item.type === "page");
  if (scopedTarget?.webSocketDebuggerUrl) return scopedTarget;

  const newTarget = await fetchJson(
    `http://127.0.0.1:${config.port}/json/new?${encodeURIComponent(config.startUrl)}`,
    { method: "PUT" }
  );
  if (!newTarget?.webSocketDebuggerUrl) {
    throw new Error("Could not create Chrome DevTools page target");
  }
  return newTarget;
}

async function connectPage() {
  const target = await getOrCreateTarget();
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  const pending = new Map();
  let id = 0;

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      pending.get(message.id)(message);
      pending.delete(message.id);
    }
  };

  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });

  function send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const callId = ++id;
      pending.set(callId, (message) => {
        if (message.error) reject(new Error(`${method}: ${message.error.message}`));
        else resolve(message.result);
      });
      ws.send(JSON.stringify({ id: callId, method, params }));
    });
  }

  await send("Page.enable");
  await send("Runtime.enable");
  return { send, close: () => ws.close() };
}

function normalizeUrl(rawUrl, baseUrl = config.startUrl) {
  try {
    const url = new URL(rawUrl, baseUrl);
    url.hash = "";
    if (url.search === "?") url.search = "";
    return url.toString();
  } catch {
    return null;
  }
}

function isInScope(rawUrl) {
  try {
    const url = new URL(rawUrl, config.startUrl);
    return (
      url.origin === config.startOrigin &&
      config.scopePrefixes.some((prefix) => url.pathname.startsWith(prefix)) &&
      !url.pathname.includes("/api/")
    );
  } catch {
    return false;
  }
}

function fileBaseName(urlText) {
  const url = new URL(urlText);
  const hash = crypto.createHash("sha1").update(urlText).digest("hex").slice(0, 8);
  let slug = url.pathname
    .replace(/^\/+|\/+$/g, "")
    .replace(/%/g, "pct")
    .replace(/[\\/:*?"<>|]+/g, "_")
    .replace(/\s+/g, "_");
  if (!slug) slug = "index";
  if (slug.length > 150) slug = `${slug.slice(0, 150)}-${hash}`;
  return slug;
}

function uniqueFileName(base, used) {
  let name = base;
  let suffix = 2;
  while (used.has(name)) {
    name = `${base}-${suffix}`;
    suffix += 1;
  }
  used.add(name);
  return name;
}

async function evaluate(page, expression, returnByValue = true) {
  const result = await page.send("Runtime.evaluate", {
    expression,
    returnByValue,
    awaitPromise: true,
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text || "Runtime error");
  }
  return returnByValue ? result.result.value : result.result;
}

function browserState() {
  const main = document.querySelector("main article, article, main");
  const bodyText = document.body ? document.body.innerText || "" : "";
  const mainText = main ? main.innerText || "" : "";
  return {
    url: location.href,
    title: document.title,
    readyState: document.readyState,
    bodyTextLen: bodyText.length,
    mainTextLen: mainText.length,
    hasArticle: Boolean(document.querySelector("main article, article, .theme-doc-markdown, main")),
  };
}

async function waitUntilReady(page) {
  const deadline = Date.now() + 30000;
  let last = null;
  while (Date.now() < deadline) {
    const state = await evaluate(page, `(${browserState.toString()})()`);
    last = state;
    const enoughText = state.mainTextLen > 40 || state.bodyTextLen > 200;
    if (state.readyState === "complete" && state.hasArticle && enoughText) {
      await sleep(config.settleMs);
      return state;
    }
    await sleep(350);
  }
  return last;
}

async function navigate(page, url) {
  await page.send("Page.navigate", { url });
  await waitUntilReady(page);
}

function browserExtractReactSeeds(options) {
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const visible = (el) => {
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    return rect.width > 0 && rect.height > 0 && style.visibility !== "hidden" && style.display !== "none";
  };
  const inScope = (rawUrl) => {
    try {
      const url = new URL(rawUrl, location.href);
      return (
        url.origin === options.origin &&
        options.scopePrefixes.some((prefix) => url.pathname.startsWith(prefix)) &&
        !url.pathname.includes("/api/")
      );
    } catch {
      return false;
    }
  };
  const toUrl = (href) => {
    if (!href) return null;
    let value = href;
    if (value.startsWith("Global/")) value = `/doc/${value}`;
    if (value.startsWith("doc/")) value = `/${value}`;
    if (!value.startsWith("/") && !/^https?:\/\//.test(value)) value = `/doc/${value}`;
    try {
      const url = new URL(value, location.origin);
      url.hash = "";
      return url.toString();
    } catch {
      return null;
    }
  };
  const flatten = (items, tabLabel, groupTitle) => {
    const rows = [];
    for (const group of items || []) {
      for (const item of group.items || []) {
        const url = toUrl(item.href);
        if (url && inScope(url)) {
          rows.push({
            tab: tabLabel,
            group: groupTitle || "",
            subTitle: group.subTitle || "",
            label: item.label || "",
            href: item.href || "",
            url,
          });
        }
      }
    }
    return rows;
  };
  const collectActive = (tabLabel) => {
    const rows = [];
    const elements = [...document.querySelectorAll(options.serviceItemSelector)].filter(visible);
    for (const el of elements) {
      const fiberKey = Object.keys(el).find((key) => key.startsWith("__reactFiber"));
      let fiber = fiberKey ? el[fiberKey] : null;
      for (let i = 0; fiber && i < 14; i += 1, fiber = fiber.return) {
        const props = fiber.memoizedProps;
        if (props && Array.isArray(props.items) && props.title) {
          rows.push(...flatten(props.items, tabLabel, props.title));
          break;
        }
      }
    }
    return rows;
  };
  return (async () => {
    const all = [];
    const tabs = [...document.querySelectorAll(options.tabSelector)];
    const labels = options.tabLabels?.length ? options.tabLabels : [null];
    for (const tabLabel of labels) {
      if (tabLabel) {
        const tab = tabs.find((item) => (item.innerText || "").trim() === tabLabel);
        if (tab) {
          tab.click();
          await sleep(1000);
        }
      }
      all.push(...collectActive(tabLabel || "default"));
    }
    const deduped = [];
    const seen = new Set();
    for (const row of all) {
      if (!seen.has(row.url)) {
        seen.add(row.url);
        deduped.push(row);
      }
    }
    return deduped;
  })();
}

async function collectReactSeeds(page) {
  if (!config.collectReactSeeds) return [];
  console.log("Collecting React service-list seeds...");
  await navigate(page, config.startUrl);
  const options = {
    origin: config.startOrigin,
    scopePrefixes: config.scopePrefixes,
    tabLabels: config.tabLabels,
    serviceItemSelector: config.serviceItemSelector,
    tabSelector: config.tabSelector,
  };
  const rows = await evaluate(page, `(${browserExtractReactSeeds.toString()})(${JSON.stringify(options)})`);
  const counts = rows.reduce((acc, row) => {
    acc[row.tab] = (acc[row.tab] || 0) + 1;
    return acc;
  }, {});
  for (const [label, count] of Object.entries(counts)) {
    console.log(`  tab=${label} seeds=${count}`);
  }
  return rows.map((row) => row.url);
}

function browserExtract(options) {
  const absolute = (value) => {
    try {
      return new URL(value, location.href).toString();
    } catch {
      return value || "";
    }
  };
  const inScope = (rawUrl) => {
    try {
      const url = new URL(rawUrl, location.href);
      return (
        url.origin === options.origin &&
        options.scopePrefixes.some((prefix) => url.pathname.startsWith(prefix)) &&
        !url.pathname.includes("/api/")
      );
    } catch {
      return false;
    }
  };
  const cleanText = (value) => (value || "").replace(/\s+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
  const inline = (node) => {
    if (!node) return "";
    if (node.nodeType === Node.TEXT_NODE) return node.nodeValue.replace(/\s+/g, " ");
    if (node.nodeType !== Node.ELEMENT_NODE) return "";
    const tag = node.tagName.toLowerCase();
    if (tag === "br") return "  \n";
    if (tag === "code") return "`" + node.textContent.replace(/\s+/g, " ").trim().replace(/`/g, "\\`") + "`";
    if (tag === "strong" || tag === "b") return "**" + [...node.childNodes].map(inline).join("").trim() + "**";
    if (tag === "em" || tag === "i") return "*" + [...node.childNodes].map(inline).join("").trim() + "*";
    if (tag === "a") {
      const label = [...node.childNodes].map(inline).join("").trim() || node.getAttribute("href") || "";
      const href = absolute(node.getAttribute("href") || "");
      return href ? "[" + label + "](" + href + ")" : label;
    }
    if (tag === "img") {
      const alt = node.getAttribute("alt") || "";
      const src = absolute(node.getAttribute("src") || "");
      return src ? "![" + alt.replace(/[\[\]]/g, "") + "](" + src + ")" : "";
    }
    return [...node.childNodes].map(inline).join("");
  };
  const blockChildren = (node) => [...node.childNodes].map((child) => block(child)).join("");
  const block = (node) => {
    if (!node) return "";
    if (node.nodeType === Node.TEXT_NODE) return node.nodeValue.trim() ? node.nodeValue.trim() + "\n\n" : "";
    if (node.nodeType !== Node.ELEMENT_NODE) return "";
    const tag = node.tagName.toLowerCase();
    if (["script", "style", "noscript", "svg", "button"].includes(tag)) return "";
    if (tag.match(/^h[1-6]$/)) return "#".repeat(Number(tag[1])) + " " + inline(node).trim() + "\n\n";
    if (tag === "p") return inline(node).trim() ? inline(node).trim() + "\n\n" : "";
    if (tag === "pre") return "```\n" + node.innerText.replace(/\n+$/, "") + "\n```\n\n";
    if (tag === "blockquote") {
      return blockChildren(node)
        .trim()
        .split("\n")
        .map((line) => (line ? "> " + line : ">"))
        .join("\n") + "\n\n";
    }
    if (tag === "ul" || tag === "ol") {
      return [...node.children]
        .filter((child) => child.tagName.toLowerCase() === "li")
        .map((li, index) => {
          const marker = tag === "ol" ? `${index + 1}. ` : "- ";
          const text = blockChildren(li)
            .trim()
            .replace(/\n\n/g, "\n")
            .split("\n")
            .map((line, i) => (i === 0 ? line : "  " + line))
            .join("\n");
          return marker + text;
        })
        .join("\n") + "\n\n";
    }
    if (tag === "table") {
      const rows = [...node.querySelectorAll("tr")].map((tr) =>
        [...tr.children].map((cell) => inline(cell).replace(/\|/g, "\\|").trim())
      );
      if (!rows.length) return "";
      const width = Math.max(...rows.map((row) => row.length));
      const padded = rows.map((row) => Array.from({ length: width }, (_, i) => row[i] || ""));
      const header = padded[0];
      const sep = Array.from({ length: width }, () => "---");
      return [header, sep, ...padded.slice(1)].map((row) => "| " + row.join(" | ") + " |").join("\n") + "\n\n";
    }
    if (tag === "details") {
      const summary = node.querySelector(":scope > summary");
      const title = summary ? inline(summary).trim() : "Details";
      const clone = node.cloneNode(true);
      clone.querySelector(":scope > summary")?.remove();
      return "### " + title + "\n\n" + blockChildren(clone);
    }
    if (tag === "img") return inline(node) + "\n\n";
    return blockChildren(node);
  };

  const sourceRoot =
    document.querySelector("main article .theme-doc-markdown") ||
    document.querySelector("main article") ||
    document.querySelector("article") ||
    document.querySelector("main") ||
    document.body;
  const clone = sourceRoot.cloneNode(true);
  clone
    .querySelectorAll("script, style, noscript, button, .theme-edit-this-page, .pagination-nav, nav, aside")
    .forEach((node) => node.remove());
  clone.querySelectorAll("[href]").forEach((node) => node.setAttribute("href", absolute(node.getAttribute("href"))));
  clone.querySelectorAll("[src]").forEach((node) => node.setAttribute("src", absolute(node.getAttribute("src"))));
  clone.querySelectorAll("[srcset]").forEach((node) => {
    const srcset = node
      .getAttribute("srcset")
      .split(",")
      .map((entry) => {
        const parts = entry.trim().split(/\s+/);
        parts[0] = absolute(parts[0]);
        return parts.join(" ");
      })
      .join(", ");
    node.setAttribute("srcset", srcset);
  });

  const title =
    clone.querySelector("h1")?.innerText.trim() ||
    document.querySelector("h1")?.innerText.trim() ||
    document.title.split("|")[0].split("｜")[0].trim() ||
    location.pathname.split("/").filter(Boolean).pop() ||
    "Untitled";

  const links = [...document.querySelectorAll("a[href]")]
    .map((a) => absolute(a.getAttribute("href")))
    .filter(inScope)
    .map((href) => {
      const url = new URL(href);
      url.hash = "";
      if (url.search === "?") url.search = "";
      return url.toString();
    });

  const html = clone.innerHTML.trim();
  let markdown = block(clone).replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
  if (!markdown.startsWith("#")) markdown = "# " + title + "\n\n" + markdown;
  markdown = `<!-- source: ${location.href} -->\n\n` + markdown + "\n";

  return {
    url: location.href,
    title,
    html,
    markdown,
    textLen: cleanText(clone.innerText).length,
    links: [...new Set(links)],
  };
}

async function extract(page) {
  const options = { origin: config.startOrigin, scopePrefixes: config.scopePrefixes };
  return evaluate(page, `(${browserExtract.toString()})(${JSON.stringify(options)})`);
}

function escapeHtml(text) {
  return String(text).replace(/[<>&"]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }[c]));
}

function baseCss() {
  return `body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif;line-height:1.65;margin:0;color:#1f2933;background:#fff}
main{max-width:980px;margin:0 auto;padding:32px 24px 72px}
.source{color:#65758b;font-size:13px;border-bottom:1px solid #e5e7eb;padding-bottom:16px;margin-bottom:24px;word-break:break-all}
pre{background:#f6f8fa;border:1px solid #e5e7eb;border-radius:6px;padding:14px;overflow:auto}
code{font-family:Consolas,"SFMono-Regular",monospace}
table{border-collapse:collapse;width:100%;margin:16px 0}
th,td{border:1px solid #d7dde5;padding:8px 10px;vertical-align:top}
th{background:#f6f8fa}
img{max-width:100%;height:auto}
a{color:#0969da}`;
}

function fullHtml(page) {
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(page.title)}</title>
  <style>${baseCss()}</style>
</head>
<body>
<main>
<div class="source">Source: <a href="${page.url}">${page.url}</a></div>
${page.html}
</main>
</body>
</html>
`;
}

async function prepareOutput() {
  if (config.clean) {
    await fs.rm(config.outputDir, { recursive: true, force: true });
  } else {
    const existing = await fs.readdir(config.outputDir).catch(() => []);
    if (existing.length) {
      throw new Error(`Output directory is not empty. Use --clean or choose a new directory: ${config.outputDir}`);
    }
  }
  await fs.mkdir(path.join(config.outputDir, "html"), { recursive: true });
  await fs.mkdir(path.join(config.outputDir, "md"), { recursive: true });
}

async function writeIndexes(pages) {
  const publicPages = pages.map(({ html, markdown, ...rest }) => rest);
  const okPages = pages.filter((item) => !item.error);
  const failedPages = pages.filter((item) => item.error);
  const indexMd = [
    "# Browser Doc Crawl Index",
    "",
    `- Start URL: ${config.startUrl}`,
    `- Scope prefixes: ${config.scopePrefixes.join(", ")}`,
    `- Pages: ${okPages.length}`,
    `- Failed: ${failedPages.length}`,
    "",
    ...pages.map((item, index) => {
      if (item.error) return `${index + 1}. ${item.url} - FAILED: ${item.error}`;
      return `${index + 1}. [${item.title}](${item.mdFile})  \n   HTML: [${item.htmlFile}](${item.htmlFile})  \n   Source: ${item.url}`;
    }),
    "",
  ].join("\n");
  await writeUtf8(path.join(config.outputDir, "index.md"), indexMd, { bom: config.markdownBom });

  const indexHtml = `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>Browser Doc Crawl Index</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif;line-height:1.6;max-width:1100px;margin:32px auto;padding:0 24px}li{margin:10px 0}.meta{color:#65758b}</style>
</head><body><h1>Browser Doc Crawl Index</h1>
<p class="meta">Start URL: ${escapeHtml(config.startUrl)}<br>Scope: ${escapeHtml(config.scopePrefixes.join(", "))}<br>Pages: ${okPages.length}, Failed: ${failedPages.length}</p>
<ol>${pages
    .map((item) =>
      item.error
        ? `<li><code>${escapeHtml(item.url)}</code> - FAILED: ${escapeHtml(item.error)}</li>`
        : `<li><a href="${item.htmlFile}">${escapeHtml(item.title)}</a><br><span class="meta"><a href="${item.mdFile}">Markdown</a> | <a href="${item.url}">Source</a></span></li>`
    )
    .join("\n")}</ol>
</body></html>
`;
  await writeUtf8(path.join(config.outputDir, "index.html"), indexHtml);

  if (config.combined) {
    const allMd = [
      "# Browser Doc Crawl Bundle",
      "",
      `- Start URL: ${config.startUrl}`,
      `- Pages: ${okPages.length}`,
      "",
      ...okPages.map((item) => `\n---\n\n<!-- file: ${item.mdFile} -->\n\n${item.markdown}`),
      "",
    ].join("\n");
    await writeUtf8(path.join(config.outputDir, "all.md"), allMd, { bom: config.markdownBom });

    const allHtml = `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Browser Doc Crawl Bundle</title><style>${baseCss()} section{border-bottom:1px solid #e5e7eb;padding-bottom:48px;margin-bottom:48px}</style></head>
<body><main><h1>Browser Doc Crawl Bundle</h1><p class="source">Source root: <a href="${config.startUrl}">${config.startUrl}</a></p>
${okPages
    .map(
      (item, index) =>
        `<section id="doc-${index + 1}"><div class="source">${index + 1}. Source: <a href="${item.url}">${item.url}</a></div>${item.html}</section>`
    )
    .join("\n")}
</main></body></html>
`;
    await writeUtf8(path.join(config.outputDir, "all.html"), allHtml);
  }

  await writeUtf8(
    path.join(config.outputDir, "manifest.json"),
    JSON.stringify({ config: { ...config, outputDir: config.outputDir }, pages: publicPages }, null, 2)
  );
}

async function main() {
  if (typeof WebSocket !== "function") {
    throw new Error("This script requires a Node.js runtime with global WebSocket support.");
  }
  await prepareOutput();
  const page = await connectPage();
  const queue = [normalizeUrl(config.startUrl), ...config.extraSeeds.map((url) => normalizeUrl(url))].filter(Boolean);
  const queued = new Set(queue);
  const visitedInputUrls = new Set();
  const savedUrls = new Set();
  const usedNames = new Set();
  const pages = [];

  try {
    const reactSeeds = await collectReactSeeds(page);
    for (const seed of reactSeeds) {
      if (seed && isInScope(seed) && !queued.has(seed)) {
        queued.add(seed);
        queue.push(seed);
      }
    }
    console.log(`Initial queue=${queue.length}`);

    while (queue.length && savedUrls.size < config.maxPages) {
      const url = queue.shift();
      if (!url || visitedInputUrls.has(url) || !isInScope(url)) continue;
      visitedInputUrls.add(url);
      console.log(`[${savedUrls.size + 1}] ${url}`);
      try {
        await navigate(page, url);
        const data = await extract(page);
        const canonicalUrl = normalizeUrl(data.url, data.url) || url;
        if (!isInScope(canonicalUrl)) {
          console.log(`    out-of-scope-final ${canonicalUrl}`);
          continue;
        }
        if (savedUrls.has(canonicalUrl)) {
          console.log(`    duplicate-final ${canonicalUrl}`);
          continue;
        }
        savedUrls.add(canonicalUrl);

        const base = uniqueFileName(fileBaseName(canonicalUrl), usedNames);
        const htmlFile = `html/${base}.html`;
        const mdFile = `md/${base}.md`;
        const encodingWarnings = collectEncodingWarnings(data);
        if (encodingWarnings.length) {
          console.warn(`    encoding-warn ${encodingWarnings.join("; ")}`);
        }
        await writeUtf8(path.join(config.outputDir, htmlFile), fullHtml(data));
        await writeUtf8(path.join(config.outputDir, mdFile), data.markdown, { bom: config.markdownBom });
        pages.push({
          title: data.title,
          url: canonicalUrl,
          htmlFile,
          mdFile,
          textLen: data.textLen,
          encodingWarnings,
          html: data.html,
          markdown: data.markdown,
        });

        for (const link of data.links) {
          const normalized = normalizeUrl(link, canonicalUrl);
          if (normalized && isInScope(normalized) && !queued.has(normalized) && !visitedInputUrls.has(normalized)) {
            queued.add(normalized);
            queue.push(normalized);
          }
        }
        console.log(`    saved ${mdFile} / ${htmlFile}; links=${data.links.length}; queue=${queue.length}`);
      } catch (error) {
        console.error(`    ERROR ${error.message}`);
        pages.push({ title: "(failed)", url, error: error.message });
      }
    }
  } finally {
    page.close();
  }

  await writeIndexes(pages);
  const ok = pages.filter((item) => !item.error).length;
  const failed = pages.filter((item) => item.error).length;
  console.log(`DONE output=${config.outputDir} pages=${ok} failed=${failed}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
