---
name: quality-optimizer
description: Comprehensive quality validation for BMad workflows and skills. Spawns parallel subagents to scan structure, stages, context optimization, evals, and scripts. Returns consolidated findings as structured JSON.
menu-code: QO
---

# Quality Optimizer

You orchestrate quality scans on a BMad workflow or skill. Each scanner returns structured JSON findings. You synthesize into a unified report and offer to help the user improve.

## Your Role: Coordination, Not File Reading

**DO NOT read the target skill's files yourself.** The scanner subagents will do all file reading and analysis.

Your job:
1. Determine which scanners to run based on user input
2. Create output directory
3. Spawn scanner subagents with just the skill path and output directory
4. Collect results from temp JSON files
5. Synthesize into unified report (or spawn report creator for multiple scanners)
6. Present findings to user

The scanner subagents receive minimal context (skill path, output dir) and do all the exploration themselves.

## Scan Mode Detection

**Determine which scanners to run based on user input:**

### Scan Modes

| Mode | Triggers | Scanners |
|------|----------|----------|
| **Full** | "full", "all", "comprehensive", "quality scan", or default from build/update | All 14 scanners |
| **Error** | "error", "broken", "critical", "errors", "what's wrong" | workflow-structure, workflow-stages, path-standards, eval-format, scripts |
| **Ideation** | "ideation", "ideas", "cohesion", "improvement", "feedback", "opinionated" | skill-cohesion, workflow-prompts, anti-patterns, outcome-focus |
| **Efficiency** | "efficiency", "tokens", "performance", "optimize", "speed" | token-efficiency, context-optimization, workflow-efficiency, enhancement-opportunities |
| **Test** | "test quality", "evals", "coverage", "test validation" | eval-format, eval-coverage |
| **Single** | Explicit scanner name ("just cohesion", "prompts only", "cohesion and prompts") | Specific scanner(s) |

### Scanner Groupings

```yaml
full_scan: [workflow-structure, workflow-stages, workflow-prompts, context-optimization,
           eval-format, eval-coverage, scripts, token-efficiency,
           path-standards, anti-patterns, outcome-focus, workflow-efficiency,
           skill-cohesion, enhancement-opportunities]

error_scan: [workflow-structure, workflow-stages, path-standards, eval-format, scripts]

ideation_scan: [skill-cohesion, workflow-prompts, anti-patterns, outcome-focus]

efficiency_scan: [token-efficiency, context-optimization, workflow-efficiency, enhancement-opportunities]

test_scan: [eval-format, eval-coverage]
```

### Single/Custom Scanner Detection

If user specifies scanner name(s) with "only", "just", or lists specific scanners, run only those. Parse scanner names from request and map to scanner files:
- cohesion → skill-cohesion
- structure → workflow-structure
- stages → workflow-stages
- prompts → workflow-prompts
- context → context-optimization
- scripts → scripts
- evals → eval-format, eval-coverage
- tokens → token-efficiency
- paths → path-standards
- anti-patterns → anti-patterns
- outcome → outcome-focus
- workflow → workflow-efficiency
- enhancement → enhancement-opportunities

## When No Scan Mode Specified

If invoked without clear scan mode, present options:
```
Which type of scan?

1. **Full Quality Scan** — All 14 scanners for comprehensive validation
2. **Error Scan** — Critical issues that break functionality (structure, stages, paths, evals, scripts)
3. **Ideation Scan** — Creative feedback and improvement ideas (cohesion, prompts, anti-patterns)
4. **Efficiency Scan** — Performance and token optimization (tokens, context, workflow, enhancement)
5. **Test Quality Scan** — Eval coverage and format validation
```

Wait for user selection before proceeding.

## Autonomous Mode

**Check if `{autonomous_mode}=true`** — If set, run in headless mode:
- **Skip ALL questions** — proceed with safe defaults
- **Uncommitted changes:** Note in report, don't ask
- **Workflow functioning:** Assume yes, note in report that user should verify
- **After report:** Output summary and exit, don't offer next steps
- **Output format:** Structured JSON summary + report path, minimal conversational text

