# Memory Hub MCP Server

A persistent memory system for AI agents using the Model Context Protocol (MCP). Memory Hub provides vector-based storage and retrieval through stdio transport, enabling agents to maintain context across sessions.

## Overview

Memory Hub acts as a "central brain" for AI agents, allowing them to:
- **Preserve context** across sessions and conversations
- **Organize memories** hierarchically (app → project → ticket → run)
- **Search semantically** with vector embeddings and keyword enhancement
- **Resume work** by retrieving all relevant context without guessing search terms
- **Version memories** automatically when updating information

### Key Features

- 🧠 **Hierarchical Memory**: Flexible 4-level hierarchy: app_id → project_id → ticket_id → run_id with validation
- 🔍 **Hybrid Search**: Vector similarity + keyword matching + LLM synthesis
- 📊 **Cascading Retrieval**: Automatically include parent-level context when querying
- 🎯 **Token Optimization**: Choose between summary, raw chunks, or both
- 🔄 **Version Management**: Automatic versioning for memory updates
- ⏰ **Time-based Queries**: Retrieve memories from last N hours
- 🧭 **Hierarchy Overview**: List children (projects/tickets/runs) with counts for quick orientation
- 🏷️ **Type & Tag Filters**: Slice results across the hierarchy by memory type or cross-project tags
- 📅 **Date Ranges**: Retrieve memories between explicit start/end timestamps
- 🗺️ **Contextual Search**: Group semantic search results by app/project/ticket/run path
- 📦 **Snapshot Export**: Dump scoped memories as JSON for backups or analysis
- 🚀 **Discovery Helpers**: `get_scope_overview` (alias: `get_hierarchy_overview`) to list children, `get_quick_start` for common workflows and parameter hints
- 📡 **stdio Transport**: Direct MCP protocol communication (no HTTP)

## Quick Start

### Installation

```bash
# Install and run directly with uvx (recommended)
uvx memory-hub-mcp

# Or install with uv
uv pip install memory-hub-mcp
memory-hub-mcp
```

### For Claude Desktop / MCP Clients

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "memory-hub": {
      "command": "uvx",
      "args": [
        "memory-hub-mcp",
        "--qdrant-url",
        "http://192.168.1.100:6333",
        "--lm-studio-url",
        "http://192.168.1.100:1234/v1"
      ]
    }
  }
}
```

> **Note**: Replace IP addresses with your Qdrant and LM Studio server locations.

## Configuration

### Required Services

Memory Hub depends on two external services:

1. **Qdrant** - Vector database for embeddings storage
   ```bash
   # Using Docker
   docker-compose up -d
   ```

2. **LM Studio** - Provides embeddings and chat completions
   - Download from: https://lmstudio.ai
   - Load an embedding model (e.g., `nomic-embed-text-v1.5`)
   - Load a chat model (e.g., `gemma-3-4b`)

### Environment Variables

- `QDRANT_URL`: Qdrant server URL (default: `http://localhost:6333`)
- `LM_STUDIO_BASE_URL`: LM Studio base URL (default: `http://localhost:1234/v1`)
- `MIN_SCORE_THRESHOLD`: Minimum similarity score (default: `0.60`)
- `ENABLE_GEMMA_SUMMARIZATION`: Enable LLM summarization (default: `true`)

### CLI Arguments

```bash
memory-hub-mcp \
  --qdrant-url http://192.168.1.100:6333 \
  --lm-studio-url http://192.168.1.100:1234/v1 \
  --log-level DEBUG
```

## Hierarchical Memory Structure

Memory Hub enforces a strict 4-level hierarchy:

### Hierarchy Levels
1. `app_id` - Application/Product level
2. `project_id` - Feature area within app
3. `ticket_id` - Specific feature/task (maps to git branch in AutoStack)
4. `run_id` - Individual execution (maps to git commit in AutoStack)

### Rules
- `app_id` is **always required**
- `project_id` requires `app_id`
- `ticket_id` requires **both** `app_id` AND `project_id`
- `run_id` requires `app_id` + `project_id` + `ticket_id`

