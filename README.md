# 代码质量 Agent Skill 对比测评报告

> 测试日期：2026-05-09
> 测试方法：A/B 对照（有 Skill vs 无 Skill），子 Agent 并行隔离，**真实本地 SKILL.md 加载**
> 测试对象：`superpowers`（TDD + Review + Debug）、`clean-code-rules`

---

## 结论

| Skill 来源 | 测试方式 | 核心增量 | 评分 | 推荐 |
|------------|:---:|----------|:----:|:----:|
| **superpowers** (TDD + Review + Debug) | 本地 SKILL.md 加载 | 流程完全改变：测试先行、安全扫描、`[verified]` commit | **8.5/10** | ★★★ 必装 |
| **clean-code-rules** | 本地 SKILL.md 加载 | 7 个单函数 → 每个 ≤15 行；每项改进可追溯 Clean Code 规则 | **8.2/10** | ★★★ 必装 |

> **insecure-defaults**（trailofbits/skills）因测试依赖模型对隐蔽漏洞的先验知识，A/B 对照在明显漏洞场景下无法产生有意义差异，**pass**。

**核心发现**：两个 Skill 都走通了完整链路——安装 SKILL.md → Agent 调用 `skills_list()` 发现 → `skill_view()` 加载 → 行为改变。superpowers 改变**工作流程**，clean-code-rules 提升**产出质量**，两者互补。

---

## 测评总分

```
┌──────────────────────────────────────────────────────────────┐
│ Skill 来源              代码质量   流程规范   安全/边界   总分 │
│                         (40%)      (35%)      (25%)           │
├──────────────────────────────────────────────────────────────┤
│ superpowers                 3.4        3.3        1.8      8.5 │
│ clean-code-rules            3.6        2.9        1.7      8.2 │
└──────────────────────────────────────────────────────────────┘
```

---

## 测试环境

### 测试库

`~/skill-test-repo` — 刻意埋雷的 Python 计算器项目

| 文件 | 埋雷内容 | 雷类型 |
|------|----------|:------:|
| `app.py` | `divide()` 除零、缺失 `multiply()`、`eval()` 用户输入、SQL 拼接 | 流程+安全 |
| `test_app.py` | 测试命名 `test1`/`test2`、缺边界测试 | 流程 |
| `config.py` | 硬编码 `API_KEY`/`DB_PASSWORD`/`JWT_SECRET` | 安全 |
| `utils.py` | 80 行单函数做 5 件事、6 处魔法数字、`do_stuff`/`tmp`/`x` | 坏味道 |

### 测试基础设施

- 每对对照分配**独立副本**（`/tmp/skill-test-{1..12}`），避免交叉污染
- 子 Agent 通过 `delegate_task` 并行启动，上下文完全隔离
- **WITH 组**: `toolsets=["skills","terminal","file"]`，Agent 自行调用 `skills_list()` + `skill_view()` 加载本地 SKILL.md
- **WITHOUT 组**: `toolsets=["terminal","file"]`，无 Skill 系统访问

---

## 详细测评

### 1. superpowers（真实本地 Skill 加载）

**来源**: Hermes 内置 `software-development` 分类，含 `test-driven-development` / `requesting-code-review` / `systematic-debugging` 三个 SKILL.md

**测试场景**: 实现 `modulus()` + 修复 `divide()` + 添加 `average()` → 跑测试 → 提交

**Skill 加载证据**:

```
WITH 组 Agent 实际执行:
  [1] skills_list()          → 132 skills found
  [2] skill_view("requesting-code-review")  → loaded
  [3] skill_view("test-driven-development") → loaded
  [4] skill_view("systematic-debugging")    → loaded
```

**行为对比**:

| 维度 | 无 Skill（toolsets=[terminal,file]） | 有 Skill（toolsets=[skills,terminal,file]） |
|------|--------------------------------------|---------------------------------------------|
| 开发流程 | 直接写实现 → 补测试 → 好了 | RED: 先写测试 → 看失败 → GREEN: 最小实现 → 通过 → REFACTOR |
| 测试数量 | 36 个（pytest class 重写，过度工程化） | 9 个（精准覆盖需求，无冗余） |
| 安全扫描 | 无 | 扫描硬编码密钥/注入/eval/pickle 四类 |
| 代码审查 | 无 | 自我审查 diff + 记录 |
| Commit | `add modulus, fix divide-by-zero, add average, test coverage` | `[verified] add modulus, fix divide-by-zero, add average, comprehensive tests` |

