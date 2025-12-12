# Troubleshooting

Solutions for common issues and errors.

## Connection Issues

### Cannot Connect to Chroma Server

**Error:** `ConnectionError: Failed to connect to http://localhost:9500`

**Causes:**
- Chroma server not running
- Wrong host/port configuration
- Network connectivity issues

**Solutions:**

```bash
# Start Chroma with Docker
docker-compose up -d

# Or run with Python
chroma run

# Check connection
curl http://localhost:9500/api/v1/heartbeat
```

### CORS Errors

**Error:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Cause:** Chroma server is not allowing requests from your client

**Solution:** Ensure Chroma is running and accessible:

```bash
# In docker-compose.yml, Chroma port should be exposed
docker-compose down && docker-compose up -d
```

## Ingestion Issues

### Out of Memory During Ingestion

**Error:** `MemoryError` or process killed

**Causes:**
- Batch size too large
- Too many files at once
- Chunk size too large

**Solutions:**

```python
# 1. Reduce batch size
ingester.ingest_files(batch_size=25)  # Was 100

# 2. Reduce chunk size
CodeIngester(chunk_size=500)  # Was 1000

# 3. Ingest by folder separately
folder1 = CodeIngester("/path/to/folder1")
folder1.ingest_files()

folder2 = CodeIngester("/path/to/folder2")
folder2.ingest_files()
```

### No Files Found

**Error:** `ValueError: No files found matching patterns`

**Cause:** File patterns don't match any files

**Solutions:**

```python
# Check patterns
ingester = CodeIngester(
    target_folder="/path/to/code",
    file_patterns=["**/*.py", "**/*.md"]  # Add patterns
)

# Verify folder exists
files = ingester.discover_files()
print(f"Found {len(files)} files")

# If empty, try broader patterns
ingester = CodeIngester(
    target_folder="/path/to/code",
    file_patterns=["**/*"]  # Match all files
)
```

### Collection Already Has Chunks

**Error:** `Expected IDs to be unique` or similar

**Cause:** Re-ingesting same files without clearing old chunks

**Solutions:**

```python
# Option 1: Use upsert (default) - automatically handles duplicates
ingester.ingest_files()  # Safe to run multiple times

# Option 2: Delete collection first
from chroma_ingestion import delete_collection
delete_collection("my_collection")
ingester.ingest_files()

# Option 3: Reset client
from chroma_ingestion import reset_client
reset_client()
```

### File Encoding Issues

**Error:** `UnicodeDecodeError` or similar

**Cause:** File uses non-UTF-8 encoding

**Solutions:**

```python
# Check file encoding
file_path = "/path/to/problematic_file"

# Try converting to UTF-8
import chardet
with open(file_path, 'rb') as f:
    raw = f.read()
    result = chardet.detect(raw)
    print(f"Detected encoding: {result['encoding']}")

# Exclude problematic files
ingester = CodeIngester(
    target_folder="/path/to/code",
    file_patterns=["**/*.py", "**/*.md"]  # More specific patterns
)
```

## Retrieval Issues

### No Results from Query

**Error:** Empty result list or all results have high distance

**Causes:**
- Query too specific or vague
- Chunks don't contain relevant content
- Distance threshold too strict

**Solutions:**

```python
# 1. Broaden the query
results = retriever.query("authentication", n_results=10)

# 2. Increase results
results = retriever.query(query, n_results=20)  # vs 5

# 3. Check distance threshold
results = retriever.query_semantic(
    query,
    distance_threshold=0.6  # Less strict (was 0.3)
)

# 4. Verify collection has data
info = retriever.get_collection_info()
print(f"Collection has {info['count']} chunks")
```

### Poor Relevance Quality

**Error:** Results don't match query intent

**Causes:**
- Chunk size too large or too small
- Collection not re-ingested after chunk changes
- Query terminology doesn't match code

**Solutions:**

```python
# 1. Check chunk distribution
info = retriever.get_collection_info()
avg = info['count'] / (len(files) if hasattr(info, 'files') else 1)

# 2. Re-ingest with different chunk size
ingester = CodeIngester(
    chunk_size=1200,  # Adjusted from 1000
    chunk_overlap=250
)
delete_collection("my_collection")
ingester.ingest_files()

# 3. Use domain-specific language
results = retriever.query(
    "FastAPI GET endpoint with dependency injection",
    n_results=5
)
```

### Too Many False Positives

**Error:** Irrelevant results mixed with good ones

**Solutions:**

```python
# 1. Use higher distance threshold
results = retriever.query_semantic(
    query,
    distance_threshold=0.2  # Stricter
)

# 2. Filter by metadata
results = retriever.query_by_metadata(
    query,
    where={"file_type": ".py"},  # More specific
    n_results=5
)

# 3. Reduce chunk size
CodeIngester(chunk_size=700, chunk_overlap=150)
```

