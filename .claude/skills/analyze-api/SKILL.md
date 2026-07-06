---
name: analyze-api
description: Extract a normalized spec.yaml from a backend service's source code and/or wiki docs. Use when onboarding an internal service into agent-terraform — point it at a code checkout, doc exports, or both. Handles Spring (Java/Kotlin) and Python (FastAPI/Flask/Django) services.
---

# analyze-api

Produce `services/<name>/spec.yaml` conforming to `docs/spec-format.md` from
whatever sources exist for one service. Read `docs/spec-format.md` first.

## Inputs to ask for (if not given)

1. Service short name (`[a-z0-9-]`).
2. Path to a source checkout, and/or paths to doc exports (markdown, HTML,
   wiki dumps). Either alone works; both is better.
3. Base URL env-var name and how consumers authenticate today, if known.

## Extraction procedure

### 1. Find the API surface in code

- **Spring (Java/Kotlin):** grep for `@RestController`, `@Controller`,
  `@RequestMapping`, `@GetMapping|@PostMapping|@PutMapping|@DeleteMapping|@PatchMapping`.
  Class-level `@RequestMapping` prefixes method-level paths. Extract param
  sources from `@PathVariable`, `@RequestParam`, `@RequestBody`, `@RequestHeader`.
  Response shapes: follow the returned DTO classes; note nullability and enums.
  Check `@ControllerAdvice` / `@ExceptionHandler` classes — they are the
  authoritative error table.
- **FastAPI:** grep for `@app.` / `@router.` decorators and `include_router`
  prefixes. Pydantic models give you request/response shapes and enums
  almost for free; `HTTPException` raises give the error table.
- **Flask:** `@app.route` / `@bp.route` with `methods=`; shapes usually only
  visible in `jsonify(...)` call sites — read the handler bodies.
- **Django:** `urls.py` for routing, then views/serializers (DRF
  `Serializer` classes are the shape source).

### 2. Mine the docs for semantics code can't give you

Code tells you *what* exists; docs tell you *when/why*. From wiki/docs pull:
intended use cases (→ `when_to_use`), value formats and id schemes, rate
limits, deprecations, and any "don't do X" warnings. When docs and code
disagree, trust code for shapes and docs for intent — and record the
disagreement as a `gap`.

### 3. Classify every endpoint

- `expose: false` for health checks, metrics, admin/internal callbacks —
  with a one-line reason.
- `safety`: `readonly` / `additive` / `destructive`. Beware liars: a GET
  that mutates state is `destructive` and worth a `gap` entry too.
- Idempotency: look for idempotency-key headers, upsert semantics, or
  natural idempotency (PUT by id).

### 4. Identify workflows

Look for call sequences implied by the domain: in docs ("first create X,
then..."), in integration tests, and in client code if available. Every
multi-call intent an agent will plausibly need becomes a `workflows` entry.
This is the highest-value part of the analysis — don't skip it.

### 5. Record gaps honestly

Never guess. Anything you could not determine — an undocumented query
syntax, an error code with unknown meaning, auth details you couldn't
verify — goes in `gaps`, with `blocking: true` if an agent could do damage
without that knowledge.

## Output

1. Write `services/<name>/spec.yaml`.
2. Add/update the service's row in `services/registry.yaml`
   (`status: analyzed`).
3. Summarize for the user: endpoint count (exposed/hidden), workflow count,
   gap count with the blocking ones called out.

Then suggest running `assess-readiness` on the result.
