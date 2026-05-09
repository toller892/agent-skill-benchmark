# Agent Skill Code-Quality Benchmark

A/B comparison test of AI agent code-quality skills: **superpowers** and **clean-code-rules**.

## What This Is

Two code-quality agent skills tested side-by-side against a deliberately buggy Python codebase. Each test: same task → one agent WITH the skill, one WITHOUT → compare behavior, code output, and process.

## Tested Skills

| Skill | Source | Stars | Score |
|-------|--------|-------|:-----:|
| superpowers (TDD + Review + Debug) | [obra/superpowers](https://github.com/obra/superpowers) | 183k | **8.5/10** |
| clean-code-rules | [ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books) | 1.2k | **8.2/10** |

## Key Finding

Both skills **actually change agent behavior** when loaded as real SKILL.md files — not just text-injected context:

- **superpowers**: Agent goes from "write code then test" to RED-GREEN-REFACTOR. Adds security scanning and `[verified]` commit messages.
- **clean-code-rules**: Agent goes from 2-helper refactor to 7 single-function decomposition. Every improvement traceable to a specific Clean Code rule.

## Methodology

- **A/B control**: Each test = two parallel sub-agents, identical task, identical codebase
- **Real skill loading**: Skills installed as `SKILL.md` files, agents call `skills_list()` → `skill_view()` to load
- **Isolated contexts**: `delegate_task` sub-agents, `/tmp` scratch copies, no context pollution

## Files

```
├── TEST_REPORT.md              # Full comparison report (pyramid structure)
├── test-fixtures/              # Planted-bug codebase used for testing
│   ├── app.py                  #   Calculator with divide bug, eval(), SQL injection
│   ├── test_app.py             #   Incomplete tests, bad naming
│   ├── config.py               #   Hardcoded secrets
│   └── utils.py                #   80-line function, magic numbers, bad names
└── skills/                     # SKILL.md that was tested
    └── clean-code-rules/
        └── SKILL.md            #   14 Clean Code rules in SKILL.md format
```

## Read the Report

[TEST_REPORT.md](TEST_REPORT.md) — Conclusion first, detailed evidence below.
