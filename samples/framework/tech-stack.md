# Approved internal tech stack

Owned by the product owner. `/stack` may only choose technologies listed here; `check_gate.py` rejects a G2 component map whose technology is not in the **Technology** column.

<!-- SAMPLE DATA for the fictional organization "Northwind Public Services". Replace with your own before real use. -->

| Layer | Technology | Status | Notes / constraints |
|---|---|---|---|
| Channel / UI | Northwind Staff Portal | approved | React web app on the intranet; WCAG 2.1 AA components |
| Channel / UI | Microsoft Teams bot | approved | Staff-facing chat only; no Protected B in chat history |
| Channel / UI | Outlook add-in | pilot | Tier 1 only until security review completes |
| Orchestration | Temporal | approved | Durable workflows for fixed processes |
| Orchestration | Claude Agent SDK | approved | Agents with tools; must run behind AI Gateway |
| Models | Claude Sonnet 5.5 | approved | Default model, via AI Gateway |
| Models | Claude Haiku 5.5 | approved | High-volume classification and extraction |
| Models | Claude Opus 5.5 | approved | Complex reasoning only; cost approval above 10k calls/month |
| Knowledge and retrieval | Azure AI Search | approved | Hybrid search; Protected B index in Canada Central only |
| Knowledge and retrieval | SharePoint Online | approved | Source of policy documents |
| Tools and integrations | Northwind MCP Gateway | approved | All MCP servers registered here with scoped tokens |
| Tools and integrations | SAP S/4HANA OData API | approved | Read via MCP Gateway; writes need HITL approval |
| Tools and integrations | ServiceNow REST API | approved | |
| Memory and state | PostgreSQL 16 | approved | Case state; 7-year retention tier available |
| Memory and state | Redis | approved | Session cache only, no Protected B |
| HITL workflow | Northwind Approval Service | approved | Shared queue + screens; see component-library |
| Guardrails | Northwind Guardrail Layer | approved | PII redaction, prompt-injection filter, output policy |
| Identity and access | Microsoft Entra ID | approved | Users and agent service principals |
| Observability and evaluation | OpenTelemetry + Grafana | approved | Traces, logs, cost dashboards |
| Observability and evaluation | Northwind Eval Harness | approved | Golden-set runs in CI |
| Hosting and environments | Azure Container Apps | approved | dev / test / prod in Canada Central |
| Hosting and environments | On-prem Kubernetes | retiring | Do not use for new work |

Status values: `approved`, `pilot` (allowed for Tier 1 only), `retiring` (do not choose for new work).
