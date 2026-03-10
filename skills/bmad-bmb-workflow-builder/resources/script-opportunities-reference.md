# Quality Scan Script Opportunities — Reference Guide

This document identifies deterministic operations that should be offloaded from the LLM into scripts for quality validation of BMad workflows and skills.

---

## Core Principle

Scripts validate structure and syntax (deterministic). Prompts evaluate semantics and meaning (judgment). Create scripts for checks that have clear pass/fail criteria.

---

## Priority 1: High-Value Validation Scripts

### 1. Frontmatter Validator

**What:** Validate SKILL.md frontmatter structure and content

**Why:** Frontmatter is the #1 factor in skill triggering. Catch errors early.

**Checks:**
- name exists and is kebab-case
- description exists and follows pattern
- No forbidden fields
- Optional fields have valid values if present

**Output:** JSON with pass/fail per field, line numbers for errors

### 2. Manifest Schema Validator

**Status:** Exists at `scripts/validate-manifest.py`

**Enhancement opportunities:**
- Add `--skill-path` flag for auto-discovery
- Verify stage prompt files exist for complex workflows
- Check path standards in all referenced files

### 3. Template Artifact Scanner

**What:** Scan for orphaned template substitution artifacts

**Why:** Build process may leave `{if-complex-workflow}`, `{skill-name}`, etc.

**Checks:**
- Orphaned `{if-*}` / `{/if-*}` blocks
- Unreplaced placeholders (camelCase or kebab-case in braces)

**Output:** JSON with file path, line number, artifact type

### 4. Stage File Validator (Complex Workflows)

**What:** Verify numbered stage prompts exist and are properly sequenced

**Why:** Missing or misnumbered stages break workflow progression

**Checks:**
- All referenced stage files exist in prompts/
- Numbering is sequential (01, 02, 03...)
- Each stage has progression conditions
- No gaps in numbering

**Output:** JSON with missing/misnumbered stages

### 5. Path Standards Checker

**What:** Scan all .md files for path standard violations

**Why:** Missing `{skill-root}` or `{project-root}` prefixes cause failures

**Checks:**
- Paths use required prefixes
- No double-prefix patterns
- No absolute paths
- No relative paths without prefix

**Output:** Structured JSON of violations

---

## Priority 2: Analysis Scripts

### 6. Token Counter

**What:** Count tokens in each file of a workflow/skill

**Why:** Identify verbose files that need optimization

### 7. Dependency Graph Generator

**What:** Map skill → external skill dependencies

**Why:** Understand workflow's dependency surface

### 8. Config Integration Checker

**What:** Verify bmad-init config loading pattern

**Why:** Config must be loaded correctly for module-based skills

**Checks:**
- bmad-init invocation present in activation
- Required core variables loaded
- Config variables used consistently

---

## Script Output Standard

All scripts MUST output structured JSON for agent consumption:

```json
{
  "script": "script-name",
  "version": "1.0.0",
  "skill_path": "/path/to/skill",
  "timestamp": "2025-03-08T10:30:00Z",
  "status": "pass|fail|warning",
  "findings": [
    {
      "severity": "critical|high|medium|low|info",
      "category": "structure|performance|consistency",
      "location": {"file": "SKILL.md", "line": 42},
      "issue": "Clear description",
      "fix": "Specific action to resolve"
    }
  ],
  "summary": {
    "total": 10,
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4
  }
}
```

---

## Implementation Checklist

When creating validation scripts:

- [ ] Uses `--help` for documentation
- [ ] Accepts `--skill-path` for target skill
- [ ] Outputs JSON to stdout
- [ ] Writes diagnostics to stderr
- [ ] Returns meaningful exit codes (0=pass, 1=fail, 2=error)
- [ ] Self-contained (PEP 723 for Python)
- [ ] No interactive prompts
