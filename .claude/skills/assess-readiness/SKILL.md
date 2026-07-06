---
name: assess-readiness
description: Score a service's agent-readiness from its spec.yaml using the 8-dimension rubric, producing readiness.md with a green/yellow/red gate and remediation list. Use after analyze-api and before generating any serving layer.
---

# assess-readiness

Score `services/<name>/spec.yaml` against `.gravity/readiness/SPEC.md` and
write `services/<name>/readiness.md`. Read the rubric first — the
dimension definitions and the gate thresholds live there, not here.

## Procedure

1. Read the service's `spec.yaml` in full.
2. Score each of the 8 dimensions 0–2. For every score, cite the evidence
   from the spec (specific endpoints, gaps, or fields) — a score without a
   pointer into the spec is not acceptable.
3. Apply the gate: green (13–16), yellow (8–12), red (0–7). Any gap with
   `blocking: true` caps the result at yellow regardless of score.
4. For every dimension scoring 0 or 1, write:
   - **Remediation** — what the owning team should change in the backend.
   - **Compensation** — what the generators will do meanwhile (use the
     compensation table in the rubric). Red means no compensation is
     offered: the remediation list is the deliverable.

## Output format (`readiness.md`)

```markdown
# Agent-Readiness: <service> — <GREEN|YELLOW|RED> (<score>/16)
Assessed: <date> · Spec: services/<name>/spec.yaml

| Dimension | Score | Evidence |
|---|---|---|
| Discoverability | 2 | all 7 exposed endpoints have when_to_use |
...

## Remediation (for team <owner>)
1. ...

## Compensation applied by generators
1. ...
```

Update the service's row in `services/registry.yaml`
(`status: assessed`, `readiness: green|yellow|red`, `score: n`).

Tell the user the verdict and, unless red, suggest `generate-mcp` and
`generate-agent-skill`.
