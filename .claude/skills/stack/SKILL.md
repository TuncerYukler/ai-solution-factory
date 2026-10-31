---
name: stack
description: Phase 2 pattern and tech stack. Picks the solution pattern and maps all 11 component layers to the approved internal stack, with reuse checked.
argument-hint: "[UC-nnn]"
---

# /stack

Apply the common rules in CLAUDE.md. Use case: `$ARGUMENTS` if given, else `usecases/.active`.

1. Read `usecase.yaml`. Stop if `gates.g1_requirements.status != passed`, unless `risk_tier` is 1 and the product owner explicitly says to start early (record that as a decision).
2. Read `01-requirements/` and `framework/reference/`: `solution-patterns.md`, `component-architecture.md`, `tech-stack.md`, `component-library.md`.
3. If `tech-stack.md` still has only TODO rows, stop and ask the product owner to fill it (it is in `framework/`, which you must not edit unless asked).
4. Pick the pattern: the **simplest** that meets the requirements. Explain why and name the runner-up.
5. Copy `framework/templates/02-component-map.md` to `02-stack/component-map.md`. Fill `Pattern: <id>`, then every one of the 11 layers: `needed` / `not needed`, technology (only from tech-stack.md), `reuse` / `extend` / `new` (check component-library.md first), owner. Draw the component diagram.
6. Tier 2+: copy `02-tech-decisions.md` to `02-stack/tech-decisions.md` and write one `TD-nn` record per non-obvious choice. Tier 1: optional.
7. Ask the product owner about gaps, max 5 questions per round. Unknowns → `OPEN: OQ-nn <question>` + `open_questions` entry with that `id` and an owner.
8. Delegate review to the **solution-architect** subagent. Save to `reviews/phase2-review.md` and apply fixes.
9. Update `usecase.yaml`: `phase: 2`, `pattern: <id>`, append a decision entry. Validate.
10. Print: pattern and runner-up, components to reuse / extend / build new, open questions, next step `/gate 2`.
