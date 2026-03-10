---
name: bmad-{module-code-or-empty}{skill-name}
description: {skill-description}
---

# {skill-name}

## Overview

{overview-template}

Act as {role-guidance}.

{if-headless}
## Activation Mode Detection

**Check activation context immediately:**

1. **Headless mode**: Check for `--autonomous`/`--headless` flags
   - If detected: skip questions, proceed with safe defaults, output structured results
   - If `--autonomous:{task-name}` → run that specific task
   - If just `--autonomous` → run default headless behavior

2. **Interactive mode** (default): Proceed to `## On Activation` section below
{/if-headless}

## On Activation

{if-bmad-init}
1. **Load config via bmad-init skill** — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` for all communications
   {if-creates-docs}- Use `{document_output_language}` for output documents{/if-creates-docs}
   - Store any other config variables as `{var-name}` and use appropriately

2. **Greet user** as `{user_name}`, speaking in `{communication_language}`
{/if-bmad-init}

3. **Check if workflow in progress:**
   - If output doc exists (user specifies path or we prompt):
     - Read doc to determine current stage
     - Resume from last completed stage
   - Else: Start at `prompts/01-{stage-1-name}.md`

4. **Route to appropriate stage** based on progress

{if-headless}
**Headless mode routing:**
- Default: Run all stages sequentially with safe defaults
- Named task: Execute specific stage or task
- Output structured JSON results when complete
{/if-headless}

## Stages

| # | Stage | Purpose | Prompt |
|---|-------|---------|--------|
| 1 | {stage-1-name} | {stage-1-purpose} | `prompts/01-{stage-1-name}.md` |
| 2 | {stage-2-name} | {stage-2-purpose} | `prompts/02-{stage-2-name}.md` |

{if-external-skills}
## External Skills

This workflow uses:
{external-skills-list}
{/if-external-skills}

{if-scripts}
## Scripts

Available scripts in `scripts/`:
- `{script-name}` — {script-description}
{/if-scripts}
