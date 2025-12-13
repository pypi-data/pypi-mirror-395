# RecallBricks Python SDK

**Enterprise-Grade Memory Layer for AI** - Persistent, intelligent memory across all AI models with advanced metacognition features.

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://pypi.org/project/recallbricks/)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Installation

```bash
pip install recallbricks
```

## Authentication

RecallBricks supports two authentication methods:

### 1. API Key (User-Level Access)
For individual users and development:

```python
from recallbricks import RecallBricks

rb = RecallBricks(api_key="rb_dev_xxx")
```

### 2. Service Token (Server-to-Server Access)
For production services and server-to-server communication:

```python
from recallbricks import RecallBricks

rb = RecallBricks(service_token="rbk_service_xxx")
```

**Note:** You must provide either `api_key` or `service_token`, but not both.

## Quick Start (< 10 lines)

```python
from recallbricks import RecallBricks

# Option 1: API key authentication
rb = RecallBricks(api_key="rb_dev_xxx")

# Option 2: Service token authentication
# rb = RecallBricks(service_token="rbk_service_xxx")

# Save and retrieve memories
rb.save("User prefers dark mode", tags=["preference", "ui"])

# Get intelligent suggestions based on context
suggestions = rb.suggest_memories("Building a login form", min_confidence=0.7)
for sug in suggestions:
    print(f"💡 {sug.content} - {sug.reasoning}")
```

## Features

### 🧠 Phase 2A: Metacognition & Intelligence

RecallBricks now includes advanced metacognition features that make your AI smarter about its own memory:

#### 1. **Predict Memories** - Proactive Memory Suggestions

Predict which memories might be useful based on context and recent usage patterns:

```python
# Predict memories based on what you're working on
predictions = rb.predict_memories(
    context="User is implementing authentication",
    recent_memory_ids=["mem_123", "mem_456"],  # Recently accessed
    limit=10
)

for pred in predictions:
    print(f"Predicted: {pred.content}")
    print(f"Confidence: {pred.confidence_score}")
    print(f"Reasoning: {pred.reasoning}")
```

#### 2. **Suggest Memories** - Context-Aware Recommendations

Get intelligent memory suggestions based on current context:

```python
# Get suggestions for current task
suggestions = rb.suggest_memories(
    context="Building a React authentication flow with JWT",
    limit=5,
    min_confidence=0.7,
    include_reasoning=True
)

for sug in suggestions:
    print(f"\n📌 {sug.content}")
    print(f"   Confidence: {sug.confidence:.2%}")
    print(f"   Why: {sug.reasoning}")
    print(f"   Context: {sug.relevance_context}")
```

#### 3. **Learning Metrics** - Understand Memory Performance

Analyze how your AI is learning and using memories:

```python
# Get learning metrics for the past 30 days
metrics = rb.get_learning_metrics(days=30)

print(f"Average Helpfulness: {metrics.avg_helpfulness:.2%}")
print(f"Total Usage: {metrics.total_usage}")
print(f"Active Memories: {metrics.active_memories}/{metrics.total_memories}")
print(f"Helpfulness Trend: {metrics.trends.helpfulness_trend}")
print(f"Usage Trend: {metrics.trends.usage_trend}")
print(f"Growth Rate: {metrics.trends.growth_rate:.2%}")
```

#### 4. **Pattern Analysis** - Discover Usage Patterns

Discover patterns in how memories are being used:

```python
# Analyze memory usage patterns
patterns = rb.get_patterns(days=14)

print(f"Summary: {patterns.summary}")
print(f"\nMost Useful Tags: {', '.join(patterns.most_useful_tags[:5])}")

print("\nFrequently Accessed Together:")
for pair in patterns.frequently_accessed_together[:3]:
    print(f"  - {pair[0]} ↔ {pair[1]}")

print("\nUnderutilized Memories:")
for mem in patterns.underutilized_memories[:5]:
    print(f"  - {mem['text']}")
```

#### 5. **Weighted Search** - Intelligent Search Ranking

Search with intelligent weighting based on usage, helpfulness, and recency:

```python
# Smart search with adaptive weighting
results = rb.search_weighted(
    query="authentication",
    limit=10,
    weight_by_usage=True,        # Boost frequently used memories
    decay_old_memories=True,      # Reduce score for old memories
    adaptive_weights=True,        # Use ML-based adaptive weighting
    min_helpfulness_score=0.7     # Filter by helpfulness
)

for result in results:
    print(f"\n🔍 {result.text}")
    print(f"   Relevance: {result.relevance_score:.2f}")
    print(f"   Usage Boost: +{result.usage_boost:.2f}")
    print(f"   Helpfulness: +{result.helpfulness_boost:.2f}")
    print(f"   Recency: +{result.recency_boost:.2f}")
    print(f"   Tags: {', '.join(result.tags)}")
```

