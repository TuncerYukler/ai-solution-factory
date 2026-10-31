# CloudLedger Inc. — SOC 2 Type II Report (excerpt)
CONFIDENTIAL — provided under NDA to Northwind Bank

Service auditor: Harlow & Finch LLP
Report on: CloudLedger Treasury Platform system
Period: **April 1, 2025 to March 31, 2026**
Trust Services Criteria: Security, Availability, Confidentiality
Report date: May 22, 2026

---

## Section 1 — Independent Service Auditor's Report (p. 3–6)

Opinion (p. 5): In our opinion, **except for the effects of the matters described in the Basis for
Qualified Opinion paragraph**, in all material respects, the controls stated in the description were
suitably designed and operated effectively throughout the period.

Basis for Qualified Opinion (p. 5): CloudLedger's description states that privileged access to production
databases is reviewed quarterly (Control CC6.3-02). Reviews were not performed for the quarters ended
September 30, 2025 and December 31, 2025. As a result, controls did not operate effectively to achieve
the criterion CC6.3 during that portion of the period.

## Section 3 — System description (p. 12–31)

3.4 Infrastructure (p. 15): The Treasury Platform runs on Amazon Web Services in regions ca-central-1
(primary) and **us-east-1 (disaster recovery and analytics workloads)**.

3.6 Subservice organisations (p. 18): CloudLedger uses the **carve-out method** for:
- Amazon Web Services (hosting)
- Okta Inc. (workforce identity)
- PayBridge Analytics Ltd. (customer usage analytics; receives transaction metadata)

Controls at these subservice organisations are not included in the scope of this report.

3.9 Complementary User Entity Controls (p. 27):
- CUEC-1: User entities are responsible for provisioning and de-provisioning their own users in the platform.
- CUEC-2: User entities are responsible for enabling SSO/MFA for their users.
- CUEC-3: User entities are responsible for reviewing their user access quarterly.

## Section 4 — Controls and test results (p. 34–118, selected rows)

| Control | Description | Test performed | Result |
|---|---|---|---|
| CC2.2-01 | Annual security awareness training for all staff | Inspected completion for 40 staff | No exceptions noted |
| CC6.1-01 | MFA enforced for all remote access to production | Inspected Okta policy and 25 logins | No exceptions noted |
| CC6.2-04 | Access of terminated employees removed within 1 business day | Inspected 25 terminations | **Exception: 3 of 25 removed after 4–9 business days** |
| CC6.3-02 | Quarterly review of privileged database access | Inspected review evidence for 4 quarters | **Exception: no review for Q3 and Q4 2025** |
| CC6.7-01 | Data encrypted at rest with AES-256 (AWS KMS) | Inspected configuration | No exceptions noted |
| CC6.7-02 | TLS 1.2+ enforced for data in transit | Inspected load balancer policy | No exceptions noted |
| CC7.1-02 | Critical vulnerabilities remediated within 30 days | Inspected 15 critical tickets | No exceptions noted |
| CC7.2-01 | Security events forwarded to SIEM, retained 13 months | Inspected SIEM configuration | No exceptions noted |
| CC7.3-01 | 24×7 monitoring by managed SOC provider | Inspected contract and alert samples | No exceptions noted |
| CC7.4-01 | Incident response plan tested annually | Inspected tabletop exercise, Nov 2025 | No exceptions noted |
| CC8.1-03 | Production changes approved by a second engineer | Inspected 40 changes | No exceptions noted |
| A1.2-02 | Backups encrypted; restore tested semi-annually | Inspected 2 restore tests | No exceptions noted |
| A1.3-01 | DR test performed annually; RTO 8 hours | Inspected DR test report, Jan 2026 | No exceptions noted |

## Management's response (p. 119)
Privileged access reviews were missed during a team reorganisation. Reviews resumed in January 2026
and have been automated in the IGA tool as of March 2026.

---

## Bridge letter (separate document, dated July 3, 2026)
Management of CloudLedger confirms that, **for the period April 1, 2026 to June 30, 2026**, there have
been no material changes to the system or controls described in the SOC 2 Type II report.
— Priya Anand, CISO, CloudLedger Inc.
