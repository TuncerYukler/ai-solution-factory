---
name: gate
description: Check a governance gate (0-5) for the active use case. Runs the mechanical check script, then the gate-reviewer subagent, then records the human approver on pass.
argument-hint: <0-5> [UC-nnn]
---

# /gate <n>

Use case: second argument in `$ARGUMENTS` if given, else `usecases/.active`.

1. Run `python3 scripts/check_gate.py <n> <id>`. Show the output.
2. Delegate to the **gate-reviewer** subagent: "Gate <n> for `usecases/<folder>/`". Give it the check_gate output.
3. Write `usecases/<folder>/reviews/gate-<n>.md` with:
   - date, gate, overall result (PASS only if the script exited 0 **and** the reviewer says `VERDICT: PASS`),
   - the script output,
   - the reviewer's findings table,
   - a gap list of everything to fix, and the required approvers for this tier.
4. **On fail:** set `gates.<gate>.status: failed`, append a decision entry (`G<n> failed: <top gaps>`), and print the gap list with the command to re-run after fixing.
5. **On pass:** ask the product owner for the approver name(s) required by `framework/reference/risk-tiers.md`. Never fill an approver yourself. Then:
   - set `gates.<gate>` to `{status: passed, date: <today>, approver: <names>}`;
   - for G0 also set `outcome: go | no-go | park` from the intake recommendation (as confirmed by the product owner); `no-go` → `status: rejected`, `park` → `status: parked`;
   - for G5 set `status: live`;
   - set `phase` to `<n> + 1` (max 5) unless G0 was no-go or park;
   - append a decision entry (`G<n> passed`, by: approver).
6. Validate with `python3 scripts/check_gate.py --validate-only <id>`.
7. Print the result and the next command: G0 → `/discover`, G1 → `/stack`, G2 → `/design`, G3 → `/handoff` then `/test-plan` and `/rollout`, G4 → `/gate 5` after the pilot, G5 → done.
