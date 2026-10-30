AI Solution Factory — Claude Code Build Design
Oct 30, 2026 · @tuncer
1. Purpose and how it works
The AI Solution Factory is a Claude Code project that turns a department's AI request into a developer-ready handoff package. It runs through six gated phases, and each phase is one slash command.
You act as product owner. Claude Code interviews you (or works from meeting notes and documents you drop in), fills the templates, runs specialist reviews through subagents, and checks each gate before the next phase opens.
Scope
	•	In: intake, requirements, solution pattern and tech stack, solution design, test planning, rollout planning, gate checks, and handoff packaging.
	•	Out: writing the production code. Your dev team builds from the handoff package, in their own repository.
	•	Everything is built in-house. There is no buy-vs-build step; Phase 2 chooses from your internal stack and shared components.
Design principles
	•	One folder per use case. All outputs for a use case live together, versioned in git.
	•	Templates over blank pages. Every phase fills a standard template, so outputs are consistent across departments.
	•	Risk tier sets the depth. Low-risk use cases take a fast lane with fewer required artifacts.
	•	Gates are checked, not assumed. A gate script and a reviewer subagent confirm the exit criteria before a phase is marked done.
	•	Reuse compounds. Each delivered use case adds to the pattern catalog and component library, so the next one is faster.
End-to-end flow
	•	A department submits a request; you run /new-usecase and /intake.
	•	/discover captures requirements with the department.
	•	/stack picks the pattern and maps components to your stack.
	•	/design produces the architecture, agent specs, HITL design, and threat model.
	•	/test-plan and /rollout produce the test and pilot plans.
	•	/gate checks each phase; /handoff packages everything for developers.

factory flow · 6 phases, 6 gates
Phases 0 to 3 run in sequence with you and the department; after G3 the handoff lets developers start while you plan testing and rollout.
2. Repository structure
One git repository holds the factory itself (framework, skills, agents, scripts) and every use case it processes.
ai-solution-factory/ ├── CLAUDE.md                      # Factory rules: role, phases, conventions, gate policy ├── .claude/ │   ├── settings.json              # Permissions, hooks │   ├── skills/                    # One skill per command (invoked as /name) │   │   ├── new-usecase/SKILL.md │   │   ├── intake/SKILL.md │   │   ├── discover/SKILL.md │   │   ├── stack/SKILL.md │   │   ├── design/SKILL.md │   │   ├── test-plan/SKILL.md │   │   ├── rollout/SKILL.md │   │   ├── gate/SKILL.md │   │   ├── handoff/SKILL.md │   │   └── status/SKILL.md │   └── agents/                    # Specialist subagents │       ├── requirements-analyst.md │       ├── solution-architect.md │       ├── security-reviewer.md │       ├── test-engineer.md │       └── gate-reviewer.md ├── framework/ │   ├── templates/                 # One markdown template per artifact │   │   ├── 00-intake.md │   │   ├── 01-usecase-canvas.md │   │   ├── 01-process-map.md │   │   ├── 01-nfr.md │   │   ├── 02-component-map.md │   │   ├── 02-tech-decisions.md │   │   ├── 03-solution-architecture.md │   │   ├── 03-agent-spec.md │   │   ├── 03-hitl-design.md │   │   ├── 03-threat-model.md │   │   ├── 03-backlog.md │   │   ├── 03-eval-golden-set.csv │   │   ├── 04-test-plan.md │   │   ├── 05-rollout-plan.md │   │   └── handoff-readme.md │   ├── reference/ │   │   ├── solution-patterns.md │   │   ├── component-architecture.md │   │   ├── tech-stack.md          # Your approved internal technologies │   │   ├── component-library.md   # Reusable internal components built so far │   │   ├── autonomy-levels.md │   │   ├── risk-tiers.md │   │   ├── governance-gates.md │   │   └── raci.md │   └── schemas/ │       └── usecase.schema.json ├── usecases/ │   └── UC-001-<slug>/ │       ├── usecase.yaml           # State: phase, tier, gates, decisions │       ├── inputs/                # Meeting notes, docs, sample data from the department │       ├── 00-intake/ │       ├── 01-requirements/ │       ├── 02-stack/ │       ├── 03-design/ │       ├── 04-testing/ │       ├── 05-rollout/ │       ├── reviews/               # Subagent review reports │       └── handoff/               # Final package for developers └── scripts/     ├── new_usecase.py             # Scaffold folder + usecase.yaml     ├── check_gate.py              # Validate required artifacts and fields     ├── build_handoff.py           # Assemble handoff/ from phase outputs     └── portfolio_status.py        # Table of all use cases and their phase
	•	framework/ changes rarely and is owned by you. usecases/ grows with every request.
	•	inputs/ is the only place department material goes. Skills read from it and never edit it.
