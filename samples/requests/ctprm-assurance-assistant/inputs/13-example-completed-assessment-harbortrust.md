# Cyber Third-Party Risk Assessment — HarborTrust Payroll Services
(Example of a completed report written by Chloe Bernard — use for tone and structure. Fictional.)

| Field | Value |
|---|---|
| Vendor | HarborTrust Payroll Services Ltd. |
| Service assessed | Outsourced payroll processing for Northwind employees |
| Assessment type | Periodic |
| Vendor criticality (inherent risk) | High |
| Data shared | Employee PII incl. SIN, bank account, salary (~9,800 employees) |
| Analyst | Chloe Bernard |
| Date | 2026-06-18 |
| Residual risk rating | **Medium** |
| Next review due | 2027-06-18 |

## 1. Executive summary
HarborTrust processes payroll for all Northwind employees and holds sensitive employee PII. The
SOC 2 Type II report for 2025 shows an unqualified opinion with one exception relating to delayed
leaver access removal (CTPCS IAM-03). The ISO 27001 certificate covers the payroll platform. The 2026
pen test found no open high or critical issues. Control effectiveness is assessed as **Adequate**,
giving a residual rating of **Medium**. The main actions are evidence of leaver-process remediation and
confirmation that the new Manila support centre is covered by background checks.

## 2. Scope and evidence reviewed
| Document | Period / date | Issuer | Covers service? |
|---|---|---|---|
| SOC 2 Type II | 2025-01-01 to 2025-12-31 | Clarke Doyle LLP | Yes |
| ISO 27001 certificate + SoA | Exp. 2027-03 | BSI | Yes |
| Pen test summary | 2026-02 | NCC Group | Yes |
| SIG Lite | 2026-05 | Vendor | Yes |

## 3. Key findings
1. **IAM-03 — High gap.** SOC 2 control CC6.2-03 exception: 4 of 25 leavers removed after 3–6 days (SOC 2, p. 61).
2. **HR-01 — Medium gap.** SIG E.4 states background checks for "Canadian staff"; the new Manila support centre (SOC 2 p. 14) is not addressed.

## 4. Risk observations
- Carve-out subservice organisation: Microsoft Azure (hosting). Azure SOC 2 reviewed separately — no issues.
- Concentration: HarborTrust also processes payroll for two other Northwind subsidiaries.

## 5. Recommended actions
| Action | Owner | Due | Finding |
|---|---|---|---|
| Provide evidence of automated leaver de-provisioning | Vendor | 2026-09-30 | 1 |
| Confirm background check policy for Manila staff | Vendor | 2026-08-31 | 2 |

## 6. Residual risk rating justification
Inherent risk High. One High gap (IAM-03) and one Medium gap (HR-01) → control effectiveness **Adequate**
per the rating matrix → residual **Medium**.

## 7. Analyst sign-off
Chloe Bernard, 2026-06-18 · Lead Analyst review: Raj Patel, 2026-06-20
