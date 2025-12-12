#!/usr/bin/env python3
"""Test connection to ChromaDB on port 9500.

This script verifies that:
1. ChromaDB HTTP server is running and reachable
2. Connection can be established successfully
3. Collections can be listed (data is accessible)

Usage:
    python connect.py
    or
    uv run python connect.py
"""

import chromadb

print("🔌 Connecting to ChromaDB on port 9500...")

# Connect to your custom port
client = chromadb.HttpClient(host="localhost", port=9500)

try:
    # 1. Test the connection with a heartbeat
    heartbeat = client.heartbeat()
    print(f"✅ Connection successful! Server heartbeat: {heartbeat} nanoseconds")

    # 2. List existing collections to verify data
    collections = client.list_collections()
    print(f"📂 Found {len(collections)} collections: {[c.name for c in collections]}")

except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("👉 Make sure your 'uv run chroma run ...' terminal is still running!")
