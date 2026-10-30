# Component reference architecture

Every component map (`02-component-map.md`) walks **all 11 layers** in this order and marks each `needed` or `not needed`. `check_gate.py` checks that all 11 appear at G2.

| # | Layer | Covers |
|---|---|---|
| 1 | Channel / UI | Where users interact (web app, Teams, email, existing system) |
| 2 | Orchestration | Workflow engine or agent framework that runs the steps |
| 3 | Models | Which LLMs, for which tasks, with fallback |
| 4 | Knowledge and retrieval | Document stores, indexing, vector search, freshness |
| 5 | Tools and integrations | MCP servers and APIs into business systems, with scopes |
| 6 | Memory and state | Case state, conversation history, retention |
| 7 | HITL workflow | Approval queues, screens, notifications, SLAs |
| 8 | Guardrails | Input and output filtering, PII handling, policy checks |
| 9 | Identity and access | User auth, agent service identities, authorization |
| 10 | Observability and evaluation | Tracing, logs, eval runs, dashboards, cost tracking |
| 11 | Hosting and environments | Runtime platform, dev/test/prod, network zones |

For each needed layer: pick the technology from `tech-stack.md`, and mark it **reuse** (exists in `component-library.md`), **extend** (exists, needs changes), or **new**.
