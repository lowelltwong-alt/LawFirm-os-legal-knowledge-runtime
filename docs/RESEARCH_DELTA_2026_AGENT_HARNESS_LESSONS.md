# Research Delta: 2026 Agent Harness Lessons for Legal Knowledge Runtime

## What changed

The base Legal Knowledge Runtime seed is still correct. The new research sharpens the safety/eval layer:

- Multi-agent is not a free lunch; keep a single manager and bounded tools by default.
- Eval design is adversarial; private legal eval fixtures matter.
- Long delegated document workflows can silently corrupt documents.
- Prompt injection can enter through retrieved text, document payloads, browser results, and tool outputs.
- Working memory should not become record memory.
- Complex legal outputs should be decomposed into source-bound claims or subgoals.

## Runtime implications

Legal Knowledge Runtime should add small local helpers for:

1. retrieval eval case loading;
2. document integrity checks;
3. safety/hostile-context checks;
4. claim/subgoal verification scaffolding.

These helpers are deterministic and synthetic-first. They are not autonomous agents and do not call live services.

## Boundary reminders

- Do not ingest real client data in MVP.
- Do not store full raw legal documents in Exception Lake.
- Do not let runtime eval failures mutate Semantic Substrate.
- Do not treat working memory as a record source.
