# Discovery workshop — C-TPRM assurance assistant
Date: 2026-10-29 · Attendees: Elena Marsh, Raj Patel, Chloe Bernard, Marcus Ito, product owner

## Volumes
- 640 vendors in scope: 48 Critical, 112 High, 290 Medium, 190 Low (Low = questionnaire only).
- ~210 full assessments/year (onboarding ~70, periodic ~120, trigger-based ~20).
- Per full assessment: document review 6–10 h, report writing 3–5 h, admin 1–2 h.
- Average 9 documents per vendor; SOC 2 Type II is present for ~60% of High/Critical.
- 12% of vendor documents are in French (Québec vendors).

## Feature 1 — document analyzer (Raj)
- Analysts read the SOC 2 system description, the control matrix, and especially the
  "exceptions noted" and complementary user entity controls (CUECs).
- Things they check every time: report period and age (> 12 months = stale), qualified
  opinion, exceptions, carve-out subservice orgs, bridge letter coverage, ISO certificate
  scope vs. the service we buy, pen test date and open high/critical findings.
- Mapping is to CTPCS (see 03-ctpcs-control-standard.md); 42 controls in 9 domains.
- Analysts disagree on mapping maybe 1 in 10 controls today — Raj wants AI to be at least
  as consistent as a senior analyst.
- Must show *where* in the document each claim came from (page/section). Raj: "if I can't
  click through to the evidence, I can't sign it".

## Feature 2 — report drafting (Chloe)
- Template is fixed (see 05-assessment-report-template.md).
- Inputs: analyzer output, the bank's inherent risk questionnaire (filled by the business
  owner), business impact info (data shared, criticality, substitutability).
- Rating: Inherent risk × control effectiveness → residual rating (Low/Medium/High/Critical)
  per 04-current-assessment-process.md. Analyst decides; AI drafts justification.
- Chloe: reports must not sound generic. Findings must cite specific evidence.

## Feature 3 — continuous monitoring (Marcus)
- Vendor inventory lives in Archer (GRC). Export sample: 07-vendor-inventory.csv.
- Event sources: threat-intel news feed (vendor mentions), regulator enforcement lists,
  vendor breach notifications to the procurement mailbox. Sample: 08-vendor-events-feed.json.
- Wanted: automatic review task in Archer when something triggers, email/Teams to the
  assigned analyst, and a "review package" (latest docs, last assessment, what changed).
- Marcus: Archer has a REST API; whether we may *write* to it from an AI service needs
  approval from the Archer platform team. OPEN.
- Elena wants task creation automatic (no human click). Raj worried about noise from
  false-positive news matches (common vendor names like "Summit").

## Constraints
- Confidential vendor documents must not leave the bank's tenant; NDA terms forbid
  sharing with third parties (check that the model hosting is in-tenant).
- Retention: assessment records 7 years (Records Policy RP-4).
- Model risk: Elena says Model Risk Management will want to review anything that
  influences a risk rating.

## Not settled
- Accuracy target before analysts can rely on the mapping.
- Who signs off when AI and analyst disagree on a gap.
- Whether Low-tier vendors are in scope for v1.
- Can the agent create Archer tasks itself, or only propose them?
