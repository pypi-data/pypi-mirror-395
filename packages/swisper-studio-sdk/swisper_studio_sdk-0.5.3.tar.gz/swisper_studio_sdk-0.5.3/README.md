# SwisperStudio SDK

Simple, high-performance integration for tracing Swisper LangGraph applications.

**v0.4.0 - Redis Streams Architecture:**
- 🚀 **50x faster** - 500ms → 10ms overhead
- 🧠 **LLM reasoning** - See thinking process (`<think>...</think>`)
- 📡 **Connection status** - Heartbeat-based health monitoring
- ⚙️ **Per-node config** - Fine-grained control

## Installation

### From PyPI (Recommended)

```bash
pip install swisper-studio-sdk>=0.5.2
```

That's it! No authentication needed.

### From Source (Development)

```bash
git clone https://github.com/Fintama/swisper_studio.git
cd swisper_studio/sdk
pip install -e .
```

**Note:** Source installation requires Fintama GitHub organization access.

## Quick Start (30 seconds)

### 1. Initialize at Startup (Redis Streams)

```python
# In your main.py or startup code
from swisper_studio_sdk import safe_initialize

# Async initialization (in lifespan or startup) - RECOMMENDED
status = await safe_initialize(
    redis_url="redis://swisper_studio_redis:6379",  # SwisperStudio Redis
    project_id="your-project-id",                    # From SwisperStudio
    enabled=True
)

if status["initialized"]:
    logger.info("SwisperStudio tracing enabled")
else:
    logger.info("Tracing disabled (Swisper continues normally)")
```

**Note:** `safe_initialize()` NEVER blocks or raises exceptions. If Redis is unavailable, Swisper continues normally with tracing disabled.

### 2. ONE LINE CHANGE to Enable Tracing

```python
# Before:
from langgraph.graph import StateGraph
graph = StateGraph(GlobalSupervisorState)

# After (change ONE line):
from swisper_studio_sdk import create_traced_graph
graph = create_traced_graph(GlobalSupervisorState, trace_name="supervisor")

# That's it! All nodes added to this graph are automatically traced!
```

### 3. Add Nodes as Normal

```python
# Add nodes - they're automatically traced!
graph.add_node("intent_classification", intent_classification_node)
graph.add_node("memory", memory_node)
graph.add_node("planner", planner_node)
graph.add_node("ui_node", ui_node)

# Compile and run as usual
app = graph.compile()
result = await app.ainvoke(initial_state)

# All executions are now traced to SwisperStudio! 🎉
```

## Features

### **Core Features:**
- ✅ **One-line integration** - `create_traced_graph()` instead of `StateGraph()`
- ✅ **Auto-instrumentation** - All nodes automatically traced
- ✅ **State capture** - Captures input/output state at each node
- ✅ **Error tracking** - Captures exceptions and error messages
- ✅ **Nested observations** - Supports parent-child relationships
- ✅ **Zero boilerplate** - No decorators needed on individual nodes

### **v0.4.0 New Features:**
- ✅ **Redis Streams** - 50x faster than HTTP (500ms → 10ms)
- ✅ **LLM Reasoning** - Captures `<think>...</think>` tags from DeepSeek R1, o1, etc.
- ✅ **Streaming Support** - Captures full responses from streaming LLM calls
- ✅ **Connection Status** - Verifies SwisperStudio consumer is running
- ✅ **Per-Node Config** - Enable/disable reasoning per node
- ✅ **Memory Safety** - Auto-cleanup prevents memory leaks

## Advanced Usage

### LLM Reasoning Capture

Control reasoning capture per node:

```python
from swisper_studio_sdk import traced

# Enable reasoning with custom length limit
@traced("classify_intent", capture_reasoning=True, reasoning_max_length=20000)
async def classify_intent_node(state):
    # Captures <think>...</think> tags (up to 20KB)
    return state

# Disable reasoning for specific nodes
@traced("memory_node", capture_reasoning=False)
async def memory_node(state):
    # No reasoning captured (faster, less data)
    return state

# Use defaults (reasoning enabled, 50KB limit)
@traced("global_planner")
async def global_planner_node(state):
    return state
```

**What gets captured:**
- ✅ LLM prompts (system + user messages)
- ✅ Reasoning process (`<think>...</think>` tags)
- ✅ Final responses (structured output or streaming)
- ✅ Token usage (prompt + completion)

**Supported models:**
- DeepSeek R1 (with reasoning)
- OpenAI o1/o3 (with reasoning)
- GPT-4, Claude, Llama (no reasoning, just prompts + responses)

### Manual Tracing (Optional)

For fine-grained control, use `@traced` decorator:

```python
from swisper_studio_sdk import traced

# Full control over observation
@traced(
    name="intent_classification",
    observation_type="GENERATION",
    capture_reasoning=True,
    reasoning_max_length=10000
)
async def intent_classification_node(state):
    return state
```

### Observation Types

- `AUTO` - Auto-detect based on LLM data (default, recommended)
- `SPAN` - Generic execution span
- `GENERATION` - LLM generation
- `EVENT` - Point-in-time event
- `TOOL` - Tool call
- `AGENT` - Agent execution

## Architecture

### Redis Streams (v0.4.0)

```
Your App (Swisper)         Redis Stream              SwisperStudio
       │                        │                           │
  @traced decorator             │                           │
       │                        │                           │
  XADD event (1-2ms) ──────────→ │                           │
       │                        │                           │
  Return immediately            │                           │
  (zero latency!)               │                           │
                                │   Consumer reads batch    │
                                │ ←─────────────────────────┤
                                │                           │
                                │   Store in PostgreSQL     │
                                │ ──────────────────────────→
```

**Benefits:**
- **50x faster** than HTTP (500ms → 10ms overhead)
- **No race conditions** (ordered stream delivery)
- **Reliable** (persistent queue, automatic retry)
- **Scalable** (100k+ events/sec)

### How It Works

1. `create_traced_graph()` monkey-patches `add_node()` to auto-wrap functions
2. `@traced` decorator publishes events to Redis Streams (1-2ms)
3. SwisperStudio consumer reads from stream and stores in database
4. Zero user-facing latency (fire-and-forget pattern)

## Configuration

### Required Settings

```python
# In your config.py or .env
SWISPER_STUDIO_REDIS_URL: str = "redis://redis:6379"
SWISPER_STUDIO_PROJECT_ID: str = "your-project-id"
SWISPER_STUDIO_STREAM_NAME: str = "observability:events"
```

### Optional Settings

```python
# Reasoning capture
SWISPER_STUDIO_CAPTURE_REASONING: bool = True
SWISPER_STUDIO_REASONING_MAX_LENGTH: int = 50000  # 50 KB

# Connection verification
SWISPER_STUDIO_VERIFY_CONSUMER: bool = True  # Check consumer health
```

## Requirements

- Python 3.11+
- LangGraph >= 1.0.0, < 2.0.0
- langgraph-checkpoint >= 2.1.0 (v0.5.2 removed upper bound for HITL compatibility)
- httpx >= 0.25.2
- redis >= 5.0.0

## Migration

Upgrading from v0.3.x? See [SDK_MIGRATION_v0.3.4_to_v0.4.0.md](../../SDK_MIGRATION_v0.3.4_to_v0.4.0.md)

**Migration time:** ~15 minutes  
**Breaking changes:** None (backward compatible)

## License

MIT

