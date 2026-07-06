# Service Spec Format (`spec.yaml`)

The normalized intermediate spec is the contract between the **analysis** side
(code/docs extraction) and the **generation** side (MCP servers, agent skills).
Every onboarded service gets one at `services/<name>/spec.yaml`.

It is deliberately *not* OpenAPI. OpenAPI describes what an API accepts;
this spec describes what an **agent needs to know to use it well**: when to
call something, what is safe to call, and how multi-step workflows fit
together. If a service has an OpenAPI spec, treat it as one input among
others — the wiki docs and code usually carry the "when/why" that OpenAPI lacks.

## Top-level structure

```yaml
service:
  name: orders                      # short id, [a-z0-9-], used for dirs/registry
  title: Order Management Service
  description: >                    # 2-4 sentences, written for an agent:
    Manages customer orders: lookup, creation, cancellation and refunds.
    Use this service whenever a task involves an order id (ORD-xxxxx) or a
    customer asking about a purchase.
  base_url_env: ORDERS_BASE_URL     # base URL always comes from env, never hardcoded
  owner: team-commerce              # who to ask when something is wrong
  sources:                          # where this spec was extracted from
    - type: code
      location: github.com/acme/orders-service (src/main/kotlin/.../controller)
      analyzed_at: 2026-07-06
    - type: docs
      location: wiki/Orders-API-Guide

auth:
  type: api_key                     # api_key | none (internal network)
  in: header                        # header | query
  name: X-Api-Key
  env: ORDERS_API_KEY               # env var the serving layer reads
  notes: Issued per consumer by team-commerce; scoped read vs write keys exist.

endpoints: [...]                    # see below
workflows: [...]                    # see below
gaps: [...]                        # see below
```

## Endpoints

One entry per HTTP endpoint that agents may need. Endpoints that agents should
*never* call (admin, internal callbacks, health checks) are listed with
`expose: false` and a reason, so a re-analysis doesn't re-discover them as gaps.

```yaml
endpoints:
  - id: get_order                   # stable snake_case id; generators key on this
    method: GET
    path: /api/v1/orders/{order_id}
    expose: true
    summary: Fetch a single order with line items and status.
    when_to_use: >                  # THE most important field. Write for an agent:
      Use when you have an order id and need current status, items or totals.
      Do NOT use for searching — use search_orders instead.
    safety: readonly                # readonly | additive | destructive
    idempotent: true
    params:
      - name: order_id
        in: path                    # path | query | header | body
        type: string
        required: true
        description: Order id in the form ORD-xxxxx.
        example: ORD-58201
    request_body: null              # JSON schema-ish shape when present
    response:
      shape: |                      # trimmed example or schema sketch — enough for
        { "id": "ORD-58201",        #   an agent to know what fields exist
          "status": "SHIPPED",
          "items": [{"sku": "...", "qty": 1}],
          "total_cents": 4200 }
      notes: status is one of PLACED|PAID|SHIPPED|DELIVERED|CANCELLED.
    errors:
      - status: 404
        meaning: No order with that id — likely a typo or a different region.
        agent_action: Report the id was not found; suggest search_orders.
      - status: 409
        meaning: Order is mid-transition (e.g. being cancelled).
        agent_action: Retry once after a short wait, then surface to user.
    pagination: null                # or {style: cursor|page|offset, params: {...}}
```

### Field notes

- **`safety`** drives generator behavior:
  - `readonly` — plain tool.
  - `additive` — creates data but nothing is lost (create order, add comment).
  - `destructive` — deletes/overwrites/spends money. The MCP generator marks
    these with destructive tool annotations and the skill generator adds an
    explicit confirm-with-user instruction.
- **`when_to_use`** is mandatory for exposed endpoints. If the source code and
  docs don't reveal it, that's a `gap`, not a blank.
- **`errors[].agent_action`** turns backend error tables into recovery
  behavior. This is what makes wrappers feel "agent-native".

## Workflows

Multi-step intents that agents actually need. These become the primary MCP
tools and the how-to sections in generated skills — endpoints are the parts,
workflows are the product.

```yaml
workflows:
  - id: refund_order
    summary: Refund a delivered order, fully or partially.
    when_to_use: Customer asks for money back on a delivered order.
    steps:
      - endpoint: get_order
        purpose: Verify status is DELIVERED and get line items.
      - endpoint: create_refund
        purpose: Issue the refund for selected items.
      - endpoint: get_refund_status
        purpose: Confirm the refund reached PROCESSING before reporting success.
    failure_notes: >
      If create_refund returns 422 REFUND_WINDOW_EXPIRED, the order is older
      than 90 days — escalate to a human, do not retry.
```

## Gaps

Everything the analysis could not determine. Gaps feed the readiness
assessment and are the to-do list for the service's owning team.

```yaml
gaps:
  - kind: missing_semantics          # missing_semantics | undocumented_error |
                                     # unclear_auth | no_pagination_info | other
    endpoint: search_orders
    detail: Query syntax for the `q` parameter is undocumented; found three
      formats in tests but no authoritative grammar.
    blocking: false                  # true => readiness gate should fail
```

## Conventions

- Everything an agent reads (`summary`, `when_to_use`, `errors`, workflow
  steps) is written in imperative second person, addressed to the agent.
- Never invent facts during extraction. Unknown → `gaps`, not guesses.
- Secrets never appear in a spec; only `env:` names of variables.
