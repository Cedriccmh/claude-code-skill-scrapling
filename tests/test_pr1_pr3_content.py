#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def read(rel: str) -> str:
    path = ROOT / rel
    assert path.exists(), f"missing {rel}"
    return path.read_text(encoding="utf-8")

def assert_contains(rel: str, *needles: str) -> None:
    text = read(rel)
    for needle in needles:
        assert needle in text, f"{rel} missing {needle!r}"

checks = []

def check(name):
    def deco(fn):
        checks.append((name, fn))
        return fn
    return deco

@check("security guardrails are routed from SKILL.md")
def _():
    assert_contains(
        "SKILL.md",
        "references/security.md",
        "--ai-targeted",
        "Guardrails",
        "cookie-vault.local.md",
        "site-patterns.local.md",
    )

@check("security reference documents prompt-injection, cookies, authorization")
def _():
    assert_contains(
        "references/security.md",
        "Prompt injection",
        "--ai-targeted",
        "cookie-vault.local.md",
        "明确授权",
        "robots.txt",
        "redact",
    )

@check("upstream map documents official skill relationship and sync checklist")
def _():
    assert_contains(
        "references/upstream-map.md",
        "scrapling-official",
        "D4Vinci/Scrapling",
        "agent-skill/Scrapling-Skill",
        "sync checklist",
        "CLI quick path",
        "--ai-targeted",
    )

@check("README documents local overlays and upstream alignment")
def _():
    assert_contains(
        "README.md",
        "cookie-vault.local.md",
        "site-patterns.local.md",
        "references/security.md",
        "references/upstream-map.md",
        "--ai-targeted",
    )

@check("gitignore protects local sensitive overlays")
def _():
    assert_contains(".gitignore", "**/cookie-vault.local.md", "**/site-patterns.local.md")

@check("troubleshooting points real cookies to local vault")
def _():
    text = read("references/troubleshooting.md")
    assert "cookie-vault.local.md" in text, "troubleshooting should mention cookie-vault.local.md"
    assert "参见 `cookie-vault.md`" not in text, "troubleshooting should not imply cookie-vault.md stores real values"

failures = []
for name, fn in checks:
    try:
        fn()
        print(f"PASS {name}")
    except Exception as exc:
        failures.append((name, exc))
        print(f"FAIL {name}: {exc}")

if failures:
    print(f"\n{len(failures)} checks failed")
    sys.exit(1)

print("ALL PR1/PR3 content checks passed")
