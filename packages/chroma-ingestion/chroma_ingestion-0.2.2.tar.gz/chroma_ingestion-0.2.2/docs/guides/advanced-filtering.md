# Advanced Filtering

Master metadata-based filtering for precise result targeting.

## Filtering Fundamentals

### Metadata Available for Filtering

Every chunk includes these fields:

```python
{
    'source': str,        # Full file path
    'filename': str,      # Base filename
    'chunk_index': int,   # Position in file (0-based)
    'folder': str,        # Parent directory
    'file_type': str,     # File extension (.py, .md, etc.)
}
```

### Basic Filtering Syntax

```python
from chroma_ingestion import CodeRetriever

retriever = CodeRetriever("my_collection")

# Filter by single value
results = retriever.query_by_metadata(
    query_text="authentication",
    where={"file_type": ".py"},  # Only Python files
    n_results=10
)

# Filter by multiple values
results = retriever.query_by_metadata(
    query_text="configuration",
    where={"file_type": {
        "$in": [".py", ".yaml", ".json"]  # Multiple file types
    }},
    n_results=15
)
```

## Filter Operators

### Equality ($eq)

```python
# Exact match - useful for specific files
results = retriever.query_by_metadata(
    query_text="error handling",
    where={"filename": {"$eq": "auth.py"}},
    n_results=5
)

# Shorthand - omit $eq for direct values
results = retriever.query_by_metadata(
    query_text="error handling",
    where={"filename": "auth.py"},  # Same as above
    n_results=5
)
```

### In ($in)

```python
# Match any value in list
results = retriever.query_by_metadata(
    query_text="imports",
    where={"file_type": {"$in": [".py", ".ts", ".js"]}},
    n_results=20
)

# Match multiple files
results = retriever.query_by_metadata(
    query_text="API routes",
    where={"filename": {"$in": ["routes.py", "api.py", "endpoints.py"]}},
    n_results=10
)
```

### Not Equal ($ne)

```python
# Exclude specific values
results = retriever.query_by_metadata(
    query_text="implementation",
    where={"file_type": {"$ne": ".md"}},  # Exclude documentation
    n_results=15
)

# Exclude specific file
results = retriever.query_by_metadata(
    query_text="configuration",
    where={"filename": {"$ne": "test.py"}},
    n_results=10
)
```

### Not In ($nin)

```python
# Exclude multiple values
results = retriever.query_by_metadata(
    query_text="implementation",
    where={"file_type": {"$nin": [".md", ".txt"]}},  # Skip docs
    n_results=20
)

# Exclude test files
results = retriever.query_by_metadata(
    query_text="production code",
    where={"filename": {"$nin": ["test.py", "conftest.py"]}},
    n_results=10
)
```

## Filtering by Path

### Filter by Folder

```python
# All chunks from specific folder
results = retriever.query_by_metadata(
    query_text="authentication",
    where={"folder": "/app/auth"},  # Exact folder
    n_results=10
)

# Multiple folders
results = retriever.query_by_metadata(
    query_text="models",
    where={"folder": {
        "$in": ["/app/models", "/app/schemas"]
    }},
    n_results=15
)
```

### Filter by Source File

```python
# Exact file path
results = retriever.query_by_metadata(
    query_text="user management",
    where={"source": "/app/models/user.py"},
    n_results=5
)

# Multiple source files
results = retriever.query_by_metadata(
    query_text="database operations",
    where={"source": {
        "$in": [
            "/app/models/user.py",
            "/app/models/product.py"
        ]
    }},
    n_results=10
)
```

### Filter by File Type

```python
# Single type
results = retriever.query_by_metadata(
    query_text="function definition",
    where={"file_type": ".py"},
    n_results=20
)

# Multiple types
results = retriever.query_by_metadata(
    query_text="configuration",
    where={"file_type": {
        "$in": [".py", ".yaml", ".json", ".env"]
    }},
    n_results=25
)

# Exclude type
results = retriever.query_by_metadata(
    query_text="code implementation",
    where={"file_type": {"$ne": ".md"}},
    n_results=20
)
```

## Complex Filters

### Multiple Conditions (AND Logic)

```python
# Filter by type AND folder
results = retriever.query_by_metadata(
    query_text="authentication",
    where={
        "file_type": ".py",           # AND
        "folder": "/app/auth"         # AND
    },
    n_results=5
)

# Filter by multiple conditions
results = retriever.query_by_metadata(
    query_text="implementation",
    where={
        "file_type": {"$in": [".py", ".ts"]},  # AND
        "folder": {"$ne": "/tests"}             # AND (not in tests)
    },
    n_results=15
)
```

### Filtering by Chunk Index

```python
# Get first chunk from each file (chunk_index=0)
first_chunks = retriever.query_by_metadata(
    query_text="module imports",
    where={"chunk_index": 0},
    n_results=20
)

# Skip early chunks (avoid imports)
results = retriever.query_by_metadata(
    query_text="implementation",
    where={"chunk_index": {"$ne": 0}},
    n_results=20
)
```

## Real-World Filtering Examples

### Example 1: Find API Endpoints Only

```python
retriever = CodeRetriever("fastapi_code")

# Get chunks from API folder, Python only, excluding tests
endpoints = retriever.query_by_metadata(
    query_text="GET POST endpoint route",
    where={
        "folder": "/app/api",
        "file_type": ".py",
        "filename": {"$nin": ["test.py", "conftest.py"]}
    },
    n_results=10
)

print(f"Found {len(endpoints)} API endpoint chunks")
for result in endpoints:
    print(f"  - {result['metadata']['filename']}")
```

