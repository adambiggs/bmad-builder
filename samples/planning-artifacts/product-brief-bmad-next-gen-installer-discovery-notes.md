---
title: "Discovery Notes: BMAD Next-Gen Installer"
type: discovery-notes
source: "product-brief-bmad-next-gen-installer.md"
created: "2026-03-12"
purpose: "Detailed supporting context captured during product brief discovery"
---

## Current Installer Architecture (Migration Context)

- Entry point: `tools/cli/bmad-cli.js` using Commander.js, routes install/uninstall/status commands
- Core installer: `tools/cli/installers/lib/core/installer.js` orchestrates all installation
- Platform configs: `tools/cli/installers/lib/ide/platform-codes.yaml` defines ~20 platforms with target dirs, legacy dirs, template types, and special flags (ancestor conflict checks, skill format toggles)
- Manifest generation: produces CSV files (`skill-manifest.csv`, `workflow-manifest.csv`, `agent-manifest.csv`) — these are the current source of truth, NOT the JSON manifests
- External modules: `tools/cli/commands/external-official-modules.yaml` lists official modules (CIS, GDS, TEA, WDS) installed from npm with semver
- Dependency resolution: 4-pass system (collect primary files, parse deps, resolve paths, resolve transitive) — limited to YAML-declared deps
- Config collection: prompts user for name, communication language, document output language, output folder path
- Current install directory structure: `_bmad/` for core files, `._config/` for manifests, plus per-IDE skill directories (`.claude/skills/`, `.cursor/skills/`, etc.)
- Supports install, update, quick-update, and compile-agents actions
- Custom modules supported via file paths in addition to npm packages

## Existing Skill/Manifest Primitives (Already Partially Built)

- Skills already use directory-per-skill layout: `skill-name/SKILL.md` with frontmatter (name, description)
- `bmad-manifest.json` sidecar files already exist alongside skills — example from product-brief skill: `{"module-code": "bmm", "replaces-skill": "bmad-create-product-brief", "capabilities": [{"name": "create-brief", "menu-code": "CB", "description": "...", "supports-headless": true, "phase-name": "1-analysis", "after": ["brainstorming"], "before": ["create-prd"], "is-required": true, "output-location": "{planning_artifacts}"}]}`
- `bmad-skill-manifest.yaml` files define `canonicalId` and artifact type in source
- The gap: JSON manifests exist but CSV remains single source of truth; no runtime scanning/registration; manifests are static, generated once at install

## Vercel Skills CLI Technical Details

- CLI tool: `npx skills add <source>` — installs from GitHub repos, GitLab, local paths, git URLs
- Supports 40+ agents with per-agent path mappings (Claude Code: `.claude/skills/`, Cursor: `.cursor/skills/`, etc.)
- Installation methods: symlinks (recommended) or copies
- Scope: project-level (shared via git) or global (user-wide)
- Discovery: scans `skills/`, `.agents/skills/`, agent-specific paths, and `.claude-plugin/marketplace.json` manifests
- Recognizes Anthropic plugin marketplace format: `{"metadata": {"pluginRoot": "./plugins"}, "plugins": [{"name": "my-plugin", "skills": ["./skills/review"]}]}`
- Key commands: add, list, find, remove, check, update, init
- Supports interactive selection or non-interactive CI/CD flags (`-y`, `--all`)
- MIT licensed, backed by Vercel

## Competitive Landscape

- **Vercel Skills.sh**: 83K+ skills, 18 agents, largest curated leaderboard — but dev-only, skills trigger unreliably (20% without explicit prompting)
- **SkillsMP**: 400K+ skills directory, pure aggregator with no curation or CLI
- **ClawHub/OpenClaw**: ~3.2K curated skills with versioning/rollback, small ecosystem
- **Lindy**: No-code AI agent builder for business automation — closed platform, no skill sharing
- **Microsoft Copilot Studio**: Enterprise no-code agent builder — vendor-locked to Microsoft
- **MindStudio**: No-code AI agent platform — siloed, no interoperability
- **Make/Zapier AI**: Workflow automation adding AI agents — workflow-centric, not methodology-centric
- **Key gap**: NO competitor combines structured methodology with plugin marketplace — this is BMAD's whitespace

## Market Context

- AI agent market: $7.84B in 2025, projected $52.62B by 2030
- Agent Skills spec is ~4 months old, ecosystem grew from thousands to 351K+ skills in that time
- Three standards converging under Linux Foundation's AAIF: MCP (tool integration, 97M monthly SDK downloads), AGENTS.md (project instructions), A2A (agent-to-agent communication)
- Skills quality crisis: 13.4% have critical vulnerabilities (Snyk study); most community skills are "AI slop"
- Skill activation reliability is a known problem: 20% trigger rate without explicit prompting — BMAD's structured invocation patterns may be an advantage here
- BMAD already has established presence: GitHub repo, npm package, docs site, organic coverage on DEV.to and Medium