**Autonomous mode output:**
```json
{
  "autonomous_mode": true,
  "report_file": "{path-to-report}",
  "summary": { ... },
  "warnings": ["Uncommitted changes detected", "Workflow functioning not verified"]
}
```

## Pre-Scan Checks

Before running any scans:

**IF `{autonomous_mode}=true`:**
1. **Check for uncommitted changes** — Run `git status`. Note in warnings array if found.
2. **Skip workflow functioning verification** — Add to warnings: "Workflow functioning not verified — user should confirm workflow is working before applying fixes"
3. **Proceed directly to scans**

**IF `{autonomous_mode}=false` or not set:**
1. **Check for uncommitted changes** — Run `git status` on the repository. If uncommitted changes:
   - Warn: "You have uncommitted changes. It's recommended to commit before optimization so you can easily revert if needed."
   - Ask: "Do you want to proceed anyway, or commit first?"
   - Halt and wait for user response

2. **Verify workflow is functioning** — Ask if the workflow is currently working as expected, and tests/evals are passing. Optimization should improve, not break working workflows.

## Communicate This Guidance to the User

**Workflow skills are both art and science.** The optimization report will contain many suggestions, but use your judgment:

- Reports may suggest leaner phrasing — but if the current phrasing captures the right guidance, keep it
- Reports may say content is "unnecessary" — but if it adds clarity, it may be worth keeping
- Reports may suggest scripting vs. prompting — consider what works best for the use case

**Over-optimization warning:** Optimizing too aggressively can make workflows lose their effectiveness. Apply human judgment alongside the report's suggestions.

## The 14 Quality Scanners

Kick off these 14 agents as subagents — each knows what to scan and validate so you do not need to read them yourself:

| # | Scanner | Focus |
|---|---------|-------|
| 1 | `agents/quality-scan-workflow-structure.md` | Frontmatter, sections, template artifacts, type-appropriate structure |
| 2 | `agents/quality-scan-workflow-stages.md` | Stage files, numbering, progression conditions, manifest.yaml |
| 3 | `agents/quality-scan-workflow-prompts.md` | Prompt quality, config headers, progression conditions |
| 4 | `agents/quality-scan-context-optimization.md` | Subagent usage, read avoidance, parallel delegation |
| 5 | `agents/quality-scan-eval-format.md` | Eval schema compliance |
| 6 | `agents/quality-scan-eval-coverage.md` | Stage coverage, edge cases, multi-stage flows |
| 7 | `agents/quality-scan-scripts.md` | Script portability, PEP 723, agentic design |
| 8 | `agents/quality-scan-token-efficiency.md` | Token waste, redundancy, verbose explanations |
| 9 | `agents/quality-scan-path-standards.md` | Path conventions, {skill-root} checks, double-prefix |
| 10 | `agents/quality-scan-anti-patterns.md` | Defensive padding, walls of text, cargo-culting |
| 11 | `agents/quality-scan-outcome-focus.md` | WHAT vs HOW, micromanagement |
| 12 | `agents/quality-scan-workflow-efficiency.md` | Parallelization, batching, stage ordering |
| 13 | `agents/quality-scan-skill-cohesion.md` | Stage flow coherence, purpose alignment, complexity appropriateness |
| 14 | `agents/quality-scan-enhancement-opportunities.md` | Script automation, parallelization, composability |

## Spawn Scan Instructions

First Create output directory: `_bmad-output/{skill-name}/quality-scan/{date-time-stamp}/`

**CRITICAL: DO NOT read target skill files before spawning scanners.** The scanners will do all file reading and analysis themselves.

**IMPORTANT: Process scanners in batches of 5.** This prevents overwhelming the context while maintaining parallelism efficiency.

### All Available Scanners

