# AI Solution Factory

A Claude Code project that turns a department's AI request into a developer-ready handoff package through six gated phases. Full design: [DESIGN.md](DESIGN.md). Operating rules for Claude: [CLAUDE.md](CLAUDE.md).

## Setup

```bash
pip3 install -r requirements.txt
python3 -m unittest discover tests
```

Before the first real use case, the product owner fills:

1. `framework/reference/tech-stack.md`: your approved technologies per layer (G2 fails until this is done).
2. `framework/reference/component-library.md`: internal components you already have.
3. `framework/reference/risk-tiers.md`: align tiers and approvers with your AI governance policy.
4. `framework/schemas/usecase.schema.json`: change the `data_classification` labels if yours differ.
5. `CLAUDE.md`: the data classification this environment is approved for.

`framework/` is write-protected by a hook. To edit it through Claude, run `touch .claude/maintain-framework`, then delete that file when you're done.

## Use it from the web UI

```bash
python3 ui/server.py
```

Open http://localhost:8000. From there you can create a use case or load a sample, drop department files into inputs/, run each phase with one click, answer Claude's questions in the chat panel, check gates, and read every document with its diagrams.

Each button runs Claude Code (`claude -p`) in this folder, so the skills, reviewers, hooks and permissions all apply. Claude Code must be signed in: run `claude` once in a terminal and use `/login` if asked. The UI listens only on 127.0.0.1.

## Run a use case from the terminal

Open Claude Code in this folder, then:

```
/new-usecase invoice-triage     # scaffold + set active
# drop notes/docs/samples into usecases/UC-001-invoice-triage/inputs/
/intake      →  /gate 0
/discover    →  /gate 1
/stack       →  /gate 2
/design      →  /gate 3
/handoff                         # dev team starts building
/test-plan   /rollout            # in parallel with development
/gate 4      /gate 5             # once eval and pilot results are in
/status                          # portfolio table, any time
```

## Layout

| Path | What |
|---|---|
| `.claude/skills/` | The 10 slash commands |
| `.claude/agents/` | 5 read-only reviewer subagents |
| `.claude/settings.json` | Permissions and hooks (inputs/ and framework/ protection, state validation, next-step reminder) |
| `framework/templates/` | One template per artifact |
| `framework/reference/` | Patterns, layers, stack, autonomy levels, risk tiers, gates, RACI |
| `scripts/` | `new_usecase.py`, `check_gate.py`, `build_handoff.py`, `portfolio_status.py`, plus `hooks/` |
| `tests/` | Unit tests with a fixture that passes G1 and one that fails it |
| `usecases/` | One folder per use case |
