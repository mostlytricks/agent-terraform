# SPEC.onboarding.md

This is the compact agent-loadable contract for `onboarding` — running the
pipeline against a **real internal service** (as opposed to editing the
pipeline itself). Load it before any `onboard-service` / `analyze-api` run on
real code, in any environment (work machine, any model — written for Claude
Code with Opus 4.8 or stronger).

**Gate:** `python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('services/**/*.yaml', recursive=True)]"` parses green, **and** the generated server passes `generate-mcp`'s verify steps (imports cleanly + lists tools). No stronger automated gate exists yet — the readiness scorecard itself is `[review]`.

## Core Definition

A valid unit is one **completed onboarding run** for one service: a
`services/<name>/spec.yaml` + `services/<name>/readiness.md` + a registry row —
plus, when the gate passes, `serving/mcp/<name>/` and `serving/skills/<name>/`.

## Minimal Shape

```text
# in a Claude Code session opened at the agent-terraform checkout,
# with read access to the service source (open the parent folder or use --add-dir):

"onboard payments, code at ../payments-service, docs at ../wiki-export/payments/"

# produces:
services/payments/spec.yaml       # normalized spec (contract: .gravity/spec/SPEC.md)
services/payments/readiness.md    # scorecard + gate verdict (rubric: .gravity/readiness/SPEC.md)
services/registry.yaml            # row updated by the skills
serving/mcp/payments/             # only if green/yellow
serving/skills/payments/          # only if green/yellow
```

## Generate (the loop)

1. Gather the **inputs checklist** (PLAN.md) — code path, doc exports, auth facts, owner.
2. Run `onboard-service`; stop at the readiness gate and honor its verdict.
3. Run the **Gate** above → green; commit spec + readiness + serving layer together.

## Rules

- `[review]` Internal service **source code never enters this repo** — only the derived `spec.yaml`. Specs name env vars and repo-relative source locations; secrets, API keys, tokens, and internal hostnames/URLs never appear (base URLs live in env vars only).
- `[review]` Analysis reads **sources on disk** (code checkout, doc exports) — never model memory of what an API "probably" looks like. No source for a claim → it's a `gaps:` entry, not a field value.
- `[review]` The readiness gate is binding: **red produces a remediation list and no serving layer**. Do not generate around it "just to have something".
- `[review]` One onboarding = one commit-able unit: spec + readiness + registry row (+ serving layer) land together, so `services/` never shows a half-run.
- `[—]` Use the strongest model available for `analyze-api` (Opus 4.8+ — extraction quality caps everything downstream); generation stages are less model-sensitive.
- `[—]` Large Spring codebases: sweep for controller annotations first, then analyze **one controller per batch**; follow returned DTOs for shapes; read `@ControllerAdvice` for the error table; integration tests are the best source of workflow semantics.
- `[—]` Re-onboarding a changed service: re-run `analyze-api`, then **diff the new spec against the committed one** and show the user endpoint/safety changes before regenerating (never silently regenerate a tool whose `safety` changed).

## Gotchas

- Claude Code must be able to *read* the service checkout — open the common parent directory, or add the path with `--add-dir`. The pipeline writes only into agent-terraform.
- Wiki exports beat live wiki access: export to HTML/markdown first so the analysis is reproducible and citable in `sources:`.
- `services/example-orders/` is fictional — delete it in the same commit as the first real onboarding, so the registry never mixes real and fake.
- The skills reference `.gravity/spec/SPEC.md` and `.gravity/readiness/SPEC.md` by path — run from the agent-terraform root, not from inside the service repo.

---

Strategy, pilot criteria, and the preparation checklist live in `PLAN.md` (same folder). The spec format itself is `.gravity/spec/SPEC.md`; the rubric is `.gravity/readiness/SPEC.md`.
