# agent-terraform

Turn internal backend APIs into agent-consumable serving layers —
MCP servers and Agent Skills — through a repeatable, spec-driven pipeline
run with Claude Code.

## Why

Internal APIs are usually not agent-consumable as-is: endpoints are too
granular, descriptions say *what* but never *when*, errors assume a human
developer, and nothing marks what is destructive. Pointing an agent at a raw
API produces an agent that confidently does the wrong thing.

This repo fixes that with a pipeline instead of one-off wrappers:

```
service code + wiki docs
        │
        ▼  /analyze-api                ← extracts from Spring/FastAPI/Flask/Django
services/<name>/spec.yaml              ← normalized spec: the contract
        │
        ▼  /assess-readiness           ← 8-dimension scorecard, green/yellow/red gate
services/<name>/readiness.md
        │
        ├──▶ /generate-mcp             → serving/mcp/<name>/     Python FastMCP server
        └──▶ /generate-agent-skill     → serving/skills/<name>/  SKILL.md for any agent
```

Design principles:

- **Spec in the middle.** One extraction front-end (code + docs → `spec.yaml`),
  many generation back-ends. Re-analysis after an API change is a diff, not a redo.
- **Tools ≠ endpoints.** Generators curate intents and workflows; multi-call
  recipes become single server-side tools.
- **Readiness is a gate.** Red services get a remediation list for the owning
  team, not a wrapper.
- **Never guess.** Unknowns are recorded as `gaps` in the spec and surface as
  "known unknowns" in generated skills.

## Usage

Open this repo in Claude Code and say:

```
onboard <service-name>, code at <path>, docs at <path>
```

The `onboard-service` skill runs the whole pipeline with a stop at the
readiness gate. Each stage is also runnable standalone (`/analyze-api`,
`/assess-readiness`, `/generate-mcp`, `/generate-agent-skill`).

## Layout

| Path | What |
|---|---|
| `.claude/skills/` | The pipeline skills |
| `.gravity/MISSION.html` | Why this exists, principles, phased direction |
| `.gravity/spec/SPEC.md` | The intermediate spec format (start here) |
| `.gravity/readiness/SPEC.md` | Scoring dimensions and the gate |
| `services/registry.yaml` | All onboarded services and their state |
| `services/<name>/` | Per-service `spec.yaml` + `readiness.md` |
| `serving/mcp/<name>/` | Generated MCP servers (runnable, env-configured) |
| `serving/skills/<name>/` | Generated Agent Skills |
| `templates/mcp-server/` | Structural reference for generated servers |

`services/example-orders/` is a fictional worked example of the spec format.
