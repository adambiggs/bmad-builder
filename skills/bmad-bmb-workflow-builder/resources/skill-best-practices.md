# Skill Authoring Best Practices

Write effective Skills that Claude discovers and uses successfully.

---

**Goal**: Concise, well-structured, tested Skills. Context window is shared with system prompt, conversation history, and other Skills—minimize tokens without losing clarity.

## Contents

1. [Core Principles](#core-principles) — Conciseness, freedom levels
2. [Skill Structure](#skill-structure) — Frontmatter, naming, descriptions, progressive disclosure
3. [Workflows](#workflows) — Checklists, feedback loops
4. [Content Guidelines](#content-guidelines) — Time-sensitivity, terminology
5. [Common Patterns](#common-patterns) — Templates, examples, conditional workflows
6. [Evaluation](#evaluation) — Build evals first, observe navigation
7. [Anti-Patterns](#anti-patterns) — What to avoid
8. [Skills with Code](#skills-with-code) — Error handling, utilities, MCP tools

## Core Principles

### 1. Conciseness

**Default**: Claude is smart. Only add what it doesn't know.

**Challenge every paragraph**: "Would the agent do the wrong thing without this?" If no, delete it.

| Bad (verbose, ~150 tokens) | Good (concise, ~50 tokens) |
|----------------------------|----------------------------|
| "PDF files contain text and images. You'll need a library. pdfplumber is recommended because..." | "Use pdfplumber for text extraction:\n```python\nimport pdfplumber\nwith pdfplumber.open('f.pdf') as pdf:\n    text = pdf.pages[0].extract_text()\n```" |

### 2. Freedom Levels

Match specificity to task fragility:

| Freedom | When to Use | Example |
|---------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches, context-dependent | "1. Analyze structure, 2. Check bugs, 3. Suggest improvements" |
| **Medium** (pseudocode/templates) | Preferred pattern exists, some variation OK | `def generate_report(data, format="markdown"):` |
| **Low** (exact scripts) | Fragile operations, consistency critical | `python scripts/migrate.py --verify --backup` (do not modify) |

**Analogy**: Narrow bridge with cliffs = low freedom. Open field = high freedom.

## Skill Structure

### Frontmatter Requirements

```yaml
---
name: processing-pdfs  # max 64 chars must match folder name the skill is in
description: Extract text/tables from PDFs, fill forms, merge docs. Use when user mentions PDFs, forms, or document extraction.  # max 1024 chars no special characters
---
```

### Naming

**Prefer gerund form**: `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`

**Avoid**: `helper`, `utils`, `tools`, vague names like `documents` or `data`

### Description Rules

- **Third person only**: "Processes Excel files" ✓ / "I can help process files" ✗
- **Include triggers**: what it does + when to use it
- **Specific terms**: "Extract text from PDF files. Use when user mentions PDFs, forms, or document extraction."

### Progressive Disclosure

Keep SKILL.md well under 500 lines. Split content into separate folder files. If skill.md has alternate large paths in the SKILL.md, consider choosing path and routing to a prompts folder:

```
pdf-extractor/
├── SKILL.md          # Main (loaded when triggered)
├── prompts/do-x.md             # Skills Routes to optional path do-x
├── prompts/do-y.md             # Skills Routes to optional path do-y
├── references/reference.md      # API reference
├── references/FORMS.md          # Form guide (loaded as needed)
└── references/examples.md       # Usage examples
```

**Patterns**:
1. **High-level guide**: SKILL.md links to topic-specific files
2. **Domain-specific**: `references/finance.md`, `references/sales.md` — load only relevant domain
3. **Conditional details**: Basic in SKILL.md, link to advanced topics

**Reference depth**: Max 1 level from SKILL.md. Avoid chains like `SKILL.md → advanced.md → details.md`.

**Long files**: Add TOC for files >100 lines:

```markdown
## Contents
- Authentication
- Core methods (create, read, update, delete)
- Advanced features
```

## Workflows

### Checklist Pattern

For multi-step tasks, provide copy-able checklist and use task tool to track progress:

```markdown
## Research workflow

Copy and track progress with task tool:
```
- [ ] Step 1: Read source documents
- [ ] Step 2: Identify themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create summary
- [ ] Step 5: Verify citations
```

**Step 1: Read sources**
Review each document in `sources/`. Note arguments and evidence.

**Step 2: Identify themes**
Find patterns. Where do sources agree/disagree?
```

### Feedback Loops

**Pattern**: Run validator → fix errors → repeat

```markdown
1. Draft content following STYLE_GUIDE.md
2. Validate: `python scripts/validate.py`
3. If fails: fix errors, re-validate
4. Only proceed when validation passes
5. Finalize
```

## Content Guidelines

### Avoid Time-Sensitivity

**Bad**: "Before August 2025 use old API, after use new API"

**Good**:

```markdown
## Current method
Use v2: `api.example.com/v2/messages`

## Old patterns
<details><summary>Legacy v1 (deprecated 2025-08)</summary>
`api.example.com/v1/messages` — no longer supported
</details>
```

### Consistent Terminology

Choose one term per concept:
- ✓ Always "API endpoint", "field", "extract"
- ✗ Don't mix "URL"/"API route"/"path", "box"/"element", "pull"/"retrieve"

## Common Patterns

### Template Pattern

**Strict** (must follow exactly):

````markdown
## Report structure
ALWAYS use this template:
```markdown
# [Title]
## Summary
[One paragraph]
## Findings
- Finding 1 with data
- Finding 2 with data
```
````

**Flexible** (adapt as needed):

````markdown
Here's a sensible default, use judgment:
```markdown
# [Title]
## Summary
[Overview]
```
Adapt based on context.
````

### Examples Pattern

Input/output pairs show expected style:

````markdown
## Commit message format

**Example 1:**
Input: "Added user authentication with JWT tokens"
Output:
```
feat(auth): implement JWT-based authentication
Add login endpoint and token validation middleware
```

**Example 2:**
Input: "Fixed bug where dates displayed incorrectly"
Output:
```
fix(reports): correct date formatting in timezone conversion
Use UTC timestamps consistently
```

Follow: type(scope): brief description, then details.
````

### Conditional Workflow

```markdown
1. Determine modification type:
   **Creating new?** → Creation workflow
   **Editing existing?** → Editing workflow

2. Creation: Use docx-js, build from scratch
3. Editing: Unpack, modify XML, validate, repack
```

## Evaluation

### Build Evaluations First

**Before** extensive documentation, create evaluations to identify real gaps:

1. Run Claude on representative tasks without Skill
2. Document specific failures
3. Create 3-5 scenarios testing those gaps
4. Establish baseline
5. Write minimal instructions to pass
6. Iterate

**Evaluation structure**:

```json
{
  "skills": ["pdf-processing"],
  "query": "Extract text from this PDF",
  "files": ["test.pdf"],
  "expected_behavior": [
    "Reads PDF using appropriate library",
    "Extracts text from all pages",
    "Saves to output.txt"
  ]
}
```

### Observe Navigation Patterns

Watch for:
- **Unexpected exploration paths** → structure unclear
- **Missed connections** → links need to be more explicit
- **Overreliance on sections** → move to SKILL.md
- **Ignored content** → unnecessary or poorly signaled

## Anti-Patterns

| Anti-Pattern | Solution |
|--------------|----------|
| Windows paths (`\`) | Use forward slashes (`/`) — cross-platform |
| Too many options | Provide one default with escape hatch for edge cases |
| Time-sensitive content | Use "old patterns" collapsible section |
| Inconsistent terminology | Choose one term per concept, stick to it |
| Deep nesting (A→B→C) | Keep references 1 level from SKILL.md |

## Skills with Code

### Solve, Don't Punt

Handle errors explicitly:

```python
# Good
def process_file(path):
    try:
        return open(path).read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, "w") as f:
            f.write("")
        return ""

# Bad
def process_file(path):
    return open(path).read()  # Let Claude figure it out
```

### Document Constants

Avoid "voodoo constants":

```python
# Good
# HTTP requests typically complete within 30 seconds
REQUEST_TIMEOUT = 30
# Three retries balances reliability vs speed
MAX_RETRIES = 3

# Bad
TIMEOUT = 47  # Why 47?
RETRIES = 5
```

### Utility Scripts

**Benefits**: More reliable, save tokens, save time, ensure consistency

**Make intent clear**:
- "Run `analyze_form.py` to extract fields" (execute)
- "See `analyze_form.py` for extraction algorithm" (read as reference)

### Verifiable Intermediate Outputs

For complex/open-ended tasks: plan → validate → execute → verify

**Example**: Update 50 PDF form fields from spreadsheet
1. Analyze form structure
2. **Create** `changes.json` with planned updates
3. **Validate** `changes.json` with script
4. Execute changes
5. Verify output

**Benefits**: Catches errors early, machine-verifiable, reversible planning, clear debugging

### Package Dependencies

- **claude.ai**: Can install npm/PyPI packages, pull from GitHub
- **Claude API**: No network, no runtime package installation

List required packages in SKILL.md. Verify availability in code execution environment.

### Runtime Environment

**How Claude accesses Skills**:
1. Metadata (name/description) pre-loaded at startup
2. Files read on-demand via bash Read tools
3. Scripts executed without loading contents
4. No context penalty for files until accessed

**Implications**:
- Use forward slashes in paths
- Name files descriptively: `form_validation_rules.md` not `doc2.md`
- Organize by domain: `references/finance.md`, `references/sales.md`
- Bundle comprehensive resources — no penalty until accessed
- Prefer scripts for deterministic operations
- Test file access patterns

### MCP Tool References

Use fully qualified names: `ServerName:tool_name`

```markdown
Use BigQuery:bigquery_schema to retrieve schemas.
Use GitHub:create_issue to create issues.
```

Without server prefix, tool lookup may fail.