3. Use case state model
Each use case has one usecase.yaml. It is the single source of truth for where the use case stands, and every skill reads it first and updates it last.
id: UC-001 slug: invoice-triage name: Invoice triage assistant department: Finance Operations sponsor: <name, title> smes: [<name>, <name>] product_owner: <you> created: 2026-10-30  phase: 1                     # 0-5, current phase status: in_progress          # in_progress | blocked | parked | rejected | handed_off | live  risk_tier: 2                 # 1 low | 2 medium | 3 high (set in Phase 0, revisable) autonomy_target: L1          # highest autonomy level any step will reach data_classification: Protected B pattern: null                # set in Phase 2, e.g. workflow-automation  gates:   g0_intake:       {status: passed, date: 2026-10-30, approver: <name>}   g1_requirements: {status: open}   g2_stack:        {status: open}   g3_design:       {status: open}   g4_test:         {status: open}   g5_rollout:      {status: open}  decisions:                   # append-only log   - date: 2026-10-30     decision: Approved for discovery, Tier 2     by: <name>  open_questions:   - Who owns exceptions over $50K?
	•	framework/schemas/usecase.schema.json validates this file. check_gate.py refuses to pass a gate if the file is invalid.
	•	decisions is append-only. Skills add entries; nothing removes them. This gives you an audit trail for governance reviews.
	•	data_classification should use your organization's labels (for example Unclassified, Protected A/B). Adjust the schema to match.
4. Phase-to-command workflow
Each phase maps to one command, one lead subagent, a set of templates, and a gate. Run them in order; /gate must pass before the next command will start.
Phase
Command
Lead subagent
Reads
Writes
Gate
Setup
/new-usecase <slug>
none
none
Folder scaffold, usecase.yaml
none
0 Intake & triage
/intake
requirements-analyst
inputs/
00-intake/intake.md (value, feasibility, risk tier)
G0: go / no-go / park, tier set
1 Discovery & requirements
/discover
requirements-analyst
Intake, inputs/
usecase-canvas.md, process-map.md, nfr.md
G1: sponsor sign-off on requirements
2 Pattern & tech stack
/stack
solution-architect
Phase 1, reference/
component-map.md, tech-decisions.md
G2: architecture review
3 Solution design
/design
solution-architect, security-reviewer
Phases 1-2
Architecture, agent specs, HITL design, threat model, backlog, golden set
G3: design + TRA approved
4 Testing
/test-plan
test-engineer
Phases 1-3
test-plan.md, eval suite definition
G4: tests passed, pilot readiness
5 Pilot & operate
/rollout
solution-architect
Phases 1-4
rollout-plan.md (stages, monitoring, rollback)
G5: go-live approval
Any
/gate <n>
gate-reviewer
Phase outputs, usecase.yaml
reviews/gate-<n>.md, gate status
Pass / fail with gaps
After G3
/handoff
none
All phases
handoff/ package
none
Any
/status
none
All usecase.yaml files
Portfolio table in chat
none
	•	/test-plan and /rollout can run in parallel with development, after G3. G4 and G5 are passed later, once the dev team has built and tested.
	•	/handoff runs right after G3, so developers can start while you plan testing.
5. Skill specifications
Every skill follows the same pattern: check state, gather input, fill the template, run a review, update state. Write each as .claude/skills/<name>/SKILL.md.
Common rules for all phase skills
	•	Read usecase.yaml. Refuse to run if the previous gate is not passed (unless tier 1 allows skipping, see section 7).
	•	Read everything in inputs/ and the previous phases' outputs before asking anything.
	•	Ask only for what is still missing, in batches of at most 5 questions. Mark unanswered items as OPEN: in the output, never invent them.
	•	Copy the template from framework/templates/, fill it, and save it in the phase folder.
	•	Hand the draft to the lead subagent for review; apply fixes; save the review in reviews/.
	•	Update usecase.yaml (phase, decisions, open questions) and print a short summary with next step.
