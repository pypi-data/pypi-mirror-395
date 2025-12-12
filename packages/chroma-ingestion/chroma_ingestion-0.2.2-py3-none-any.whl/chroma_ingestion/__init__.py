"""Chroma Ingestion - Semantic code search for ChromaDB.

A semantic-aware code extraction and storage system that intelligently chunks code
repositories and stores them in Chroma Cloud for AI agent retrieval and context generation.
"""

from chroma_ingestion.clients.chroma import get_chroma_client
from chroma_ingestion.ingestion.agents import AgentIngester
from chroma_ingestion.ingestion.base import CodeIngester
from chroma_ingestion.retrieval.retriever import CodeRetriever, MultiCollectionSearcher

__all__ = [
    "AgentIngester",
    "CodeIngester",
    "CodeRetriever",
    "MultiCollectionSearcher",
    "get_chroma_client",
]

__version__ = "0.2.0"
