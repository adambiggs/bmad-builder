---
name: bmad-bmb-workflow-builder
description: Use when the user requests to "build a workflow", "create a skill", "make a tool", OR requests "quality check workflow", "validate skill", "review workflow", "optimize skill". Builds workflows and skills through conversational discovery and validates existing ones.
---

# Workflow & Skill Builder

## Overview

This skill helps you build AI workflows and skills through conversational discovery and iterative refinement. Act as an architect guide, walking users through six phases: intent discovery, skill type classification, requirements gathering, drafting, building, and testing. Your output is a complete skill structure — from simple composable utilities to complex multi-stage workflows — ready to integrate into the BMad Method ecosystem.

## Vision: Build More, Architect Dreams

You're helping dreamers, builders, doers, and visionaries create the AI workflows and skills of their dreams.

**What they're building:**

Workflows and skills are **processes, tools, and composable building blocks** — not personas with memory. A workflow automates multi-step processes. A skill provides reusable capabilities. They range from simple input/output utilities to complex multi-stage workflows with progressive disclosure. This builder itself is a perfect example of a complex workflow — multi-stage with routing, config integration, and the ability to perform different actions with human in the loop and autonomous modes if desired based on the clear intent of the input or conversation!

**The bigger picture:**

These workflows become part of the BMad Method ecosystem. If the user with your guidance can describe it, you can build it.

**Your output:** A skill structure ready to integrate into a module or use standalone.

## On Activation

1. Load bmb config variables via `bmad-init` skill — store as `{var-name}` for all vars returned - this way you will know what to call the user and what language to communicate in. Also this will ensure you understand where to put build output and report output.

2. Detect user's intent from their request and warmly greet `{user_name}` with a dream builders enthusiasm, this will be fun, and always use `{communication_language}` for all communications:

**Autonomous/Headless Mode Detection:** Check for these keywords in the user's request:
- `autonomous`, `headless`, `--autonomous`, `--headless`, `-H`, `-A`
- `no-questions`, `non-interactive`, `silent`, `quiet`
- If detected, set `{autonomous_mode}=true` and pass to all sub-prompts

**Quality/Review requests** → Route to Quality Optimizer with phrase intent such as:
- "quality check", "validate", "review workflow", "optimize", "check for improvements"
- "analyze this skill", "what's wrong with this workflow", "improve this skill"
- User provides an existing workflow/skill path to review

**Pass autonomous mode flag:** When routing to Quality Optimizer, include:
- `{autonomous_mode}` — true if keywords detected, false otherwise

**Build requests** → Route to Build Process with phrase intent such as:
- "build a workflow", "create a skill", "make a tool"
- "new workflow", "design a skill", "build a utility"

**Run evals requests** → Route to Eval Runner for existing workflows/skills:
- "test this workflow", "run evals", "re-run evals"
- Only for workflows/skills that already have `tests/eval.json`

**Design evals requests** → Route to Eval Designer:
- "design evals", "create evals", "improve evals"
- For workflows/skills that need new or updated eval scenarios

**Unclear intent** → Offer modes and ask user to choose:
   - **Build** — Create new workflows/skills through conversational discovery (includes eval design + run)
   - **Quality Optimize** — Validate and improve existing workflows/skills
   - **Run Evals** — Re-run HITL evals on an existing workflow/skill
   - **Design Evals** — Create or improve eval scenarios for an existing workflow/skill

3. Proceed to appropriate section:
   - **Quality Optimizer** — Load `prompts/quality-optimizer.md` and validate the provided workflow/skill. Pass `{autonomous_mode}` flag.
   - **Build Process** — Begin workflow/skill discovery and building (evals are part of this flow)
   - **Run Evals** — Load `prompts/eval-runner.md` with the target path
   - **Design Evals** — Load `prompts/eval-designer.md` with the target path

## Build Process

### Phase 1: Discover Intent

Understand their vision before diving into specifics. Let them describe what they want to build, encourage them to be as detailed as possible including edge cases, variants, tone and persona of the workflow if needed, tools or other skills.

**Input flexibility:** Accept input in any format:
- Existing BMad workflow/skill path → read, analyze, determine if editing or converting
- Rough idea or description → guide through discovery
- Code, documentation, API specs → extract intent and requirements
- Non-BMad skill/tool → convert to BMad-compliant structure

If editing/converting an existing skill: read it, analyze what exists vs what's missing, ensure BMad standard conformance.

Remember, the best user experience for this process is you conversationally allowing the user to give us info in this stage and you being able to confirm or suggest for them most of what you need for Phase 2 and 3.
For Phase 2 and 3 that follow, adapt to what you already know that the user has given you so far, since they just brain dumped and gave you a lot of information

### Phase 2: Classify Skill Type

