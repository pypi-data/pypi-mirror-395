# Memory Hub MCP Server (UV/UVX)

A local memory hub for AI agents with MCP integration, designed for ZenCoder and other MCP clients using stdio transport.

## Quick Start with UVX

### Installation & Usage

```bash
# Install and run directly with uvx
uvx memory-hub-mcp

# Or install locally first
uv pip install memory-hub-mcp
memory-hub-mcp
```

### For ZenCoder Integration

In ZenCoder's custom MCP server configuration, you must now provide the URLs for the dependent services (Qdrant and LM Studio).

**Command:** `uvx`

**Arguments:** 
```json
[
    "memory-hub-mcp",
    "--qdrant-url",
    "http://<ip_address_of_qdrant>:6333",
    "--lm-studio-url",
    "http://<ip_address_of_lm_studio>:1234/v1"
]
```
> **Note:** Replace `<ip_address_...>` with the actual IP addresses where your services are running. If they are on the same machine, the IP will be the same for both.

## Development Setup

```bash
# Clone and setup
git clone <your-repo>
cd memory-hub
uv venv
source .venv/bin/activate
uv pip install -e .

# Run in development
memory-hub-mcp --log-level DEBUG --qdrant-url http://localhost:6333 --lm-studio-url http://localhost:1234/v1
```

## Publishing to PyPI

To publish a new version of the package to PyPI:

1.  **Update the Version**: Increment the `version` number in `pyproject.toml`. PyPI does not allow re-uploading the same version.
    
    ```toml
    # pyproject.toml
    [project]
    name = "memory-hub-mcp"
    version = "0.1.2" # Increment this
    ```

2.  **Clean and Rebuild**: Remove old builds and create the new distributions.
    
    ```bash
    rm -rf dist/
    uv build
    ```

3.  **Publish with an API Token**:
    
    The recommended way to publish is to use a PyPI API token. You can provide it directly to the command via an environment variable for security.
    
    ```bash
    # Replace <your_pypi_token> with your actual token
    UV_PUBLISH_TOKEN=<your_pypi_token> uv publish dist/*
    ```

## Available Tools

- **add_memory**: Store content with hierarchical metadata (app_id, project_id, ticket_id)
- **search_memories**: Semantic search with keyword enhancement and LLM synthesis
- **get_project_memories**: Retrieve ALL memories for a specific app_id/project_id without search queries
- **update_memory**: Update existing memories with automatic version incrementing
- **get_recent_memories**: Retrieve memories from the last N hours (perfect for resuming work)
- **list_app_ids**: List all application IDs
- **list_project_ids**: List all project IDs  
- **list_ticket_ids**: List all ticket IDs
- **list_memory_types**: List memory types currently in use (with counts and metadata)
- **get_memory_type_guide**: Get the recommended memory type conventions
- **health_check**: Server health status

## Configuration

The server expects:
- **Qdrant**: Vector database running (see docker-compose.yml)
- **LM Studio**: For embeddings and chat completions
- **Environment**: Standard .env configuration

## Key File & Directory Locations

- **`pyproject.toml`**: Defines project metadata, dependencies, and the `memory-hub-mcp` script entry point.
- **`src/memory_hub/`**: The main Python package source code.
- **`src/memory_hub/cli.py`**: The command-line interface logic that launches the server.
- **`src/memory_hub/mcp_server.py`**: Core `stdio` server implementation and tool registration.
- **`src/memory_hub/core/handlers/`**: Contains the implementation for each MCP tool (e.g., `add_memory`, `search_memories`).
- **`src/memory_hub/core/services.py`**: Handles communication with external services like Qdrant and LM Studio.
- **`src/memory_hub/core/models.py`**: Pydantic models defining the data structures used throughout the application.
- **`docker-compose.yml`**: Defines the Qdrant service dependency.

## Architecture

- **stdio transport**: Direct MCP protocol communication
- **No HTTP dependencies**: Lightweight, focused on MCP clients
- **Hierarchical memory**: Flexible app/project/ticket organization
- **Hybrid search**: Vector similarity + keyword matching + LLM synthesis
- **Version management**: Automatic versioning for memory updates
- **Time-based retrieval**: Query recent memories by hours

## Agent Usage Guide

### Saving Agent Progress
```python
# Save initial work
add_memory(
    content="Implemented user authentication with JWT tokens...",
    metadata={
        "app_id": "eatzos",
        "project_id": "next",
        "type": "feature_implementation"
    }
)

# Update existing memory
update_memory(
    app_id="eatzos",
    project_id="next", 
    memory_type="feature_implementation",
    new_content="Completed authentication with JWT tokens and added refresh token logic..."
)
```

### Resuming Agent Work
```python
# Get ALL context for a project (no search guessing!)
get_project_memories(
    app_id="eatzos",
    project_id="next",
    limit=50
)

# See what changed recently
get_recent_memories(
    app_id="eatzos",
    hours=24,
    include_summary=True
)
```

## Differences from HTTP Version

This UV/UVX version:
- ✅ Uses stdio transport (ZenCoder compatible)
- ✅ No FastAPI dependencies
- ✅ Lightweight packaging
- ✅ Direct MCP protocol
- ❌ No web interface
- ❌ No HTTP endpoints 