/new-usecase
	•	Runs scripts/new_usecase.py <slug>: next free ID, folder scaffold, usecase.yaml with defaults.
	•	Asks for department, sponsor, and SMEs; tells you to drop material into inputs/.
/intake (Phase 0)
	•	Fills 00-intake.md: problem statement, affected roles, volume and frequency, current pain (time, errors, backlog), desired outcome.
	•	Scores value (1-5), feasibility (1-5: data availability, process stability, integration access) and assigns a risk tier using reference/risk-tiers.md.
	•	Recommends go, no-go, or park, with one-paragraph rationale.
/discover (Phase 1)
	•	Fills the Use Case Canvas: purpose, functionality, users and personas, inputs (source, format, volume, classification), outputs (format, consumer, downstream system), business requirements (numbered BR-01…).
	•	Fills the process map: as-is steps, to-be steps, and for each to-be step the actor (AI / human / system) and autonomy level from reference/autonomy-levels.md. Includes a Mermaid flowchart.
	•	Fills NFRs: accuracy target, latency, volume, availability, audit and retention, privacy, official languages, accessibility.
	•	Defines success metrics (baseline and target) and acceptance criteria that Phase 4 will test.
	•	Produces a stakeholder interview guide if inputs/ is thin, so you can run the session and come back with notes.
/stack (Phase 2)
	•	Picks a solution pattern from reference/solution-patterns.md, explaining why and noting the runner-up.
	•	Fills the component map: each layer of reference/component-architecture.md marked needed / not needed, with the chosen technology from reference/tech-stack.md.
	•	Marks each component as reuse (exists in component-library.md), extend, or new.
	•	Records each non-obvious choice in tech-decisions.md (context, options, decision, consequences).
/design (Phase 3)
	•	Solution architecture: context diagram, logical components, data flow (Mermaid), integration contracts, deployment view, environments.
	•	Agent specs: one file per agent: role, goal, instructions draft, tools with permission scope, inputs and outputs schema, autonomy level, escalation rules, failure and fallback behaviour.
	•	HITL design: approval points, queue and screen fields, SLA, what happens on reject or timeout, override logging.
	•	Threat model / TRA: security-reviewer subagent covers data flows, trust boundaries, and AI threats (prompt injection, data leakage, excessive agency, tool misuse, model output trust, supply chain).
	•	Backlog: epics and user stories with acceptance criteria, traced to BR numbers.
	•	Eval golden set: CSV of real or realistic inputs with expected outputs; minimum size set by tier.
/test-plan (Phase 4)
	•	Functional and integration tests traced to user stories.
	•	AI quality evals against the golden set: accuracy, hallucination rate, consistency, refusal behaviour; regression on each prompt or model change.
	•	Red-team cases derived from the threat model.
	•	HITL UAT scripts for department users; performance and cost test at expected volume.
/rollout (Phase 5)
	•	Staged plan: shadow → assisted → supervised autonomy, with entry and exit criteria for each stage.
	•	Monitoring: quality drift, override rate, cost per transaction, incidents, user feedback.
	•	Rollback plan, support model, ownership after handover, re-review date.
/gate <n>
	•	Runs scripts/check_gate.py <n> for required files and fields, then the gate-reviewer subagent for quality.
	•	Writes reviews/gate-<n>.md with pass / fail and a gap list. On pass, records approver name you provide and sets status.
/handoff
	•	Runs scripts/build_handoff.py: copies final design artifacts into handoff/, generates handoff/README.md (what to build, where to start, open questions, contacts) and handoff/CLAUDE.md so developers can use Claude Code on the build too.
/status
	•	Runs scripts/portfolio_status.py and shows a table: ID, name, department, phase, tier, status, next gate, days in phase.
