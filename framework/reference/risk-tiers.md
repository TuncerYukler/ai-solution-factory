# Risk tiers

Tier is set at intake (`/intake`) from four factors: **data sensitivity**, **decision impact**, **autonomy wanted**, and **who is affected** (staff only vs public). Take the highest tier any factor points to. Revisable at any gate, with a decision entry.

> These numbers are starting defaults. Align tier definitions and approvers with your AI governance policies before first use.

| Requirement | Tier 1 Low | Tier 2 Medium | Tier 3 High |
|---|---|---|---|
| Example | Internal summarizer, public data, L0 | Staff workflow, Protected A/B, up to L1 | Affects public or decisions about people, or L2+ |
| Use Case Canvas and NFRs | Short form | Full | Full |
| Process map with autonomy levels | Required | Required | Required |
| Tech decision records | Optional | Required | Required |
| Threat model / TRA | Lightweight checklist | Full threat model | Full TRA + formal security sign-off |
| Golden set minimum | 25 cases | 100 cases | 250 cases + edge cases |
| Red-team testing | Basic prompt-injection set | Threat-model derived | Threat-model derived + independent tester |
| Rollout stages | Assisted | Shadow then assisted | Shadow, assisted, then supervised |
| Gate approvers | Product owner | Product owner + architecture | Product owner + architecture + security + sponsor |

## Tier 1 fast lane

- Canvas and NFR short form: Purpose, Functionality, Users, Inputs, Outputs, Business requirements; NFR Accuracy, Privacy, Success metrics, Acceptance criteria. Other headings may contain `N/A (tier 1)`.
- `02-tech-decisions.md` optional.
- Threat model: the lightweight checklist section only.
- G1 and G2 may be checked together (`/gate 1` then `/gate 2` in one sitting); `/stack` may start once G1 is passed **or** while G1 is pending if the product owner says so, recorded as a decision.
