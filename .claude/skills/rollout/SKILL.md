---
name: rollout
description: Phase 5 pilot and operate. Writes the staged rollout plan with monitoring thresholds, rollback, support and ownership. Runs after G3.
argument-hint: "[UC-nnn]"
---

# /rollout

Apply the common rules in CLAUDE.md. Use case: `$ARGUMENTS` if given, else `usecases/.active`.

1. Read `usecase.yaml`. Stop if `gates.g3_design.status != passed`.
2. Read phases 1–4 outputs and `framework/reference/risk-tiers.md`.
3. Copy `framework/templates/05-rollout-plan.md` to `05-rollout/rollout-plan.md` and fill it:
   - Stages for the tier (tier 1 assisted; tier 2 shadow → assisted; tier 3 shadow → assisted → supervised), each with entry and exit criteria and duration.
   - Monitoring: quality drift, override rate, cost per transaction, incidents, user feedback — each with a threshold, alert recipient and action.
   - Rollback plan, support model, `Owner: <name, role>` after handover, re-review date.
4. Explain that G5 later needs `05-rollout/pilot-results.md` summarising pilot metrics against thresholds.
5. Ask about gaps, max 5 questions per round. Unknowns → `OPEN: OQ-nn <question>` + `open_questions` entry with that `id` and an owner.
6. Delegate review to the **solution-architect** subagent → `reviews/phase5-review.md`. Apply fixes.
7. Update `usecase.yaml`: append a decision entry. Validate.
8. Print: stages, key thresholds, owner, open questions, next step `/gate 5` once pilot results are in.
