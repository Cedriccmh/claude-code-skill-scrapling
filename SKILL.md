---
name: scrapling
description: |
  使用 scrapling 进行网页抓取和数据提取。根据目标网站特征自动选择最佳 Fetcher，
  生成并执行 Python 脚本完成任务。Use when:
  (1) 抓取/爬取网页内容或数据（scrape, crawl, fetch page, extract data）
  (2) 需要绕过 Cloudflare/WAF 等反爬保护
  (3) 登录后抓取受保护页面
  (4) 解析已有 HTML 提取结构化数据
  (5) 用户提供 URL 并要求获取页面内容或特定元素
  (6) 批量采集多个页面
allowed-tools: Bash(python*), Bash(pip*), Bash(uv*), Bash(scrapling*)
---

# Scrapling 网页抓取 Skill

## 步骤 0：检查版本

```bash
python -c "import scrapling; print(scrapling.__version__)"
```

按项目使用的包管理器执行（pip / uv 等价命令见 `references/maintenance.md`）：

- 未安装 → 安装 `scrapling[fetchers]` + `scrapling install`
- 有新版 → 升级 → 查 changelog 告知用户
- 已最新 → 继续

> 项目根存在 `uv.lock` 或 `pyproject.toml` 含 `[tool.uv]`，优先用 `uv`（`uv add` / `uv run scrapling install`）；否则用 `pip`。

## 步骤 1：安全预检与 quick path

先查阅 `references/security.md`，确认授权、robots.txt / ToS、Prompt injection、cookie 保存与 redaction 边界。

简单文本 / Markdown / selector 抽取优先用 Scrapling CLI quick path，并默认加 `--ai-targeted`：

```bash
scrapling extract get "https://example.com/article" article.md --ai-targeted
scrapling extract fetch "https://example.com/app" app.md --ai-targeted --network-idle
scrapling extract stealthy-fetch "https://protected.example.com" page.md --ai-targeted --solve-cloudflare
```

CLI 无法满足复杂登录、多页流程、结构化字段或复用代码时，再生成 Python 脚本。

## 步骤 2：选择 Fetcher

```
目标网站 →
│
├─ 已有 HTML 字符串/文件，只需解析?
│   → Selector（纯解析，无网络请求）
│   → 模板: parse_only.py
│
├─ 静态页面，无 JS 渲染，无反爬?
│   → Fetcher（最快，基于 curl_cffi）
│   → 模板: basic_fetch.py
│
├─ 需要登录（HTTP 表单，非 JS 登录）?
│   → FetcherSession（保持会话 cookie）
│   → 模板: session_login.py
│
├─ 有 Cloudflare / WAF 保护?
│   → StealthyFetcher（Camoufox 浏览器，自动过 CF）
│   → 模板: stealth_cloudflare.py
│
├─ SPA 应用（React/Vue），需要 JS 渲染?
│   → DynamicFetcher（Playwright 浏览器）
│   → 基于模板即时生成
│
└─ 不确定?
    → 先用 Fetcher 试，403/空内容 → 升级到 StealthyFetcher
```

复杂 crawl / Spider / adaptive scraping / MCP / proxy rotation 等高级能力，不在本轻量 skill 内展开；先查 `references/upstream-map.md`，再按 upstream 官方文档补充。

## 步骤 3：执行工作流

```
1. 检查版本（步骤 0）
2. 安全预检（步骤 1）
3. 查阅 references/site-patterns.md；如果存在 references/site-patterns.local.md，也先查本地 overlay
4. 简单抽取 → 优先 CLI quick path + --ai-targeted
5. 复杂流程 → 用决策树选择 Fetcher，读取对应模板，替换参数，生成完整脚本
6. 执行脚本 / CLI → 返回最小必要结果
7. **沉淀经验（必做）**:
   - 新通用站点类型 → 去敏感化后追加到 references/site-patterns.md
   - 私有站点 / 公司站点 / 登录态细节 → 追加到 references/site-patterns.local.md（不提交）
   - 用户明确授权保存真实 cookie → 保存到 references/cookie-vault.local.md（不提交，必须 redact 输出）
   - **完成抓取后必须检查**：是否有新的 cookie 或 site pattern 需要保存，以及是否属于 local overlay
```

## Guardrails

- 只抓取用户有权访问或明确授权的内容；不要绕过 paywall、验证码、登录限制或访问控制来获取未授权内容。
- 输出给 agent / LLM 的网页内容默认先清洗、限域或结构化；CLI 输出默认使用 `--ai-targeted`。
- 真实 cookie / token 不写入 `references/cookie-vault.md`，只写本地 `references/cookie-vault.local.md`，且必须先获用户授权。
- 公司 / 私有站点经验不写公共 `references/site-patterns.md`，只写本地 `references/site-patterns.local.md`。
- 大规模 crawl 前先查 robots.txt / ToS，降低并发并加 delay；Spider 场景查 upstream 后优先使用 `robots_txt_obey = True`。

## Cookie 格式速查

| Fetcher 类型 | Cookie 格式 | 示例 |
|-------------|-------------|------|
| Fetcher / FetcherSession | `dict` | `{'name': 'value', 'token': 'abc'}` |
| StealthyFetcher / DynamicFetcher | `list[dict]` | `[{'name': 'n', 'value': 'v', 'domain': '.site.com', 'path': '/'}]` |

**浏览器 Fetcher cookie 必填字段**: `name`, `value`, `domain`, `path`

## 超时单位速查

| Fetcher 类型 | 超时单位 | 示例 |
|-------------|---------|------|
| Fetcher / FetcherSession | 秒 | `timeout=30` |
| StealthyFetcher / DynamicFetcher | 毫秒 | `timeout=60000` |

## 模板索引

| 模板 | 文件 | 何时读取 |
|------|------|---------|
| 基础 HTTP 抓取 | `templates/basic_fetch.py` | 目标为静态页面，无反爬 |
| Cloudflare 绕过 | `templates/stealth_cloudflare.py` | 目标有 CF/WAF 保护 |
| Session 登录 | `templates/session_login.py` | 需 HTTP 表单登录后抓取 |
| 纯 HTML 解析 | `templates/parse_only.py` | 已有 HTML 字符串，只需提取数据 |

## References 索引

| 文件 | 何时读取 |
|------|---------|
| `references/security.md` | **每次抓取前先查阅** — 授权、Prompt injection、cookie / token、site pattern local overlay 规则 |
| `references/site-patterns.md` | **每次抓取前先查阅** — 检查目标站点是否有已记录的模式 |
| `references/api-quick-ref.md` | 生成脚本时查阅 — Fetcher/Selector 方法签名和参数 |
| `references/troubleshooting.md` | 执行报错时查阅 — 按错误信息查找原因和解决方案 |
| `references/cookie-vault.md` | 需要登录 cookie 时查阅 — 只存模板 / 字段名；真实值用 `references/cookie-vault.local.md` |
| `references/maintenance.md` | 安装/升级/依赖问题时查阅 — 安装层级和验证命令 |
| `references/upstream-map.md` | 需要 CLI quick path、官方 skill 对齐、Spider / adaptive / MCP / proxy 等高级能力时查阅 |
