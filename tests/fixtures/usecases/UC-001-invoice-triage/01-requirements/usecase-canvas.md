# Use Case Canvas — UC-001 Invoice triage assistant

## Purpose
Reduce invoice triage time and misroutes in Accounts Payable.

## Functionality
- Extract supplier, amount, PO number from invoices
- Propose the routing queue
- Flag missing fields

## Users and personas
AP clerk: processes 60 invoices a day.

## Inputs
| Input | Source | Format | Volume | Classification |
|---|---|---|---|---|
| Supplier invoice | AP mailbox | PDF | 1,200/week | Protected B |

## Outputs
| Output | Format | Consumer | Downstream system |
|---|---|---|---|
| Routing proposal | JSON | AP clerk | ERP work queue |

## Business requirements
- BR-01: Propose a routing queue for every invoice.
- BR-02: Flag invoices missing a PO number.

## Out of scope
Payment approval.

## Assumptions
Invoices arrive as text-based PDFs.

## Open questions
- OPEN: Who owns exceptions over $50K? (owner: Dana Lee)
