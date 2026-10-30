# Autonomy levels

Assigned **per process step**, not per solution. A single solution can have L0 and L2 steps. No step may exceed `usecase.yaml` → `autonomy_target`.

| Level | Name | AI does | Human does |
|---|---|---|---|
| L0 | Suggest | Recommends or drafts; takes no action | Decides and acts |
| L1 | Draft for approval | Prepares the action fully | Approves, edits, or rejects before it runs |
| L2 | Act with review | Acts; output is reviewed after, can be reversed | Samples or reviews, reverses errors |
| L3 | Act and notify | Acts within limits and notifies | Handles exceptions and escalations |

Steps performed by a human or a deterministic system get level `n/a`.
