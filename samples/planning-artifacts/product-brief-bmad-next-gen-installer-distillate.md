---
type: bmad-distillate
sources:
  - "product-brief-bmad-next-gen-installer.md"
  - "product-brief-bmad-next-gen-installer-discovery-notes.md"
downstream_consumer: "PRD creation"
created: "2026-03-13"
---

## Core Concept
- BMAD Next-Gen Installer: replaces monolithic Node.js CLI with skill-based plugin architecture for distributing BMAD methodology across 40+ AI platforms
- Three layers: self-describing plugins (bmad-manifest.json), cross-platform install via Vercel skills CLI (MIT), runtime registration via bmad-init skill
- Transforms BMAD from dev-only methodology into open platform for any domain (creative, therapeutic, educational, personal)

## Problem
- Current installer maintains ~20 platform configs manually; each platform convention change requires installer update, test, release — largest maintenance burden on team
- Node.js/npm required — blocks non-technical users on UI-based platforms (Claude Co-Work, etc.)
- CSV manifests are static, generated once at install; no runtime scanning/registration
- Unsustainable at 40+ platforms; new tools launching weekly

## Solution Architecture
- Plugins: skill bundles with Anthropic plugin standard as base format + bmad-manifest.json extending for BMAD-specific metadata (installer options, capabilities, help integration, phase ordering, dependencies)
- Existing manifest example: `{"module-code":"bmm","replaces-skill":"bmad-create-product-brief","capabilities":[{"name":"create-brief","menu-code":"CB","supports-headless":true,"phase-name":"1-analysis","after":["brainstorming"],"before":["create-prd"],"is-required":true}]}`
- Vercel skills CLI handles platform translation; integration pattern (wrap/fork/call) is PRD decision
- bmad-init: global skill scanning installed bmad-manifest.json files, registering capabilities, configuring project settings; always included as base skill in every bundle (solves bootstrapping)
- bmad-update: plugin update path without full reinstall; technical approach (diff/replace/preserve customizations) is PRD decision
- Distribution tiers: (1) NPX installer wrapping skills CLI for technical users, (2) zip bundle + platform-specific README for non-technical users, (3) future marketplace
- Non-technical path has honest friction: "copy to right folder" requires knowing where that folder is; per-platform README instructions for common tools; improves over time as low-code space matures

## Differentiation
- Anti-fragmentation: BMAD = cross-platform constant; no competitor provides shared methodology layer across AI tools
- Curated quality: all submissions gated, human-reviewed by BMad + core team personally; 13.4% of community skills have critical vulnerabilities (Snyk 2026); quality gate value increases as ecosystem gets noisier
- Domain-agnostic: no competitor builds beyond software dev workflows; same plugin system powers any domain via BMAD Builder (separate initiative)

## Users (ordered by v1 priority)
- Module authors (primary v1): package/test/distribute plugins independently without installer changes
- Developers: single-command install on any of 40+ platforms via NPX
- Non-technical users: install without Node/Git/terminal; emerging segment including PMs, designers, educators
- Future plugin creators: non-dev authors using BMAD Builder; need distribution without building own installer

## Success Criteria
- Zero (or near-zero) custom platform directory code; delegated to skills CLI ecosystem
- Installation verified on top platforms by volume; skills CLI handles long tail
- Non-technical install path validated with non-developer users
- bmad-init discovers/registers all plugins from manifests; clear errors for malformed manifests
- At least one external module author successfully publishes plugin using manifest system
- bmad-update works without full reinstall
- Existing CLI users have documented migration path

## Scope
- In: manifest spec, bmad-init, bmad-update, Vercel CLI integration, NPX installer, zip bundles, migration path
- Out: BMAD Builder, marketplace web platform, skill conversion (prerequisite, separate), one-click install for all platforms, monetization, quality certification process (gated-submission principle is architectural requirement; process defined separately)
- Deferred: CI/CD integration, telemetry for module authors, air-gapped enterprise install, zip bundle integrity verification (checksums/signing), deeper non-technical platform integrations

## Current Installer (migration context)
- Entry: `tools/cli/bmad-cli.js` (Commander.js) → `tools/cli/installers/lib/core/installer.js`
- Platforms: `tools/cli/installers/lib/ide/platform-codes.yaml` (~20 platforms with target dirs, legacy dirs, template types, special flags)
- Manifests: CSV files (skill/workflow/agent-manifest.csv) are current source of truth, not JSON
- External modules: `external-official-modules.yaml` (CIS, GDS, TEA, WDS) from npm with semver
- Dependencies: 4-pass resolver (collect → parse → resolve → transitive); YAML-declared only
- Config: prompts for name, communication language, document output language, output folder
- Actions: install, update, quick-update, compile-agents
- Skills already use directory-per-skill layout (skill-name/SKILL.md); bmad-manifest.json sidecars already exist but are not source of truth
- Key shift: CSV-based static manifests → JSON-based runtime scanning

## Vercel Skills CLI
- `npx skills add <source>` — GitHub, GitLab, local paths, git URLs
- 40+ agents; per-agent path mappings; symlinks (recommended) or copies
- Scopes: project-level or global
- Discovery: `skills/`, `.agents/skills/`, agent-specific paths, `.claude-plugin/marketplace.json`
- Commands: add, list, find, remove, check, update, init
- Non-interactive: `-y`, `--all` flags for CI/CD

## Competitive Landscape
- No competitor combines structured methodology + plugin marketplace (whitespace)
- Skills.sh (Vercel): 83K skills, dev-only, 20% trigger reliability without explicit prompting
- SkillsMP: 400K skills, aggregator only, no curation
- ClawHub: 3.2K curated, versioning, small
- No-code platforms (Lindy, Copilot Studio, MindStudio, Make/Zapier): closed/siloed, no skill portability, business-only
- Market: $7.84B (2025) → $52.62B (2030); Agent Skills spec ~4 months old, 351K+ skills; standards converging under Linux Foundation AAIF (MCP, AGENTS.md, A2A)
- BMAD's structured invocation patterns may advantage vs 20% trigger reliability problem

## Rejected Alternatives
- Building own platform support matrix: unsustainable at 40+; delegate to Vercel ecosystem
- One-click install for non-technical v1: emerging space; guidance-based, improve over time
- Prior roadmap/brainstorming: clean start, unconstrained by previous planning

## Open Questions
- Vercel CLI integration pattern: wrap/fork/call/peer dependency?
- bmad-update mechanics: diff/replace? Preserve user customizations?
- Migration story: command/manual reinstall/compatibility shim?
- Cross-platform testing: CI matrix for top N? Community testing for rest?
- bmad-manifest.json as open standard submission to Agent Skills governance?
- Platforms NOT supported by Vercel skills CLI?
- Manifest versioning strategy for backward compatibility?
- Plugin author getting-started experience and tooling?

## Opportunities (from review)
- Module authors as acquisition channel: each published plugin distributes BMAD to creator's audience
- CI/CD integration: bmad-init as pipeline one-liner increases stickiness
- Educational institutions: structured methodology + non-technical install → university AI curriculum
- Skill composability: mixing BMAD modules with third-party skills for custom methodology stacks

## Risks
- Manifest format evolution creates versioning/compatibility burden once third-party authors publish
- Quality gate needs defined process, not just claim — gated review model addresses
- 40+ platform testing environments even with Vercel handling translation
- Scope creep pressure from marketplace vision (explicitly excluded but primary long-term value)
- Vercel dependency: minor supply-chain risk; MIT license allows fork if deprioritized; supporting many platforms is core differentiator regardless
