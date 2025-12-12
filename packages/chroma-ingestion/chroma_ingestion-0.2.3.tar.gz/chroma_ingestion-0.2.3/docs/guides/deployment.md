# Deployment & Hosting

Guide to deploying chroma-ingestion in production environments.

## Docker Deployment

### Local Development with Docker Compose

Start Chroma server locally for development:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f chroma

# Stop services
docker-compose down
```

**Docker Compose Configuration:**

```yaml
version: '3.8'
services:
  chroma:
    image: ghcr.io/chroma-core/chroma:latest
    environment:
      IS_PERSISTENT: 'TRUE'
      CHROMA_DB_IMPL: duckdb+parquet
      CHROMA_DATA_VOLUME_PATH: /chroma/data
    ports:
      - "9500:8000"
    volumes:
      - ./chroma_data:/chroma/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Production Chroma Cloud

For production use, deploy to Chroma Cloud:

```bash
# Set environment variables
export CHROMA_HOST=api.chroma.com
export CHROMA_PORT=443
export CHROMA_API_KEY=your-api-key

# Your app now connects to cloud
python -c "from chroma_ingestion import get_chroma_client; print('Connected')"
```

## Package Deployment

### PyPI Release

The package is published to PyPI automatically via GitHub Actions.

#### Manual PyPI Release (if needed)

```bash
# Build distribution
python -m build

# Test on TestPyPI first
twine upload -r testpypi dist/*

# Verify on https://test.pypi.org/project/chroma-ingestion/

# Upload to production PyPI
twine upload dist/*

# Verify on https://pypi.org/project/chroma-ingestion/
```

#### TestPyPI Testing

```bash
# Install from TestPyPI
pip install -i https://test.pypi.org/simple/ chroma-ingestion==X.Y.ZrcN

# Test installation
chroma-ingest --help
```

### GitHub Releases

Releases are automatically created when publishing:

```bash
# Version tag (auto-creates release)
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0

# GitHub Actions automatically:
# 1. Builds distribution
# 2. Publishes to PyPI
# 3. Creates GitHub Release
```

## Application Deployment

### Django/FastAPI Integration

```python
# fastapi_app.py
from fastapi import FastAPI
from chroma_ingestion import CodeRetriever

app = FastAPI()

# Initialize retriever (reuse across requests)
retriever = CodeRetriever("my_collection")

@app.get("/search")
async def search(q: str):
    results = retriever.query(q, n_results=5)
    return {"results": results}

@app.on_event("startup")
async def startup():
    # Ingest code on startup if needed
    pass
```

### Production Considerations

1. **Connection Pooling:** Use singleton pattern (built-in)
   ```python
   from chroma_ingestion import get_chroma_client
   # Same client used across app
   ```

2. **Error Handling:**
   ```python
   try:
       results = retriever.query(query)
   except ConnectionError:
       # Handle Chroma server down
       return {"error": "Search unavailable"}
   except Exception as e:
       # Log and handle gracefully
       logger.error(f"Query failed: {e}")
   ```

3. **Timeouts:**
   ```python
   # Set connection timeout
   import os
   os.environ["CHROMA_REQUEST_TIMEOUT"] = "30"
   ```

4. **Rate Limiting:**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def cached_query(q: str):
       return retriever.query(q, n_results=5)
   ```

## Kubernetes Deployment

### Chroma Deployment

```yaml
# chroma-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chroma
spec:
  replicas: 1
  selector:
    matchLabels:
      app: chroma
  template:
    metadata:
      labels:
        app: chroma
    spec:
      containers:
      - name: chroma
        image: ghcr.io/chroma-core/chroma:latest
        ports:
        - containerPort: 8000
        env:
        - name: IS_PERSISTENT
          value: "TRUE"
        - name: CHROMA_DATA_VOLUME_PATH
          value: /chroma/data
        volumeMounts:
        - name: chroma-data
          mountPath: /chroma/data
        livenessProbe:
          httpGet:
            path: /api/v1/heartbeat
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
      volumes:
      - name: chroma-data
        persistentVolumeClaim:
          claimName: chroma-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: chroma-service
