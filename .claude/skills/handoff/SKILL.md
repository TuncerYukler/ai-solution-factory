---
name: handoff
description: Package the design for developers after G3. Builds handoff/ with README.md and a developer CLAUDE.md.
argument-hint: "[UC-nnn]"
---

# /handoff

1. Use case: `$ARGUMENTS` if given, else `usecases/.active`. Read `usecase.yaml`. Stop if `gates.g3_design.status != passed`.
2. Run `python3 scripts/build_handoff.py <id> --by "<product owner>"`.
3. Read the generated `handoff/README.md` and `handoff/CLAUDE.md`. If "What to build" is thin or a section reads oddly, improve the **template or script**, not the generated file, then re-run.
4. Print: package location, file list, open questions the dev team must know about, and the reminder that the golden set must pass before any PR to main.
5. Next steps: `/test-plan` and `/rollout` can run now, in parallel with development.
