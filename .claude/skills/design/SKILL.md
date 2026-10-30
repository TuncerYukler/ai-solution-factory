---
name: design
description: Phase 3 solution design. Produces the solution architecture, agent specs, HITL design, threat model, backlog and eval golden set.
argument-hint: "[UC-nnn]"
---

# /design

Apply the common rules in CLAUDE.md. Use case: `$ARGUMENTS` if given, else `usecases/.active`.

1. Read `usecase.yaml`. Stop if `gates.g2_stack.status != passed`.
2. Read `inputs/`, `01-requirements/`, `02-stack/`, and `framework/reference/risk-tiers.md` and `autonomy-levels.md`.
3. Copy each template from `framework/templates/` into `03-design/` without the `03-` prefix, and fill it:
   - `solution-architecture.md`: context diagram, logical components, **Agents table** (one row per agent, or `None`), data flow with classification at each hop (Mermaid), integration contracts, deployment view, environments, error handling.
   - `agents/<agent-id>.md` from `03-agent-spec.md`, one per agent in the Agents table: role, goal, instructions draft, tools with least-privilege scopes, input and output schema, `Level: Ln` (never above `autonomy_target`), escalation, fallback.
   - `hitl-design.md`: one approval point per HITL action in the process map; queue fields, screen layout, SLA, reject and timeout handling, override logging.
   - `threat-model.md`: tier 1 lightweight checklist; tier 2 full threat model; tier 3 full TRA. Cover STRIDE and the AI threats listed in the template.
   - `backlog.md`: epics and user stories with acceptance criteria; each story has a `Traces:` line. **Every BR-nn and AC-nn must be traced.**
   - `eval-golden-set.csv`: real (from `inputs/`) or realistic inputs with expected outputs. Minimum 25 / 100 / 250 rows for tier 1 / 2 / 3; tier 3 includes edge cases. Mark `source` as `real` or `synthetic`. If you cannot reach the minimum from real material, generate realistic synthetic rows and tell the product owner how many are synthetic.
4. Ask the product owner about gaps, max 5 questions per round. Unknowns → `OPEN:` + `open_questions`.
5. Delegate review to the **solution-architect** subagent → `reviews/phase3-architecture-review.md`, and to the **security-reviewer** subagent → `reviews/phase3-security-review.md`. Run them in parallel. Apply fixes. When a blocker is fixed, append `RESOLVED` to that row.
6. Update `usecase.yaml`: `phase: 3`, append a decision entry. Validate.
7. Print: what was produced, agents and their autonomy levels, open blockers (if any), open questions, next step `/gate 3`.
