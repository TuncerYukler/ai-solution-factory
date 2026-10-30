# RACI

R = Responsible, A = Accountable, C = Consulted, I = Informed. Adjust roles to your organization.

| Activity | Product owner | Department sponsor | Department SMEs | Architecture | Security | Dev team | Claude Code |
|---|---|---|---|---|---|---|---|
| Intake & triage (P0) | A | C | C | I | I | I | R (drafts) |
| Discovery & requirements (P1) | A | C (signs off G1) | C | I | I | I | R (drafts) |
| Pattern & tech stack (P2) | A | I | I | C (G2 review) | I | C | R (drafts) |
| Solution design (P3) | A | I | C | C | C (TRA) | C | R (drafts) |
| Handoff | A | I | I | I | I | R (builds) | R (packages) |
| Testing (P4) | A | C (UAT) | R (UAT) | I | C (red-team) | R | R (plans) |
| Pilot & operate (P5) | A | C (go-live) | C | C | C | R | R (plans) |
| Gate approval | A/R | R (tier 3, G1, G5) | — | R (tier 2+) | R (tier 3) | — | prepares checks |
| Framework maintenance | A/R | — | — | C | C | C | R (on request) |
