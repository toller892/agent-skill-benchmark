---
name: clean-code-rules
description: Use when refactoring code, improving readability, or reviewing code quality. Applies Robert C. Martin's Clean Code principles — small functions, meaningful names, no magic numbers, DRY, readable happy paths.
---

# Clean Code Rules

From Robert C. Martin's "Clean Code". Apply these when refactoring or reviewing.

## Decision Rules

- Treat cleanliness as part of delivery. Leave touched code cleaner within scope.
- Write for local reasoning. A reader should understand without reconstructing hidden state.
- Use precise names and one term per concept. Rename when vocabulary hides intent.
- Keep functions small, focused, and at one level of abstraction.
- Keep parameters few and meaningful. Avoid boolean flags and output parameters.
- Separate commands from queries. A function that answers should not also mutate.
- Keep the happy path readable. Isolate error handling.
- Expose behavior rather than raw representation. Avoid train-wreck access.
- Make public APIs small, explicit, and hard to misuse.
- Use comments only for rationale, constraints, warnings. Do not narrate code.
- Treat tests as production code: readable, deterministic, aligned with contract.
- Eliminate magic numbers. Replace with named constants.
- Eliminate duplicated code. Extract common patterns.
- When touching code, remove the smell that most increases change cost.

## Trigger Rules

- When a function mixes setup, validation, computation, and side effects → split phases.
- When a comment explains control flow → simplify names or structure instead.
- When duplication, repeated switches, or primitive clusters appear → name the concept.
- When magic numbers appear (like 86400, 3.14159, 0.75) → extract to named constant.
- When a function exceeds 20 lines → consider splitting at natural boundaries.
- When cleanup starts spreading → cut back to smallest safe refactor.

## Verification

After refactoring, always verify behavior is unchanged:
- Run existing tests: `python -m pytest`
- Run the original code path with sample input and compare output
- Do NOT claim success without verification evidence
