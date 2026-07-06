---
name: generate-mcp
description: Generate a Python FastMCP server for a service from its spec.yaml, curating agent-facing tools (intents and workflows, not raw endpoints). Use after assess-readiness passes green or yellow.
---

# generate-mcp

Generate `serving/mcp/<name>/` — a runnable Python MCP server — from
`services/<name>/spec.yaml`. Use `templates/mcp-server/` as the structural
reference; read it before writing code so all generated servers stay
uniform.

Refuse (and say why) if the service has no `readiness.md` or is red.

## Tool curation — the important part

Do **not** map endpoints 1:1 to tools. Curate:

1. **Workflows become tools first.** Each `workflows` entry becomes one
   tool that chains the calls server-side and returns one coherent result.
   An agent should not have to orchestrate `get_order → create_refund →
   get_refund_status` itself when the spec already knows the recipe.
2. **Exposed endpoints become tools** only if not already subsumed by a
   workflow tool, skipping `expose: false` ones.
3. **Names are `verb_noun`** (`get_order`, `search_orders`, `refund_order`),
   unique across the server, ≤ 3 words.
4. **Descriptions are the spec's `when_to_use`**, including the negative
   guidance ("do NOT use for searching..."). This text is the tool's UI —
   it decides whether agents pick the right tool.
5. **Safety annotations:** set FastMCP tool annotations from `safety` —
   `readOnlyHint=True` for readonly; `destructiveHint=True` for
   destructive. Destructive tools also take a required
   `confirm: bool = False` parameter and return an explanation instead of
   acting when it is false.

## Implementation rules

- One directory per service: `server.py`, `client.py`, `pyproject.toml`,
  `README.md` (run instructions + required env vars).
- Config only from env: `<NAME>_BASE_URL` and the auth env var named in the
  spec. Fail at startup with a clear message listing missing vars.
- `client.py` holds a thin `httpx.AsyncClient` wrapper; `server.py` holds
  only tool definitions. Timeouts explicit (10s default), one retry on
  connect errors for readonly calls only, never for writes.
- **Error mapping:** every `errors[]` entry in the spec becomes a branch
  returning its `meaning` + `agent_action` text as the tool result — an
  agent-legible sentence, not a stack trace. Unknown errors return status +
  first 500 chars of body.
- **Payload bounds:** cap list responses (default page size ≤ 20, hard cap
  on response chars ~10k with a "truncated, refine your query" note) when
  the spec's payload-sanity compensation calls for it.
- Type hints on every tool parameter; `str | None = None` for optionals;
  docstring = description (FastMCP uses it).

## Verify before finishing

1. `uv run --directory serving/mcp/<name> python -c "import server"` (or
   pip equivalent) — it must import cleanly.
2. Start it with dummy env vars and confirm it lists tools (e.g. via
   `fastmcp dev` or a 2-line stdio client script) — tools must appear with
   their descriptions and annotations.
3. Update `services/registry.yaml` (`serving.mcp: serving/mcp/<name>`).

Report to the user: tool list (name + one-line description + safety), and
the env vars needed to run it for real.
