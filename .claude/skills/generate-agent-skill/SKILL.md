---
name: generate-agent-skill
description: Generate a distributable Agent Skill (SKILL.md) that teaches any agent when and how to use a service, from its spec.yaml. Use after assess-readiness; complements generate-mcp (the MCP server is the hands, the skill is the judgment).
---

# generate-agent-skill

Generate `serving/skills/<name>/SKILL.md` from `services/<name>/spec.yaml`.

The MCP server gives an agent *callable tools*; this skill gives it
*judgment*: which tool for which situation, the recipes, and the failure
lore. Write it for a future agent that has the service's MCP tools
available but has never seen the backend.

Refuse if the service has no `readiness.md` or is red.

## Structure to generate

```markdown
---
name: using-<service>
description: <when an agent should reach for this service at all — trigger
  phrases, entity formats like order ids, task types. This line decides
  whether the skill gets loaded, so pack it with concrete triggers.>
---

# Using <service title>

<2-3 sentence orientation: what the service owns, what it does not.>

## Choosing an operation
A decision table mapping situations to tools:
| If the task involves... | Use | Notes |

## Recipes
One section per workflow from the spec: numbered steps, what to check
between steps (from steps[].purpose), and failure_notes verbatim.

## Safety rules
Explicit list of destructive tools; instruction to confirm with the user
before each, including what to show the user (e.g. items and amounts
before a refund).

## Known failure modes
From the spec's errors[]: symptom → meaning → what to do. Include the
gaps[] that survived generation as "known unknowns" so agents don't
bluff through them.

## Data formats
Id schemes, enums, date formats, pagination cursors — every literal an
agent might need to construct or parse.
```

## Rules

- Everything is imperative, second person, addressed to the consuming
  agent. No backend implementation detail unless it changes agent behavior.
- Only reference tools that the generated MCP server actually exposes (or
  raw HTTP if no MCP server exists — then include auth/env setup).
- Keep it under ~150 lines; move bulky reference tables to separate files
  in the same directory and link them.

## Finish

Update `services/registry.yaml` (`serving.skill: serving/skills/<name>`),
then show the user the decision table and safety rules for a sanity check.