Example skill file
--- name: discover description: Phase 1 discovery. Builds the use case canvas, process map with HITL points, NFRs and success metrics for the current use case. ---  # /discover  1. Read usecases/<id>/usecase.yaml. Stop if gates.g0_intake.status != passed. 2. Read usecases/<id>/inputs/ and 00-intake/intake.md. 3. Copy framework/templates/01-usecase-canvas.md, 01-process-map.md, 01-nfr.md    into usecases/<id>/01-requirements/. 4. Fill every section from what you read. List the gaps. 5. Ask the product owner about the gaps, max 5 questions per round.    Anything still unknown: write "OPEN: <question>" and add it to open_questions. 6. For each to-be step, assign actor and autonomy level using    framework/reference/autonomy-levels.md. Never exceed autonomy_target. 7. Delegate review to the requirements-analyst subagent.    Save its report to reviews/phase1-review.md and apply fixes. 8. Update usecase.yaml: phase: 1, append a decision entry. 9. Print: what was produced, open questions, next step (/gate 1).
6. Subagent definitions
Five subagents give each phase an independent specialist review, so drafts are not graded by the session that wrote them. Each lives in .claude/agents/<name>.md with its own instructions and a limited tool set.
Subagent
Used in
Reviews for
Tools
requirements-analyst
Phases 0-1
Completeness of canvas, testable requirements, every to-be step has an actor and autonomy level, metrics have baselines, no invented facts
Read, Grep, Glob
solution-architect
Phases 2, 3, 5
Pattern fits the problem, every component traced to a requirement, reuse checked against the library, design is buildable and consistent
Read, Grep, Glob
security-reviewer
Phase 3 (and G3)
Threat model coverage, trust boundaries, data classification handling, least-privilege tool scopes, AI-specific threats, logging and audit
Read, Grep, Glob
test-engineer
Phase 4
Every acceptance criterion and BR has a test, golden set size and coverage, red-team cases trace to threats
Read, Grep, Glob
gate-reviewer
Every /gate
Exit criteria in governance-gates.md met for the use case's tier; produces pass / fail and a gap list
Read, Grep, Glob
	•	All subagents are read-only. They return findings; the main session applies the fixes. This keeps a clear record of what was reviewed and what changed.
	•	Each returns findings in one format: severity (blocker / major / minor), location (file and section), issue, suggested fix.
Example agent file
--- name: security-reviewer description: Reviews AI solution designs for security and AI-specific threats. Use in Phase 3 and at gate 3. tools: Read, Grep, Glob ---  You are a senior security architect reviewing an AI solution design.  Read usecase.yaml, 01-requirements/, 02-stack/ and 03-design/. Check: - Data flows and trust boundaries are complete; classification is handled   at every hop. - Every agent tool has least-privilege scope and an autonomy limit   no higher than usecase.yaml autonomy_target. - Threat model covers: prompt injection (direct and indirect), sensitive   data leakage, excessive agency, tool misuse, insecure output handling,   model and supply chain risk, denial of wallet. - HITL points cannot be bypassed; overrides are logged. - Audit logging meets the retention NFR.  Return a table: severity | location | issue | suggested fix. Do not edit files.
7. Reference catalogs
These files in framework/reference/ are what make the factory consistent. The skills cite them; you maintain them.
Solution patterns (solution-patterns.md)
Pattern
Use when
Typical HITL
Copilot / assistant
Users want help drafting, summarizing, or answering inside their own work
User reviews every output
RAG knowledge assistant
Answers must come from a defined body of documents, with citations
User judges answers; feedback loop
Document processing
Structured data must be extracted or classified from documents at volume
Review of low-confidence items
Workflow automation with an LLM step
A fixed process has one or two steps needing judgment or language
Approval at decision steps
Single agent with tools
The steps vary per case and the agent must choose actions across systems
Approval before any write action
Multi-agent orchestration
Several distinct specialist tasks must be coordinated, each with own tools
Approval at hand-offs and final output
Rule of thumb for the solution-architect: choose the simplest pattern that meets the requirements. Agents only when the steps genuinely vary.
Component reference architecture (component-architecture.md)
Every component map walks these layers and marks each needed or not:
	•	Channel / UI: where users interact (web app, Teams, email, existing system).
	•	Orchestration: workflow engine or agent framework that runs the steps.
	•	Models: which LLMs, for which tasks, with fallback.
	•	Knowledge and retrieval: document stores, indexing, vector search, freshness.
	•	Tools and integrations: MCP servers and APIs into business systems, with scopes.
	•	Memory and state: case state, conversation history, retention.
	•	HITL workflow: approval queues, screens, notifications, SLAs.
	•	Guardrails: input and output filtering, PII handling, policy checks.
	•	Identity and access: user auth, agent service identities, authorization.
	•	Observability and evaluation: tracing, logs, eval runs, dashboards, cost tracking.
	•	Hosting and environments: runtime platform, dev/test/prod, network zones.
