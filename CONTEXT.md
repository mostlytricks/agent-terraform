# CONTEXT — agent-terraform

Last touched: 2026-07-06

## Completed
- Scaffolded the full pipeline: 5 skills (`analyze-api`, `assess-readiness`, `generate-mcp`, `generate-agent-skill`, `onboard-service`), `docs/spec-format.md`, `docs/readiness-rubric.md`, FastMCP server template, fictional `example-orders` worked spec.
- Wrote `MISSION.html` (mission, gravity relationship, principles, 3-phase direction); recorded decision: per-service MCP servers.
- Opened PR #1 (branch `claude/agent-skills-serving-layer-41ztqz` → `main`) with the whole scaffold.
- Registered the project in gravity (ai-workspace `PROJECTS.md`, active tier) and adopted the two-doc minimum (this file + CLAUDE.md).

## Current State
- PR #1 open, not yet merged; `main` still has only the initial README commit.
- No real service onboarded — everything is designed on paper; `example-orders` is fictional.
- No test suite; YAML files verified parseable.

## Next Step
- Merge PR #1, then run Phase 1 (MISSION.html): pick the first real backend service (a small Python one, per plan), add its repo to the session, and run `onboard-service` end-to-end. Expect `docs/spec-format.md` and the rubric to need revision after first real contact.

---