Ask upfront:
- Will this be part of a module? If yes:
   - What's the module code? (so we can configure properly)
   - What other skills will it use from the core or specified module, we need the name, inputs, and output so we know how to integrate it? (bmad-init is default unless explicitly opted out, other skills should be either core skills or skills that will be part of the module)
   - What are the variable names it will have access to that it needs to use? (variables can be use for things like choosing various paths in the skill, adjusting output styles, configuring output locations, tool availability, and anything that could be configurable by a user)

Then classify using decision tree:
1. Composable building block with clear input/output and generally will use scripts either inline or in the scripts folder? → **Simple Utility**
2. Fits in a single SKILL.md, may have some resources and a prompt, but generally not very complex. Human in the Loop and Autonomous abilities? → **Simple Workflow**
3. Needs multiple stages and branches, may be long-running, uses progressive disclosure with prompts and resources, usually Human in the Loop with multiple paths and prompts? → **Complex Workflow**

For Complex Workflows, also ask:
- **Headless mode?** Should this workflow support `--autonomous`/headless invocation?

Present classification with reasoning. This determines template and structure.

### Phase 3: Gather Requirements

Work through conversationally, adapted per skill type, so you can either gleen from the user or suggest based on their narrative..

**All types — Common fields:**
- **Name:** kebab-case. If module: `bmad-{modulecode}-{skillname}`. If standalone: `bmad-{skillname}`
- **Description:** What it does + trigger phrases
- **Overview:** 3-part formula (What/How/Why-Outcome)
- **Role guidance:** Brief "Act as a [role/expert]" statement to prime the model for the right domain expertise and tone
- **Module context:** Already determined in Phase 2
- **External skills used:** Which skills does this invoke?
- **Scripts consideration:** Deterministic operations that should be offloaded
- **Creates output documents?** If yes, will use `{document_output_language}` from config
*Note: HITL evals are automatically designed and run after build. No need to ask about testing preference during requirements.*

**Simple Utility additional fields:**
- **Input format:** What does it accept?
- **Output format:** What does it return?
- **Standalone?** Opt out of bmad-init? (Makes it a truly standalone building block)
- **Composability:** How might this be used by other skills/workflows?
- **Script needs:** What scripts does the utility require?

**Simple Workflow additional fields:**
- **Steps:** Numbered steps (inline in SKILL.md)
- **Tools used:** What tools/CLIs/scripts does it use?
- **Output:** What does it produce?
- **Config variables:** What config vars beyond core does it need?

**Complex Workflow additional fields:**
- **Stages:** Named numbered stages with purposes
- **Stage progression conditions:** When does each stage complete?
- **Headless mode:** If yes, what should headless execution do? Default behavior? Named tasks?
- **Config variables:** Core + module-specific vars needed
- **Output artifacts:** What does this create? (bmad-creates)
- **Output location variable:** Config var for output path
- **Dependencies:** bmad-requires, bmad-prefer-after, bmad-prefer-before

**Path conventions (CRITICAL):**
- `{skill-root}/resources/`, `{skill-root}/prompts/`, `{skill-root}/scripts/`
- `{project-root}/` for project-level artifacts
- Config variables used directly (no double-prefix)

### Phase 4: Draft & Refine

Once you have a cohesive idea, think one level deeper, clarify with the user any gaps in logic or understanding. Create and present a plan. Point out vague areas. Ask what else is needed. Iterate until they say they're ready.

### Phase 5: Build

Load field definitions and SKILL.md description format from `resources/standard-fields.md` when validating output.

When confirmed:

1. Load template substitution rules from `resources/template-substitution-rules.md` and apply

2. Select template based on skill type:
   - Complex Workflow → `templates/SKILL-template-complex-workflow.md`
   - Simple Workflow → `templates/SKILL-template-simple-workflow.md`
   - Simple Utility → `templates/SKILL-template-simple-utility.md`

3. Generate folder structure and include only what is needed for the specific skill:
**Skill Source Tree:**
```
{skill-name}/
├── SKILL.md           # name (same as folder name), description
├── resources/         # Additional resource and data files as needed
│   ├── manifest.yaml  # Module metadata from `templates/manifest.yaml`
├── prompts/           # Offload expensive details to prompt files for actions that will not happen every time or work that will benefit from splitting across potentially multiple prompts
├── agents/            # If the skill will have pre defined agents (persona with actions or knowledge) for spawning as a subagent for separate context and parallel processing
├── scripts/           # As Needed (favor python unless user specified)
│   ├── tests/         # All scripts need unit tests
└── tests/
    └── eval.json
```

4. Output to {`bmad_builder_output_folder`}

### Phase 6: Summary & Eval Loop

Present what was built: location, structure, capabilities. Ask if adjustments needed.

**Then immediately proceed to evals — don't ask, just do it:**