## CLI Issues

### Command Not Found

**Error:** `chroma-ingest: command not found`

**Cause:** Package not installed or not in PATH

**Solutions:**

```bash
# Install package
pip install chroma-ingestion

# Verify installation
pip show chroma-ingestion

# Try full path
python -m chroma_ingestion.cli ingest --help

# Or use Python API directly
python -c "from chroma_ingestion import CodeIngester; ..."
```

### Permission Denied

**Error:** `PermissionError` when accessing files

**Cause:** Insufficient permissions on target folder

**Solutions:**

```bash
# Check permissions
ls -la /path/to/folder

# Grant read permissions
chmod -R +r /path/to/folder

# Or run with elevated privileges (not recommended)
sudo python script.py
```

## Testing Issues

### Tests Fail When Chroma Server Offline

**Error:** Connection errors in tests

**Solution:** Ensure test infrastructure is running

```bash
# Start Docker containers for tests
docker-compose -f docker-compose.test.yml up -d

# Or skip integration tests
pytest tests/unit/ -v

# Run full test suite
pytest tests/ -v
```

### Flaky Tests

**Error:** Tests pass sometimes, fail other times

**Causes:**
- Race conditions in async code
- Network timeouts
- Port already in use

**Solutions:**

```bash
# Increase test timeout
pytest --timeout=30 tests/

# Run tests sequentially
pytest -n0 tests/

# Check for port conflicts
lsof -i :9500  # Check if Chroma port is in use

# Kill process on port
kill -9 <PID>
```

## Performance Issues

### Slow Ingestion

**Error:** Ingestion takes too long

**Solutions:**

```python
# 1. Increase batch size
ingester.ingest_files(batch_size=500)

# 2. Use smaller chunk overlap
CodeIngester(chunk_overlap=100)  # Was 200

# 3. Reduce chunk size
CodeIngester(chunk_size=700)

# 4. Ingest large codebases in parts
# Process multiple folders in parallel
from multiprocessing import Pool

folders = ["/app/backend", "/app/frontend", "/app/api"]
for folder in folders:
    CodeIngester(target_folder=folder).ingest_files()
```

### Slow Queries

**Error:** Queries take > 1 second

**Solutions:**

```python
# 1. Use smaller result set
results = retriever.query(query, n_results=3)  # vs 20

# 2. Filter before querying
results = retriever.query_by_metadata(
    query,
    where={"folder": "/app/specific_folder"},
    n_results=5
)

# 3. Check Chroma server load
# Monitor Chroma logs: docker logs chroma
```

## Data Issues

### Missing Chunks

**Error:** Expected chunks not returned

**Cause:** Files not ingested or filtered out

**Solutions:**

```python
# 1. Verify files were discovered
files = ingester.discover_files()
print(f"Found {len(files)} files")

# 2. Check if file is in collection
results = retriever.get_by_source("specific_file.py")
print(f"Found {len(results)} chunks from file")

# 3. Re-ingest missing files
ingester.ingest_files()
```

### Metadata Inconsistencies

**Error:** Metadata filters return unexpected results

**Solutions:**

```python
# 1. Check actual metadata values
results = retriever.query("any", n_results=1)
print(results[0]['metadata'])

# 2. Verify filter syntax
results = retriever.query_by_metadata(
    "test",
    where={"file_type": ".py"}  # Exact match
)

# 3. Use correct operators
results = retriever.query_by_metadata(
    "test",
    where={"filename": {"$in": ["file1.py", "file2.py"]}}
)
```

## Getting Help

### Debug Information

When reporting issues, include:

```python
from chroma_ingestion import get_chroma_client

# System info
import sys
print(f"Python: {sys.version}")

# Package version
import chroma_ingestion
print(f"chroma-ingestion: {chroma_ingestion.__version__}")

# Collection info
retriever = CodeRetriever("my_collection")
print(retriever.get_collection_info())

# Connection test
try:
    client = get_chroma_client()
    print("✓ Chroma connection successful")
except Exception as e:
    print(f"✗ Connection failed: {e}")
```

### Support Resources

- 📖 [Documentation](../index.md) - Complete guide
- 💬 [GitHub Issues](https://github.com/your-org/chroma-ingestion/issues) - Report bugs
- 🐛 [Test Suite](../../tests/) - See working examples
- 📚 [Examples](../../examples/) - Reference implementations

## Next Steps

- 🔧 [Configuration](../getting-started/configuration.md) - Advanced setup
- 📚 [Guides](../guides/ingestion-workflow.md) - Detailed walkthroughs
- 💡 [Best Practices](../guides/chunking-strategy.md) - Optimization tips
