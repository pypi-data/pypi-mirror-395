# Configuration

## Environment Variables

Chroma-ingestion uses environment variables for configuration. You can set these in your shell or in a `.env` file.

### Chroma Connection

#### Cloud Connection

```bash
# Using Chroma Cloud
CHROMA_HOST=api.chroma.com
CHROMA_PORT=443
```

#### Local Connection

```bash
# Using local Chroma instance
CHROMA_HOST=localhost
CHROMA_PORT=8000  # default
```

### Client Configuration

The singleton client is configured once when first imported:

```python
from chroma_ingestion import get_chroma_client

# Uses env vars from environment or .env file
client = get_chroma_client()
```

## .env File Example

Create a `.env` file in your project root:

```
# Chroma Local Connection
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Or Chroma Cloud
# CHROMA_HOST=api.chroma.com
# CHROMA_PORT=443
```

## Python Configuration

Set environment variables before importing:

```python
import os

os.environ['CHROMA_HOST'] = 'api.chroma.com'
os.environ['CHROMA_PORT'] = '443'

# Now import
from chroma_ingestion import CodeIngester
```

Or load from `.env`:

```python
from dotenv import load_dotenv

load_dotenv()  # Loads .env file
from chroma_ingestion import CodeIngester
```

## Default Values

If not configured, chroma-ingestion defaults to:

```
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

This is perfect for local development with Chroma running via Docker.

## Resetting Client Connection

If you need to change configuration after importing:

```bash
# Via CLI
chroma-ingest reset-client

# Via Python
from chroma_ingestion.clients.chroma import reset_chroma_client
reset_chroma_client()
```

## Troubleshooting Configuration

### "Could not authenticate with Chroma"

```
❌ Error connecting to Chroma
```

**Check:**
1. Chroma is running: `curl http://localhost:8000/api/v1/heartbeat`
2. Host and port are correct
3. Network connectivity if using Cloud

### "Invalid hostname"

```
❌ Invalid CHROMA_HOST: invalid.host.com
```

**Solution:**
- Verify hostname spelling
- Check DNS resolution: `ping api.chroma.com`
- Use IP address if hostname fails

## Advanced Configuration

### Custom Client Initialization

See [Architecture: Singleton Pattern](../architecture/singleton-pattern.md) for advanced configuration options.

## Next Steps

- 🚀 [Quick Start](quick-start.md) - Get started
- 📚 [User Guides](../guides/basic-usage.md) - Learn more
