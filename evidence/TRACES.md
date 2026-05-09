# Evidence: Sub-Agent Test Traces

## superpowers A/B Test (skill-test-9 vs skill-test-10)

### WITHOUT skill (skill-test-9)
- toolsets: ["terminal", "file"] — NO skill system access
- API calls: 12
- Diff: `evidence/superpowers/without-skill.diff` (240 lines)
- Behavior: direct implementation → add tests → commit (no TDD cycle)
- Tests: 36 (over-engineered, pytest class rewrite)
- Security scan: none
- Commit: plain message

### WITH skill (skill-test-10)
- toolsets: ["skills", "terminal", "file"] — loaded 3 skills
- API calls: 17 (5 skill-related: skills_list + 3× skill_view)
- Diff: `evidence/superpowers/with-skill.diff` (96 lines)
- Skills loaded:
  1. requesting-code-review (loaded)
  2. test-driven-development (loaded)
  3. systematic-debugging (loaded)
- Behavior: RED (write test → fail) → GREEN (minimal code → pass) → REFACTOR
- Tests: 9 (focused, TDD-aligned)
- Security scan: 4 categories (secrets/injection/eval/pickle)
- Self-review: performed
- Commit: `[verified] add modulus, fix divide-by-zero, add average, comprehensive tests`

---

## clean-code-rules A/B Test (skill-test-11 vs skill-test-12)

### WITHOUT skill (skill-test-11)
- toolsets: ["terminal", "file"] — NO skill system access
- API calls: 11
- Diff: `evidence/clean-code-rules/without-skill.diff` (142 lines)
- Helper functions extracted: 4
- Magic numbers eliminated: 8/8
- Comments: retained all narration comments (# Part 1, # Part 2, ...)
- DRY: partial
- Rule mapping: none
- Behavior verification: a few sample cases

### WITH skill (skill-test-12)
- toolsets: ["skills", "terminal", "file"] — loaded 1 skill
- API calls: 7 (2 skill-related: skills_list + skill_view)
- Diff: `evidence/clean-code-rules/with-skill.diff` (144 lines)
- Skill loaded: clean-code-rules (14 rules + 6 triggers)
- Helper functions extracted: 7 (each ≤15 lines)
- Magic numbers eliminated: 6/6
- Comments: ALL narration comments DELETED (Clean Code Rule: comments only for rationale/constraints/warnings)
- DRY: complete (mean() extracted, eliminated 3 duplications)
- Dead code: removed (avg variable never read)
- Rule mapping: 11 improvements each traced to specific Clean Code rule
- Behavior verification: 31 test cases, ALL PASSED