### 🔗 Relationship Support

Build connected knowledge graphs with memory relationships:

```python
# Save a memory
memory = rb.save("Fixed authentication bug in login flow")

# Get relationships for a memory
rels = rb.get_relationships(memory['id'])
print(f"Found {rels['count']} relationships")

# Get memory graph with relationships
graph = rb.get_graph_context(memory['id'], depth=2)
print(f"Graph contains {len(graph['nodes'])} connected memories")

# Search with relationships included
results = rb.search("authentication", include_relationships=True)
for result in results:
    if result.get('relationships'):
        print(f"Memory: {result['text']}")
        print(f"Related memories: {result['relationships']['count']}")
```

### 🛡️ Enterprise-Grade Reliability

- **Automatic Retry Logic**: Exponential backoff (1s, 2s, 4s) with 3 retry attempts
- **Rate Limiting Handling**: Automatic retry on 429 errors with respect for rate limits
- **Network Timeout Recovery**: Configurable timeouts with automatic recovery
- **Input Sanitization**: Protection against injection attacks (SQL, XSS, command injection)
- **Comprehensive Error Handling**: Detailed error messages and status codes

```python
# Configure timeout and automatic retries
rb = RecallBricks(
    api_key="rb_dev_xxx",  # or service_token="rbk_service_xxx"
    timeout=30  # 30 second timeout
)

# All methods automatically retry on transient failures
memory = rb.save("Important data")  # Retries up to 3 times on failure
```

## API Reference

### Core Methods

#### `save(text, user_id=None, source="api", project_id="default", tags=None, metadata=None, max_retries=3)`
Save a new memory with automatic retry on failure. Note: `user_id` is required when using service token authentication.

#### `get_all(limit=None)`
Retrieve all memories.

#### `search(query, limit=10, include_relationships=False)`
Search memories by text.

#### `get(memory_id)`
Get a specific memory by ID.

#### `delete(memory_id)`
Delete a memory.

### Metacognition Methods (Phase 2A)

#### `predict_memories(context=None, recent_memory_ids=None, limit=10)`
Predict which memories might be useful.

#### `suggest_memories(context, limit=5, min_confidence=0.6, include_reasoning=True)`
Get memory suggestions based on context.

#### `get_learning_metrics(days=30)`
Get learning metrics showing memory usage patterns.

#### `get_patterns(days=30)`
Analyze patterns in memory usage and access.

#### `search_weighted(query, limit=10, weight_by_usage=False, decay_old_memories=False, adaptive_weights=True, min_helpfulness_score=None)`
Search with intelligent weighting.

### Relationship Methods

#### `get_relationships(memory_id)`
Get relationships for a specific memory.

#### `get_graph_context(memory_id, depth=2)`
Get memory graph with relationships at specified depth.

## Type Definitions

The SDK includes comprehensive type definitions for all Phase 2A features:

```python
from recallbricks import (
    PredictedMemory,
    SuggestedMemory,
    LearningMetrics,
    PatternAnalysis,
    WeightedSearchResult
)
```

## Error Handling

```python
from recallbricks import (
    RecallBricks,
    RecallBricksError,
    AuthenticationError,
    RateLimitError,
    APIError
)

try:
    rb = RecallBricks(api_key="rb_dev_xxx")  # or service_token="rbk_service_xxx"
    memory = rb.save("Test memory")
except AuthenticationError:
    print("Invalid API key or service token")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after}")
except APIError as e:
    print(f"API error: {e.status_code}")
except RecallBricksError as e:
    print(f"General error: {str(e)}")
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test suites
python tests/test_authentication.py    # Authentication tests
python tests/test_relationships.py     # Relationship tests
python tests/test_stress.py           # Stress tests
python tests/test_load_stress.py      # Load stress tests
python tests/test_phase2a_security.py # Security tests

# Run with coverage
pip install pytest pytest-cov
pytest tests/ --cov=recallbricks --cov-report=html
```

## Documentation

- **Full Documentation**: https://recallbricks.com/docs
- **API Reference**: https://recallbricks.com/docs/api
- **TypeScript SDK**: https://github.com/recallbricks/recallbricks-typescript

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Support

- **GitHub Issues**: https://github.com/recallbricks/recallbricks-python/issues
- **Email**: support@recallbricks.com
- **Documentation**: https://recallbricks.com/docs
