# Discovery workshop — Invoice triage
Date: 2026-10-22 · Attendees: Dana Lee, Sam Ortiz, Priya Nair, Joy Chen, product owner

## Today's process (Priya walked through it)
1. Invoice arrives by email (PDF, ~85%) or supplier portal (PDF/XML, ~15%).
2. Clerk opens it, keys header fields into a spreadsheet tracker.
3. Clerk looks up the PO in SAP (transaction ME23N) if there is one.
4. Clerk picks the work queue using the routing rules (see 03-routing-rules.md).
5. Clerk creates the parked invoice in SAP (MIRO) and assigns it to the queue.
6. Exceptions (no PO and > $10K, supplier not in SAP, amount differs from PO by > 5%)
   go to Sam.

## Numbers
- 1,200 invoices/week; month-end week ~2,300.
- 6 min average handling; 8% misrouted (Sam's audit of 500 invoices in August).
- ~3% of invoices are duplicates that slip through today.
- 14% of invoices are in French.
- Lost early-payment discounts: about $180K last fiscal year.

## What "good" looks like (Dana)
- Triage under 1 minute of clerk time per invoice.
- Misroutes under 2%.
- Duplicates caught before posting.
- Clerk always approves before the parked invoice is created in SAP.

## Systems
- SAP S/4HANA: Joy confirms the read-only SAP MCP server already exposes vendors, POs and
  invoice history. Creating parked invoices needs a write API — not built yet.
- Mailbox is Exchange Online.
- Retention: financial records 7 years (Finance Records Schedule FR-2).

## Concerns
- Joy: bank detail changes on invoices are a known fraud vector. Any invoice whose bank
  details differ from the SAP vendor master must go to exceptions, never auto-proposed.
- Sam: must be able to see *why* the AI chose a queue.
- Dana: must work in French too.

## Still open
- Who owns exceptions over $50K — Sam, or the Controller?
- Accuracy target for field extraction — Dana says "better than us", no number yet.
- Can the AI see expense reimbursement invoices (employee names), or should those be
  excluded from v1?