**硬指标**:

| 指标 | 无 Skill | 有 Skill | 差值 |
|------|:---:|:---:|:---:|
| TDD 测试先行 | ❌ | ✅ | — |
| RED-GREEN-REFACTOR 记录 | ❌ | ✅ | — |
| 安全扫描 | ❌ | ✅（4 类） | — |
| 自我审查 | ❌ | ✅ | — |
| commit 含 `[verified]` | ❌ | ✅ | — |
| API 调用数 | 12 | 17（含 5 次 Skill 相关） | +5 |

**debugging 子技能对比**（同一轮中如何修复 `divide()`）：

```python
# 无 Skill — try/except 吞异常，返回类型不一致
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None       # ← 有时 float，有时 None

# 有 Skill — 复现 → 诊断 → 精准修复
def divide(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b           # ← 始终返回 float
```

**评分**:

| 维度 | 得分 | 评语 |
|------|:---:|------|
| 代码质量 (40%) | 3.4/4 | TDD 减少过度工程化；Debug 修复类型安全 |
| 流程规范 (35%) | 3.3/3.5 | RED-GREEN-REFACTOR + 安全扫描 + `[verified]` 全链路 |
| 安全/边界 (25%) | 1.8/2.5 | 安全扫描 + 边界测试补充 |
| **总分** | **8.5/10** | |

---

### 2. clean-code-rules（真实本地 Skill 加载）

**来源**: 基于 ciembor/agent-rules-books Clean Code mini 版，制作为 SKILL.md 安装至 `~/.hermes/skills/software-development/clean-code-rules/`

**Skill 安装**: 本地写入 `SKILL.md`，含 14 条 Clean Code 决策规则 + 6 条触发器规则

**测试场景**: 重构 `utils.py`（80 行单函数 + 魔法数字 + 坏命名）

**Skill 加载证据**:

```
WITH 组 Agent 实际执行:
  [1] skills_list()          → 133 skills found
  [2] skill_view("clean-code-rules")  → loaded（含 14 条规则 + 触发器）
```

**行为对比**:

| 改进项 | 无 Skill | 有 Skill（本地加载） |
|--------|----------|----------------------|
| 函数拆分 | 拆 4 个 helper | 拆 7 个聚焦函数，每个 ≤15 行 |
| 魔法数字消除 | 8/8（全部） | 6/6（全部） |
| 命名改善 | `do_stuff`→`process_numeric_data` | `do_stuff`→`do_stuff`（保留兼容）+ 内部全改善 |
| DRY 重复消除 | 部分 | 全面（`mean()` 提取消除 3 处重复） |
| 代码注释 | 保留 | **删除所有叙事性注释**（Clean Code 规则：注释只用来说明理由/约束/警告） |
| 验证行为不变 | ✅ 几个 sample case | ✅ **31 个 test case**，逐个对比原版 |
| 规则可追溯 | ❌ | ✅ **每项改进标注 Clean Code 规则编号** |

**关键差异 — 注释处理**:

```
无 Skill:  保留 # Part 1: filter valid numbers / # Part 2: transform based on mode ...
           （用注释解释控制流 → Clean Code 规则明确禁止）

有 Skill:  删除所有叙事注释，用函数名替代
           extract_positive_numbers() / scale_numbers() / normalize_numbers()
           threshold_average() / apply_time_decay() / format_output()
           （函数名本身就是最好的注释）
```

**关键差异 — 消除重复**:

```
无 Skill:  threshold 模式、Part 3 统计、Part 5 最终计算
           → 三处独立实现均值逻辑（partial DRY）

有 Skill:  提取 mean() 函数
           → threshold_average() 调用 sum/len
           → 主流程调用 mean()
           → 单一职责，零重复
```

**关键差异 — 验证**:

```
无 Skill:  几个 sample case 验证行为不变

有 Skill:  31 个 test case，覆盖:
           所有 mode × 边界（空输入/字符串混入/负数/全零）
           → ALL 31 PASSED
```

**改进对照表（有 Skill 侧的规则映射）**:

