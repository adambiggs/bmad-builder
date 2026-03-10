# Quality Dimensions

Before finalizing a skill, verify it against these 6 dimensions.

## 1. Intelligence Placement

**Principle:** Token-based reasoning is expensive. Automation is cheap.

Scripts are plumbing (fetch, transform, transport) — not classification.
The prompt is intelligence (interpretation, judgment, decision-making).

**Test:** If a script contains an `if` that decides what content *means*, intelligence has leaked.
Could a script contain regex-based classification? That's intelligence done badly — brittleness without accuracy.

## 2. Token Efficiency

**Principle:** Every unnecessary token costs money.

- No redundant instructions explaining what the model already knows
- No defensive padding ("make sure you...", "don't forget...")
- No excessive trigger phrases in description
- Progressive disclosure: detailed docs belong in `resources/`, loaded on-demand
- Target: SKILL.md under ~100 lines

## 3. Outcome Focus

**Principle:** Describe WHAT to achieve, not HOW to achieve it step-by-step.

The model knows how common CLIs work — don't explain them.
Exception: corrective instructions from past failures are justified.

**Test:** Is this micromanaging, or stating the outcome?

## 4. Workflow Ordering

**Principle:** Sequential steps must truly depend on each other's output.

Independent data-gathering steps written sequentially waste time.
Identify real dependencies and flag parallelization opportunities.

**Test:** Could steps 2 and 3 run simultaneously?

## 5. Automate Mechanics

**Principle:** Purely mechanical steps burn tokens unnecessarily.

Extract to scripts when: deterministic operations, repeated patterns, complex I/O.
Keep inline when: requires judgment, context-dependent, one-off operations.
Standard shell pipelines (curl, jq, grep) stay inline unless used repeatedly.

## 6. Path Construction — CRITICAL

**Principle:** ALL paths MUST use explicit prefixes for tools and LLMs to resolve correctly.

Without `{skill-root}` or `{project-root}` prefixes, tools fail to find files and LLMs cannot resolve paths correctly.

**Required prefixes:**
- `{skill-root}` — for skill-internal files (resources, prompts, scripts)
- `{project-root}` — for project-level artifact paths

**Correct patterns:**
```
{skill-root}/resources/reference.md
{skill-root}/prompts/stage-one.md
{project-root}/_bmad/planning/prd.md
{project-root}/{config_variable}/output.md
```

**Incorrect patterns — NEVER use:**
```
./resources/reference.md           # Relative path fails
../references/file.md              # Parent directory escape fails
resources/reference.md             # No prefix fails
/Users/username/project/file.md    # Absolute path not portable
```

**Config-resolved variables:** When a config variable like `{planning_artifacts}` already resolves to a full path, do NOT prefix again:
- ✅ `{planning_artifacts}/prd.md`
- ❌ `{project_root}/{planning_artifacts}/prd.md`

**Test:** Does every file path start with `{skill-root}` or `{project-root}`?