spec:
  selector:
    app: chroma
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: chroma-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### App Deployment

```yaml
# app-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: app
        image: my-app:1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: CHROMA_HOST
          value: "chroma-service"
        - name: CHROMA_PORT
          value: "8000"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Monitoring & Logging

### Health Checks

```python
# health_check.py
from chroma_ingestion import get_chroma_client

def health_check():
    try:
        client = get_chroma_client()
        # Test connection
        client.heartbeat()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    ingester = CodeIngester(...)
    files, chunks = ingester.ingest_files()
    logger.info(f"Ingested {files} files, {chunks} chunks")
except Exception as e:
    logger.error(f"Ingestion failed: {e}")
```

### Metrics

```python
from prometheus_client import Counter, Histogram
import time

query_count = Counter('chroma_queries_total', 'Total queries')
query_duration = Histogram('chroma_query_duration_seconds', 'Query duration')

@query_duration.time()
def monitored_query(retriever, query):
    query_count.inc()
    return retriever.query(query)
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ingest-and-deploy.yml
name: Ingest and Deploy

on:
  push:
    branches: [main]

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install chroma-ingestion
          docker-compose up -d

      - name: Wait for Chroma
        run: |
          until curl http://localhost:9500/api/v1/heartbeat; do
            sleep 1
          done

      - name: Ingest code
        run: |
          python -c "
          from chroma_ingestion import CodeIngester
          ingester = CodeIngester('./src')
          files, chunks = ingester.ingest_files()
          print(f'Ingested {files} files, {chunks} chunks')
          "

      - name: Deploy
        run: |
          # Deploy to production
          kubectl apply -f k8s/
```

## Backup & Recovery

### Backup Strategy

```bash
# Backup Chroma data
docker cp chroma_data:/chroma/data ./backups/chroma-$(date +%s)

# Or with volumes
docker run --volumes-from chroma -v $(pwd)/backups:/backup \
  alpine tar czf /backup/chroma.tar.gz /chroma/data
```

### Recovery

```bash
# Restore Chroma data
docker cp ./backups/chroma-backup chroma_data:/chroma/data

# Or rebuild from source
from chroma_ingestion import CodeIngester
CodeIngester("/path/to/source").ingest_files()
```

## Environment Setup

### Production Environment Variables

```bash
# .env.production
CHROMA_HOST=api.chroma.com
CHROMA_PORT=443
CHROMA_API_KEY=<your-api-key>

# Optional: Request timeout
CHROMA_REQUEST_TIMEOUT=60

# Optional: Disable SSL verification (not recommended)
# CHROMA_SSL_VERIFY=false

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Security

### API Key Management

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("CHROMA_API_KEY")

if not api_key:
    raise ValueError("CHROMA_API_KEY not set")
```

### Network Security

```yaml
# Use private network for Chroma
apiVersion: v1
kind: Service
metadata:
  name: chroma-internal
spec:
  type: ClusterIP  # Not exposed externally
  selector:
    app: chroma
  ports:
  - port: 8000
    targetPort: 8000
```

### Data Protection

- Use TLS for all connections
- Enable authentication on Chroma API
- Encrypt data at rest (Chroma Cloud handles this)
- Regular backups

## Troubleshooting Deployment

### Connection Issues in Production

```python
# Debug connection
import os
print(f"CHROMA_HOST: {os.getenv('CHROMA_HOST')}")
print(f"CHROMA_PORT: {os.getenv('CHROMA_PORT')}")

try:
    from chroma_ingestion import get_chroma_client
    client = get_chroma_client()
    print("✓ Connected to Chroma")
except Exception as e:
    print(f"✗ Connection failed: {e}")
```

### Performance Issues

```bash
# Monitor Chroma
docker logs -f chroma

# Check resource usage
docker stats chroma

# Increase resources
docker-compose.yml: memory limit, CPU limit
```

## Next Steps

- 📖 [Configuration](../getting-started/configuration.md) - Environment setup
- 🔧 [Guides](../guides/ingestion-workflow.md) - Detailed walkthroughs
- 🐛 [Troubleshooting](troubleshooting.md) - Common issues
