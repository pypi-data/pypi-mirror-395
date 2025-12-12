# Installation

## From PyPI (Recommended)

The easiest way to install chroma-ingestion:

```bash
pip install chroma-ingestion
```

## From Source

For development or latest features:

```bash
git clone https://github.com/chroma-core/chroma-ingestion.git
cd chroma-ingestion
pip install -e ".[dev]"
```

## Requirements

- **Python:** 3.11 or higher
- **Chroma:** Running Chroma instance (local or Cloud)
- **Optional:** Docker (for running Chroma locally)

## Verify Installation

```bash
# Test imports
python -c "from chroma_ingestion import CodeIngester; print('✅ Installation successful')"

# Test CLI
chroma-ingest --help
```

## Running Chroma Locally (Optional)

For local development without Chroma Cloud:

### Option 1: Docker Compose (Recommended)

```bash
docker-compose up -d
```

This starts Chroma on `localhost:8000`

### Option 2: Docker

```bash
docker run -p 8000:8000 ghcr.io/chroma-core/chroma:latest
```

### Option 3: Python Package

```bash
pip install chroma
chroma run
```

## Configuration

### Using Chroma Cloud

Set environment variables:

```bash
export CHROMA_HOST=api.chroma.com
export CHROMA_PORT=443
```

Or in `.env` file:

```
CHROMA_HOST=api.chroma.com
CHROMA_PORT=443
```

### Using Local Chroma

Default configuration uses `localhost:8000`:

```bash
# Start Chroma
docker-compose up -d

# Use chroma-ingestion (no config needed)
chroma-ingest ./code --collection my_collection
```

## Troubleshooting

### Connection Error to Chroma

```
Error: Could not connect to Chroma at localhost:8000
```

**Solution:**
1. Verify Chroma is running: `curl http://localhost:8000/api/v1/heartbeat`
2. Check host/port configuration in `.env`
3. Start Chroma: `docker-compose up -d`

### Import Error

```
ImportError: No module named chroma_ingestion
```

**Solution:**
```bash
# Reinstall
pip install --force-reinstall chroma-ingestion

# Or from source
pip install -e .
```

## Development Setup

For contributing to chroma-ingestion:

```bash
# Clone repository
git clone https://github.com/chroma-core/chroma-ingestion.git
cd chroma-ingestion

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking
mypy src/chroma_ingestion
```

## Next Steps

- 🚀 [Quick Start](quick-start.md) - Try it out
- ⚙️ [Configuration](configuration.md) - Setup guide
- 📚 [User Guides](../guides/basic-usage.md) - Learn more
