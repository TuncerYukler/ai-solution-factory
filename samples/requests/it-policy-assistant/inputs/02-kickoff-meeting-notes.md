# Kickoff notes — IT policy assistant
Date: 2026-10-24 · Attendees: Marcus Webb, Aisha Karim, Tom Fischer, product owner

## Current situation
- Service desk handles ~2,400 tickets/month. Aisha's sample of last month: 31% were
  "policy / how-to" questions answerable from existing articles.
- Average handling time for these: 9 minutes (analyst reads, finds article, replies).
- Median wait for the employee: 1.5 business days, because they sit behind incidents.
- 4 analysts; this work is the main reason the desk misses its 4-hour first-response SLA
  about 20% of the time.

## Sources
- 38 IT policies (PDF) on SharePoint, "IT Policies" library. Tom owns them.
- ~420 knowledge articles in ServiceNow KB, published to all staff.
- Policies are reviewed yearly; KB articles change weekly. Some KB articles contradict
  older policy versions — Tom says the policy wins.
- Everything is English and French; about 15% of staff ask in French.

## What they want
- Teams bot. Answer + link to source. Say "I don't know, open a ticket" with a link to
  the ServiceNow form when not confident.
- No actions: no password resets, no software installs, no ticket creation by the bot
  (for now — maybe phase 2).
- Analysts would like to see which questions it couldn't answer, to write new articles.

## Concerns raised
- Tom: it must never "invent" a policy. Wrong answers about security rules are worse than
  no answer.
- Aisha: people will paste error messages and screenshots; can it cope? (Text only is OK
  for v1.)
- Marcus: success = fewer how-to tickets. He'd be happy with a 40% reduction in that
  category in 6 months.

## Not discussed / still unknown
- How accurate does it need to be before launch?
- Who keeps the index fresh when KB articles change?
- Do we need to keep the chat logs, and for how long?
