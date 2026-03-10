# Standard Workflow/Skill Fields

## Common Fields (All Types)

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Full skill name (kebab-case) | `bmad-bmb-workflow-builder`, `bmad-validate-json` |
| `skillName` | Functional name (kebab-case) | `workflow-builder`, `validate-json` |
| `description` | What it does + trigger phrases | "Use when the user requests to 'build a workflow'..." |
| `role-guidance` | Brief expertise primer | "Act as a senior DevOps engineer" |
| `module-code` | Module code (if module-based) | `bmb`, `cis` |

## Simple Utility Fields

| Field | Description | Example |
|-------|-------------|---------|
| `input-format` | What it accepts | JSON file path, stdin text |
| `output-format` | What it returns | Validated JSON, error report |
| `standalone` | Opts out of bmad-init? | true/false |
| `composability` | How other skills use it | "Called by quality scanners for validation" |

## Simple Workflow Fields

| Field | Description | Example |
|-------|-------------|---------|
| `steps` | Numbered inline steps | "1. Load config 2. Read input 3. Process" |
| `tools-used` | CLIs/tools/scripts | gh, jq, python scripts |
| `output` | What it produces | PR, report, file |

## Complex Workflow Fields

| Field | Description | Example |
|-------|-------------|---------|
| `stages` | Named numbered stages | "01-discover, 02-plan, 03-build" |
| `progression-conditions` | When stages complete | "User approves outline" |
| `headless-mode` | Supports autonomous? | true/false |
| `config-variables` | Beyond core vars | `planning_artifacts`, `output_folder` |
| `output-artifacts` | What it creates (bmad-creates) | "PRD document", "agent skill" |
| `output-location-variable` | Config var for output | `bmad_builder_output_folder` |

## Overview Section Format

The Overview is the first section after the title — it primes the AI for everything that follows.

**3-part formula:**
1. **What** — What this workflow/skill does
2. **How** — How it works (approach, key stages)
3. **Why/Outcome** — Value delivered, quality standard

**Templates by skill type:**

**Complex Workflow:**
```markdown
This skill helps you {outcome} through {approach}. Act as {role-guidance}, guiding users through {key stages}. Your output is {deliverable}.
```

**Simple Workflow:**
```markdown
This skill {what it does} by {approach}. Act as {role-guidance}. Use when {trigger conditions}. Produces {output}.
```

**Simple Utility:**
```markdown
This skill {what it does}. Use when {when to use}. Returns {output format} with {key feature}.
```

## SKILL.md Description Format

```
{description of what the skill does}. Use when the user requests to {trigger phrases}.
```

## Role Guidance Format

Every generated workflow SKILL.md includes a brief role statement in the Overview or as a standalone line:
```markdown
Act as {role-guidance}. {brief expertise/approach description}.
```
This is NOT a full persona (no Identity/Communication Style/Principles sections like agents) — just enough prompt priming for the right expertise and tone.

## Path Rules

**Critical**: All paths must use explicit prefixes.

### Skill-Internal Files
Use `{skill-root}/` prefix:
- `{skill-root}/resources/reference.md`
- `{skill-root}/prompts/01-discover.md`
- `{skill-root}/scripts/validate.py`

### Project-Level Artifacts
Use `{project-root}/` prefix:
- `{project-root}/_bmad/planning/prd.md`
- `{project-root}/docs/architecture.md`

### Config Variables
Use directly — they already contain full paths:
- `{output_folder}/file.md`
- `{planning_artifacts}/prd.md`

**Never double-prefix:**
- `{project-root}/{output_folder}/file.md` (WRONG — double-prefix breaks resolution)
