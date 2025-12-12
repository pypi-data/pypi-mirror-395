# Agent Ingestion Plan - December 2, 2025

## Summary
Plan to ingest 55+ agent definitions from 5 source folders into Chroma for semantic analysis, then consolidate into 10 focused agents tailored to our tech stack.

## Key Decisions
- **Exclusions**: C#, Java, Swift/macOS, Svelte, Go, Electron, Mobile, enterprise-specific tools
- **Inclusions**: Next.js, React, Python, FastAPI, PostgreSQL, Playwright, AI/ML, DevOps

## Source Folders
1. `.github/agents` (9 files)
2. `ccs/.claude/agents` (~50 files with subfolders)
3. `ghc_tools/agents` (23 files)
4. `scf/src/superclaude/agents` (20 files)
5. `SuperClaude_Framework` - SKIP (duplicate)

## Target Consolidated Agents (10)
1. frontend-expert (Next.js, React, TypeScript)
2. backend-expert (Python, FastAPI)
3. architect-expert (System design)
4. testing-expert (Playwright, Vitest)
5. ai-ml-expert (AI/ML, prompts)
6. devops-expert (Docker, deployment)
7. security-expert (Security auditing)
8. quality-expert (Code review)
9. database-expert (PostgreSQL, Neon)
10. planning-expert (Tasks, requirements)

## Implementation Files
- `src/agent_ingestion.py` - AgentIngester class with enhanced metadata
- `ingest_agents.py` - CLI script
- `analyze_agents.py` - Semantic analysis
- `AGENT_INGEST.md` - Full plan document

## Enhanced Metadata Schema
- agent_name, description, model, tools
- category, tech_stack (extracted keywords)
- source_collection, chunk_index, total_chunks

## Next Steps
1. Create AgentIngester class
2. Run ingestion
3. Analyze clusters and duplicates
4. Generate consolidation report
5. Create 10 consolidated agents
