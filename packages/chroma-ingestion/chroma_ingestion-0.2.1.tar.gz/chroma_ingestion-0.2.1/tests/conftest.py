"""Shared pytest fixtures for all tests.

This module provides reusable fixtures for unit and integration tests,
including temporary files, mock clients, and database setup.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def tmp_code_folder(tmp_path: Path) -> Path:
    """Create a temporary folder with sample code files for testing.

    Returns:
        Path to temporary folder containing sample Python and Markdown files.
    """
    # Create sample Python file
    py_file = tmp_path / "example.py"
    py_file.write_text(
        """\"\"\"Example module for testing.\"\"\"

def hello_world():
    \"\"\"Print hello world.\"\"\"
    print("Hello, World!")

class Calculator:
    \"\"\"Simple calculator for testing.\"\"\"

    def add(self, a: int, b: int) -> int:
        \"\"\"Add two numbers.\"\"\"
        return a + b
"""
    )

    # Create sample Markdown file
    md_file = tmp_path / "README.md"
    md_file.write_text(
        """# Example Project

This is a test project for code ingestion.

## Features

- Testing
- Documentation
- Code organization

## Usage

```python
calculator = Calculator()
result = calculator.add(2, 3)
print(result)  # Output: 5
```
"""
    )

    return tmp_path


@pytest.fixture
def sample_agent_files(tmp_path: Path) -> Path:
    """Create a temporary folder with sample agent markdown files.

    Returns:
        Path to temporary folder containing .agent.md files.
    """
    # Create sample agent file
    agent_file = tmp_path / "auth_agent.agent.md"
    agent_file.write_text(
        """---
name: Authentication Agent
description: Handles user authentication and token management
version: 1.0.0
---

# Authentication Agent

Manages user authentication, JWT tokens, and authorization.

## Endpoints

### POST /api/auth/login
Authenticate user with credentials.

```python
@router.post("/auth/login")
async def login(credentials: LoginRequest):
    # Validate credentials
    # Generate JWT token
    # Return token
    pass
```

### GET /api/auth/me
Get current user info.

```python
@router.get("/api/auth/me")
async def get_current_user(token: str = Depends(get_token)):
    # Verify token
    # Return user info
    pass
```

## Security

- Uses JWT tokens
- Implements refresh token rotation
- Rate limits login attempts
"""
    )

    # Create another sample agent
    service_file = tmp_path / "payment_service.agent.md"
    service_file.write_text(
        """---
name: Payment Service Agent
description: Handles payment processing and transactions
version: 2.1.0
---

# Payment Service Agent

Manages payment processing, invoicing, and transaction history.

## Core Functions

- Process credit card payments
- Handle refunds
- Generate invoices
- Track transaction history
"""
    )

    return tmp_path


@pytest.fixture
def mock_chroma_client() -> MagicMock:
    """Create a mock ChromaDB client for unit testing.

    Returns:
        MagicMock object configured as a ChromaDB client.
    """
    mock_client = MagicMock()

    # Configure mock collection
    mock_collection = MagicMock()
    mock_collection.count.return_value = 100
    mock_collection.get.return_value = {
        "ids": ["1", "2"],
        "documents": ["doc1", "doc2"],
        "metadatas": [{"source": "file1"}, {"source": "file2"}],
    }
    mock_collection.query.return_value = {
        "ids": [["1", "2"]],
        "documents": [["doc1", "doc2"]],
        "distances": [[0.1, 0.2]],
        "metadatas": [[{"source": "file1"}, {"source": "file2"}]],
    }
    mock_collection.upsert.return_value = None

    mock_client.get_collection.return_value = mock_collection
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_client.list_collections.return_value = ["test_collection"]

    return mock_client


@pytest.fixture
def chroma_config() -> dict:
    """Provide default ChromaDB configuration for testing.

    Returns:
        Dictionary with ChromaDB connection parameters.
    """
    return {
        "host": "localhost",
        "port": 9500,
        "is_persistent": False,
    }


@pytest.fixture
def ingestion_params() -> dict:
    """Provide standard ingestion parameters for testing.

    Returns:
        Dictionary with ingestion configuration.
    """
    return {
        "chunk_size": 500,  # Smaller for testing
        "chunk_overlap": 100,
        "batch_size": 10,
    }


@pytest.fixture
def sample_query() -> str:
    """Provide a sample query for testing retrieval.

    Returns:
        Sample natural language query string.
    """
    return "How do I authenticate users in this codebase?"
