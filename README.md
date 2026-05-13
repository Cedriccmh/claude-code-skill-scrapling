# Claude Code Skill: Scrapling

[English](#english) | [中文](#中文)

---

## English

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for web scraping and data extraction using [scrapling](https://github.com/D4Vinci/Scrapling).

Automatically selects the best Fetcher based on target website characteristics, generates and executes Python scripts.

### Features

- **Fetcher Decision Tree** — Auto-select between Fetcher, StealthyFetcher, DynamicFetcher, FetcherSession, or Selector
- **Cloudflare Bypass** — Built-in support for Cloudflare/WAF protected sites via StealthyFetcher (Camoufox)
- **Session Login** — HTTP form-based login with cookie persistence
- **Site Pattern Library** — Reusable patterns for common site types (Discourse, SPA, static blogs, APIs)
- **Cookie Vault** — Local storage for login cookies with per-site templates
- **Troubleshooting Guide** — Solutions for common errors indexed by error message

### Installation

#### 1. Install scrapling

Pick whichever package manager your project uses:

```bash
# pip
pip install "scrapling[fetchers]"
scrapling install  # Install browser dependencies

# uv (project)
uv add "scrapling[fetchers]"
uv run scrapling install

# uv (global / standalone, no pyproject.toml)
uv pip install "scrapling[fetchers]"
scrapling install
```

#### 2. Install this skill

Copy the skill directory to your Claude Code skills folder:

```bash
# Copy to user-level skills (available in all projects)
cp -r . ~/.claude/skills/scrapling

# Or copy to a specific project
cp -r . /path/to/project/.claude/skills/scrapling
```

### Structure

```
.
├── SKILL.md                           # Skill definition (entry point)
├── references/
│   ├── api-quick-ref.md               # Fetcher/Selector API cheat sheet
│   ├── cookie-vault.md                # Cookie storage template
│   ├── maintenance.md                 # Installation & upgrade guide
│   ├── site-patterns.md               # Site-specific scraping patterns
│   └── troubleshooting.md             # Error solutions
└── templates/
    ├── basic_fetch.py                 # Static page scraping
    ├── stealth_cloudflare.py          # Cloudflare bypass
    ├── session_login.py               # Login + multi-page scraping
    └── parse_only.py                  # HTML parsing without network
```

### Usage

Once installed, Claude Code will automatically activate this skill when you ask it to:

- Scrape or crawl a website
- Extract data from a URL
- Bypass Cloudflare protection
- Parse HTML content
- Login and scrape protected pages

#### Examples

```
> Scrape the title and content from https://example.com/blog

> Extract all product prices from this page: https://shop.example.com

> This site has Cloudflare, scrape it anyway: https://protected.example.com

> I have this HTML, extract all links from it
```

### Cookie Vault

The `references/cookie-vault.md` file is a **template**. For actual use:

1. Copy it to `cookie-vault.local.md` (or keep it in your local skill installation)
2. Fill in real cookie values from your browser's DevTools
3. **Never commit real cookie values to version control**

---

## 中文

基于 [scrapling](https://github.com/D4Vinci/Scrapling) 的 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 网页抓取技能。

根据目标网站特征自动选择最佳 Fetcher，生成并执行 Python 脚本完成抓取任务。

### 功能特性

- **Fetcher 决策树** — 自动选择 Fetcher、StealthyFetcher、DynamicFetcher、FetcherSession 或 Selector
- **Cloudflare 绕过** — 通过 StealthyFetcher (Camoufox) 内置支持 Cloudflare/WAF 防护站点
- **Session 登录** — 基于 HTTP 表单的登录，自动保持 cookie 会话
- **站点模式库** — 常见站点类型的可复用抓取模式（Discourse 论坛、SPA、静态博客、API）
- **Cookie 保险库** — 按站点模板存储登录 cookie
- **故障排查指南** — 按错误信息索引的常见问题解决方案

### 安装

#### 1. 安装 scrapling

按项目所用的包管理器选一种即可：

```bash
# pip
pip install "scrapling[fetchers]"
scrapling install  # 安装浏览器依赖

# uv（项目内）
uv add "scrapling[fetchers]"
uv run scrapling install

# uv（全局 / 独立，无 pyproject.toml）
uv pip install "scrapling[fetchers]"
scrapling install
```

#### 2. 安装此技能

将技能目录复制到 Claude Code 的 skills 文件夹：

```bash
# 复制到用户级 skills（所有项目可用）
cp -r . ~/.claude/skills/scrapling

# 或复制到特定项目
cp -r . /path/to/project/.claude/skills/scrapling
```

### 目录结构

```
.
├── SKILL.md                           # 技能定义（入口文件）
├── references/
│   ├── api-quick-ref.md               # Fetcher/Selector API 速查表
│   ├── cookie-vault.md                # Cookie 存储模板
│   ├── maintenance.md                 # 安装与升级指南
│   ├── site-patterns.md               # 站点专用抓取模式
│   └── troubleshooting.md             # 错误解决方案
└── templates/
    ├── basic_fetch.py                 # 静态页面抓取
    ├── stealth_cloudflare.py          # Cloudflare 绕过
    ├── session_login.py               # 登录 + 多页抓取
    └── parse_only.py                  # 纯 HTML 解析（无需网络）
```

### 使用方式

安装后，当你向 Claude Code 提出以下需求时，技能会自动激活：

- 抓取或爬取网站
- 从 URL 提取数据
- 绕过 Cloudflare 防护
- 解析 HTML 内容
- 登录后抓取受保护页面

#### 示例

```
> 抓取 https://example.com/blog 的标题和正文

> 提取这个页面的所有商品价格：https://shop.example.com

> 这个站点有 Cloudflare，帮我绕过抓取：https://protected.example.com

> 我有这段 HTML，提取里面所有链接
```

### Cookie 保险库

`references/cookie-vault.md` 是一个**模板文件**。实际使用时：

1. 复制为 `cookie-vault.local.md`（或在本地 skill 安装目录中保存）
2. 从浏览器 DevTools 填入真实 cookie 值
3. **切勿将真实 cookie 值提交到版本控制**

## License

MIT
