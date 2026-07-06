# Agent-Readiness Rubric

Scored per service by the `assess-readiness` skill, from its `spec.yaml`.
Each dimension scores 0–2. Total is out of 16.

| # | Dimension | 0 — blocked | 1 — usable with wrapping | 2 — agent-ready |
|---|-----------|-------------|--------------------------|-----------------|
| 1 | **Discoverability** — can an agent tell *when* to use each operation? | No usable descriptions in code or docs | Descriptions exist but say *what*, not *when* | Every exposed op has a real `when_to_use` |
| 2 | **Granularity** — do operations map to user intents? | Common intents need 4+ chained calls with client-side logic | Some intents need multi-call workflows (capture as `workflows`) | Most intents are 1 call |
| 3 | **Error semantics** — can an agent recover from failures? | Opaque 500s / HTML error pages | Status codes correct but bodies uninformative | Structured errors with actionable meaning |
| 4 | **Safety clarity** — is it clear what is destructive? | Destructive ops indistinguishable from reads (e.g. GET that mutates) | Inferable from method + naming | Explicitly documented, ideally reversible/dry-run |
| 5 | **Auth friction** — can a headless agent authenticate? | Interactive/browser-only auth | Static keys but manual issuance | Keys or tokens obtainable and rotatable programmatically |
| 6 | **Determinism & idempotency** — safe to retry? | Retries cause duplicates (no idempotency keys on writes) | Reads safe, writes risky | Idempotency keys / natural idempotency on writes |
| 7 | **Payload sanity** — are responses consumable in a context window? | Unbounded responses, no pagination, MBs of JSON | Pagination exists but defaults are huge | Bounded, paginated, field-selectable |
| 8 | **Spec confidence** — how much of the spec is verified vs guessed? | Major `gaps` with `blocking: true` | Minor gaps only | No gaps, verified against a live call or tests |

## Gate

- **13–16: green** — generate MCP + skill directly.
- **8–12: yellow** — generate, but the wrapper must compensate (see below), and
  gaps go to the owning team.
- **0–7: red** — don't generate a serving layer yet; the output is the
  remediation list, not a wrapper. A wrapper over a red API produces an agent
  that confidently does the wrong thing.

## Compensation table (yellow scores)

What the generators do to compensate per weak dimension:

| Weak dimension | MCP generator compensates by | Skill generator compensates by |
|----------------|------------------------------|--------------------------------|
| Discoverability | Writing `when_to_use` into tool descriptions by hand during analysis | Leading with a decision table: "if the task is X, use tool Y" |
| Granularity | Emitting workflow-level tools that chain endpoints server-side | Documenting step-by-step recipes with checkpoints |
| Error semantics | Mapping raw errors to structured messages with `agent_action` text | Listing known failure modes and recoveries |
| Safety clarity | Destructive annotations + refusing ambiguous ops | "Always confirm with the user before..." instructions |
| Payload sanity | Truncating/summarizing responses, enforcing page-size caps in the wrapper | Warning about large responses, prescribing filters |
