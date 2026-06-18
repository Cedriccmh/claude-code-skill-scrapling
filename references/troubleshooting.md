# Scrapling 踩坑记录与解决方案

## ModuleNotFoundError: curl_cffi

**错误信息**: `ModuleNotFoundError: No module named 'curl_cffi'`
**原因**: 安装了基础包 `pip install scrapling`，不含抓取依赖
**解决方案**:
```bash
pip install "scrapling[fetchers]"
```

## Cloudflare 403 + "Just a moment"

**错误信息**: 返回 403，页面内容包含 "Just a moment" 或 "Checking your browser"
**原因**: Fetcher（curl_cffi）无法通过 Cloudflare 验证
**解决方案**: 换用 StealthyFetcher + `solve_cloudflare=True`
```python
from scrapling.fetchers import StealthyFetcher
page = StealthyFetcher.fetch(url, headless=True, solve_cloudflare=True, timeout=60000)
```

## cf_clearance cookie 无效

**错误信息**: 手动传入 `cf_clearance` cookie 但仍被 Cloudflare 拦截
**原因**: `cf_clearance` 绑定浏览器指纹（TLS/JA3/UA），不可跨客户端复用
**解决方案**: 不要手动传 `cf_clearance`，让 StealthyFetcher 自己通过 Cloudflare 获取

## Expected array, got object at $.cookies

**错误信息**: `Expected array, got object` at `$.cookies`
**原因**: 浏览器 Fetcher（StealthyFetcher/DynamicFetcher）cookie 必须是 `list[dict]`，不能是 `dict`
**解决方案**:
```python
# ❌ 错误
cookies = {'name': 'value'}

# ✅ 正确
cookies = [{'name': 'cookie_name', 'value': 'cookie_value', 'domain': '.site.com', 'path': '/'}]
```

## Cookie should have a url or a domain/path pair

**错误信息**: `Cookie should have a url or a domain/path pair`
**原因**: cookie dict 缺少 `domain` 和 `path` 字段
**解决方案**: 每个 cookie dict 必须包含 `domain`（以 `.` 开头）和 `path`（通常 `/`）
```python
cookies = [
    {'name': 'token', 'value': 'abc', 'domain': '.example.com', 'path': '/'},
]
```

## 404 "page is private"

**错误信息**: 返回 404，页面提示内容为私有
**原因**: Cloudflare 已通过，但目标页面需要登录态
**解决方案**: 带上登录 cookie（从浏览器手动获取）。字段模板见 `cookie-vault.md`；真实 cookie 值只能保存到本地未提交的 `cookie-vault.local.md`，输出时必须 redact
```python
page = StealthyFetcher.fetch(
    url,
    solve_cloudflare=True,
    cookies=[{'name': '_session', 'value': '...', 'domain': '.site.com', 'path': '/'}],
    timeout=60000,
)
```

## Cloudflare 多轮 Turnstile

**现象**: StealthyFetcher 运行时间很长（30-90 秒），日志显示多次 Turnstile 验证
**原因**: 正常现象，Cloudflare 有时需要 2-3 轮验证
**解决方案**: 耐心等待，确保 `timeout` 足够长（至少 60000ms）。如果超时失败，增加到 120000ms 重试

## scrapling: command not found

**错误信息**: `scrapling: command not found`
**原因**: Python Scripts 目录不在 PATH 中
**解决方案**:
```python
# 方式 1: 使用 python -c
python -c "from scrapling.cli import main; main(['install'])"

# 方式 2: 使用 python -m（如果支持）
python -m scrapling install
```

## StealthyFetcher/DynamicFetcher 报浏览器未安装

**错误信息**: 类似 "browser not found" 或 Playwright/Camoufox 相关错误
**原因**: 未安装浏览器依赖
**解决方案**:
```bash
# 安装 scrapling 浏览器依赖
scrapling install
# 或
python -c "from scrapling.cli import main; main(['install'])"
```
