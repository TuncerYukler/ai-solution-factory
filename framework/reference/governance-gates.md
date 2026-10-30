# Governance gates

Each gate has two checks: `scripts/check_gate.py <n>` for mechanical criteria and the **gate-reviewer** subagent for quality. Both must pass; then the product owner records the human approver(s) per `risk-tiers.md`.

| Gate | Mechanical check (`check_gate.py`) | Quality check (gate-reviewer) |
|---|---|---|
| G0 Intake | `intake.md` exists, value and feasibility scores and tier set, recommendation present | Tier justified; problem is real and measurable |
| G1 Requirements | Canvas, process map, NFRs exist; no empty sections; BRs and ACs numbered; every to-be step has actor and level | Requirements testable; HITL points sensible; no step above `autonomy_target` |
| G2 Stack | Pattern set in `usecase.yaml`; all 11 layers marked; every technology is in `tech-stack.md` | Simplest pattern that works; reuse checked |
| G3 Design | All design files exist; one agent spec per agent; golden set meets tier minimum; BR and AC traced into backlog | Buildable, consistent, threat model complete; security-reviewer has no open blockers |
| G4 Test | Test plan traces every AC; eval results file present and above accuracy NFR | Red-team results acceptable; UAT signed |
| G5 Rollout | Rollout plan has stages, thresholds, rollback, owner | Pilot results support go-live |

## Rules

- **Open blockers from any subagent review fail the gate.** A review file in `reviews/` with a row of severity `blocker` not marked `RESOLVED` is an open blocker.
- `OPEN:` items in artifacts are allowed only if the same question is in `usecase.yaml` → `open_questions` with an owner.
- G0 outcome is `go`, `no-go` or `park`. `no-go` sets status `rejected`; `park` sets status `parked`.
- A gate passes only with a named human approver. Claude never fills the approver itself.

## Evidence files for G4 and G5

- G4: `04-testing/eval-results.md` must contain a line `Accuracy: <n>%` and `UAT: signed by <name>`.
- G5: `05-rollout/pilot-results.md` summarising pilot metrics against thresholds.
