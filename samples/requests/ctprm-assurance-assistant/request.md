# Request — C-TPRM assurance assistant (sample)

Fictional organization: **Northwind Bank**. All vendors, people and numbers are made up.

Load with `python3 samples/load_sample.py ctprm-assurance-assistant`, or create the use case in the UI and upload everything in `inputs/`.

- Slug: `ctprm-assurance-assistant`
- Name: C-TPRM assurance assistant
- Department: Cyber Third-Party Risk Management
- Sponsor: Elena Marsh, Director, Cyber Third-Party Risk
- SMEs: Raj Patel (Lead Analyst), Chloe Bernard (Senior Analyst), Marcus Ito (TPRM Platform Owner)

## Three features expected

1. **Vendor assurance document analyzer** — ingest SOC 2, ISO 27001, pen test and SIG documents, extract controls, map them to the bank's Cyber Third-Party Control Standard, highlight gaps.
2. **Assessment report drafting** — from the analysis plus questionnaire and business impact, draft the executive summary, findings, recommended actions and rating justification for the analyst to edit.
3. **Continuous assurance monitoring** — watch certificate and SOC report expiry, incidents and regulatory actions; create review tasks, notify analysts, assemble review packages.

## What the factory should surface

- Tier: probably **3**. The output informs decisions about critical vendors, and feature 3 wants the agent to create tasks on its own (L2/L3). The inputs leave this tension for `/intake` to resolve.
- Data: vendor SOC reports are "Confidential — Vendor NDA" in the bank's scheme. Map to `Protected B` in `usecase.yaml`, or change the schema labels.
- Pattern: likely `multi-agent-orchestration` or `single-agent-tools` with a document-processing step. `/stack` should question whether feature 3 needs an LLM at all for date tracking.
- Planted issues in the vendor documents: SOC 2 exceptions and an expired bridge letter, ISO certificate scope that excludes the contracted service, open high pen test findings, a SIG answer contradicting the SOC report, and a news-feed item containing an embedded instruction (indirect prompt injection).
- Deliberately open: accuracy target, who owns the rating decision, whether the bank's GRC tool can accept tasks through an API.

## Suggested answers when Claude asks

- Accuracy target: 95% control-mapping agreement with analyst on the golden set; 0 missed critical gaps.
- Rating decision owner: the assigned analyst; Lead Analyst signs off Critical vendors.
- Autonomy target: L1 for features 1–2; task creation in feature 3 at L2 (auto-created, reviewed daily).
- GRC tool: Archer, REST API available read/write for the TPRM module (owner: Marcus Ito).
- Out of scope v1: sending anything to vendors.
