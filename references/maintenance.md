# Scrapling 安装与维护

## 包管理器

支持 pip 和 uv，按项目实际使用的包管理器执行命令即可。判断规则：项目根存在 `uv.lock` 或 `pyproject.toml` 含 `[tool.uv]` → 用 uv；否则用 pip。

## 安装层级

| extras | pip | uv（项目内） | 包含内容 |
|---|---|---|---|
| 核心 | `pip install scrapling` | `uv add scrapling` | 仅 Selector，无网络抓取 |
| **fetchers**（推荐） | `pip install "scrapling[fetchers]"` | `uv add "scrapling[fetchers]"` | + Fetcher/StealthyFetcher/DynamicFetcher |
| ai | `pip install "scrapling[ai]"` | `uv add "scrapling[ai]"` | + transformers |
| shell | `pip install "scrapling[shell]"` | `uv add "scrapling[shell]"` | + 交互式 shell |
| all | `pip install "scrapling[all]"` | `uv add "scrapling[all]"` | 全部功能 |

uv 全局 / 无 pyproject 场景：把 `uv add` 替换成 `uv pip install`。

**推荐**: 大多数场景使用 `scrapling[fetchers]` 即可。

## 检查安装状态

```bash
# 查看版本（跨包管理器通用）
python -c "import scrapling; print(scrapling.__version__)"

# 验证基础包可用
python -c "from scrapling.parser import Selector; print('Parser OK')"

# 验证 Fetcher 可用（需要 [fetchers]）
python -c "from scrapling.fetchers import Fetcher; print('Fetcher OK')"

# 验证 StealthyFetcher 可用
python -c "from scrapling.fetchers import StealthyFetcher; print('StealthyFetcher OK')"

# 验证 DynamicFetcher 可用
python -c "from scrapling.fetchers import DynamicFetcher; print('DynamicFetcher OK')"
```

## 安装浏览器依赖

StealthyFetcher 和 DynamicFetcher 需要浏览器引擎，安装后需执行:

```bash
# pip / 全局 Python（PATH 包含 Scripts 目录时）
scrapling install

# uv 项目内
uv run scrapling install

# 通用兜底（避免 PATH 问题）
python -c "from scrapling.cli import main; main(['install'])"
```

## 升级

```bash
# pip
pip install --upgrade "scrapling[fetchers]"

# uv（项目内）
uv lock --upgrade-package scrapling
uv sync

# uv（全局 / 无 pyproject）
uv pip install --upgrade "scrapling[fetchers]"
```

升级后建议重新验证三个 Fetcher 是否可用（见上方检查命令）。

## 三 Fetcher 完整验证脚本

```python
#!/usr/bin/env python3
"""验证 scrapling 三个 Fetcher 均可正常使用"""
import scrapling

print(f"scrapling version: {scrapling.__version__}")

# 1. Fetcher (curl_cffi)
from scrapling.fetchers import Fetcher
page = Fetcher.get("https://httpbin.org/get", impersonate='chrome', timeout=15)
print(f"Fetcher: status={page.status}")

# 2. StealthyFetcher (Camoufox)
from scrapling.fetchers import StealthyFetcher
page = StealthyFetcher.fetch("https://httpbin.org/get", headless=True, timeout=30000)
print(f"StealthyFetcher: status={page.status}")

# 3. DynamicFetcher (Playwright)
from scrapling.fetchers import DynamicFetcher
page = DynamicFetcher.fetch("https://httpbin.org/get", headless=True, timeout=30000)
print(f"DynamicFetcher: status={page.status}")

print("\nAll Fetchers verified successfully")
```
