# Router — where the docs live & what to read before a change

> Read `.gravity/GRAVITY.md` (the protocol card) first if you're new to `.gravity/` docs —
> it explains the doc kinds, their rates of change, and the navigation discipline.

## Doc Map (`.gravity/`)

Docs are grouped by **subject domain**, not by doc-type. A domain folder holds whichever of three kinds it needs — `ARCHITECTURE.html` (human deep-dive), `SPEC.md` (change contract), `PLAN.*.md` (what/next) — named by *kind* because the folder already names the subject. **Recognized only when present.**

```
.gravity/
  MISSION.html      # why — north star, principles, phases, decisions (browser-read)
  spec/       SPEC.md   # the intermediate spec.yaml contract (analysis ↔ generation)
  readiness/  SPEC.md   # the 8-dimension rubric + green/yellow/red gate
  onboarding/ SPEC.md · PLAN.md   # running the pipeline on REAL internal services: rules + Phase 1 strategy
```

Precedence: CONTEXT (now) > CLAUDE (how) > SPECs (contracts) > MISSION (why).

## What to read before a change (router)

Before touching a domain, load its `SPEC.md` — the compact change contract. The paired `ARCHITECTURE.html` is the human reference behind it (read only when you need the full rationale). A "—" means that kind doesn't exist for the domain yet.

| If you're changing… | Read first | Human reference |
|---|---|---|
| `analyze-api` skill, `spec.yaml` fields, anything that writes or reads specs | `.gravity/spec/SPEC.md` | — |
| `assess-readiness` skill, scoring, the gate, compensations | `.gravity/readiness/SPEC.md` | — |
| `generate-mcp` / `generate-agent-skill`, `templates/mcp-server/` | `.gravity/spec/SPEC.md` (they consume it) | `.gravity/MISSION.html` (principles) |
| **Onboarding a real internal service** (any environment/model) | `.gravity/onboarding/SPEC.md`, then its `PLAN.md` (pilot strategy + checklist) | — |
| Direction, phases, recorded decisions | `.gravity/MISSION.html` | — |

## Adding a domain (start here for a new feature)

A **domain** is a durable subject area an agent will repeatedly navigate and change — not every feature is one. Mint a `.gravity/<domain>/` folder only when the feature has its own *gravity*; otherwise it's a slice under an existing domain. Domains have two legitimate axes, and **capability comes first**: vertical (business/capability) domains — the units of purpose a user scenario names — are the default diagnosis; horizontal (structural) domains (`data`, `security`, `ops`, …) earn folders only where a runtime owns real rules worth fencing. One-folder-per-service is the degenerate case — "it's a separate repo/deployable" is not a principle, and that topology already lives in `integration`'s Boundary Map. (`/new-domain <project> <domain>` does steps 2–3 for you.) The optional `integration` domain is reserved for contracts between services/domains: API/client type flow, auth/session behavior, ports/base URLs, shared env, queues/events, webhooks, database access boundaries, and required change order.

**1. Gate — is it a domain?** It earns a folder when it has its own *principle* and you can say yes to most of:
- rules an agent must respect to change it safely → wants a `SPEC.md`
- a "how it's built" a human needs beyond a file map → wants an `ARCHITECTURE.html`
- a multi-step arc, not a single PR → wants a `PLAN.*.md`
- a one-line *why* + non-goal that should win arguments → wants a MISSION row
- for `integration`: a cross-boundary contract that repeatedly affects more than one domain/service → wants an integration `SPEC.md`; otherwise keep it in `CONTRACT.md`

If not: it's a **`PLAN.*.md` under an existing domain** (or an `ops/` folder for cross-cutting), not a new domain. If it spans domains, it's work *in* them — a **Track** row in `IMPLEMENTATION_PLAN.md` plus one slice per touched domain, never a new folder.

**2. Start minimal — one doc, the one it needs now.** Docs are recognized only when present, so don't scaffold all four. A feature starts as intent, so almost always:
- create `.gravity/<domain>/PLAN.md` (the what/next) — usually the only file on day one;
- add `SPEC.md` the moment an agent will *change* it and there are rules to not break;
- add `ARCHITECTURE.html` when "how it's built" outgrows the file map and a human needs the rationale;
- add the **MISSION row** once it's confirmed a durable domain (the why + guard).

**3. Wire the indexes (the cost of faceting is discoverability).** Adding a folder means updating, so it's never orphaned:
- this file's **Doc Map** → add the folder line;
- this file's **router table** → add the change→read-first row (once it has a `SPEC.md`);
- `.gravity/MISSION.html` → add the why/principle/non-goal row (once it's a real domain);
- `.gravity/IMPLEMENTATION_PLAN.md` **status spine** → add the `○/◑/✓` row;
- new `ARCHITECTURE.html` lede → back-pointer to its MISSION row.

**4. Lifecycle.** idea → `PLAN.md` (`○`) → building earns `SPEC`/`ARCH` (`◑`) → shipped (`✓`). Retiring a domain = fold its `PLAN` into a neighbor or archive it, then remove its rows from the four indexes above.

**Naming:** folder = the subject (kebab-case); files inside named by *kind* (`ARCHITECTURE.html` / `SPEC.md` / `PLAN.md`), with a slug suffix only when a kind repeats (`PLAN.improvement.md`).
