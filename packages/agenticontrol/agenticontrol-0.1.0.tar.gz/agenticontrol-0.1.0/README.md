# AGENTICONTROL V0 MVP

Control plane for AI agents with synchronous blocking and asynchronous logging.

## Overview

AGENTICONTROL provides:
- **Synchronous Blocking**: Zero-latency policy checks and loop detection
- **Asynchronous Logging**: Non-blocking trace event ingestion
- **Terminal Viewer**: Real-time structured trace output for local debugging
- **Cloud Backend**: Scalable trace storage and analytics

## Key Features

- 🛑 **Policy V0 Checks**: Block dangerous operations (SQL DROP, DELETE, PII patterns)
- 🔄 **Loop Detection**: Detect and halt infinite loops (Rule A & B)
- 💰 **Cost Monitoring**: Track token usage and estimated costs
- 📊 **Terminal Viewer**: Beautiful real-time trace visualization with `rich`
- ☁️ **Cloud Uplink**: Async trace ingestion to Supabase

## Installation

```bash
pip install agenticontrol
```

## Quick Start

### Installation

```bash
pip install agenticontrol
```

### Basic Usage with LangChain

```python
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from agenticontrol.hooks.langchain_handler import AgenticontrolCallbackHandler

# Initialize the callback handler
handler = AgenticontrolCallbackHandler(
    api_url="http://localhost:8000/api/v1/ingest/trace",  # Your backend URL
    api_key=None,  # Optional API key
    enable_blocking=True,  # Enable Policy V0 and Loop Detection
    enable_logging=True,  # Enable async trace logging
)

# Use with LangChain agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    callbacks=[handler],
    verbose=True
)

# Run agent - blocking checks happen automatically
try:
    result = agent.run("Your query here")
    print(f"Result: {result}")
except PolicyViolationError as e:
    print(f"Agent blocked: {e}")

# Cleanup
import asyncio
asyncio.run(handler.flush())
asyncio.run(handler.close())
```

### Local-Only Mode (No Cloud Backend)

```python
from agenticontrol.hooks.langchain_handler import AgenticontrolCallbackHandler

# Local-only mode: blocking checks work, but no cloud logging
handler = AgenticontrolCallbackHandler(
    api_url=None,  # Local-only mode
    enable_blocking=True,
    enable_logging=False
)
```

### Terminal Viewer

The terminal viewer provides real-time trace visualization:

```python
from agenticontrol.local.viewer import TraceViewer, get_viewer

# Get the viewer instance
viewer = get_viewer()

# Events are automatically displayed when using the callback handler
# The viewer shows:
# - 💭 LLM prompts and responses
# - 🛠 Tool calls and outputs
# - 🛑 Blocked operations (Policy V0, Loop Detection)
# - 💰 Cost tracking
```

### Examples

See the `examples/` directory for complete examples:
- `basic_usage.py` - Basic LangChain integration
- `loop_detection_demo.py` - Loop detection demonstration
- `policy_v0_demo.py` - Policy V0 checks demonstration

## Features

### 🛑 Policy V0 Checks
Blocks dangerous operations synchronously (zero latency):
- SQL commands: `DROP TABLE`, `DELETE FROM`
- File system: `rm -rf`, dangerous paths
- PII patterns: Email addresses, SSNs, etc.

```python
# Automatically blocks dangerous operations
agent.run("DROP TABLE users")  # Raises PolicyV0ViolationError
```

### 🔄 Loop Detection
Detects and halts infinite loops (Rule A & B):
- **Rule A**: Identical LLM prompts repeated
- **Rule B**: Identical tool calls repeated

```python
# Blocks after 5 identical tool calls
for i in range(10):
    agent.run("search for 'test'")  # Blocks on 6th identical call
```

### 💰 Cost Monitoring
Tracks token usage and estimated costs:
- Accumulates tokens per run
- Calculates USD cost based on model rates
- Updates in real-time

### 📊 Terminal Viewer
Beautiful real-time trace visualization:
- Tree-like structure showing agent execution
- Color-coded events (LLM, tools, errors)
- Prominent display of blocked operations

### ☁️ Cloud Uplink
Async trace ingestion to Supabase:
- Non-blocking HTTP calls
- Batched uploads for efficiency
- Never delays agent execution

## Architecture

### Synchronous Blocking (Zero Latency)
- Policy V0 checks run in-memory
- Loop detection runs synchronously
- Raises `PolicyViolationError` to halt execution immediately

### Asynchronous Logging (Non-Blocking)
- Trace events sent via async HTTP
- Batched uploads for efficiency
- Never blocks agent execution

## API Reference

### AgenticontrolCallbackHandler

Main callback handler for LangChain integration.

**Parameters:**
- `api_url` (str, optional): Backend API URL for trace ingestion
- `api_key` (str, optional): API key for authentication
- `run_id` (UUID, optional): Unique identifier for this run (auto-generated)
- `risk_engine` (RiskEngine, optional): Custom risk engine instance
- `enable_blocking` (bool): Enable synchronous blocking checks (default: True)
- `enable_logging` (bool): Enable async trace logging (default: True)

**Methods:**
- `flush()`: Flush pending events to cloud (async)
- `close()`: Close client connections (async)

### Exceptions

- `PolicyViolationError`: Base exception for all policy violations
- `PolicyV0ViolationError`: Raised when Policy V0 check fails
- `LoopDetectedError`: Raised when loop detection triggers
- `CostThresholdExceededError`: Raised when cost threshold exceeded

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/yourorg/agenticontrol.git
cd agenticontrol

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src/agenticontrol --cov-report=html

# Format code
black src tests examples

# Lint code
ruff check src tests examples

# Type checking
mypy src
```

### Running Examples

```bash
# Basic usage
python examples/basic_usage.py

# Loop detection demo
python examples/loop_detection_demo.py

# Policy V0 demo
python examples/policy_v0_demo.py
```

### Running Backend

```bash
cd backend
python run_server.py
# Or: python -m uvicorn backend.app.main:app --reload
```

### Project Structure

```
src/agenticontrol/
├── models.py              # Pydantic models (TraceEvent, RunMetadata, RiskResult)
├── risk_engine.py         # Synchronous blocking checks
├── client.py              # Async HTTP client
├── exceptions.py          # PolicyViolationError hierarchy
└── hooks/
    └── langchain_handler.py  # LangChain integration

local/
└── viewer.py              # Terminal trace viewer

backend/
└── app/                   # FastAPI backend (separate repo)
```

## Schema Versioning

The `TraceEvent` model includes a `schema_version` field for backward compatibility.
Current version: `1.0.0`

## License

MIT

## Contributing

See CONTRIBUTING.md (coming soon)

