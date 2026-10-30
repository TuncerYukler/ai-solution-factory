# Non-functional requirements — UC-001 Invoice triage assistant

## Accuracy
Target: 95%
Routing proposals correct on the golden set.

## Latency
Under 10 seconds per invoice.

## Volume
1,200 per week, 2x at month end.

## Availability
Business hours, 99%.

## Audit and retention
Keep proposals and approvals 7 years.

## Privacy
Protected B; stays in approved tenant.

## Languages
English and French.

## Accessibility
WCAG 2.1 AA.

## Success metrics
| Metric | Baseline | Target | How measured |
|---|---|---|---|
| Triage time | 6 min | 1 min | Queue timestamps |

## Acceptance criteria
- AC-01: 95% of routing proposals correct on the golden set.
- AC-02: Missing PO flagged on 100% of test invoices without one.
