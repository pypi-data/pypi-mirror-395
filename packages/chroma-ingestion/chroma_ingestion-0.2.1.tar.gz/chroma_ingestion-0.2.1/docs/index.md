# Welcome to Chroma Ingestion

**Chroma Ingestion** is a semantic-aware code extraction and storage system that intelligently chunks code repositories and stores them in Chroma Cloud for AI agent retrieval and context generation.

## What is it?

Think of it as a tool that:
1. **Reads** your entire codebase
2. **Understands** semantic structure (functions, classes, modules)
3. **Chunks** code intelligently while preserving context
4. **Stores** in Chroma for semantic search
5. **Retrieves** relevant code snippets based on natural language queries

## Why use it?

- 🚀 **Fast Setup** - Get started in minutes
- 🧠 **Semantic Understanding** - AI-aware chunking preserves code logic
- 🔍 **Powerful Search** - Query code with natural language
- 📊 **Rich Metadata** - Track source, type, and location of every chunk
- 🔄 **Scalable** - Handle large codebases efficiently
- 🎯 **Production Ready** - Full test coverage, type hints, CI/CD

## Quick Start

### Installation

```bash
pip install chroma-ingestion
```

### Basic Usage

**Command-line:**
```bash
chroma-ingest /path/to/code --collection my_collection
chroma-ingest search "authentication patterns" --collection my_collection
```

**Python API:**
```python
from chroma_ingestion import CodeIngester, CodeRetriever

# Ingest code
ingester = CodeIngester(target_folder="/path/to/code", collection_name="my_collection")
ingester.ingest_files()

# Search
retriever = CodeRetriever("my_collection")
results = retriever.query("How do we handle errors?", n_results=3)
```

## Features

✅ **Code-Aware Splitting** - Preserves semantic structure
✅ **Multi-Format Support** - Python, Markdown, Agent definitions
✅ **Batch Processing** - Efficiently handles large codebases
✅ **Metadata Tracking** - Source file info, chunk indices, types
✅ **Chroma Cloud Integration** - Secure, scalable storage
✅ **Verification Tools** - Built-in data quality validation

## Core Concepts

### CodeIngester
Reads files recursively and chunks them semantically:
- Respects code structure (functions, classes, modules)
- Maintains configurable overlap for context
- Batches uploads for efficiency

### CodeRetriever
Searches ingested code with semantic understanding:
- Natural language queries
- Metadata-based filtering
- Relevance scoring

### Collections
Logical groupings in Chroma:
- One per codebase or project
- Indexed independently
- Searchable via API

## Use Cases

- **AI Agents** - Provide code context to LLM-powered agents
- **Code Search** - Find relevant code snippets with descriptions
- **Documentation** - Generate docs from ingested code patterns
- **Knowledge Bases** - Build searchable code repositories
- **Onboarding** - Help new developers understand codebases

## Next Steps

- 📖 [Installation Guide](getting-started/installation.md) - Setup instructions
- 🚀 [Quick Start](getting-started/quick-start.md) - Your first ingest/search
- 📚 [User Guides](guides/basic-usage.md) - Detailed workflows
- 🔧 [API Reference](api/overview.md) - Complete API documentation

## Get Help

- 📝 [Troubleshooting Guide](guides/troubleshooting.md) - Common issues
- 💬 [GitHub Issues](https://github.com/chroma-core/chroma-ingestion/issues) - Report bugs
- 📢 [GitHub Discussions](https://github.com/chroma-core/chroma-ingestion/discussions) - Ask questions

## Contributing

Contributions welcome! See [CONTRIBUTING.md](https://github.com/chroma-core/chroma-ingestion/blob/main/CONTRIBUTING.md) for guidelines.

## License

MIT License - See LICENSE for details
