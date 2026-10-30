---
name: status
description: Show the portfolio table of all use cases with phase, tier, status, next gate and days in phase.
---

# /status

1. Run `python3 scripts/portfolio_status.py` and show the table as-is.
2. Below it, list in one line each: use cases marked `(INVALID)`, use cases more than 30 days in one phase, and use cases with status `blocked`.
3. For the active use case, show its open questions and the next command.