| # | 改进 | 对应 Clean Code 规则 |
|---|------|---------------------|
| 1 | 6 个命名常量替代所有魔法数字 | Eliminate magic numbers |
| 2 | 53 行拆为 7 个 ≤15 行函数 | Keep functions small, focused, at one level of abstraction |
| 3 | `extract_positive_numbers()` 分离数据过滤 | Split phases when function mixes setup/validation/computation |
| 4 | 提取 `mean()` 消除 3 处重复 | Eliminate duplicated code |
| 5 | 删除 `avg` 死代码 | Cut back to smallest safe refactor |
| 6 | **删除所有叙事注释**（Part 1/2/3...） | Comments only for rationale, constraints, warnings |
| 7 | `x` → `base`（变量名揭示意图） | Use precise names |
| 8 | `do_stuff` 读作: filter→dispatch→decay→avg→format | Keep the happy path readable |
| 9 | for-i-in-range → list comprehension | Expose behavior rather than raw representation |
| 10 | 模块 docstring 从自嘲改为描述性 | Write for local reasoning |
| 11 | 每个函数含单句 docstring | One term per concept |

**评分**:

| 维度 | 得分 | 评语 |
|------|:---:|------|
| 代码质量 (40%) | 3.6/4 | 7 个单函数 ≤15 行；消除叙事注释 + 死代码 + 3 处重复 |
| 流程规范 (35%) | 2.9/3.5 | 每项改进可追溯 Clean Code 规则；31 case 验证 |
| 安全/边界 (25%) | 1.7/2.5 | 验证覆盖全面但无安全特定改进 |
| **总分** | **8.2/10** | |

---

## insecure-defaults — pass 说明

**来源**: trailofbits/skills，insecure-defaults 安全审计插件

**评估结论**: 此 Skill 旨在发现**隐蔽安全漏洞**（fail-open 默认值、弱加密算法误用、默认宽松权限等），而测试库中的漏洞（`eval()`、硬编码密钥、SQL 拼接）对当前 LLM 而言是**明显漏洞**。A/B 测试中两组的漏洞发现数量完全相同（8 vs 8），无法衡量 Skill 在隐蔽场景中的增量价值。

**不做评分的原因**: 需要构造更专业的测试库（含 fail-open 模式、生产环境配置默认值陷阱等）才能公平评估。这不是 Skill 的问题，是测试方法不匹配。

---

## Skill 触发机制发现

测试中发现关键行为：**Skill 不会自动生效**。

```
Agent 有 skills 工具     ≠     Agent 会加载 Skill
Agent 加载了 Skill        ≠     Agent 会严格遵循 Skill
```

**触发条件**（从多轮测试总结）：

| 条件 | 必要程度 | 说明 |
|------|:---:|------|
| toolsets 含 `skills` | 必须 | 否则 Agent 看不到 Skill 列表 |
| 任务规模足够大 | 重要 | "加一个函数"级别不会触发审查 Skill |
| 明确提示检查 Skill | 建议 | 给 Agent 一句"先检查可用的 Skill"即可触发 |
| Skill description 匹配任务 | 核心 | Agent 根据 description 判断是否加载 |

---

## 附录：测试原始数据

### 子 Agent 调用统计

| 对照对 | 测试方式 | 无 Skill 调用 | 有 Skill 调用 | Skill 相关调用 |
|--------|:---:|:---:|:---:|:---:|
| superpowers | **本地加载** | 12 | 17 | 5（skills_list + 3×skill_view） |
| clean-code-rules | **本地加载** | 11 | 7 | 2（skills_list + skill_view） |

### 测试库文件

- `/Users/tony/skill-test-repo/app.py`
- `/Users/tony/skill-test-repo/test_app.py`
- `/Users/tony/skill-test-repo/config.py`
- `/Users/tony/skill-test-repo/utils.py`

### 本地安装的 Skill

- `~/.hermes/skills/software-development/test-driven-development/SKILL.md`
- `~/.hermes/skills/software-development/requesting-code-review/SKILL.md`
- `~/.hermes/skills/software-development/systematic-debugging/SKILL.md`
- `~/.hermes/skills/software-development/clean-code-rules/SKILL.md`（本次新装）

### 测试副本

- superpowers 测试：`/tmp/skill-test-{7..10}`
- clean-code-rules 测试：`/tmp/skill-test-{11..12}`