## User & Distribution Requirements Captured

- NPX installer should still exist for technical users, potentially wrapping Vercel skills CLI
- Non-technical path: download zip, get platform-specific README, copy skills to folder, run bmad-init
- No requirement for Node.js, Git, or terminal for the non-technical path
- Install messages (like current installer shows) are valued — NPX path should preserve this UX
- Users may share bundles peer-to-peer, not just from marketplace
- Marketplace initially just a download button + zip + README popup with instructions
- As low-code platforms mature, provide better per-platform guidance — but this is an emerging space, we're betting on the future

## Technical Decisions & Constraints

- Adopt Anthropic plugin standard as base format (what Vercel uses)
- `bmad-manifest.json` extends the base standard for BMAD-specific needs (installer options, capabilities, help system integration, phase ordering, dependency declarations)
- bmad-init must always be included as a base skill in every bundle/install (solves bootstrapping problem)
- Vercel CLI integration pattern (wrap vs fork vs call) is a PRD/architecture decision
- Manifest format stability is critical once third-party authors publish against it — needs careful upfront design
- Migration from current CSV-based manifests to JSON-based runtime scanning is a key technical shift

## Quality & Curation Model

- All plugin submissions will be gated — not an open bazaar
- Human review by BMad and core team personally
- This is a key differentiator: curated quality vs ecosystem noise
- Certification process details are out of scope for the brief, but gated-submission is a core architectural requirement
- The quality gate becomes MORE valuable over time as the broader ecosystem gets noisier

## Scope Signals (In/Out/Maybe for PRD)

- **In**: manifest spec, bmad-init, bmad-update, Vercel CLI integration, NPX installer, zip bundles, migration path
- **Out**: BMAD Builder, marketplace web platform, skill conversion work, one-click install for all platforms, monetization
- **Maybe/Future**: deeper platform-specific integrations for non-technical users, CI/CD integration (bmad-init as GitHub Action one-liner), telemetry/usage analytics for module authors, offline/air-gapped enterprise install story, integrity verification for zip bundles (checksums/signing)

## Rejected Ideas / Decisions Made

- **Not building our own platform support matrix going forward** — delegating to Vercel skills CLI ecosystem. Rationale: maintaining 20+ platform configs is the biggest maintenance burden; it's unsustainable at 40+
- **Not requiring one-click install for non-technical users in v1** — emerging space, guidance-based for now. Rationale: we don't know what all the low-code platforms will be; better to provide good READMEs and improve over time
- **Not using existing roadmap or prior brainstorming** — starting fresh for this initiative. Rationale: BMad wanted a clean vision unconstrained by previous planning

## Open Questions for PRD

- Exact Vercel skills CLI integration pattern: wrap as subprocess? Fork and bundle? Use as a library? Peer dependency?
- How does bmad-update work technically? Diff-based? Full replacement? Does it preserve user customizations?
- What's the migration story for existing users? Migration command? Manual reinstall? Compatibility shim?
- How do we test installation correctness across 40+ platforms? CI matrix for top N? Community testing?
- Should bmad-manifest.json be proposed as an open standard to Agent Skills governance?
- How do we handle platforms NOT supported by the Vercel skills CLI?
- What's the manifest versioning strategy? How do we evolve the format without breaking existing plugins?
- What does the plugin author getting-started experience look like? What tooling do they need?

## Reviewer Insights Worth Preserving

- **Opportunity**: Module authors are an acquisition channel — every published plugin is a distribution event bringing the creator's audience into the ecosystem
- **Opportunity**: CI/CD integration (bmad-init as a pipeline one-liner) makes BMAD part of repo infrastructure, dramatically increasing stickiness
- **Opportunity**: Educational institutions are an overlooked segment — structured methodology + non-technical install maps onto university AI curriculum
- **Opportunity**: Skill composability as a first-class primitive — letting users mix BMAD modules with third-party skills for custom methodology stacks
- **Risk**: Manifest format evolution creates a versioning/compatibility matrix — once third-party authors publish, changes break plugins (same maintenance burden in a new form)
- **Risk**: "Methodology-backed quality" needs to be a defined process, not just a claim — the gated review model addresses this
- **Risk**: Platform proliferation means 40+ testing environments, even with Vercel handling translation
- **Risk**: Scope creep pressure from marketplace vision — brief explicitly excludes it but it's the primary long-term value
