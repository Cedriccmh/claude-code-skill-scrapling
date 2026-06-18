# Cookie 保险库模板

按站点分区记录 cookie 字段、来源和格式，供抓取时快速查找使用。

> **安全提示**: 此文件只存模板和字段名，不存真实 cookie / token。
> 真实值只能写入本地未提交文件 `cookie-vault.local.md`，且必须先获得用户明确授权。
> 输出日志、错误报告和 commit diff 中必须 redact 真实值。

---

## 示例站点 (example.com)

**最后更新**: YYYY-MM-DD
**状态**: 有效 / 可能已过期
**登录 cookie 字段**: `session_id`, `auth_token`
**Fetcher 类型**: StealthyFetcher

### Playwright 格式（StealthyFetcher/DynamicFetcher 用）

```python
cookies = [
    {'name': 'session_id', 'value': '<redacted>', 'domain': '.example.com', 'path': '/'},
    {'name': 'auth_token', 'value': '<redacted>', 'domain': '.example.com', 'path': '/'},
]
```

### 备注

- 从浏览器 DevTools > Application > Cookies 获取真实值，并写入 `cookie-vault.local.md`
- cookie 有效期取决于站点设置，过期后需重新获取

---

## 模板：添加新站点

复制以下模板，替换具体内容后追加到此文件：

```markdown
## 站点名称 (域名)

**最后更新**: YYYY-MM-DD
**状态**: 有效 / 可能已过期
**登录 cookie 字段**: `field1`, `field2`
**Fetcher 类型**: Fetcher / StealthyFetcher / DynamicFetcher

### Playwright 格式

\```python
cookies = [
    {'name': 'field1', 'value': '<redacted>', 'domain': '.example.com', 'path': '/'},
]
\```

### 备注

- 相关注意事项
- 真实值保存位置：`cookie-vault.local.md`
```
