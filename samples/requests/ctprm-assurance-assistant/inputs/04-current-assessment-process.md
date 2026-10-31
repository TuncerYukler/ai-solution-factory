# Current C-TPRM assessment process (as-is)

1. **Trigger** — Procurement opens an onboarding request in Archer, or the analyst's periodic-review
   spreadsheet / calendar reminder fires, or someone forwards news about a vendor.
2. **Scoping** — Analyst reads the business owner's Inherent Risk Questionnaire (IRQ) and sets
   inherent risk (Low/Medium/High/Critical).
3. **Evidence request** — Analyst emails the vendor for SOC 2, ISO certificate + SoA, pen test summary,
   SIG. Average wait 9 business days.
4. **Document review** — Analyst reads everything, fills a CTPCS mapping spreadsheet control by control
   (6–10 h).
5. **Gap follow-up** — Questions back to the vendor by email.
6. **Rating** — Residual risk = inherent risk adjusted by control effectiveness:

   | Inherent \ Controls | Strong | Adequate | Weak |
   |---|---|---|---|
   | Critical | Medium | High | Critical |
   | High | Low | Medium | High |
   | Medium | Low | Low | Medium |
   | Low | Low | Low | Low |

   "Weak" = any Critical gap, or 3+ High gaps. "Adequate" = 1–2 High gaps or several Medium gaps.
7. **Report** — Analyst writes the report in Word from the template (3–5 h).
8. **Review & sign-off** — Lead Analyst reviews Critical/High vendors; analyst signs others.
9. **Upload** — Report and mapping uploaded to Archer; next review date typed into the spreadsheet.
10. **Follow-up** — Remediation actions tracked by email; re-review dates tracked in the spreadsheet.

Pain points: step 4 and 7 take most time; step 9–10 cause the missed reviews flagged by Internal Audit (IA-2026-014).
