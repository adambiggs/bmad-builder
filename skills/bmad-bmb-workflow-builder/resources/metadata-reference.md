# Module Metadata Reference

BMad module workflows have a `resources/manifest.yaml` file for help system integration.

## File Structure

```
{skillname}/
├── SKILL.md              # Lean: just name, description, what it does
└── resources/
    └── manifest.yaml     # Help system metadata
```

## SKILL.md Frontmatter (Minimal)

```yaml
---
name: bmad-{modulecode}-{skillname}
description: What it does, trigger phrases
---
```

## resources/manifest.yaml (Full Metadata)

```yaml
# Core identification
bmad-type: bmad-workflow                  # bmad-workflow | bmad-skill
bmad-module-name: {Module Display Name}   # Full human-readable module name
bmad-module-code: {modulecode}            # Short identifier (e.g., cis, cool, xyz)

# Optional: replace an existing BMad skill
replaces: {skill-name}                    # Optional: Inherits metadata from this skill during bmad-init

# Phase context (inherited if replaces is set, unless overridden)
bmad-phase: {phase | anytime}             # Which phase it belongs to
bmad-required: {true | false}             # Is this skill itself required?

# Execution relationships (dependency graph)
bmad-requires: []                         # Hard: must complete first
bmad-prefer-after: []                     # Soft: nicer if these ran first
bmad-prefer-before: []                    # Soft: ideally run before these

# Output tracking
bmad-creates: {what this creates}         # What artifact/output?
bmad-output-location-variable: {var | none} # Config variable for output location
```

## Field Explanations

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `bmad-type` | string | Distinguishes workflows from simple skills | `bmad-workflow` |
| `bmad-module-name` | string | Human-readable module name for UI/docs | "Creative Intelligence Suite" |
| `bmad-module-code` | string | Short code for namespacing (used in skill name) | `cis`, `cool`, `xyz` |
| `replaces` | string | Optional: Replace an existing BMad skill (inherits its metadata) | `bmad-bmb-original-workflow` |
| `bmad-phase` | string | Which phase it belongs to | `planning`, `analysis`, `anytime` |
| `bmad-required` | boolean | Is this skill itself required? | `true`, `false` |
| `bmad-requires` | list | Hard dependencies — must complete first | `["skill-a", "skill-b"]` |
| `bmad-prefer-after` | list | Soft predecessors — nicer if these ran first | `["brainstorming"]` |
| `bmad-prefer-before` | list | Soft successors — ideally run before these | `["prd", "brief"]` |
| `bmad-creates` | string | What artifact does this produce? | `bmad agent`, `validation report`, `documentation` |
| `bmad-output-location-variable` | string | Which config variable controls output? | `bmad_builder_output_folder`, `none` |

### The `replaces` Field

When `replaces` is set, the skill inherits all metadata from the replaced skill during `bmad-init`. Any fields explicitly defined in the new skill's `manifest.yaml` override the inherited values.

**Example:**
```yaml
# My custom brief workflow
replaces: bmad-bmb-brief
bmad-prefer-perform: "Use my custom brief process - includes stakeholder interviews"
# All other fields (phase, requires, etc.) inherited from bmad-bmb-brief
```

## Standalone Skills vs Module Workflows

```yaml
# Standalone skill (no module)
metadata:
  bmad-type: bmad-skill

# Module workflow
metadata:
  bmad-type: bmad-workflow
  bmad-module-name: My Module
  bmad-module-code: mm
  bmad-phase: anytime
  bmad-sequence: none
  # ... other module fields
```

## Config Loading Requirement

All module workflows MUST use the `bmad-load-config-vars` skill at startup.

See `resources/bmad-module-workflows.md` for the config loading pattern.

## Path Construction Rules — CRITICAL

All paths in BMad workflows MUST use explicit prefixes to ensure tools and LLMs resolve them correctly.

**Required prefixes:**
- `{skill-root}` — for skill-internal files (resources, prompts, scripts)
- `{project-root}` — for project-level artifact paths

**Correct patterns:**
```
{skill-root}/resources/reference.md
{skill-root}/prompts/stage-one.md
{skill-root}/scripts/validate.sh
{project-root}/_bmad/planning/prd.md
{project-root}/{config_variable}/output.md
```

**Incorrect patterns — NEVER use:**
```
./resources/reference.md           # Relative path fails
../references/file.md              # Parent directory escape fails
resources/reference.md             # No prefix fails
/Users/username/project/file.md    # Absolute path not portable
{project_root}/_bmad/planning/{prd_location}/file.md  # Double-nested variable
```

**Config-resolved variables:**
When a config variable like `{planning_artifacts}` resolves to a full path, do NOT prefix it again:
- ✅ `{planning_artifacts}/prd.md`
- ❌ `{project_root}/{planning_artifacts}/prd.md`

This rule applies to ALL path references in SKILL.md, prompts, and subagent instructions.
