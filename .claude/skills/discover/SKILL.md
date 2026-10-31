---
name: discover
description: Phase 1 discovery. Builds the use case canvas, process map with HITL points, NFRs and success metrics for the current use case.
argument-hint: "[UC-nnn]"
---

# /discover

Apply the common rules in CLAUDE.md. Use case: `$ARGUMENTS` if given, else `usecases/.active`.

1. Read `usecases/<id>/usecase.yaml`. Stop if `gates.g0_intake.status != passed`.
2. Read `usecases/<id>/inputs/` and `00-intake/intake.md`.
3. Copy `framework/templates/01-usecase-canvas.md`, `01-process-map.md`, `01-nfr.md` into `usecases/<id>/01-requirements/` as `usecase-canvas.md`, `process-map.md`, `nfr.md`. Replace `{{id}}` and `{{name}}`.
4. Fill every section from what you read. Tier 1 may use the short form (`N/A (tier 1)` where risk-tiers.md allows). List the gaps.
   - Canvas: purpose, functionality, users and personas, inputs (source, format, volume, classification), outputs (format, consumer, downstream system), business requirements numbered `BR-01…`.
   - NFRs: accuracy (`Target: nn%`), latency, volume, availability, audit and retention, privacy, languages, accessibility; success metrics with baseline and target; acceptance criteria numbered `AC-01…`.
5. If `inputs/` is too thin to fill the canvas, write `usecases/<id>/01-requirements/interview-guide.md` (questions grouped by canvas section) and tell the product owner to run the session and drop the notes in `inputs/`. Stop there.
6. Ask the product owner about the gaps, max 5 questions per round.
   Anything still unknown: write `OPEN: OQ-nn <question>` and add it to `open_questions` with the next free `id` and an owner.
7. For each to-be step, assign actor (AI / human / system) and autonomy level using `framework/reference/autonomy-levels.md`. Never exceed `autonomy_target`. Replace the example Mermaid flowchart with the real to-be flow.
8. Delegate review to the **requirements-analyst** subagent. Save its report to `reviews/phase1-review.md` and apply fixes.
9. Update `usecase.yaml`: `phase: 1`, append a decision entry, update `open_questions`. Validate with `python3 scripts/check_gate.py --validate-only <id>`.
10. Print: what was produced, open questions, next step `/gate 1` (sponsor sign-off needed).
