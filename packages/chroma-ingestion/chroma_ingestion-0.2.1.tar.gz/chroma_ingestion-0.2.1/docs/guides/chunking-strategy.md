# Chunking Strategy

Deep dive into how chunks are created and how to optimize for your use case.

## Chunking Fundamentals

### What is a Chunk?

A **chunk** is a meaningful unit of code or documentation that:

1. **Is semantically complete** - Can be understood in isolation
2. **Fits in context window** - Usually 500-3000 tokens
3. **Has clear boundaries** - Starts at logical break point
4. **Preserves context** - Overlaps with adjacent chunks
5. **Has metadata** - Source file, position, folder, type

### Why Not Just Index Entire Files?

| Approach | Pros | Cons |
|----------|------|------|
| **Whole files** | Simple, fast | Loses precision, big chunks |
| **Chunks (1000 tokens)** | **Balanced** | **Recommended** |
| **Small chunks (500)** | High precision | Loses context |
| **Lines** | Maximum granularity | Too granular, poor semantics |

## Chunking Process

### Step 1: Read File

```
File: auth.py (2,500 tokens)
Content: Imports, classes, functions, docstrings
```

### Step 2: Identify Split Points

The splitter looks for logical boundaries in order:

1. **Double newline** (\n\n) - Section breaks
2. **Single newline** (\n) - Line breaks
3. **Space** - Word boundaries (fallback)

```
def login(email, password):
    """Authenticate user."""  # ← Split here (after docstring)

    user = find_user(email)   # ← Or here (between functions)
    if verify_password(...):
        return token
```

### Step 3: Create Chunks with Overlap

```
Chunk 1: [Tokens 0-1000] + [overlap: 800-1000]
Chunk 2: [Tokens 800-1800] + [overlap: 1600-1800]
Chunk 3: [Tokens 1600-2500]
```

**Why overlap?**
- Query matches "token verification" across boundary
- Context preserved for cross-chunk understanding
- Search results include surrounding context

### Step 4: Add Metadata

```python
{
    'source': '/app/auth.py',
    'filename': 'auth.py',
    'chunk_index': 2,
    'folder': '/app',
    'file_type': '.py'
}
```

## Configuration Guide

### Default Settings (Recommended Starting Point)

```python
CodeIngester(
    chunk_size=1000,      # Tokens per chunk
    chunk_overlap=200     # 20% overlap
)
```

✅ **Why this works:**
- 1000 tokens = ~3-4 sentences of prose, or 30-50 lines of code
- 200 token overlap = preserves cross-boundary context
- Handles most use cases: functions, classes, API docs

### Tuning for Different Code Types

#### Small Utility Functions

```python
CodeIngester(
    chunk_size=500,       # Smaller chunks for small functions
    chunk_overlap=100
)
```

**Best for:**
- Pure functions (< 50 lines)
- Utility libraries
- Single-responsibility modules

#### Complex Business Logic

```python
CodeIngester(
    chunk_size=1500,      # Larger chunks for complex code
    chunk_overlap=300
)
```

**Best for:**
- Multi-method classes
- Complex workflows
- Business logic that needs full context

#### API Documentation

```python
CodeIngester(
    chunk_size=1200,      # Balanced
    chunk_overlap=250
)
```

**Best for:**
- Docstrings and comments
- API references
- Mixed code and documentation

#### Machine Learning Code

```python
CodeIngester(
    chunk_size=2000,      # Larger for complex ML logic
    chunk_overlap=400
)
```

**Best for:**
- Training pipelines
- Model architectures
- Data processing workflows

### Advanced Tuning

#### For Maximum Precision (Finding Specific Code)

```python
CodeIngester(
    chunk_size=700,       # Smaller = more focused
    chunk_overlap=150
)
```

**Trade-off:** Lower relevance, need more results to cover scope

#### For Maximum Recall (Finding Related Concepts)

```python
CodeIngester(
    chunk_size=2000,      # Larger = more context
    chunk_overlap=500
)
```

**Trade-off:** Lower precision, broader matches

## Understanding Chunk Size in Tokens

### Token Counting Rules

| Content | ~Tokens |
|---------|---------|
| 1 word | 1-1.5 |
| 1 line of code | 15-25 |
| 1 line of prose | 3-5 |
| 1 function (10 lines) | 150-250 |
| 1 small class (50 lines) | 750-1250 |
| 1 docstring paragraph | 25-50 |

### Estimating Chunk Count

```
File size: 5000 tokens
Chunk size: 1000 tokens
Overlap: 200 tokens (20%)

Chunks = (5000 - 1000) / (1000 - 200) + 1 = 6 chunks
```

## Chunk Quality Metrics

### Semantic Coherence

**Good chunks:**
```python
def calculate_hash(data: bytes) -> str:
    """Calculate SHA256 hash of data.

    Args:
        data: Bytes to hash

    Returns:
        Hex-encoded hash string
    """
    import hashlib
    return hashlib.sha256(data).hexdigest()
```

**Bad chunks (split mid-function):**
```python
def calculate_hash(data: bytes) -> str:
    """Calculate SHA256 hash of data.

    Args:
        data: Bytes to hash

    [CHUNK BOUNDARY HERE - SPLIT FUNCTION!]

    Returns:
        Hex-encoded hash string
    """
```

### Coverage Analysis