### Cascading Retrieval

When retrieving memories with `cascade=true` (default), you automatically get parent-level context:

- `app_id` only → Returns **app-level** memories
- `app_id + project_id` → Returns **app-level + project-level** memories
- `app_id + project_id + ticket_id` → Returns **app-level + project-level + ticket-level + ALL runs**
- `app_id + project_id + ticket_id + run_id` → Returns **app-level + project-level + ticket-level + specific run**

With `cascade=false`, you can query exact addresses (e.g., only a specific run's memories).

**Example:**
```python
# Get auth project context
get_project_memories(
    app_id="crossroads",
    project_id="auth"
)
# Returns: All "crossroads" app-level memories
#          + All "auth" project-level memories
```

## Available Tools

### Memory Management

1. **`add_memory`** - Store content with hierarchical metadata
   ```python
   # Normal memory (default chunking enabled)
   add_memory(
       content="Implemented JWT authentication with refresh tokens...",
       metadata={
           "app_id": "crossroads",
           "project_id": "auth",
           "type": "feature_implementation"
       }
   )

   # Large structured document with run_id (disable chunking for AutoStack plans, specs, etc.)
   add_memory(
       content=full_plan_markdown,  # 2000+ token document
       metadata={
           "app_id": "covenant",
           "project_id": "portal",
           "ticket_id": "auth-flow",
           "run_id": "initial-impl",  # 4th hierarchy level for multi-run scenarios
           "type": "plan"
       },
       chunking=False  # Store as single unit, not chunked
   )
   ```

2. **`update_memory`** - Update existing memories (auto-increments version)
   ```python
   update_memory(
       app_id="crossroads",
       project_id="auth",
       memory_type="feature_implementation",
       new_content="Added refresh token rotation for security..."
   )
   ```

3. **`get_project_memories`** - Retrieve memories for a scope
   ```python
   # Default: cascade=true returns app + project levels
   get_project_memories(
       app_id="crossroads",
       project_id="auth",
       cascade=true,  # default, includes parent context
       return_format="summary_only",  # or "chunks_only", "both"
       limit=50
   )

   # AutoStack: cascade=false returns only project level
   get_project_memories(
       app_id="crossroads",
       project_id="auth",
       ticket_id="FEAT-123",
       cascade=false,  # exact match only
       return_format="chunks_only"
   )
   ```

4. **`get_recent_memories`** - Time-based retrieval
   ```python
   get_recent_memories(
       app_id="crossroads",
       hours=24,
       return_format="summary_only"
   )
   ```

5. **`search_memories`** - Semantic search with keyword enhancement
   ```python
   search_memories(
       query_text="authentication implementation",
       metadata_filters={"app_id": "crossroads"},
       limit=10
   )
   ```

### Introspection

6. **`list_app_ids`** - List all application identifiers
7. **`list_project_ids`** - List all project identifiers
8. **`list_ticket_ids`** - List all ticket identifiers
9. **`list_memory_types`** - List memory types in use (with counts)
10. **`get_memory_type_guide`** - Get recommended memory type conventions
11. **`health_check`** - Server health status

## Token Optimization with `return_format`

Both `get_project_memories` and `get_recent_memories` support a `return_format` parameter:

### Options

- **`summary_only`**: AI-generated summary only (~80% token reduction)
- **`chunks_only`**: Raw memory chunks without LLM interpretation
- **`both`**: Summary + chunks (default, backward compatible)

### Usage Patterns

**1. Starting New Work** → Use `summary_only`
```python
get_project_memories(
    app_id="crossroads",
    return_format="summary_only"
)
# Returns: Concise overview, ~600 tokens vs ~3,000 tokens
```

**2. Deep Implementation** → Use `chunks_only`
```python
get_project_memories(
    app_id="crossroads",
    project_id="auth",
    return_format="chunks_only"
)
# Returns: Exact content, no LLM interpretation
```

**3. Exploration/Debugging** → Use `both`
```python
get_project_memories(
    app_id="crossroads",
    return_format="both"
)
# Returns: Summary + full chunks for reference
```

### Token Efficiency

| Memories | Format | Approx Tokens |
|----------|--------|---------------|
| 10 app-level | both | ~3,000 |
| 10 app-level | summary_only | ~600 |
| 50 project-level | both | ~15,000 |
| 50 project-level | summary_only | ~2,000 |

## Cascade Parameter (v1.5.0+)

The `cascade` parameter controls hierarchical retrieval behavior. Available on: `get_project_memories`, `get_recent_memories`, `search_memories`.

### Default Behavior (cascade=true)

By default, queries **cascade** through the hierarchy to include parent context:

```python
# Returns app-level + project-level + ticket-level memories
get_project_memories(
    app_id="covenant",
    project_id="portal",
    ticket_id="auth-flow",
    cascade=true  # default
)
```

### Exact Matching (cascade=false)

Use `cascade=false` to return **ONLY** the exact level specified:

```python
# Returns ONLY ticket-level memories (no parent context)
get_project_memories(
    app_id="covenant",
    project_id="portal",
    ticket_id="auth-flow",
    cascade=false  # exact match only
)
# Returns 0 results if nothing exists at this exact address
```

### AutoStack Checkpoint Pattern

AutoStack workflows use `cascade=false` for lightweight checkpoint checks:

```python
# Check if plan exists at this specific address
plan_check = get_project_memories(
    app_id="covenant",
    project_id="portal",
    ticket_id="auth-flow",
    cascade=false,  # Don't include parent memories
    metadata_filters={"type": "plan"},
    return_format="chunks_only",
    limit=1
)

if plan_check.total_results == 0:
    # No plan at this address → start planning
    start_planning_phase()
else:
    # Plan exists → skip to build
    start_build_phase()
```

**Why cascade=false matters:**
- **With cascade=true**: Query returns ALL parent context → 55k tokens for large projects
- **With cascade=false**: Query returns exact address only → 0 results if empty
- Enables efficient "does this address have data?" checks without pulling entire project history

### cascade Parameter Reference

| Level Query | cascade=true | cascade=false |
|------------|--------------|---------------|
| `app_id` only | App-level memories | App-level memories (same) |
| `app_id + project_id` | App + Project levels | Project-level only |
| `app_id + project_id + ticket_id` | App + Project + Ticket | Ticket-level only |

## Agent Usage Guide

### Saving Progress

```python
# Save code changes
add_memory(
    content="Modified auth/login.py to add refresh token support",
    metadata={
        "app_id": "crossroads",
        "project_id": "auth",
        "type": "code_changes",
        "files_modified": ["auth/login.py", "auth/tokens.py"]
    }
)

# Save decisions
add_memory(
    content="Decided to use JWT tokens instead of sessions because...",
    metadata={
        "app_id": "crossroads",
        "project_id": "auth",
        "type": "technical_decision",
        "importance": "high"
    }
)
```

### Resuming Work

```python
# STEP 1: Get all project context (no guessing!)
memories = get_project_memories(
    app_id="crossroads",
    project_id="auth",
    return_format="summary_only",  # Start with summary
    limit=100
)

# STEP 2: Check recent changes
recent = get_recent_memories(
    app_id="crossroads",
    hours=24,
    return_format="summary_only"
)

# STEP 3: Get specific details if needed
details = get_project_memories(
    app_id="crossroads",
    project_id="auth",
    return_format="chunks_only"  # Get raw data
)
```

### Memory Types Best Practices

| Type | Create/Update | Purpose |
|------|--------------|---------|
| `code_changes` | CREATE | Track each modification |
| `decisions` | CREATE | Document choices made |
| `progress_update` | CREATE | Milestone tracking |
| `bug_fix` | CREATE | Issues and solutions |
| `project_status` | UPDATE | Current overall state |
| `todo_list` | UPDATE | Evolving task list |

**Rule of thumb**: If it's historical (changes, updates, fixes) → CREATE. If it's current state (status, config) → UPDATE.

## Development

### Setup

```bash
# Clone repository
git clone <repository-url>
cd memory-hub

# Create virtual environment
uv venv
source .venv/bin/activate

# Install with dev dependencies
uv pip install -e ".[dev]"
```

### Running Locally

```bash
# Run with development settings
memory-hub-mcp --log-level DEBUG \
  --qdrant-url http://localhost:6333 \
  --lm-studio-url http://localhost:1234/v1

# Run tests (when available)
pytest

# Code formatting
black src/
ruff check src/
```

### Publishing to PyPI

```bash
# 1. Update version in pyproject.toml
# version = "1.4.3"

# 2. Clean and rebuild
rm -rf dist/
uv build

# 3. Publish
UV_PUBLISH_TOKEN=<your-pypi-token> uv publish dist/*
```

### Project Structure

```
memory-hub/
├── src/memory_hub/
│   ├── cli.py                    # CLI entry point
│   ├── mcp_server.py            # MCP server + tool registration
│   └── core/
│       ├── config.py            # Configuration constants
│       ├── models.py            # Pydantic data models
│       ├── services.py          # Qdrant/LM Studio integration
│       ├── chunking.py          # Semantic text chunking
│       ├── handlers/
│       │   ├── memory_handlers.py   # Memory CRUD operations
│       │   └── list_handlers.py     # Introspection operations
│       └── utils/
│           ├── validation.py    # Hierarchy validation
│           └── search_utils.py  # Search enhancement
├── pyproject.toml               # Package configuration
├── docker-compose.yml           # Qdrant service
└── CLAUDE.md                    # Development guide
```

## Architecture

### Design Patterns

- **stdio transport**: Direct MCP protocol communication (no HTTP)
- **Hierarchical memory**: Enforced app → project → ticket organization
- **Hybrid search**: Vector similarity + keyword matching + LLM synthesis
- **Async-first**: All operations use async/await patterns
- **Version management**: Automatic versioning with deduplication

### External Dependencies

- **Qdrant**: Vector database for embeddings storage
- **LM Studio**: Provides embeddings (nomic-embed) and chat completions (gemma)
- **MCP Protocol**: stdio transport for client communication

## Troubleshooting

### Common Issues

**1. Qdrant connection errors**
```
ERROR: Could not connect to Qdrant
Common causes:
  - Using https:// instead of http:// (Qdrant uses HTTP)
  - Qdrant service not running
  - Wrong IP address or port
```
**Solution**: Verify Qdrant is running at the specified URL (use `http://` not `https://`)

**2. LM Studio timeout**
```
ERROR: LM Studio connection timeout
```
**Solution**: Check LM Studio is running with embedding and chat models loaded

**3. "No memory found" on update**
```
ERROR: No memory found matching criteria
```
**Solution**: Verify exact spelling of `app_id`, `project_id`, and `memory_type`. Use `get_project_memories` to confirm the memory exists.

**4. Import errors**
```
ModuleNotFoundError: No module named 'memory_hub'
```
**Solution**: Install dependencies with `uv pip install -e .` in development mode

### Debugging

```bash
# Enable verbose logging
memory-hub-mcp --log-level DEBUG

# Check server health
# Use health_check tool from MCP client

# Verify Qdrant
curl http://localhost:6333/collections

# Verify LM Studio
curl http://localhost:1234/v1/models
```

## Updating Consumers

When you publish a new version to PyPI, consumers can update:

```bash
# Force latest version
uvx memory-hub-mcp@latest

# Or clear cache and reinstall
uv tool uninstall memory-hub-mcp
uvx memory-hub-mcp
```

For Claude Desktop users: Restart Claude Desktop after publishing to pick up updates.

## Contributing

See `CLAUDE.md` for detailed development guidelines and `AGENT_GUIDE.md` for comprehensive agent usage patterns.

## License

MIT
