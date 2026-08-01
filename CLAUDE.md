# agent-terraform

Spec-driven pipeline that turns internal backend APIs into agent-consumable serving layers (per-service MCP servers + Agent Skills), run interactively with Claude Code skills.

> **alias:** `terra`

---

<!-- gravity:router v4.2 — managed by /adopt-gravity + /sync-gravity; do not hand-edit inside the fences -->
> **gravity: v4.2** — docs live in `.gravity/`. Before working here, read `.gravity/GRAVITY.md`
> (the protocol: doc kinds + rates, navigation discipline) and `.gravity/ROUTER.md` (the Doc Map +
> what to read before changing what). Session ritual: read `CONTEXT.md` first; update it before stopping.
<!-- /gravity:router -->

## Stack

- **Pipeline:** Claude Code skills (markdown) in `.claude/skills/` — no build step; the skills *are* the program.
- **Generated output:** Python ≥ 3.11, FastMCP ≥ 2.0, httpx (per-service MCP servers under `serving/mcp/`).
- **Data:** YAML specs (`services/<name>/spec.yaml`) + `services/registry.yaml` as the state index.

## Run

Open this repo in Claude Code and say:

```
onboard <service-name>, code at <path>, docs at <path>
```

Stages are also runnable standalone: `analyze-api`, `assess-readiness`, `generate-mcp`, `generate-agent-skill`.

A generated server runs with:

```bash
export <NAME>_BASE_URL=... ; export <NAME>_API_KEY=...
uv run --directory serving/mcp/<name> fastmcp run server.py
```

## Test

```bash
python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('services/**/*.yaml', recursive=True)]"
```

No test suite yet — generated servers are verified per `generate-mcp`'s verify steps (import cleanly + tools list).

## Conventions

- Commit style: imperative subject + short body explaining the why.
- **Never hand-edit generated servers/skills** — fix the spec or the generator skill and regenerate. Hand edits are how the pipeline dies (`.gravity/MISSION.html` guardrail).
- Specs and generated code name env vars only; secrets never appear in the repo.
- `services/registry.yaml` is updated by the pipeline skills, not by hand.
- Unknowns go in a spec's `gaps:` list — never guessed.

## Constraints & Gotchas

- The readiness gate is real: red services get a remediation list, **no serving layer**. Don't generate around it.
- `services/example-orders/` is fictional — a spec-format reference. Delete once real services are onboarded.
- One MCP server per service (decided 2026-07; see `.gravity/MISSION.html`) — don't aggregate into per-domain gateways without revisiting that decision.

## Entry Points

- `.claude/skills/onboard-service/SKILL.md` — the orchestrator; each stage skill is self-contained.
- `.gravity/spec/SPEC.md` — the contract everything else keys on; change it and every skill downstream is affected.
- `templates/mcp-server/` — structural reference the generator copies; change here to change all future servers.

## Git

- Remote: `https://github.com/mostlytricks/agent-terraform`
- Default branch: `main`