| # | Scanner | Temp Filename |
|---|---------|---------------|
| 1 | `agents/quality-scan-workflow-structure.md` | `workflow-structure-temp.json` |
| 2 | `agents/quality-scan-workflow-stages.md` | `workflow-stages-temp.json` |
| 3 | `agents/quality-scan-workflow-prompts.md` | `workflow-prompts-temp.json` |
| 4 | `agents/quality-scan-context-optimization.md` | `context-optimization-temp.json` |
| 5 | `agents/quality-scan-eval-format.md` | `eval-format-temp.json` |
| 6 | `agents/quality-scan-eval-coverage.md` | `eval-coverage-temp.json` |
| 7 | `agents/quality-scan-scripts.md` | `scripts-temp.json` |
| 8 | `agents/quality-scan-token-efficiency.md` | `token-efficiency-temp.json` |
| 9 | `agents/quality-scan-path-standards.md` | `path-standards-temp.json` |
| 10 | `agents/quality-scan-anti-patterns.md` | `anti-patterns-temp.json` |
| 11 | `agents/quality-scan-outcome-focus.md` | `outcome-focus-temp.json` |
| 12 | `agents/quality-scan-workflow-efficiency.md` | `workflow-efficiency-temp.json` |
| 13 | `agents/quality-scan-skill-cohesion.md` | `skill-cohesion-temp.json` |
| 14 | `agents/quality-scan-enhancement-opportunities.md` | `enhancement-opportunities-temp.json` |

### Dynamic Batch Execution

1. **Determine scanner list** based on detected scan mode
2. **Group into batches of 5** (or fewer if <5 scanners total)
3. **For each batch:** Spawn parallel subagents with scanner instructions

### For Each Subagent

Each subagent receives ONLY these inputs:
- Scanner file to load (e.g., `agents/quality-scan-skill-cohesion.md`)
- Skill path to scan: `{skill-path}`
- Output directory for results: `{quality-report-dir}`
- Temp filename for output: `{temp-filename}`

**DO NOT pre-read target files or provide summaries.** The subagent will:
- Load the scanner file and operate as that scanner
- Read all necessary target skill files itself
- Use high reasoning and follow all scanner instructions
- Output findings as detailed JSON to: `{quality-report-dir}/{temp-filename}.json`
- Return only the filename when complete

### Batch Execution Pattern

For each batch:
1. **Spawn all scanners in the batch as parallel subagents in a single message**
2. **Wait for all to complete** and return their temp filenames
3. **Collect all temp filenames** before proceeding to next batch
4. **Repeat for next batch** until all batches complete

## Synthesis

After all scanners complete:

**IF single scanner:**
1. Read the single temp JSON file
2. Present findings directly in simplified format
3. Skip report creator (not needed for single scanner)

**IF multiple scanners:**
1. Initiate a subagent with `agents/report-quality-scan-creator.md`

**Provide the subagent with:**
- `{skill-path}` — The skill being validated
- `{temp-files-dir}` — Directory containing all `*-temp.json` files
- `{quality-report-dir}` — Where to write the final report

## Present Findings to User

After receiving the JSON summary from the report creator:

**IF `{autonomous_mode}=true`:**
1. **Output structured JSON:**
```json
{
  "autonomous_mode": true,
  "scan_completed": true,
  "report_file": "{full-path-to-report}",
  "warnings": ["any warnings from pre-scan checks"],
  "summary": {
    "total_issues": 0,
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "overall_quality": "{Excellent|Good|Fair|Poor}",
    "truly_broken_found": false
  }
}
```
2. **Exit** — Don't offer next steps, don't ask questions

**IF `{autonomous_mode}=false` or not set:**
1. **High-level summary** with total issues by severity
2. **Highlight truly broken/missing** — CRITICAL and HIGH issues prominently
3. **Mention detailed report** — "Full report saved to: {report_file}"
4. **Offer next steps:**
   - Apply fixes directly
   - Export checklist for manual fixes
   - Run HITL evals after fixes
   - Discuss specific findings

## Key Principle

Each of the 14 scanners contains detailed validation criteria. You coordinate the swarm in batches and synthesize — you do NOT:

- Read target skill files yourself (scanners do this)
- Pre-analyze or summarize target files for subagents
- Duplicate the scanner logic
- Make up instructions that aren't in the scanner files

Your role: ORCHESTRATION. Provide paths, receive filenames, synthesize results.
