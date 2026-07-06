# agent-terraform

Spec-driven pipeline that turns internal backend APIs into agent-consumable serving layers (per-service MCP servers + Agent Skills), run interactively with Claude Code skills.

> **alias:** `terra`

---

> **gravity: v1.4** · _the version of the workspace gravity system this project adopted (ai-workspace root `VERSION` / `CHANGELOG.md`). Bump when you re-sync to a newer skeleton; `/triage` flags drift._

> **Docs live in `.gravity/`.** This `CLAUDE.md` (identity, *how*) and `CONTEXT.md` (*now*) stay at the project root and auto-load; `README.md` is the user guide. Everything else — the *why* and the contracts — is organized **by subject domain** under `.gravity/`. One concern, one home — link, don't restate.

## Doc Map (`.gravity/`)

```
.gravity/
  MISSION.html      # why — north star, principles, phases, decisions (browser-read)
  spec/      SPEC.md   # the intermediate spec.yaml contract (analysis ↔ generation)
  readiness/ SPEC.md   # the 8-dimension rubric + green/yellow/red gate
```

Precedence: CONTEXT (now) > CLAUDE (how) > SPECs (contracts) > MISSION (why).

## What to read before a change (router)

| If you're changing… | Read first | Human reference |
|---|---|---|
| `analyze-api` skill, `spec.yaml` fields, anything that writes or reads specs | `.gravity/spec/SPEC.md` | — |
| `assess-readiness` skill, scoring, the gate, compensations | `.gravity/readiness/SPEC.md` | — |
| `generate-mcp` / `generate-agent-skill`, `templates/mcp-server/` | `.gravity/spec/SPEC.md` (they consume it) | `.gravity/MISSION.html` (principles) |
| Direction, phases, recorded decisions | `.gravity/MISSION.html` | — |

## Adding a domain

A domain earns a `.gravity/<domain>/` folder only when it has its own principle and rules an agent must respect (workspace CLAUDE.md §6 gate — see ai-workspace). Otherwise it's a slice under an existing domain. Wire every new folder into: this Doc Map, the router table above, and MISSION.html's "system in N domains" table.

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
