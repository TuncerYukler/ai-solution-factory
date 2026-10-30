---
name: intake
description: Phase 0 intake and triage. Scores value and feasibility, assigns the risk tier and recommends go / no-go / park for the active use case.
argument-hint: "[UC-nnn]"
---

# /intake

Apply the common rules in CLAUDE.md. Use case: `$ARGUMENTS` if given, else `usecases/.active`.

1. Read `usecases/<id>/usecase.yaml`. Stop if `status` is `rejected` or `handed_off`.
2. Read everything in `inputs/`. If it is empty, say so and offer to interview the product owner instead.
3. Copy `framework/templates/00-intake.md` to `usecases/<id>/00-intake/intake.md`. Replace `{{id}}` and `{{name}}`.
4. Fill every section from what you read: request summary, problem and pain, affected roles, volume, desired outcome. List the gaps.
5. Ask the product owner about the gaps, max 5 questions per round. Anything still unknown: write `OPEN: <question>` and add it to `open_questions` with an owner.
6. Score value (`Score: n/5`) and feasibility (`Score: n/5`: data availability, process stability, integration access), each with rationale.
7. Assign the risk tier with `framework/reference/risk-tiers.md` (data sensitivity, decision impact, autonomy wanted, who is affected; highest factor wins). Write `Tier: n` and the rationale. Confirm `data_classification` and `autonomy_target` with the product owner.
8. Write `Recommendation: go | no-go | park` and a one-paragraph rationale.
9. Delegate review to the **requirements-analyst** subagent. Save its report to `reviews/phase0-review.md` and apply fixes.
10. Update `usecase.yaml`: `phase: 0`, `risk_tier`, `autonomy_target`, `data_classification`, `open_questions`; append a decision entry (`Intake drafted: <recommendation>, tier <n>`, by: product owner). Run `python3 scripts/check_gate.py --validate-only <id>`.
11. Print: what was produced, the recommendation, open questions, next step `/gate 0`.
