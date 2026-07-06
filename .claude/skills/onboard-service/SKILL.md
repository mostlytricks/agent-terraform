---
name: onboard-service
description: Run the full agent-terraform pipeline for one service — analyze code/docs, assess agent-readiness, and (if the gate passes) generate the MCP server and agent skill. Use when the user says "onboard <service>" or points at a new backend to make agent-consumable.
---

# onboard-service

Orchestrate the pipeline end-to-end for one service. Each stage is its own
skill — read and follow each one at its stage; this file only sequences
them and defines the stop points.

## Stages

1. **Analyze** — run `analyze-api`. Collect the inputs it needs (service
   name, code path, doc paths) up front in one round of questions.
2. **Assess** — run `assess-readiness` on the fresh spec.
3. **Gate** — this is a real stop point:
   - **Green:** continue automatically.
   - **Yellow:** show the user the scorecard and the compensations that
     will be applied, then continue unless they object.
   - **Red:** stop. Deliver the remediation list from `readiness.md` as
     the outcome — do not generate a serving layer over a red API.
4. **Generate** — run `generate-mcp`, then `generate-agent-skill` (the
   skill references the MCP server's tool names, so order matters).
5. **Wrap up** — confirm `services/registry.yaml` reflects the final
   state, then summarize: readiness verdict, tools generated, env vars
   required to run, and remaining gaps assigned to the owning team.

## Re-onboarding (service changed)

Re-run `analyze-api`; diff the new spec against the committed one and show
the user what changed (new/removed endpoints, safety changes) before
re-assessing and regenerating. Never silently regenerate a tool whose
safety classification changed — call that out explicitly.
