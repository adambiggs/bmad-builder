---
name: bmad-{module-code-or-empty}{skill-name}
description: {skill-description}
---

# {skill-name}

## Overview

{overview-template}

Act as {role-guidance}.

## On Activation

{if-bmad-init}
1. **Load config via bmad-init skill** — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` for all communications
   {if-creates-docs}- Use `{document_output_language}` for output documents{/if-creates-docs}

2. **Greet user** as `{user_name}`, speaking in `{communication_language}`
{/if-bmad-init}

3. **Proceed to workflow steps below**

## Workflow Steps

### Step 1: {step-1-name}
{step-1-instructions}

### Step 2: {step-2-name}
{step-2-instructions}

### Step 3: {step-3-name}
{step-3-instructions}

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
