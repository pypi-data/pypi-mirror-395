# Agent Consolidation Project Plan

**Goal:** Consolidate 55+ agent files across 4 vibe-tools folders into 10 focused, semantic-aware consolidated agents.

**Status:** Planning phase complete - ready for Phase 1 implementation

## Project Overview

**Source Agents:** 55+ files across 4 folders
- `.github/agents/`
- `ccs/.claude/agents/`
- `ghc_tools/agents/`
- `scf/src/superclaude/agents/`

**Target:** 10 consolidated agents
- frontend-expert
- backend-expert
- architect-expert
- testing-expert
- ai-ml-expert
- devops-expert
- security-expert
- quality-expert
- database-expert
- planning-expert

## Phase Structure

### Phase 1: Pipeline Creation (2-3 hours)
- Task 1: Create `src/agent_ingestion.py` with AgentIngester class
- Task 2: Create `ingest_agents.py` CLI script

### Phase 2: Ingestion Execution (15 min)
- Task 3: Run ingestion and verify stats

### Phase 3: Semantic Analysis (1-2 hours)
- Task 4: Create `analyze_agents.py`
- Task 5: Generate consolidation report
- Task 6: Review and finalize mapping

### Phase 4: Consolidation (2-3 hours)
- Task 7: Generate 10 consolidated agents
- Task 8: Test consolidated agents
- Task 9: Archive redundant agents

## Critical Dependencies

1. Task 1 → Task 2 (AgentIngester needed for CLI)
2. Task 3 → Tasks 4-6 (need ingested data for analysis)
3. Task 6 → Task 7 (need consolidation mapping)
4. Tasks 7 and 8 can run in parallel
5. Task 8 → Task 9 (verify before archiving)

## Key Technical Patterns

1. **Singleton Pattern:** Use get_chroma_client() from src/clients/chroma_client.py
2. **Semantic Chunking:** Use Language.MARKDOWN splitter (chunk_size=1500, overlap=300)
3. **Batch Upsert:** Process in batches of 50-100 chunks
4. **Rich Metadata:** Extract frontmatter, tech stack, category, source collection
5. **YAML Parsing:** Handle triple-dash frontmatter for agent definitions

## Metadata Schema

```
- source: Full file path
- filename: File name only
- agent_name: Parsed name
- description: From frontmatter (truncated)
- model: Preferred model
- tools: Comma-separated tools
- category: Classified category
- tech_stack: Comma-separated keywords
- folder: Parent folder
- file_type: File extension
- source_collection: Which source folder
- chunk_index: Position in document
- total_chunks: Total chunks for agent
```

## Success Metrics

- Coverage: All tech areas represented
- Reduction: 55+ → 10 agents (80% reduction)
- Query Quality: distance < 0.3 for relevant results
- No Gaps: Every source agent mapped
- No Duplicates: Single source of truth per expertise

## Files to Create

1. `src/agent_ingestion.py` - AgentIngester class
2. `ingest_agents.py` - CLI entry point
3. `analyze_agents.py` - Analysis and reporting
4. `consolidated_agents/` - Folder for 10 new agents
5. `CONSOLIDATION_REPORT.md` - Analysis output
