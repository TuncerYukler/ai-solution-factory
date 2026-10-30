# Request — Invoice triage assistant (sample, Tier 2 expected)

Load with: `python3 samples/load_sample.py invoice-triage`

- Slug: `invoice-triage`
- Name: Invoice triage assistant
- Department: Finance Operations
- Sponsor: Dana Lee, Director, Accounts Payable
- SMEs: Sam Ortiz (AP Supervisor), Priya Nair (AP Clerk), Joy Chen (SAP Analyst)

Expected outcome when you run it: Tier 2, autonomy target L1, Protected B, pattern `document-processing` or `workflow-automation`.
It should reuse the SAP Read MCP Server, Approval Service, Guardrail Layer and Eval Harness from the sample component library.
One sample invoice contains an embedded instruction, so the threat model should pick up indirect prompt injection.
