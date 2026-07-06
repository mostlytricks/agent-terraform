# onboarding — PLAN

Status: ○ planned <!-- flips to ◑ when the pilot session starts on the work machine -->

## Goal

Prove the pipeline end-to-end on the **first real internal service**, run on the
work machine with Claude Code (Opus 4.8 or stronger): one session in, a
green/yellow-gated spec + a runnable MCP server + an agent skill out. First real
contact is also the shakedown for `.gravity/spec/SPEC.md` and the rubric —
expect to revise both.

## Scenario

- given a local checkout of a small internal Python service (≤ ~15 endpoints) and whatever docs exist, when I open agent-terraform in Claude Code and say `onboard <name>, code at <path>, docs at <path>` → the full pipeline runs with one stop at the readiness gate, and every unknown lands in `gaps:`, none guessed.
- given the run went green/yellow, when I set the two env vars and start `serving/mcp/<name>/` → the server lists its curated tools, and an agent completes one real task through them.
- given the run went red, when I read `readiness.md` → it names the failing dimensions with evidence and gives the owning team a concrete remediation list (that IS the deliverable — no serving layer).

## Slice

**Preparation checklist — gather before the session (nothing else blocks the run):**

1. Pilot service chosen (see criteria below) + its **code checkout path**.
2. **Doc exports** on disk (wiki → HTML/markdown dump), even if thin.
3. **Auth facts**: how consumers authenticate today (key? header name? network-trust?), and the env-var names to standardize on (`<NAME>_BASE_URL`, `<NAME>_API_KEY`).
4. **Owner**: the team/person who answers gaps and receives the remediation list.
5. agent-terraform cloned locally, session opened at its root, service path readable (`--add-dir` if needed).

**Pilot criteria** — cheapest place to learn, in order of preference: small Python service (FastAPI > Flask > Django), ≤ ~15 endpoints, at least one destructive operation (so safety gating is exercised), docs imperfect (that's the point). Spring is the *second* service, after the format survives contact.

**Files this slice produces:**

- **[NEW]** `services/<pilot>/spec.yaml` + `services/<pilot>/readiness.md`
- **[NEW]** `serving/mcp/<pilot>/` + `serving/skills/<pilot>/` (if gated in)
- **[MODIFY]** `services/registry.yaml` — pilot row; **[DELETE]** `services/example-orders/` (same commit)
- **[MODIFY]** `.gravity/spec/SPEC.md` / `.gravity/readiness/SPEC.md` — whatever first contact proves wrong

## Verification

1. Onboarding-SPEC Gate (YAML parse + server import + tools list) → green.
2. `readiness.md` cites spec evidence for all 8 dimension scores — no unevidenced score.
3. An agent session with the generated MCP server mounted completes **one real task** against the pilot (e.g. a lookup + one gated destructive op with confirm) — `[review]`, eyeballed.
4. A follow-up note lands in this PLAN: what the spec format / rubric got wrong.

## Open questions

- OPEN: which service is the pilot? (pick against the criteria above — decision goes here)
- OPEN: can the work machine's Claude Code read service checkouts outside the agent-terraform folder (policy-wise)? If not: copy the controller/router slice + docs into a scratch folder and record that as the `sources:` location.
- OPEN: where do generated skills get distributed — copied into gravity, or does gravity read this repo directly? (mirrors the MISSION open question; answer after the pilot works)

## Next

Pick the pilot service and fill the preparation checklist — then run the session.
