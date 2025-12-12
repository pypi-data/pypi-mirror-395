# Architecture Restructure Plan - December 3, 2025

## Goal
Transform chroma project from scattered root-level scripts to production-ready Python package structure following johnthagen/python-blueprint and chroma-core/chroma patterns.

## Current State Issues
- 22+ root-level Python scripts (hard to navigate)
- Test files scattered throughout
- No proper package organization
- Package implicitly named "chroma" (conflicts with chromadb)
- Markdown reports cluttering root

## Target Structure
```
chroma/
├── src/chroma_ingestion/          # Renamed package (avoids chromadb conflict)
│   ├── __init__.py                # Package exports
│   ├── py.typed                   # PEP 561 marker
│   ├── config.py                  # Configuration
│   ├── ingestion/                 # Ingestion module
│   │   ├── __init__.py
│   │   ├── base.py                # CodeIngester (from ingestion.py)
│   │   └── agents.py              # AgentIngester (from agent_ingestion.py)
│   ├── retrieval/                 # Retrieval module
│   │   ├── __init__.py
│   │   └── retriever.py           # CodeRetriever + MultiCollectionSearcher (from retrieval.py)
│   └── clients/                   # Client connections
│       ├── __init__.py
│       └── chroma.py              # Singleton HttpClient (from clients/chroma_client.py)
├── tests/                         # All tests organized
│   ├── __init__.py
│   ├── conftest.py                # Shared fixtures
│   ├── unit/                      # Unit tests
│   └── integration/               # Integration tests
├── examples/                      # Example scripts (not packaged)
├── docs/                          # Documentation
│   └── archive/                   # Old reports
└── archive/                       # Obsolete scripts (git-ignored)
```

## Phase Breakdown

### Phase 1: Directory Creation (5 min)
Create all needed directories in one batch.

### Phase 2: File Movement (10 min)
Move core source files to new locations:
- src/ingestion.py → src/chroma_ingestion/ingestion/base.py
- src/agent_ingestion.py → src/chroma_ingestion/ingestion/agents.py
- src/retrieval.py → src/chroma_ingestion/retrieval/retriever.py
- src/config.py → src/chroma_ingestion/config.py
- src/clients/chroma_client.py → src/chroma_ingestion/clients/chroma.py

### Phase 3: Package Initialization (10 min)
Create __init__.py files with proper exports for:
- chroma_ingestion/
- chroma_ingestion/ingestion/
- chroma_ingestion/retrieval/
- chroma_ingestion/clients/

### Phase 4: Test Organization (5 min)
Move test files from root to tests/ directory:
- test_agent_usability.py → tests/integration/
- test_agents_comprehensive.py → tests/integration/
- test_collection_queries.py → tests/integration/
- test_consolidated_agents.py → tests/integration/

### Phase 5: Examples Migration (5 min)
Move example/demo scripts:
- examples.py → examples/query_examples.py
- query_nextjs_patterns.py → examples/nextjs_patterns.py
- main.py → examples/basic_usage.py

### Phase 6: Archive & Cleanup (10 min)
Move obsolete files:
- *_REPORT.md → docs/archive/
- *.json analysis files → archive/
- One-off scripts → archive/

### Phase 7: Import Updates (15 min)
Update all import statements in moved files to use new chroma_ingestion package:
- From: `from src.ingestion import CodeIngester`
- To: `from chroma_ingestion.ingestion.base import CodeIngester`

### Phase 8: Verification (5 min)
- Check all Python files exist in correct locations
- Verify directory structure matches target
- Confirm no files left behind

## Risk Mitigation
- Use git (assuming repo is versioned) before starting
- Each phase is incremental and reversible
- Python imports updated systematically to avoid breakage

## Success Criteria
1. All source code under src/chroma_ingestion/
2. All tests under tests/
3. All examples under examples/
4. All reports under docs/archive/
5. All one-off scripts under archive/
6. Directory structure matches target exactly
