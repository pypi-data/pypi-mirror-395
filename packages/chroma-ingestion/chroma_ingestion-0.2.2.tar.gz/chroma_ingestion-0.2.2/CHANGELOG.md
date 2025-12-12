# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Framework for future enhancements
- Support for additional file types (coming soon)

### Changed
- Ongoing performance optimizations

## [0.2.0] - 2025-12-03

### Added
- **Modern Package Structure**: Renamed from `chroma_tools` to `chroma_ingestion` for clarity and PyPI compatibility
- **Public API Exports**: 5 well-documented public APIs in `__init__.py`
  - `CodeIngester` - Core ingestion class for code files
  - `AgentIngester` - Specialized ingester for AI agent definitions
  - `CodeRetriever` - Semantic search and retrieval interface
  - `MultiCollectionSearcher` - Cross-collection search utility
  - `get_chroma_client()` - Singleton client factory function
- **Click-Based CLI**: New command-line interface with 4 commands
  - `chroma-ingest` - Ingest code files into ChromaDB
  - `chroma-search` - Search ingested code semantically
  - `chroma-reset-client` - Reset singleton client connection
  - `chroma-list-collections` - List available collections
- **Comprehensive Testing Suite**: 140+ tests across unit and integration
  - 74 unit tests covering all modules
  - 70+ integration tests for real ChromaDB scenarios
  - ~100% estimated coverage on core modules
  - 6 shared pytest fixtures for test reuse
- **GitHub Actions CI/CD Pipeline**: Automated quality checks
  - Linting with Ruff
  - Type checking with mypy (strict mode)
  - Testing with pytest (80% minimum coverage)
  - Codecov integration for coverage tracking
- **Type Safety**: 100% type hints across codebase
  - Full mypy strict mode compliance
  - PEP 561 marker file included
  - Type inference compatible with IDE autocomplete
- **Pre-commit Hooks**: Automated code quality enforcement
  - Code formatting with ruff
  - Import organization with isort
- **Project Organization**: 70% reduction in root directory clutter
  - Archived obsolete scripts and reports
  - Consolidated documentation
  - Clean, professional structure

### Changed
- **Package Naming**: `chroma_tools` → `chroma_ingestion` (main breaking change)
- **Import Statements**: All imports now use `chroma_ingestion` package name
- **Dependency Management**: Consolidated in `pyproject.toml` with optional dev dependencies
- **Configuration**: Unified via `src/chroma_ingestion/config.py`
- **Testing Organization**: Tests moved to `tests/` with unit/integration separation

### Removed
- Deprecated root-level scripts (archived to `archive/` directory)
- Obsolete venv directories (`list_venv/`, `lisy_venv/`)
- Legacy `consolidated_agents/` directory
- Old reporting scripts and one-off analysis tools

### Fixed
- Singleton pattern now properly prevents connection pool exhaustion
- Better error handling in batch ingestion operations
- Improved test isolation with proper fixtures

### Security
- All dependencies pinned to safe minimum versions
- No known vulnerabilities in dependency chain
- Type hints catch potential runtime errors

## [0.1.0] - 2025-11-XX

### Added
- Initial release of Chroma code ingestion system
- Basic ingestion capabilities for code files
- ChromaDB integration
- Semantic text splitting with LangChain
- Environment variable configuration support

---

## Upgrade Guide

### From 0.1.0 → 0.2.0

**Breaking Change**: Package name changed from `chroma_tools` to `chroma_ingestion`

Update your imports:
```python
# Old (no longer works)
from src.ingestion import CodeIngester

# New (required)
from chroma_ingestion import CodeIngester
from chroma_ingestion.retrieval import CodeRetriever
```

Using as a CLI:
```bash
# Old approach (from root scripts)
python ingest.py --folder ./code --collection my_collection

# New approach (via entry point)
chroma-ingest ./code --collection my_collection
```

All functionality remains the same - only import paths have changed.

---

## Future Roadmap

### Coming in 0.3.0
- [ ] ReadTheDocs documentation site
- [ ] Support for additional programming languages
- [ ] Performance optimizations for large codebases (>1GB)
- [ ] Streaming ingestion for real-time updates
- [ ] Custom chunking strategies

### Coming in 0.4.0
- [ ] Web UI for ingestion and search
- [ ] REST API server
- [ ] Multiple backend support (Pinecone, Weaviate)
- [ ] Advanced filtering and faceted search

### Coming in 1.0.0
- [ ] Production-ready stability guarantee
- [ ] Long-term API stability commitment
- [ ] Official integration with ChromaDB ecosystem
- [ ] Enterprise support options

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details