```python
from chroma_ingestion import CodeIngester

# Check how many chunks a file creates
ingester = CodeIngester(
    target_folder="/path/to/code",
    chunk_size=1000,
    chunk_overlap=200
)

files = ingester.discover_files()
print(f"Total files: {len(files)}")

# After ingestion, check chunk distribution
retriever = CodeRetriever("my_collection")
info = retriever.get_collection_info()
print(f"Total chunks: {info['count']}")
print(f"Avg chunks per file: {info['count'] / len(files):.1f}")
```

## File-Specific Strategies

### Python Files

```python
# Python files: medium-large chunks (lots of whitespace)
CodeIngester(
    file_patterns=["**/*.py"],
    chunk_size=1200,
    chunk_overlap=250
)
```

**Why:** Python relies on indentation and structure

### Markdown Documentation

```python
# Markdown: flexible, respect headers
CodeIngester(
    file_patterns=["**/*.md"],
    chunk_size=1000,
    chunk_overlap=200
)
```

**Why:** Headers naturally divide content

### JavaScript/TypeScript

```python
# JS/TS: medium-small chunks (compact syntax)
CodeIngester(
    file_patterns=["**/*.{ts,tsx,js}"],
    chunk_size=800,
    chunk_overlap=150
)
```

**Why:** Compact syntax means more code per token

### YAML Configuration

```python
# YAML: small chunks (key-value pairs)
CodeIngester(
    file_patterns=["**/*.yaml", "**/*.yml"],
    chunk_size=500,
    chunk_overlap=100
)
```

**Why:** YAML is already well-structured

## Multi-Language Strategies

### Balanced Approach

```python
# When mixing languages, find middle ground
CodeIngester(
    target_folder="./project",
    file_patterns=[
        "**/*.py",
        "**/*.ts",
        "**/*.md"
    ],
    chunk_size=1000,      # Compromise
    chunk_overlap=200
)
```

### Language-Specific Collections

```python
# Better: separate collections by language

# Python code
python_ingester = CodeIngester(
    target_folder="./app/backend",
    file_patterns=["**/*.py"],
    collection_name="backend_python",
    chunk_size=1200,
    chunk_overlap=250
)

# TypeScript code
ts_ingester = CodeIngester(
    target_folder="./app/frontend",
    file_patterns=["**/*.ts", "**/*.tsx"],
    collection_name="frontend_typescript",
    chunk_size=900,
    chunk_overlap=180
)

# Documentation
docs_ingester = CodeIngester(
    target_folder="./docs",
    file_patterns=["**/*.md"],
    collection_name="docs_markdown",
    chunk_size=1000,
    chunk_overlap=200
)
```

## Measuring Effectiveness

### Test Query Relevance

```python
from chroma_ingestion import CodeIngester, CodeRetriever

# After ingestion
retriever = CodeRetriever("my_collection")

# Test queries that should find relevant code
test_cases = [
    ("error handling", ["exception", "try", "catch"]),
    ("database query", ["cursor", "execute", "select"]),
    ("API endpoint", ["route", "request", "response"]),
]

for query, keywords in test_cases:
    results = retriever.query(query, n_results=3)

    if results and results[0]['distance'] < 0.4:
        print(f"✅ '{query}' - Good match")
    else:
        print(f"❌ '{query}' - Poor match (adjust chunk size)")
```

### Distance Distribution

```python
retriever = CodeRetriever("my_collection")

# Check distance distribution
test_query = "common pattern in your code"
results = retriever.query(test_query, n_results=50)

distances = [r['distance'] for r in results]
good = len([d for d in distances if d < 0.4])
fair = len([d for d in distances if 0.4 <= d < 0.6])
poor = len([d for d in distances if d >= 0.6])

print(f"Good (< 0.4):  {good}/50 ({100*good/50:.0f}%)")
print(f"Fair (0.4-0.6): {fair}/50 ({100*fair/50:.0f}%)")
print(f"Poor (> 0.6):  {poor}/50 ({100*poor/50:.0f}%)")

# Target: > 50% good matches
```

## Best Practices Checklist

- [ ] Start with default chunk_size=1000, chunk_overlap=200
- [ ] Test with actual queries from your use case
- [ ] Monitor distance scores - aim for < 0.4 on 50%+ of results
- [ ] Adjust chunk_size up if losing context, down if too broad
- [ ] Keep different file types in separate collections if possible
- [ ] Document your chosen configuration in README
- [ ] Re-ingest after chunk size changes to update collection
- [ ] Test with edge cases (very long functions, large classes)

## Troubleshooting

### "Chunks too large (over 3000 tokens)"

```python
# Reduce chunk size
CodeIngester(chunk_size=1000, chunk_overlap=200)
```

### "Too many false positives"

```python
# Smaller chunks with less overlap
CodeIngester(chunk_size=700, chunk_overlap=100)
```

### "Missing relevant context"

```python
# Larger chunks with more overlap
CodeIngester(chunk_size=1500, chunk_overlap=400)
```

### "Uneven chunk distribution"

```python
# Increase overlap to handle sparse files
CodeIngester(chunk_size=1000, chunk_overlap=400)
```

## Next Steps

- 📚 [Ingestion Workflow](ingestion-workflow.md) - Full ingestion guide
- 🔍 [Retrieval Patterns](retrieval-patterns.md) - Query optimization
- 🎯 [Advanced Filtering](advanced-filtering.md) - Filter results by metadata
