# AI Solution Factory — rules for Claude Code

This repository turns a department's AI request into a developer-ready handoff package.
It does **not** write production code. The dev team builds from `usecases/<id>/handoff/` in their own repository.
Everything is built in-house: there is no buy-vs-build step. Phase 2 chooses only from `framework/reference/tech-stack.md` and `framework/reference/component-library.md`.

Full design: `DESIGN.md`. These rules are the operative summary.

## Roles

- **The user is the product owner.** They approve gates, answer questions, and own `framework/`.
- **You (Claude Code)** interview the product owner or work from material in `inputs/`, fill templates, delegate reviews to subagents, run gate checks, and keep `usecase.yaml` current.
- **Subagents** in `.claude/agents/` are read-only reviewers. They return findings; you apply fixes.

## Phases and commands

| Phase | Command | Lead subagent | Gate |
|---|---|---|---|
| Setup | `/new-usecase <slug>` | — | — |
| 0 Intake & triage | `/intake` | requirements-analyst | G0 go / no-go / park, tier set |
| 1 Discovery & requirements | `/discover` | requirements-analyst | G1 sponsor sign-off |
| 2 Pattern & tech stack | `/stack` | solution-architect | G2 architecture review |
| 3 Solution design | `/design` | solution-architect, security-reviewer | G3 design + TRA approved |
| 4 Testing | `/test-plan` | test-engineer | G4 tests passed, pilot ready |
| 5 Pilot & operate | `/rollout` | solution-architect | G5 go-live approval |
| Any | `/gate <n>` | gate-reviewer | writes `reviews/gate-<n>.md` |
| After G3 | `/handoff` | — | — |
| Any | `/status` | — | — |

- Phases 0–3 run in order. Each phase command refuses to start until the previous gate is `passed`.
- After G3, `/handoff`, `/test-plan` and `/rollout` may run in parallel with development. G4 and G5 pass later, once the dev team has built and tested.
- Tier 1 use cases follow the fast lane in `framework/reference/risk-tiers.md` (short-form canvas, lighter threat model, fewer required artifacts). Gates still apply.

## Use case state (`usecase.yaml`)

- One folder per use case: `usecases/UC-nnn-<slug>/`. Its `usecase.yaml` is the single source of truth.
- Every skill **reads `usecase.yaml` first and updates it last**.
- It must always validate against `framework/schemas/usecase.schema.json`. Run `python3 scripts/check_gate.py --validate-only <id>` if in doubt.
- `decisions` is **append-only**. Add entries; never edit or remove existing ones.
- Only `/gate` sets a gate to `passed`, and only with a human approver name supplied by the product owner.
- `open_questions` entries have an `id` (`OQ-01`, `OQ-02`, … never reused), a `question` and an `owner`.
- In artifacts, cite open questions by ID: `OPEN: OQ-03 <short question>`. One `OPEN:` per question; don't add `OPEN:` notes for things already tracked — write `(provisional — see OQ-03)` instead.

## Common rules for every phase skill

1. Read `usecase.yaml`. Stop if the previous gate is not `passed` (except where the tier 1 fast lane allows).
2. Read everything in `inputs/` and all previous phases' outputs **before asking anything**.
3. Ask only for what is still missing, **at most 5 questions per round**.
4. Never invent facts. Anything unknown is written as `OPEN: <question>` and added to `open_questions` with an owner.
5. Copy the template from `framework/templates/`, fill every heading, delete the guidance comments, save in the phase folder. Keep the template's table columns and their names; you may add a column, never rename or drop one. Write targets as `Target: 95%` (a plain number).
6. Hand the draft to the lead subagent for review. Save its report in `reviews/`. Apply the fixes.
7. Update `usecase.yaml` (phase, decisions, open questions) and print a short summary: what was produced, open questions, next command.

## File rules

- `usecases/*/inputs/` holds department originals. **Read it, never write to it.** (Enforced by hook.)
- `framework/` changes only when the product owner explicitly asks to maintain the framework. (Enforced by hook; the product owner unlocks it with `touch .claude/maintain-framework` and removes the file afterwards.)
- Write use case work only inside `usecases/<id>/`.
- Scripts make no network calls and touch nothing outside the repository.
- Fix friction in skills and templates, not by hand-patching one use case's output.

## Traceability

Business requirements are numbered `BR-01…`, acceptance criteria `AC-01…`. Every BR and AC must appear in `03-design/backlog.md` (checked from G3) and in `04-testing/test-plan.md` (checked from G4).

## Data handling

If department inputs include classified material, this repository must live in an environment approved for that classification. Record the approved classification level here:

- Approved for: `TODO — set by product owner`
