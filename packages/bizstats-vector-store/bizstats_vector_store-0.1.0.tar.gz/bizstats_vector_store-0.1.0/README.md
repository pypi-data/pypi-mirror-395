# @bizstats/vector-store

Milvus vector database wrapper with embedding generation and semantic search for BizStats applications.

## Features

- **Milvus Integration**: Full-featured Milvus client with collection management
- **Multiple Embedding Providers**: Support for Ollama, OpenAI, and custom HTTP endpoints
- **Document Chunking**: Smart document splitting with overlap for context preservation
- **Semantic Search**: Vector similarity search with hybrid keyword boosting
- **Redis Caching**: Optional embedding cache for improved performance
- **Two Collection Types**:
  - Chat message embeddings (single collection)
  - Knowledge base embeddings (per-project collections)

## Installation

```bash
# Core package (requires Milvus connection)
pip install bizstats-vector-store

# With Ollama support
pip install bizstats-vector-store[ollama]

# With OpenAI support
pip install bizstats-vector-store[openai]

# Full installation with all providers
pip install bizstats-vector-store[all]

# Development dependencies
pip install bizstats-vector-store[dev]
```

## Quick Start

### Configuration

```python
from bizstats_vector_store import configure

# Configure with environment variables (recommended)
# Set: VECTOR_STORE_MILVUS_HOST, VECTOR_STORE_OLLAMA_BASE_URL, etc.

# Or configure programmatically
configure(
    milvus_host="localhost",
    milvus_port=19530,
    embedding_provider="ollama",
    embedding_model="mxbai-embed-large:latest",
    ollama_base_url="http://localhost:11434",
)
```

### Document Embedding

```python
from bizstats_vector_store import DocumentChunker, EmbeddingGenerator, CollectionManager
from bizstats_vector_store.models import CollectionType

# Initialize components
chunker = DocumentChunker(max_tokens=500, overlap_tokens=50)
embedding_gen = EmbeddingGenerator()
collection_mgr = CollectionManager()

# Chunk a document
chunks = chunker.chunk_document(
    content="Your document content here...",
    document_id="doc-123",
    project_id="project-456",
    document_title="My Document",
    document_type="text",
)

# Generate embeddings
for chunk in chunks:
    result = await embedding_gen.generate(chunk.content)
    print(f"Generated {len(result.embedding)}-dim embedding")

# Store in Milvus
collection = await collection_mgr.ensure_collection(
    CollectionType.KNOWLEDGE_BASE,
    project_id="project-456",
)
```

### Semantic Search

```python
from bizstats_vector_store import SemanticSearch
from bizstats_vector_store.models import KnowledgeSearchRequest

search = SemanticSearch()

# Search knowledge base with hybrid search
request = KnowledgeSearchRequest(
    query="What is machine learning?",
    project_id="project-456",
    limit=10,
    score_threshold=0.6,
    hybrid_search=True,
)

response = await search.search_knowledge_base(request)
for result in response.results:
    print(f"Score: {result.score:.3f} - {result.title}")
    print(f"  {result.chunk_content[:100]}...")
```

### Chat Message Search

```python
from bizstats_vector_store.models import SearchRequest

request = SearchRequest(
    query="How do I reset my password?",
    limit=5,
    conversation_id="conv-789",  # Optional filter
    score_threshold=0.7,
)

response = await search.search_chat_messages(request)
for result in response.results:
    print(f"Score: {result.score:.3f} - {result.content_preview}")
```

## Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `VECTOR_STORE_MILVUS_HOST` | `localhost` | Milvus server host |
| `VECTOR_STORE_MILVUS_PORT` | `19530` | Milvus server port |
| `VECTOR_STORE_EMBEDDING_PROVIDER` | `ollama` | Provider: ollama, openai, httpx |
| `VECTOR_STORE_EMBEDDING_MODEL` | `mxbai-embed-large:latest` | Embedding model name |
| `VECTOR_STORE_EMBEDDING_DIMENSION` | `1024` | Embedding vector dimension |
| `VECTOR_STORE_OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `VECTOR_STORE_OLLAMA_API_KEY` | - | Ollama API key (optional) |
| `VECTOR_STORE_OPENAI_API_KEY` | - | OpenAI API key |
| `VECTOR_STORE_REDIS_URL` | - | Redis URL for caching |
| `VECTOR_STORE_CACHE_TTL_SECONDS` | `3600` | Cache TTL in seconds |
| `VECTOR_STORE_CHUNK_MAX_TOKENS` | `500` | Max tokens per chunk |
| `VECTOR_STORE_CHUNK_OVERLAP_TOKENS` | `50` | Overlap between chunks |

## Collection Types

### Chat Messages Collection

Single collection for all chat message embeddings. Schema:
- `pk`: Message ID (primary key)
- `embedding`: Vector embedding
- `conversation_id`: Conversation UUID
- `agent_id`: Agent UUID
- `user_id`: User UUID
- `role`: Message role (user, assistant)
- `created_at`: Timestamp
- `content_preview`: First 500 chars

### Knowledge Base Collections

Per-project collections with prefix `knowledge_project_`. Schema:
- `pk`: Auto-generated ID
- `embedding`: Vector embedding
- `document_id`: Document identifier
- `project_id`: Project identifier
- `chunk_index`: Chunk position
- `document_title`: Document title
- `document_type`: Type (text, file, url)
- `content_preview`: First 1000 chars
- `metadata_json`: JSON metadata
- `created_at`: Timestamp

## API Reference

### DocumentChunker

```python
chunker = DocumentChunker(
    max_tokens=500,      # Maximum tokens per chunk
    overlap_tokens=50,   # Overlap for context
    max_chunk_chars=800, # Character-based limit
    overlap_chars=100,   # Character overlap
)

# Standard chunking
chunks = chunker.chunk_document(content, doc_id, project_id, title)

# Sentence-based chunking
chunks = chunker.chunk_by_sentences(content, doc_id, project_id, title, max_sentences=5)
```

### EmbeddingGenerator

```python
generator = EmbeddingGenerator(provider="ollama")

# Single embedding
result = await generator.generate("Text to embed")
print(result.embedding)  # List[float]
print(result.model)      # Model used
print(result.processing_time_ms)

# Batch embedding
results = await generator.generate_batch(["Text 1", "Text 2"])
```

### MilvusClient

```python
from bizstats_vector_store.milvus import MilvusClient

client = MilvusClient()
client.connect()

# List collections
collections = client.list_collections()

# Check collection exists
exists = client.has_collection("my_collection")

# Get stats
stats = client.get_collection_stats("my_collection")

# Load/release
client.load_collection("my_collection")
client.release_collection("my_collection")

client.disconnect()
```

### CollectionManager

```python
from bizstats_vector_store.milvus import CollectionManager

manager = CollectionManager()

# Get collection name
name = manager.get_collection_name(CollectionType.KNOWLEDGE_BASE, project_id="proj-1")
# Returns: "knowledge_project_proj_1"

# Ensure collection exists
collection = await manager.ensure_collection(CollectionType.KNOWLEDGE_BASE, project_id="proj-1")

# List all collections
all_collections = await manager.list_collections()
```

### SemanticSearch

```python
from bizstats_vector_store.search import SemanticSearch

search = SemanticSearch()

# Chat search
response = await search.search_chat_messages(SearchRequest(...))

# Knowledge search with hybrid
response = await search.search_knowledge_base(KnowledgeSearchRequest(...))
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src/bizstats_vector_store --cov-report=term-missing

# Unit tests only (no external dependencies)
pytest tests/ -m "not integration"
```

## License

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI. All rights reserved. Proprietary and confidential.
