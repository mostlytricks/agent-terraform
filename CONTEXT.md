# CONTEXT — agent-terraform

Last touched: 2026-07-06

## Completed
- Scaffolded the full pipeline: 5 skills (`analyze-api`, `assess-readiness`, `generate-mcp`, `generate-agent-skill`, `onboard-service`), spec format, readiness rubric, FastMCP server template, fictional `example-orders` worked spec; wrote MISSION (per-service MCP decided); opened PR #1.
- Registered in gravity (ai-workspace `PROJECTS.md`, active tier) and adopted the full `.gravity/` doc system (v1.4): `MISSION.html` → `.gravity/`, spec format → `.gravity/spec/SPEC.md`, rubric → `.gravity/readiness/SPEC.md`; root `CLAUDE.md` is now the router (Doc Map + read-first table); all skill/doc references repointed.

## Current State
- PRs #1 and #2 merged — `main` has the full pipeline + `.gravity/` doc system (v1.4, 3 domains: spec · readiness · onboarding).
- No real service onboarded — internal services aren't reachable from remote sessions, so Phase 1 runs on the work machine (see `.gravity/onboarding/PLAN.md`); `example-orders` is fictional.
- No test suite; YAML files verified parseable.

## Next Step
- Phase 1 pilot, on the work machine with Claude Code (Opus 4.8+): fill the preparation checklist in `.gravity/onboarding/PLAN.md` (pick a small Python service ≤ ~15 endpoints, export its docs, note auth facts), clone this repo, then `onboard <name>, code at <path>, docs at <path>`. Rules: `.gravity/onboarding/SPEC.md`.

---
