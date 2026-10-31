---
name: test-plan
description: Phase 4 test planning. Writes the test plan and eval suite definition traced to every acceptance criterion. Runs after G3, in parallel with development.
argument-hint: "[UC-nnn]"
---

# /test-plan

Apply the common rules in CLAUDE.md. Use case: `$ARGUMENTS` if given, else `usecases/.active`.

1. Read `usecase.yaml`. Stop if `gates.g3_design.status != passed`.
2. Read `01-requirements/`, `02-stack/`, `03-design/`.
3. Copy `framework/templates/04-test-plan.md` to `04-testing/test-plan.md` and fill it:
   - Functional and integration tests traced to user stories, with BR / AC IDs. **Every BR-nn and AC-nn must appear.**
   - AI quality evals against the golden set: accuracy (target from `nfr.md`), hallucination rate, consistency, refusal behaviour; regression on every prompt or model change. This is the eval suite definition.
   - Red-team cases, one or more per threat ID in `threat-model.md` (tier 1: basic prompt-injection set; tier 3: name an independent tester).
   - HITL UAT scripts for department users.
   - Performance and cost tests at NFR volume and peak.
   - Pass criteria for every test type.
4. Explain to the product owner that G4 later needs `04-testing/eval-results.md` from the dev team with `Accuracy: nn%` and `UAT: signed by <name>`.
5. Ask about gaps, max 5 questions per round. Unknowns → `OPEN: OQ-nn <question>` + `open_questions` entry with that `id` and an owner.
6. Delegate review to the **test-engineer** subagent → `reviews/phase4-review.md`. Apply fixes.
7. Update `usecase.yaml`: `phase: 4`, append a decision entry. Validate.
8. Print: test counts per type, open questions, next steps (`/rollout`, then `/gate 4` once results are in).
