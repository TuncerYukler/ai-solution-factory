# Sample data for testing

Fictional organization: **Northwind Public Services**. All names, numbers and suppliers are made up.

| Sample | Department | Expected tier | What it exercises |
|---|---|---|---|
| `it-policy-assistant` | IT Service Desk | 1 (L0, Unclassified) | Fast lane, RAG pattern, bilingual sources, a KB article that contradicts policy |
| `invoice-triage` | Finance Operations | 2 (L1, Protected B) | Full design, reuse from the component library, fraud rule (bank details), an invoice with an embedded prompt injection |

Both leave some questions unanswered on purpose, so `/intake` and `/discover` have something to ask you.

## Load one

```bash
python3 samples/load_sample.py it-policy-assistant
```

This fills `framework/reference/tech-stack.md` and `component-library.md` with sample data **only if they still hold only TODO rows**, then scaffolds the use case and copies its `inputs/`. Then open Claude Code in the repository root and run `/intake`.

## Suggested answers when Claude asks

**IT policy assistant**
- Accuracy target: 90% correct answers with a valid citation; 0 invented policies on the golden set.
- Index freshness: Tom Fischer owns policies; Aisha Karim owns KB re-indexing, nightly.
- Chat logs: keep 1 year for improvement, no personal data beyond the user ID.
- Autonomy target: L0. Data classification: Unclassified.

**Invoice triage**
- Exceptions over $50K: the Controller, Ruth Adams.
- Accuracy target: 97% on header fields, 95% on queue routing.
- Expense reimbursements: excluded from v1.
- Autonomy target: L1. Data classification: Protected B.

## Reset

```bash
rm -rf usecases/UC-* usecases/.active
git checkout framework/reference/tech-stack.md framework/reference/component-library.md
```
