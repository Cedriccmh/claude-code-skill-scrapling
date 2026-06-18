# Upstream alignment map

本仓库定位为 **Claude Code 友好的轻量实战 wrapper**：保留中文决策树、常用模板、site pattern、cookie 处理和 troubleshooting；高级 API 细节以 Scrapling 官方文档 / 官方 agent skill 为 source of truth。

## Upstream source of truth

- Library repo: `D4Vinci/Scrapling`
- Official skill path: `agent-skill/Scrapling-Skill`
- Official docs path: `docs/`
- Official skill name: `scrapling-official`

不要把本仓库扩成官方文档镜像。遇到以下需求时，优先查官方 skill / docs，再把最常用结论沉淀成本仓库的短参考：

| 需求 | 本仓库入口 | Upstream 查阅位置 |
|---|---|---|
| 单页静态抓取 | `templates/basic_fetch.py` / CLI quick path | `docs/cli/extract-commands.md`, `docs/fetching/static.md` |
| Cloudflare / WAF | `templates/stealth_cloudflare.py` | `docs/fetching/stealthy.md` |
| SPA / JS rendering | `references/site-patterns.md` 的 SPA 模式 | `docs/fetching/dynamic.md` |
| 复杂 crawl / Spider | 本仓库暂只给决策提示 | `docs/spiders/*`, `agent-skill/Scrapling-Skill/references/spiders/*` |
| Adaptive scraping | 本仓库暂不展开 | `docs/parsing/adaptive.md` |
| MCP server | 本仓库暂不展开 | `docs/ai/mcp-server.md`, `agent-skill/Scrapling-Skill/references/mcp-server.md` |
| Proxy rotation / blocking | 本仓库只保留 guardrail | `docs/spiders/proxy-blocking.md` |

## CLI quick path

简单抽取文本、Markdown 或指定 selector 时，优先使用 CLI，而不是生成临时 Python：

```bash
scrapling extract get "https://example.com/article" article.md --ai-targeted
scrapling extract fetch "https://example.com/app" app.md --ai-targeted --network-idle
scrapling extract stealthy-fetch "https://protected.example.com" page.md --ai-targeted --solve-cloudflare
```

规则：

- 输出会进入 agent / LLM 上下文时，默认加 `--ai-targeted`。
- CLI 失败、需要复杂登录、多页逻辑、结构化字段或复用代码时，再切到 Python 模板。
- 大规模站内 crawl 不要手写 for-loop；查 upstream Spider 文档。

## sync checklist

每次更新 Scrapling 版本或发现当前 skill 与 upstream 行为不一致时，按以下顺序同步：

1. 查看 `D4Vinci/Scrapling` 的 release / changelog，确认最低 Python 版本、extras、CLI 参数和 fetcher 参数是否变化。
2. 对照 `agent-skill/Scrapling-Skill/SKILL.md`，确认触发词、guardrails、CLI `--ai-targeted` 要求是否变化。
3. 对照 `docs/cli/extract-commands.md`，确认 `scrapling extract` 子命令和参数是否变化。
4. 对照 `docs/fetching/{static,dynamic,stealthy}.md`，确认 timeout 单位、cookie 格式、session class、`capture_xhr`、`real_chrome` 等参数是否变化。
5. 对照 `docs/spiders/*`，确认 Spider / robots / proxy / pause-resume 相关能力是否需要新增轻量入口。
6. 更新本仓库后运行本地验证：
   ```bash
   python tests/test_pr1_pr3_content.py
   python -m py_compile templates/basic_fetch.py templates/parse_only.py templates/session_login.py templates/stealth_cloudflare.py
   python C:/Users/CedricChen/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
   ```

## Scope boundary

本仓库只承诺维护高频路径：

- CLI quick path + `--ai-targeted`
- Fetcher / StealthyFetcher / FetcherSession / Selector 基础模板
- cookie-vault 本地敏感值口径
- 可泛化 site-patterns 与 troubleshooting

以下内容不在本仓库展开为完整参考：MCP server、完整 Spider 框架、adaptive storage、proxy rotation、所有 API 参数。需要时从 upstream 查阅并在任务内按需引用。