### Example 2: Configuration Files Only

```python
retriever = CodeRetriever("config_code")

# Find all configuration-related chunks
configs = retriever.query_by_metadata(
    query_text="database connection settings",
    where={
        "file_type": {"$in": [".yaml", ".json", ".py", ".env"]},
        "folder": {"$in": ["/config", "/settings"]}
    },
    n_results=20
)

for result in configs:
    print(f"Config: {result['metadata']['filename']}")
    print(result['document'][:200] + "...\n")
```

### Example 3: Documentation Only

```python
retriever = CodeRetriever("docs_collection")

# Get documentation chunks
docs = retriever.query_by_metadata(
    query_text="how to use authentication",
    where={"file_type": ".md"},  # Markdown files only
    n_results=5
)

for result in docs:
    print(f"📚 {result['metadata']['filename']}")
    print(result['document'][:250] + "...\n")
```

### Example 4: Module Entry Points

```python
retriever = CodeRetriever("backend_code")

# Get __init__.py files (module entry points)
entry_points = retriever.query_by_metadata(
    query_text="imports exports public API",
    where={"filename": "__init__.py"},
    n_results=10
)

print("Module entry points:")
for result in entry_points:
    folder = result['metadata']['folder']
    print(f"  - {folder}")
```

### Example 5: Production Code Only

```python
retriever = CodeRetriever("full_project")

# Get production code (no tests, no examples)
production = retriever.query_by_metadata(
    query_text="user authentication flow",
    where={
        "folder": {"$nin": ["/tests", "/examples", "/docs"]},
        "filename": {
            "$nin": ["test.py", "conftest.py", "example.py", "demo.py"]
        },
        "file_type": ".py"
    },
    n_results=10
)

print("Production code matches:")
for result in production:
    print(f"  ✓ {result['metadata']['source']}")
```

## Filtering Patterns

### Find Related Files

```python
retriever = CodeRetriever("codebase")

# Find everything related to "user" feature
user_chunks = retriever.query_by_metadata(
    query_text="user authentication authorization management",
    where={
        "filename": {
            "$in": [
                "user.py",
                "auth.py",
                "user_service.py",
                "user_models.py"
            ]
        }
    },
    n_results=20
)
```

### Find Implementation vs Documentation

```python
retriever = CodeRetriever("full_project")

# Implementation (code only)
implementation = retriever.query_by_metadata(
    query_text="user login flow",
    where={"file_type": ".py"},
    n_results=5
)

# Documentation
docs = retriever.query_by_metadata(
    query_text="user login flow",
    where={"file_type": ".md"},
    n_results=5
)

print("Code implementations:")
for r in implementation:
    print(f"  - {r['metadata']['filename']}")

print("\nDocumentation:")
for r in docs:
    print(f"  - {r['metadata']['filename']}")
```

### Find by Directory Hierarchy

```python
retriever = CodeRetriever("codebase")

# Backend code
backend = retriever.query_by_metadata(
    query_text="API implementation",
    where={"folder": "/app/backend"},
    n_results=10
)

# Frontend code
frontend = retriever.query_by_metadata(
    query_text="component rendering",
    where={"folder": "/app/frontend"},
    n_results=10
)
```

## Performance Optimization

### Narrow Scope First

```python
# ❌ Slow: Search entire collection
results = retriever.query("authentication", n_results=50)

# ✅ Fast: Filter first, then search
results = retriever.query_by_metadata(
    "authentication",
    where={"folder": "/app/auth"},  # Reduces search space
    n_results=50
)
```

### Use Chunk Index Wisely

```python
# Skip imports and metadata (usually in first chunk)
results = retriever.query_by_metadata(
    query_text="implementation logic",
    where={"chunk_index": {"$ne": 0}},
    n_results=10
)
```

### Combine Query and Filter

```python
# Query narrows by semantics, filter by metadata
high_quality = retriever.query_by_metadata(
    query_text="specific pattern",
    where={"file_type": ".py"},
    n_results=10
)

# Filter for high relevance
relevant = [r for r in high_quality if r['distance'] < 0.35]
```

## Troubleshooting Filters

### Filter Returns No Results

```python
# Check if values exist
retriever = CodeRetriever("collection")

# First query without filters
all_results = retriever.query("your search", n_results=5)

# Check metadata in results
for result in all_results:
    print(f"File type: {result['metadata']['file_type']}")
    print(f"Folder: {result['metadata']['folder']}")

# Then use exact values in filter
```

### Filter Too Restrictive

```python
# Use $in for multiple values instead of exact match
results = retriever.query_by_metadata(
    query_text="models",
    where={
        "folder": {"$in": ["/models", "/schemas", "/entities"]}
    },
    n_results=10
)
```

### Case Sensitivity

```python
# Metadata is case-sensitive
results = retriever.query_by_metadata(
    query_text="code",
    where={"file_type": ".py"}  # Exactly ".py", not ".PY"
)
```

## Best Practices

✅ **Do:**
- Use filtering to reduce result size
- Combine semantic search with metadata filters
- Start broad, then narrow based on results
- Check metadata values before filtering
- Use `$in` for multiple acceptable values

❌ **Don't:**
- Use filters without understanding metadata
- Filter too narrowly (0 results)
- Ignore distance scores when filtering
- Mix different metadata sources
- Assume case-insensitive matching

## Next Steps

- 📝 [Retrieval Patterns](retrieval-patterns.md) - Query optimization
- 🔧 [Chunking Strategy](chunking-strategy.md) - Understand chunk creation
- 📖 [Basic Usage](basic-usage.md) - Core API guide