tech-stack.md lists your approved technology per layer. component-library.md lists internal components already built (for example the HITL approval service or the guardrail layer), with owner and version.
Autonomy levels (autonomy-levels.md)
Level
Name
AI does
Human does
L0
Suggest
Recommends or drafts; takes no action
Decides and acts
L1
Draft for approval
Prepares the action fully
Approves, edits, or rejects before it runs
L2
Act with review
Acts; output is reviewed after, can be reversed
Samples or reviews, reverses errors
L3
Act and notify
Acts within limits and notifies
Handles exceptions and escalations
Assigned per process step, not per solution. A single solution can have L0 and L2 steps.
Risk tiers (risk-tiers.md)
Tier is set at intake from data sensitivity, decision impact, autonomy wanted, and who is affected (staff only vs public).
Requirement
Tier 1 Low
Tier 2 Medium
Tier 3 High
Example
Internal summarizer, public data, L0
Staff workflow, Protected A/B, up to L1
Affects public or decisions about people, or L2+
Use Case Canvas and NFRs
Short form
Full
Full
Process map with autonomy levels
Required
Required
Required
Tech decision records
Optional
Required
Required
Threat model / TRA
Lightweight checklist
Full threat model
Full TRA + formal security sign-off
Golden set minimum
25 cases
100 cases
250 cases + edge cases
Red-team testing
Basic prompt-injection set
Threat-model derived
Threat-model derived + independent tester
Rollout stages
Assisted
Shadow then assisted
Shadow, assisted, then supervised
Gate approvers
You
You + architecture
You + architecture + security + sponsor
These numbers are starting defaults. Align the tier definitions and approvers with your AI governance policies before first use.
8. Templates and the handoff package
Each template is a markdown file with fixed headings and short guidance comments under each. Skills fill the headings and delete the comments.
Template
Required sections
00-intake.md
Request summary, problem and pain, affected roles, volume, desired outcome, value score, feasibility score, risk tier rationale, recommendation
01-usecase-canvas.md
Purpose, functionality, users and personas, inputs table, outputs table, business requirements (BR-nn), out of scope, assumptions, open questions
01-process-map.md
As-is steps, to-be steps table (step, actor, autonomy level, HITL action), Mermaid flowchart, exceptions and escalations
01-nfr.md
Accuracy, latency, volume, availability, audit and retention, privacy, languages, accessibility, success metrics (baseline, target), acceptance criteria (AC-nn)
02-component-map.md
Pattern chosen and why, layer table (needed, technology, reuse / extend / new, owner), component diagram
02-tech-decisions.md
One record per decision: context, options, decision, consequences
03-solution-architecture.md
Context, logical view, data flow, integration contracts, deployment view, environments, error handling
03-agent-spec.md
Role, goal, instructions draft, tools and scopes, input and output schema, autonomy level, escalation, fallback
03-hitl-design.md
Approval points, queue fields, screen layout, SLA, reject and timeout handling, override logging
03-threat-model.md
Assets, trust boundaries, data flows, threats (STRIDE + AI threats), controls, residual risk
03-backlog.md
Epics, user stories with acceptance criteria, trace to BR and AC numbers
03-eval-golden-set.csv
id, input, expected_output, category, difficulty, source
04-test-plan.md
Functional, integration, AI quality evals, red-team, UAT, performance and cost; pass criteria per type
05-rollout-plan.md
Stages with entry and exit criteria, monitoring metrics and thresholds, rollback, support, ownership, re-review date
Traceability. Every BR and AC number must appear in the backlog and the test plan. check_gate.py checks this automatically at G3 and G4.
Handoff package (handoff/)
/handoff assembles what the dev team needs and nothing they don't:
handoff/ ├── README.md             # What to build, scope, where to start, open questions, contacts ├── CLAUDE.md             # Context for developers using Claude Code on the build ├── requirements/         # Canvas, process map, NFRs (final) ├── architecture/         # Solution architecture, component map, tech decisions ├── agents/               # One spec per agent ├── hitl/                 # HITL design ├── security/             # Threat model and required controls ├── backlog.md            # Epics and stories └── evals/                # Golden set + eval suite definition
The developer CLAUDE.md tells their Claude Code session: the architecture to follow, which internal components to reuse, the autonomy limits per agent (never exceed them in code), and that the golden set must pass before any PR to main.
9. Gates, validation and hooks
Each gate has two checks: a script for the mechanical criteria and the gate-reviewer subagent for quality. Both must pass, then you record the human approver.
Gate exit criteria (governance-gates.md)
Gate
Mechanical check (check_gate.py)
Quality check (gate-reviewer)
G0 Intake
intake.md exists, scores and tier set, recommendation present
Tier justified; problem is real and measurable
G1 Requirements
Canvas, process map, NFRs exist; no empty sections; BRs and ACs numbered; every to-be step has actor and level
Requirements testable; HITL points sensible; no step above autonomy_target
G2 Stack
Pattern set in usecase.yaml; all 11 layers marked; every technology is in tech-stack.md
Simplest pattern that works; reuse checked
G3 Design
All design files exist; one agent spec per agent; golden set meets tier minimum; BR and AC traced into backlog
Buildable, consistent, threat model complete; security-reviewer has no open blockers
G4 Test
Test plan traces every AC; eval results file present and above accuracy NFR
Red-team results acceptable; UAT signed
G5 Rollout
Rollout plan has stages, thresholds, rollback, owner
Pilot results support go-live
Open blockers from any subagent review fail the gate. OPEN: items are allowed only if listed in open_questions with an owner.
check_gate.py behaviour
	•	Validates usecase.yaml against the schema.
	•	Checks required files for the gate and the tier, and that no required heading is empty.
	•	Checks traceability (BR and AC numbers) from G3 onward.
	•	Prints a pass / fail list; exit code 0 or 1 so skills and hooks can rely on it.
