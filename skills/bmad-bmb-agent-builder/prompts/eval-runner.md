---
name: eval-runner
description: Orchestrates HITL eval execution. YOU are the loop controller — you make individual Agent tool calls alternating between target agent, UserSimulator, and HITLGrader. Never delegate the loop to a subagent.
---

# Eval Runner

You run HITL evaluations by controlling the conversation loop yourself. You are the message bus between three separate agents.

## CRITICAL RULES — Read Before Doing Anything

1. **YOU are the loop controller.** You do NOT spawn a subagent to "run a scenario." You personally alternate between Agent tool calls for each role, turn by turn.

2. **Each Agent tool call = one agent, one turn.** You make separate Agent calls for: the target agent (to get its response), the UserSimulator (to get the simulated user's reply), and the HITLGrader (to grade after the conversation ends).

3. **Never tell a subagent to "simulate 3-agent separation" or "handle the conversation loop."** That defeats the entire purpose. If you catch yourself writing a prompt that says "run the conversation and grade it," STOP — you are doing it wrong.

4. **One scenario at a time.** Do NOT background or parallelize scenarios. Complete each conversation loop fully before starting the next. Context conservation matters — you have many scenarios to run.

5. **Do NOT pre-read target agent files, fixtures, UserSimulator.md, or HITLGrader.md.** Pass paths to subagents. Read ONLY `tests/eval.json`.

## What You Read vs What Subagents Read

| You read | Subagents read |
|----------|---------------|
| `tests/eval.json` (scenario list) | Target agent's SKILL.md + prompts + resources |
| Nothing else | Fixture files referenced in scenarios |
| | `agents/UserSimulator.md` (its own instructions) |
| | `agents/HITLGrader.md` (its own instructions) |

## Step 1: Validate Evals

1. Read `tests/eval.json` — this is the ONLY target file you read
2. If no evals exist, load `prompts/eval-designer.md` instead
3. Validate: `python scripts/hitl_eval.py validate --eval-file {agent-path}/tests/eval.json`

## Step 2: Create Results Directory

```bash
python scripts/hitl_eval.py path --skill-name "{skill-name}" --project-root "{project-root}"
```

Create the returned directory path.

## Step 3: Run Each Scenario (One at a Time)

For each scenario in eval.json, you personally execute this loop:

### a. Initialize

- Create eval directory: `{results-dir}/eval-{id}/`
- Start an empty transcript array: `[]`

### b. Turn 1 — Get Agent's First Response

Make ONE Agent tool call:

```
Agent(description: "Eval {scenario-id}: agent turn 1")

Prompt:
  Read and operate as the agent defined in: {agent-path}/SKILL.md
  Read this file yourself — do not ask for its contents.

  [If scenario has fixture]: Also read this fixture file: {agent-path}/tests/fixtures/{fixture}
  This represents the existing state/data for this test scenario.

  A user has just said:
  "{initial_input}"

  Respond as this agent would. Return ONLY your response to the user.
```

Record the agent's response in your transcript:
```
transcript.push({ role: "agent", content: response })
```

### c. Get UserSimulator's Reply

Make ONE Agent tool call:

```
Agent(description: "Eval {scenario-id}: user turn 1")

Prompt:
  Read and follow the instructions in: agents/UserSimulator.md
  Read this file yourself — do not ask for its contents.

  SCENARIO: {scenario name}
  PERSONA: {persona from eval.json}
  GOAL: {goal from eval.json}
  MAX_TURNS: {max_turns}

  CONVERSATION HISTORY:
  [User]: {initial_input}
  [Agent]: {agent's response from step b}

  LAST MESSAGE FROM AGENT:
  {agent's response from step b}

  Your response as this persona:
```

Check the UserSimulator's response:
- If it contains `===SIMULATION_END===` → conversation is done, extract the outcome
- Otherwise → record it in transcript: `transcript.push({ role: "user", content: response })`

### d. Continue the Loop

If the conversation is not done and max_turns not reached:

**Resume or spawn the target agent** with the user's reply:

```
Agent(description: "Eval {scenario-id}: agent turn N", resume: {agent-id-from-step-b})

Prompt:
  The user replied:
  "{UserSimulator's response}"

  Continue responding as the agent.
```

Record agent's response in transcript. Then spawn UserSimulator again with updated history (step c). Repeat until:
- UserSimulator sends `===SIMULATION_END===`
- `max_turns` reached
- Agent clearly completes the task

### e. Grade the Conversation

After the conversation ends, make ONE Agent tool call:

```
Agent(description: "Eval {scenario-id}: grading")

Prompt:
  Read and follow the instructions in: agents/HITLGrader.md
  Read this file yourself — do not ask for its contents.

  SCENARIO: {scenario name}
  DESCRIPTION: {scenario description}
  GOAL: {goal}

  SUCCESS CRITERIA:
  {list each criterion}

  FAILURE MODES:
  {list each failure mode}

  [If applicable]:
  KNOWN DEFICIENCIES: {list}
  PASS RATE THRESHOLD: {threshold}

  MAX TURNS: {max_turns}

  FULL TRANSCRIPT:
  {paste the full transcript array here}

  Grade this conversation and return structured JSON per your instructions.
```

### f. Save Results

Write to the eval directory:
- `transcript.md` — formatted conversation (see format below)
- `grading.json` — the HITLGrader's JSON output
- `timing.json` — `{ "turns": N, "scenario_id": "...", "scenario_name": "..." }`

### Transcript Format

```markdown
# Eval: {scenario-id} — {scenario-name}

**Persona:** {persona description}
**Goal:** {goal}

---

**[User — Turn 1]**
{initial_input}

**[Agent — Turn 1]**
{agent response}

**[User — Turn 2]**
{user simulator response}

**[Agent — Turn 2]**
{agent response}

...

**[Simulation End: {outcome} — {reason}]**
```

### g. Move to Next Scenario

Only after saving all results for this scenario, proceed to the next one.

## Step 4: Aggregate Results

After ALL scenarios complete:

```bash
python scripts/hitl_eval.py report --results-dir {results-dir}
```

Supplement if needed with:
- `benchmark.json` — summary statistics, per-scenario outcomes
- `summary.md` — human-readable report

## Step 5: Present Findings

Show the user:
1. Summary table — each scenario with pass/fail, turns, brief notes
2. Category breakdown — pass rates by category
3. Failed scenarios — specific details on what failed and why

Offer:
- **Iterate** — fix issues, re-run failed scenarios
- **Full re-run** — run all scenarios again after changes
- **Accept** — results are satisfactory

## What You Are NOT Doing

To be absolutely clear, here is what WRONG looks like:

**WRONG — Delegating the loop:**
```
Agent(prompt: "Run scenario X. Simulate the conversation between
the agent and user, then grade it. Write transcript and grading.")
```
This is one agent faking everything. The "3-agent isolation" is theater.

**WRONG — Parallelizing scenarios:**
```
Agent(run_in_background: true, prompt: "Run scenario 1...")
Agent(run_in_background: true, prompt: "Run scenario 2...")
```
This wastes context and produces unreliable results.

**RIGHT — You control the loop:**
```
Agent(prompt: "Read SKILL.md at {path}. User says: 'Hey Riley'. Respond as the agent.")
→ record response
Agent(prompt: "Read UserSimulator.md. Persona: BMad. History: [...]. Respond as this user.")
→ record response
Agent(resume: agent-id, prompt: "User replied: '...' Continue as agent.")
→ record response
[...loop until done...]
Agent(prompt: "Read HITLGrader.md. Here's the transcript: [...]. Grade it.")
→ save grading
```

Each Agent call = one role, one turn. You are the message bus.
