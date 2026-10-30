# Internal component library

Reusable components already built. `/stack` checks here before marking anything **new**. Add a row each time a delivered use case produces a reusable component.

<!-- SAMPLE DATA for the fictional organization "Northwind Public Services". -->

| Component | Layer | Description | Owner | Version | Used by |
|---|---|---|---|---|---|
| Northwind Approval Service | HITL workflow | Approval queues, review screens, SLA timers, override logging with reason codes | Platform team (Ana Ruiz) | 2.3 | Grants intake, Procurement Q&A |
| Northwind Guardrail Layer | Guardrails | PII redaction (EN/FR), prompt-injection classifier, output policy checks | Security engineering (Ken Obi) | 1.8 | All AI solutions |
| Northwind Eval Harness | Observability and evaluation | Runs golden sets against prompts/models in CI; reports accuracy, hallucination, cost | AI CoE (Mira Shah) | 1.2 | Grants intake |
| Document Ingestion Pipeline | Knowledge and retrieval | PDF/DOCX/email parsing, OCR, chunking, indexing into Azure AI Search | Data platform (Leo Park) | 3.0 | Procurement Q&A |
| SAP Read MCP Server | Tools and integrations | Read-only MCP server for vendors, POs and invoices in S/4HANA | ERP team (Joy Chen) | 1.1 | — |
