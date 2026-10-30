---
name: new-usecase
description: Start a new AI use case. Scaffolds usecases/UC-nnn-<slug>/ with usecase.yaml and sets it as the active use case.
argument-hint: <slug>
---

# /new-usecase

1. If no slug was given in `$ARGUMENTS`, ask for a short slug (lower-case words joined by hyphens, e.g. `invoice-triage`).
2. Ask the product owner in one round: use case name, department, sponsor (name, title), SMEs. Anything they don't know yet stays `TBD`.
3. Run `python3 scripts/new_usecase.py <slug> --name "<name>" --department "<dept>" --sponsor "<sponsor>" --sme "<sme>"...` (one `--sme` per SME).
4. If it fails, show the error and stop.
5. Print:
   - the new ID and folder,
   - "Drop meeting notes, documents and sample data into `usecases/<folder>/inputs/`",
   - next step: `/intake`.
