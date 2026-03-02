# WP-Agents Memory System

A Python-based memory management system with semantic filtering using sentence transformers.

## Structure

```
memory/
    __init__.py
    filter.py          # Memory filters (DateFilter, CrossEncoderFilter)
    memories.py        # MemoryManager for orchestrating memory operations
    memory_repository.py  # Abstract repository interface
    memory.py          # Core Memory class
    summarizer.py      # Abstract summarizer interface

user/
    __init__.py
    user.py           # User class
```

## Setup

The project uses a Python virtual environment with the following packages:
- `sentence-transformers`: For semantic similarity using cross-encoders
- `torch`: PyTorch backend for transformers
- `transformers`: Hugging Face transformers library

To activate the virtual environment:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

## Usage

### CrossEncoderFilter with Sentence Transformers

The `CrossEncoderFilter` uses sentence transformers' cross-encoder models for semantic filtering:

```python
from memory import CrossEncoderFilter, Memory
from datetime import datetime

# Initialize the filter
filter = CrossEncoderFilter(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")

# Create some memories
memories = [
    Memory("The user prefers Python over TypeScript", datetime.now()),
    Memory("The weather is sunny today", datetime.now()),
    Memory("Machine learning is fascinating", datetime.now()),
]

# Filter memories by relevance to a query
query = "What programming language does the user like?"
relevant_memories = await filter.filter(iter(memories), query)
```

### Available Cross-Encoder Models

- `cross-encoder/ms-marco-MiniLM-L-6-v2` (default): Fast and effective for semantic search
- `cross-encoder/nli-deberta-v3-base`: Natural Language Inference based
- `cross-encoder/ms-marco-TinyBERT-L-2-v2`: Faster, smaller model

## Features

- **Semantic Memory Filtering**: Uses cross-encoder models to find semantically relevant memories
- **Date-based Filtering**: Filter memories by timestamp
- **Extensible Architecture**: Abstract interfaces for filters, repositories, and summarizers
- **Async Support**: Async/await pattern for I/O operations