Hooks (.claude/settings.json)
	•	PreToolUse on Write/Edit: block any write inside usecases/*/inputs/ (department originals stay untouched) and any write to framework/ unless you are explicitly maintaining the framework.
	•	PostToolUse on Write to usecase.yaml: run schema validation so state can never go invalid.
	•	Stop hook (optional): remind you of open questions and the next command for the active use case.
Permissions
	•	Allow: Read, Glob, Grep, Write and Edit in usecases/, running the four scripts.
	•	Deny: network calls from scripts, and anything outside the repository.
	•	If department inputs include classified material, keep the repository in an environment approved for that classification, and record that in CLAUDE.md.
10. Build plan in Claude Code
Build in six steps, testing each one on a real or sample use case before moving on. Save this document as DESIGN.md in the empty repository first, so every prompt can point to it.
	•	Foundation
	•	Prompt: "Read DESIGN.md. Create the repository structure from section 2 with empty placeholder files. Write CLAUDE.md using sections 1, 3 and 4: my role as product owner, the phases, the commands, the use case state rules, and the common skill rules from section 5. Create framework/schemas/usecase.schema.json from section 3."
	•	Check: tree matches section 2; CLAUDE.md reads as clear rules, not a copy of the design.
	•	Reference catalogs
	•	Prompt: "Write the files in framework/reference/ from section 7 and section 9 (governance-gates.md). Leave tech-stack.md and component-library.md as structured tables with TODO rows for me to fill."
	•	You: fill tech-stack.md with your approved technologies per layer, and adjust risk tiers and approvers to your governance policies.
	•	Templates
	•	Prompt: "Write every template in framework/templates/ from section 8. Use the required sections as headings and add a one-line guidance comment under each. Include a Mermaid flowchart example in 01-process-map.md."
	•	Scripts
	•	Prompt: "Write the four Python scripts in scripts/ from sections 3, 8 and 9. Standard library plus PyYAML and jsonschema only. Add tests in tests/ with a sample use case fixture that passes G1 and one that fails it."
	•	Check: run the tests; run check_gate.py on both fixtures.
	•	Subagents and skills
	•	Prompt: "Write the five subagents in .claude/agents/ from section 6, then the ten skills in .claude/skills/ from section 5. Follow the example files exactly in structure. Every phase skill must apply the common rules."
	•	Then: "Configure .claude/settings.json with the hooks and permissions in section 9."
	•	Pilot run
	•	Pick one real, low-risk request. Run /new-usecase, drop notes into inputs/, then run /intake through /handoff.
	•	Fix every friction point in the skills and templates, not in the use case output. Then run a second, Tier 2 use case.
After the pilot
	•	Add each new internal component to component-library.md as it is built, so /stack reuses it next time.
	•	Review gate failures monthly; recurring gaps usually mean a template section needs better guidance.
	•	Optional later: connectors to your ticketing or wiki tools so /handoff can create the backlog and publish the package directly.
