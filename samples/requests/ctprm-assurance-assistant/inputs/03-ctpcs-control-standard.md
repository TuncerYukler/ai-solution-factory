# Northwind Bank — Cyber Third-Party Control Standard (CTPCS) v3.1 (excerpt)

Owner: Cyber Risk Governance · Effective 2026-01-15 · Classification: Internal

Applicability: "Required for" shows the minimum vendor criticality at which the control is mandatory.
Evidence sources accepted: SOC 2 Type II (period ≤ 12 months old), ISO 27001 certificate + SoA covering the contracted service, independent pen test (≤ 12 months), SIG Core/Lite, vendor policy documents.

| ID | Domain | Control requirement | Required for | Preferred evidence |
|---|---|---|---|---|
| GOV-01 | Governance | Documented information security policy, reviewed annually, approved by management | All | Policy doc, SOC 2 CC1/CC2 |
| GOV-02 | Governance | Independent assurance over security controls within the last 12 months | Medium+ | SOC 2 Type II, ISO 27001 |
| GOV-03 | Governance | Subservice organisations (fourth parties) identified and monitored | High+ | SOC 2 system description |
| IAM-01 | Identity & access | MFA for all remote and privileged access | All | SOC 2 CC6.1, pen test |
| IAM-02 | Identity & access | Privileged access reviewed at least quarterly | Medium+ | SOC 2 CC6.2/6.3 |
| IAM-03 | Identity & access | Joiner/mover/leaver access removed within 24 h of termination | Medium+ | SOC 2 CC6.2 |
| DAT-01 | Data protection | Bank data encrypted at rest (AES-256 or equivalent) | All | SOC 2 CC6.7, SIG |
| DAT-02 | Data protection | Bank data encrypted in transit (TLS 1.2+) | All | SOC 2 CC6.7, pen test |
| DAT-03 | Data protection | Bank data stored only in approved regions (Canada) | High+ | SIG, contract |
| DAT-04 | Data protection | Secure deletion of bank data at contract end, with certificate | Medium+ | SIG, policy |
| VUL-01 | Vulnerability mgmt | Critical vulnerabilities remediated within 15 days, high within 30 days | Medium+ | SOC 2 CC7.1, pen test |
| VUL-02 | Vulnerability mgmt | Independent penetration test at least annually; criticals/highs closed or risk-accepted | High+ | Pen test report |
| LOG-01 | Logging & monitoring | Security events logged centrally, retained ≥ 1 year | Medium+ | SOC 2 CC7.2 |
| LOG-02 | Logging & monitoring | 24×7 security monitoring with defined escalation | High+ | SOC 2 CC7.3, SIG |
| INC-01 | Incident response | Documented incident response plan, tested annually | All | SOC 2 CC7.4, SIG |
| INC-02 | Incident response | Bank notified of incidents affecting bank data within 24 h | All | Contract, SIG |
| BCP-01 | Resilience | Business continuity and DR plans tested annually; RTO meets bank requirement | High+ | SOC 2 A1, SIG |
| BCP-02 | Resilience | Backups encrypted, immutable copy, restore tested at least annually | High+ | SOC 2 A1.2 |
| CHG-01 | Change management | Changes to production approved, tested and segregated | Medium+ | SOC 2 CC8.1 |
| SDL-01 | Secure development | Secure SDLC with code review and SAST/DAST for bank-facing apps | High+ | SIG, pen test |
| HR-01 | People | Background checks for staff with access to bank data | Medium+ | SOC 2 CC1.4, SIG |
| HR-02 | People | Annual security awareness training | All | SOC 2 CC2.2 |

(Full standard: 42 controls in 9 domains. This excerpt covers the 22 most frequently tested.)

## Gap severity
- **Critical gap**: a required control has no evidence, or evidence shows it failing, for a Critical vendor.
- **High gap**: as above for High vendors, or an exception noted in SOC 2 against a required control.
- **Medium gap**: evidence is stale (> 12 months), partial, or scope does not clearly cover the service.
- **Low gap**: documentation weakness only.
