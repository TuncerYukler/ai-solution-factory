# Solution patterns

Used by `/stack` and the solution-architect subagent. **Rule of thumb: choose the simplest pattern that meets the requirements. Use agents only when the steps genuinely vary per case.**

Record the chosen pattern's ID in `usecase.yaml` → `pattern`.

| ID | Pattern | Use when | Typical HITL |
|---|---|---|---|
| `copilot-assistant` | Copilot / assistant | Users want help drafting, summarizing, or answering inside their own work | User reviews every output |
| `rag-knowledge-assistant` | RAG knowledge assistant | Answers must come from a defined body of documents, with citations | User judges answers; feedback loop |
| `document-processing` | Document processing | Structured data must be extracted or classified from documents at volume | Review of low-confidence items |
| `workflow-automation` | Workflow automation with an LLM step | A fixed process has one or two steps needing judgment or language | Approval at decision steps |
| `single-agent-tools` | Single agent with tools | The steps vary per case and the agent must choose actions across systems | Approval before any write action |
| `multi-agent-orchestration` | Multi-agent orchestration | Several distinct specialist tasks must be coordinated, each with own tools | Approval at hand-offs and final output |

## Choosing

1. Is the process a fixed sequence? → `workflow-automation` or `document-processing`, not an agent.
2. Is the user the one acting, with AI helping? → `copilot-assistant` (add retrieval → `rag-knowledge-assistant`).
3. Do steps vary per case across several systems? → `single-agent-tools`.
4. Are there several distinct specialist roles with separate tools and permissions? → `multi-agent-orchestration`.

Always name the runner-up pattern and why it lost.
