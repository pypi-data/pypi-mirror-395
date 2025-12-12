# Phase 2: Package Rename Execution - December 3, 2025

## Focus: Section "2.1 Rename Package" from ARCHITECTURE_IMPROVEMENT_PLAN.md

### Objective
Complete Phase 2 (Package Restructure) starting with subsection 2.1 (Rename Package) to reorganize code from `src/` flat structure into `src/chroma_ingestion/` nested package structure.

### Current State
- Source files in `src/` at root level: ingestion.py, agent_ingestion.py, retrieval.py, config.py
- Clients in `src/clients/chroma_client.py`
- Package implicitly named "chroma" (conflicts with chromadb)

### Target State
```
src/chroma_ingestion/
├── __init__.py                    (new)
├── config.py                      (moved from src/)
├── ingestion/
│   ├── __init__.py               (new)
│   ├── base.py                   (from src/ingestion.py)
│   └── agents.py                 (from src/agent_ingestion.py)
├── retrieval/
│   ├── __init__.py               (new)
│   └── retriever.py              (from src/retrieval.py)
└── clients/
    ├── __init__.py               (new)
    └── chroma.py                 (from src/clients/chroma_client.py)
```

### Bash Commands Reference
```bash
# Create directories
mkdir -p src/chroma_ingestion/{ingestion,retrieval,clients}

# Move files (preserve content, update imports later)
mv src/ingestion.py src/chroma_ingestion/ingestion/base.py
mv src/agent_ingestion.py src/chroma_ingestion/ingestion/agents.py
mv src/retrieval.py src/chroma_ingestion/retrieval/retriever.py
mv src/clients/chroma_client.py src/chroma_ingestion/clients/chroma.py
mv src/config.py src/chroma_ingestion/config.py

# Remove old empty directory
rmdir src/clients 2>/dev/null || true
```

### Import Updates Required
After file moves, must update all imports in:
- `src/chroma_ingestion/ingestion/agents.py` (imports from base.py)
- `src/chroma_ingestion/ingestion/base.py` (imports from config.py)
- `src/chroma_ingestion/retrieval/retriever.py` (imports from clients.chroma, config)
- Root-level scripts that import from src/ (ingest.py, examples.py, etc.)

### Next Steps in Workflow
1. Execute Phase 2.1 directory and file movements
2. Create __init__.py files with exports
3. Update all import statements
4. Verify structure and test imports
5. Proceed to Phase 2.2 (Create Package Exports)

### Metadata
- Created: 2025-12-03
- Task: Phase 2.1 (Rename Package) from ARCHITECTURE_IMPROVEMENT_PLAN.md line 319-334
- Priority: High (blocking other phases)
- Estimated Time: 30-45 minutes