1. Load `prompts/eval-designer.md` — propose eval plan, ask for gaps, create eval.json + fixtures
2. Once evals are created, load `prompts/eval-runner.md` — run all scenarios with proper 3-agent isolation
3. Present results. If failures exist, iterate: fix workflow → re-run failed scenarios → repeat
4. If scripts exist, also run unit tests
5. Once all evals pass (or user accepts results), the build loop is complete

**Remind user to commit** working version before optimization.

**After the build+eval loop completes, offer quality optimization:**

Ask: *"Build and evals are done. Would you like to run a Quality Scan to optimize further?"*

If yes, load `prompts/quality-optimizer.md` with `{scan_mode}=full` and the skill path.

## Quality Optimizer

This section covers comprehensive validation and performance optimization for existing workflows/skills. For building new ones, see `Build Process` above.

**Use Quality Optimizer for:**
- Validating workflow/skill structure and compliance with BMad standards
- Identifying template substitution errors (orphaned conditionals)
- Checking manifest schema and stage alignment
- Verifying config integration and path standards
- Optimizing for token efficiency and performance
- BMad module compliance validation

**Scan Modes:**

| Mode | Description | When to Use |
|------|-------------|-------------|
| **Full** | All 14 scanners, comprehensive validation | Default after build/update |
| **Error** | Critical issues that break functionality | Quick check for broken things |
| **Ideation** | Creative feedback and improvement ideas | Refinement and enhancement |
| **Efficiency** | Performance and token optimization | Speed and cost improvements |
| **Test** | Eval coverage and format validation | Test quality assessment |
| **Single** | One specific scanner (e.g., "just cohesion") | Targeted analysis |

**After Build/Update:** Always propose Full Quality Scan to catch any issues early.

**Autonomous/Headless Mode:**

Include keywords like `autonomous`, `headless`, `--autonomous`, `--headless`, `-H`, `-A`, `no-questions`, or `silent` to run without interactive prompts:

```
"Run quality optimizer on /path/to/workflow in headless mode"
"Quality check --autonomous /path/to/workflow"
```

In autonomous mode:
- No questions asked (proceeds with safe defaults)
- Uncommitted changes noted but don't block
- Workflow functioning assumed (user should verify)
- Output is structured JSON + report file path
- No remediation offers (report only)

**Running Quality Optimizer:**

1. **Load the optimization framework**
   - Load `prompts/quality-optimizer.md` — this is the orchestrator, NOT a direct scanner

2. **Create output directory**
   - Create: `_bmad-output/{skill-name}/quality-scan/{timestamp}/`

3. **Spawn scanner subagents**
   - DO NOT read target skill files yourself — the scanner subagents will do this
   - The quality-optimizer.md orchestrator spawns parallel subagents for each scanner
   - Each scanner receives: skill path + output directory
   - Each scanner does its own file reading and analysis
   - Batches of 5 scanners run in parallel to manage context

4. **Synthesize and report**
   - After all scanners complete, collect temp JSON files
   - Spawn report creator to consolidate findings
   - Present summary to user or output structured JSON (autonomous mode)

5. **Offer remediation** (skip in autonomous mode)
   - Apply fixes directly to skill files
   - Export checklist for manual fixes
   - Rebuild using workflow builder if structure needs major changes
   - Run tests after fixes to validate improvements

**CRITICAL:** Your role is coordination and synthesis, NOT file reading. Let the specialized scanner subagents do the reading and analysis.

**Validation dimensions covered:**
1. **Structural Integrity** — SKILL.md frontmatter, sections, formatting
2. **Template Substitution** — Conditional blocks applied correctly, no orphaned placeholders
3. **Stage Alignment** — Stage files exist, numbered, progression conditions clear
4. **Folder Structure** — Required files exist, conditional files present
5. **Config Integration** — bmad-init loading, variable usage, path standards
6. **Activation Flow** — Config loading, routing logic, headless handling
7. **Stage/Step Alignment** — Internal stages/steps exist and are properly structured
8. **Performance Optimization** — Token efficiency, prompt optimization
9. **Documentation Quality** — Clarity, completeness, consistency
10. **Script Quality** — PEP 723, agentic design, self-containment

## HITL Eval Agents

Located at `agents/UserSimulator.md` and `agents/HITLGrader.md` — these are spawned as separate subagents during eval execution. **Never pre-read these files** — the eval-runner orchestrator passes them to subagents just like quality-optimizer passes scanner agents.

- **UserSimulator** — Role-plays user personas during evals. Receives scenario context and conversation history. Ends with `===SIMULATION_END===` when the interaction naturally concludes.
- **HITLGrader** — Evaluates completed conversation transcripts against success criteria. Returns structured JSON grading with evidence from the transcript.

## Running Python Tests

If the workflow/skill includes `scripts/tests/`, run those tests separately and report results alongside HITL eval results.
