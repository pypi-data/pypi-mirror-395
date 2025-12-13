"""
MCP Server implementation using stdio transport for ZenCoder compatibility
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool, 
    TextContent,
    ImageContent,
    EmbeddedResource,
    CallToolRequest
)

# Import our core functionality
from .core.models import (
    MemoryItemIn, MemorySearchRequest, GetProjectMemoriesRequest, UpdateMemoryRequest,
    DeleteRunMemoriesRequest, GetRecentMemoriesRequest, ListMemoryTypesRequest,
    HierarchyOverviewRequest, ExportMemoriesRequest,
    SessionResumeRequest, SessionHandoffRequest, SessionUpdateRequest
)
from .core.handlers.memory import (
    add_memory as add_memory_handler,
    search_memories as search_memories_handler,
    get_project_memories as get_project_memories_handler,
    update_memory as update_memory_handler,
    delete_run_memories as delete_run_memories_handler,
    get_recent_memories as get_recent_memories_handler,
    get_hierarchy_overview as get_hierarchy_overview_handler,
    export_memories as export_memories_handler,
    get_quick_start_info as get_quick_start_info_handler,
    session_resume as session_resume_handler,
    session_handoff as session_handoff_handler,
    session_update as session_update_handler,
)
from .core.handlers.list_handlers import (
    list_app_ids as list_app_ids_handler,
    list_project_ids as list_project_ids_handler, 
    list_ticket_ids as list_ticket_ids_handler,
    list_memory_types as list_memory_types_handler,
    get_memory_type_guide as get_memory_type_guide_handler
)
from .core.handlers.health_handlers import health_check as health_check_handler
from .core.services import startup_event, shutdown_event, AppConfig
from .core.utils.dependencies import get_http_client
import httpx

# Module-level logger. Logging configuration is done by the CLI entrypoint so
# we avoid calling basicConfig here (import order would override the CLI file
# handler and break logging to /tmp/memory-hub-mcp.log).
logger = logging.getLogger(__name__)

# Version constant
VERSION = "1.11.0"

class MemoryHubMCPServer:
    """Memory Hub MCP Server for stdio transport"""
    
    def __init__(self, config: AppConfig):
        self.server = Server("memory-hub")
        self.config = config
        self._setup_tools()
    
    def _setup_tools(self):
        """Register MCP tools"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="add_memory",
                    description="Adds memory content. Chunks content, gets embeddings, and stores in Qdrant. Supports flexible hierarchy: app_id (required), project_id (optional), ticket_id (optional), run_id (optional).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The content to store in memory"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Metadata with flexible hierarchy: app_id (required), project_id (optional), ticket_id (optional), run_id (optional), type, etc.",
                                "properties": {
                                    "app_id": {"type": "string", "description": "Required - Application identifier"},
                                    "project_id": {"type": "string", "description": "Optional - Project identifier"},
                                    "ticket_id": {"type": "string", "description": "Optional - Ticket identifier"},
                                    "run_id": {"type": "string", "description": "Optional - Run identifier (4th hierarchy level, requires app_id + project_id + ticket_id)"},
                                    "type": {"type": "string", "description": "Memory type classification"},
                                    "version": {"type": "integer", "description": "Version number", "default": 1}
                                },
                                "required": ["app_id"]
                            },
                            "chunking": {
                                "type": "boolean",
                                "description": "Enable semantic chunking (default: true). Set to false for large structured documents (e.g., AutoStack plans, specifications) that don't need semantic search and should be stored as a single unit.",
                                "default": True
                            }
                        },
                        "required": ["content", "metadata"]
                    }
                ),
                Tool(
                    name="search_memories",
                    description="Semantic search with hierarchy-aware grouping. Scope (app/project/ticket/run), filter (memory_types, tag_filters, keyword_filters), display (group_by_path, latest_only).",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "query_text": {
                                "type": "string",
                                "description": "The query text to search for"
                            },
                            "metadata_filters": {
                                "type": "object",
                                "description": "Metadata filters for search (scope)",
                                "additionalProperties": {"type": "string"},
                                "default": {}
                            },
                            "keyword_filters": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of keywords that results must contain",
                                "default": []
                            },
                            "memory_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict results to these memory types",
                                "default": []
                            },
                            "tag_filters": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict results to memories containing any of these tags",
                                "default": []
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 10
                            },
                            "group_by_path": {
                                "type": "boolean",
                                "description": "Display: Group results by hierarchy path (app/project/ticket/run)",
                                "default": False
                            },
                            "latest_only": {
                                "type": "boolean",
                                "description": "Display: Exclude memories superseded by newer entries (alias: hide_superseded)",
                                "default": False
                            },
                            "hide_superseded": {
                                "type": "boolean",
                                "description": "(Deprecated) Same as latest_only",
                                "default": False
                            }
                        },
                        "required": ["query_text"]
                    }
                ),
                Tool(
                    name="get_project_memories",
                    description="Retrieve memories for a scope. Examples: app_id='covenant', project_id='portal'; memory_types=['plan']; latest_only=true.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Required - Application identifier"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Optional - Project identifier to filter by"
                            },
                            "ticket_id": {
                                "type": "string",
                                "description": "Optional - Ticket identifier to filter by"
                            },
                            "run_id": {
                                "type": "string",
                                "description": "Optional - Run identifier (4th hierarchy level). Requires app_id, project_id, AND ticket_id. Use for AutoStack multi-run scenarios."
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 50
                            },
                            "sort_by": {
                                "type": "string",
                                "description": "Sort field: 'timestamp' or 'score'",
                                "default": "timestamp"
                            },
                            "return_format": {
                                "type": "string",
                                "description": "Response format: 'summary_only', 'chunks_only', or 'both'",
                                "default": "both",
                                "enum": ["summary_only", "chunks_only", "both"]
                            },
                            "children_depth": {
                                "type": "integer",
                                "description": "How many levels of children to include beneath the specified scope. 0 = Only this level (default). 1 = This level + immediate children. 2 = This level + 2 levels down. -1 = All children (unlimited depth). Examples at project_id level: depth=0 → project-level only; depth=1 → project + tickets; depth=2 or -1 → project + tickets + runs.",
                                "default": 0
                            },
                            "memory_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict results to these memory types",
                                "default": []
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict results to memories containing these tags",
                                "default": []
                            },
                            "latest_only": {
                                "type": "boolean",
                                "description": "Exclude memories superseded by newer entries (alias: hide_superseded)",
                                "default": False
                            },
                            "hide_superseded": {
                                "type": "boolean",
                                "description": "(Deprecated) Same as latest_only",
                                "default": False
                            }
                        },
                        "required": ["app_id"]
                    }
                ),
                Tool(
                    name="update_memory",
                    description="Updates an existing memory by replacing its content and incrementing version. Finds memory by app_id/project_id/ticket_id/run_id/type combination.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Required - Application identifier"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Optional - Project identifier"
                            },
                            "ticket_id": {
                                "type": "string",
                                "description": "Optional - Ticket identifier"
                            },
                            "run_id": {
                                "type": "string",
                                "description": "Optional - Run identifier (requires app_id, project_id, AND ticket_id). Used to identify memory to update for AutoStack multi-run scenarios."
                            },
                            "memory_type": {
                                "type": "string",
                                "description": "Optional - Memory type to identify which memory to update"
                            },
                            "new_content": {
                                "type": "string",
                                "description": "New content to replace the existing memory"
                            },
                            "metadata_updates": {
                                "type": "object",
                                "description": "Additional metadata fields to update",
                                "additionalProperties": True,
                                "default": {}
                            },
                            "create_if_missing": {
                                "type": "boolean",
                                "description": "If true, creates memory if not found instead of raising 404 error",
                                "default": False
                            }
                        },
                        "required": ["app_id", "new_content"]
                    }
                ),
                Tool(
                    name="delete_run_memories",
                    description="Deletes all memories for a specific run_id (destructive operation, requires exact 4-level match: app_id + project_id + ticket_id + run_id)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Required - Application identifier"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Required - Project identifier"
                            },
                            "ticket_id": {
                                "type": "string",
                                "description": "Required - Ticket identifier"
                            },
                            "run_id": {
                                "type": "string",
                                "description": "Required - Run identifier to delete all memories for"
                            },
                            "dry_run": {
                                "type": "boolean",
                                "description": "If true, preview deletion without actually deleting",
                                "default": False
                            }
                        },
                        "required": ["app_id", "project_id", "ticket_id", "run_id"]
                    }
                ),
                Tool(
                    name="get_recent_memories",
                    description="Retrieves memories from the last N hours, perfect for agents resuming work. Can filter by app_id/project_id/ticket_id/run_id.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Optional - Filter by application identifier"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Optional - Filter by project identifier"
                            },
                            "ticket_id": {
                                "type": "string",
                                "description": "Optional - Filter by ticket identifier (requires app_id AND project_id)"
                            },
                            "run_id": {
                                "type": "string",
                                "description": "Optional - Filter by run identifier (requires app_id, project_id, AND ticket_id). For AutoStack multi-run scenarios."
                            },
                            "hours": {
                                "type": "integer",
                                "description": "Number of hours to look back",
                                "default": 24
                            },
                            "start_time_iso": {
                                "type": "string",
                                "description": "Optional ISO8601 start time to bound results"
                            },
                            "end_time_iso": {
                                "type": "string",
                                "description": "Optional ISO8601 end time to bound results (defaults to now when start_time_iso is set)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 20
                            },
                            "return_format": {
                                "type": "string",
                                "description": "Response format: 'summary_only', 'chunks_only', or 'both'",
                                "default": "both",
                                "enum": ["summary_only", "chunks_only", "both"]
                            },
                            "children_depth": {
                                "type": "integer",
                                "description": "How many levels of children to include beneath the specified scope. 0 = Only this level (default). 1 = This level + immediate children. 2 = This level + 2 levels down. -1 = All children (unlimited depth). Examples at project_id level: depth=0 → project-level only; depth=1 → project + tickets; depth=2 or -1 → project + tickets + runs.",
                                "default": 0
                            },
                            "memory_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict results to these memory types",
                                "default": []
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict results to memories containing these tags",
                                "default": []
                            },
                            "latest_only": {
                                "type": "boolean",
                                "description": "Exclude memories superseded by newer entries (alias: hide_superseded)",
                                "default": False
                            },
                            "hide_superseded": {
                                "type": "boolean",
                                "description": "(Deprecated) Same as latest_only",
                                "default": False
                            }
                        },
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="get_scope_overview",
                    description="Get hierarchy overview including all children (tickets/runs) under a scope. Pass app_id to see projects, add project_id to see tickets, add ticket_id to see runs. Returns counts at each level.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Required - Application identifier to explore"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Optional - Project identifier to explore children for"
                            },
                            "ticket_id": {
                                "type": "string",
                                "description": "Optional - Ticket identifier to list runs for"
                            },
                            "include_counts": {
                                "type": "boolean",
                                "description": "Include memory/run/ticket counts",
                                "default": True
                            },
                            "memory_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict overview to these memory types",
                                "default": []
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict overview to memories containing these tags",
                                "default": []
                            },
                            "latest_only": {
                                "type": "boolean",
                                "description": "Exclude memories superseded by newer entries (alias: hide_superseded)",
                                "default": False
                            },
                            "hide_superseded": {
                                "type": "boolean",
                                "description": "(Deprecated) Same as latest_only",
                                "default": False
                            },
                            "start_time_iso": {
                                "type": "string",
                                "description": "Optional ISO8601 start time bound"
                            },
                            "end_time_iso": {
                                "type": "string",
                                "description": "Optional ISO8601 end time bound"
                            }
                        },
                        "required": ["app_id"]
                    }
                ),
                Tool(
                    name="get_hierarchy_overview",
                    description="(Alias of get_scope_overview) Get children under a scope with counts.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": True
                    }
                ),
                Tool(
                    name="export_memories",
                    description="Export all memories for a scope as JSON (grouped by logical memory).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Required - Application identifier"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Optional - Project identifier"
                            },
                            "ticket_id": {
                                "type": "string",
                                "description": "Optional - Ticket identifier"
                            },
                            "run_id": {
                                "type": "string",
                                "description": "Optional - Run identifier"
                            },
                            "cascade": {
                                "type": "boolean",
                                "description": "Include parent levels alongside the requested scope",
                                "default": True
                            },
                            "memory_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict export to these memory types",
                                "default": []
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Restrict export to memories containing these tags",
                                "default": []
                            },
                            "start_time_iso": {
                                "type": "string",
                                "description": "Optional ISO8601 start time bound"
                            },
                            "end_time_iso": {
                                "type": "string",
                                "description": "Optional ISO8601 end time bound"
                            },
                            "latest_only": {
                                "type": "boolean",
                                "description": "Exclude memories superseded by newer entries (alias: hide_superseded)",
                                "default": False
                            },
                            "hide_superseded": {
                                "type": "boolean",
                                "description": "(Deprecated) Same as latest_only",
                                "default": False
                            }
                        },
                        "required": ["app_id"]
                    }
                ),
                Tool(
                    name="get_quick_start",
                    description="Quick-start guidance: common workflows, when to use each tool, and parameter hints.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="list_app_ids",
                    description="Lists all unique app_ids found in the Memory Hub",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="list_project_ids", 
                    description="Lists all unique project_ids found in the Memory Hub",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="list_ticket_ids",
                    description="Lists all unique ticket_ids found in the Memory Hub", 
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="list_memory_types",
                    description="Lists all memory types used in the Memory Hub with metadata (count, version, last updated). Helps agents understand what types are already in use.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Optional - Filter by application identifier"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Optional - Filter by project identifier"
                            }
                        },
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="get_memory_type_guide",
                    description="Returns a static guide of recommended memory types with guidelines on when to CREATE vs UPDATE",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="health_check",
                    description="Health check endpoint to verify server status",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="get_version",
                    description="Returns the current version of Memory Hub MCP Server",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                # Session Management Tools
                Tool(
                    name="session_resume",
                    description="Resume a session - returns complete context for incoming agent. Retrieves handoffs from ALL tickets in project (not just active_ticket). Creates empty session if none exists. One session per project.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Application identifier"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Project identifier"
                            },
                            "handoff_limit": {
                                "type": "integer",
                                "description": "Number of recent handoffs to retrieve (default 1, max 10)",
                                "default": 1,
                                "minimum": 1,
                                "maximum": 10
                            }
                        },
                        "required": ["app_id", "project_id"]
                    }
                ),
                Tool(
                    name="session_handoff",
                    description="Record a handoff - agent is ending, context is clearing. Stores handoff summary and updates session state atomically.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Application identifier"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Project identifier"
                            },
                            "summary": {
                                "type": "string",
                                "description": "Handoff summary content (what was done, decisions made, next steps)"
                            },
                            "session_updates": {
                                "type": "object",
                                "description": "Optional partial updates to session state (focus, decisions, blockers, next_steps, active_ticket)",
                                "additionalProperties": True
                            }
                        },
                        "required": ["app_id", "project_id", "summary"]
                    }
                ),
                Tool(
                    name="session_update",
                    description="Quick checkpoint - partial update to session state. Use after commits, decisions, or ticket switches.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "app_id": {
                                "type": "string",
                                "description": "Application identifier"
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Project identifier"
                            },
                            "updates": {
                                "type": "object",
                                "description": "Partial updates to session state. Allowed fields: active_ticket, focus, decisions, blockers, next_steps, last_commits",
                                "additionalProperties": True
                            }
                        },
                        "required": ["app_id", "project_id", "updates"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool calls"""
            try:
                if name == "add_memory":
                    # Convert arguments to MemoryItemIn
                    memory_item = MemoryItemIn(
                        content=arguments["content"],
                        metadata=arguments["metadata"],
                        chunking=arguments.get("chunking", True)
                    )
                    result = await add_memory_handler(memory_item, self.config)
                    return [TextContent(
                        type="text",
                        text=f"Memory added successfully: {result.message} ({result.chunks_stored} chunks stored)"
                    )]
                
                elif name == "search_memories":
                    # Convert arguments to MemorySearchRequest
                    latest_only_flag = arguments.get("latest_only", arguments.get("hide_superseded", False))
                    search_request = MemorySearchRequest(
                        query_text=arguments["query_text"],
                        metadata_filters=arguments.get("metadata_filters", {}),
                        keyword_filters=arguments.get("keyword_filters", []),
                        limit=arguments.get("limit", 10),
                        memory_types=arguments.get("memory_types", []),
                        tag_filters=arguments.get("tag_filters", []),
                        group_by_path=arguments.get("group_by_path", False),
                        hide_superseded=latest_only_flag
                    )
                    result = await search_memories_handler(search_request, self.config)
                    
                    # Format response
                    if result.synthesized_summary:
                        response_text = f"## Search Results Summary\n\n{result.synthesized_summary}\n\n"
                    else:
                        response_text = f"## Search Results ({result.total_results} found)\n\n"

                    if result.grouped_results:
                        response_text += "### Grouped by Path\n"
                        for group in result.grouped_results:
                            response_text += f"- {group.path}: {group.memory_count} memories (top score: {group.top_score:.3f})\n"
                        response_text += "\n"

                    for i, chunk in enumerate(result.retrieved_chunks[:5], 1):
                        response_text += f"### Result {i} (Score: {chunk.score:.3f})\n"
                        response_text += f"**Metadata:** {chunk.metadata}\n\n"
                        response_text += f"{chunk.text_chunk}\n\n---\n\n"
                    
                    return [TextContent(type="text", text=response_text)]
                
                elif name == "get_project_memories":
                    # Convert arguments to GetProjectMemoriesRequest
                    latest_only_flag = arguments.get("latest_only", arguments.get("hide_superseded", False))
                    get_request = GetProjectMemoriesRequest(
                        app_id=arguments["app_id"],
                        project_id=arguments.get("project_id"),
                        ticket_id=arguments.get("ticket_id"),
                        run_id=arguments.get("run_id"),
                        limit=arguments.get("limit", 50),
                        sort_by=arguments.get("sort_by", "timestamp"),
                        return_format=arguments.get("return_format", "both"),
                        children_depth=arguments.get("children_depth", 0),
                        memory_types=arguments.get("memory_types", []),
                        tags=arguments.get("tags", []),
                        hide_superseded=latest_only_flag
                    )
                    result = await get_project_memories_handler(get_request, self.config)
                    
                    # Format response
                    if result.synthesized_summary:
                        response_text = f"## Project Memories Summary\n\n{result.synthesized_summary}\n\n"
                    else:
                        response_text = f"## Project Memories ({result.total_results} found)\n\n"
                    
                    for i, chunk in enumerate(result.retrieved_chunks, 1):
                        response_text += f"### Memory {i}\n"
                        response_text += f"**Metadata:** {chunk.metadata}\n\n"
                        response_text += f"{chunk.text_chunk}\n\n---\n\n"
                    
                    return [TextContent(type="text", text=response_text)]
                
                elif name == "update_memory":
                    # Convert arguments to UpdateMemoryRequest
                    update_request = UpdateMemoryRequest(
                        app_id=arguments["app_id"],
                        project_id=arguments.get("project_id"),
                        ticket_id=arguments.get("ticket_id"),
                        run_id=arguments.get("run_id"),
                        memory_type=arguments.get("memory_type"),
                        new_content=arguments["new_content"],
                        metadata_updates=arguments.get("metadata_updates", {}),
                        create_if_missing=arguments.get("create_if_missing", False)
                    )
                    result = await update_memory_handler(update_request, self.config)

                    action = result.get('action', 'updated')
                    if action == 'created':
                        return [TextContent(
                            type="text",
                            text=f"Memory created (did not exist): Version 1 ({result['chunks_stored']} chunks stored)"
                        )]
                    else:
                        return [TextContent(
                            type="text",
                            text=f"Memory updated successfully: Version {result['previous_version']} → {result['new_version']} ({result['chunks_replaced']} chunks replaced)"
                        )]

                elif name == "delete_run_memories":
                    # Convert arguments to DeleteRunMemoriesRequest
                    delete_request = DeleteRunMemoriesRequest(
                        app_id=arguments["app_id"],
                        project_id=arguments["project_id"],
                        ticket_id=arguments["ticket_id"],
                        run_id=arguments["run_id"],
                        dry_run=arguments.get("dry_run", False)
                    )
                    result = await delete_run_memories_handler(delete_request, self.config)

                    # Format response based on dry_run
                    if result["dry_run"]:
                        response_text = f"🔍 **DRY RUN PREVIEW**\n\n"
                        response_text += f"Would delete **{result['deleted_memories']} memories** ({result['deleted_count']} chunks) for run_id: `{result['run_id']}`\n\n"
                        response_text += f"To actually delete, call again with dry_run=false"
                    else:
                        response_text = f"✅ **DELETED**\n\n"
                        response_text += f"Deleted **{result['deleted_memories']} memories** ({result['deleted_count']} chunks) for run_id: `{result['run_id']}`"

                    return [TextContent(
                        type="text",
                        text=response_text
                    )]

                elif name == "get_recent_memories":
                    # Convert arguments to GetRecentMemoriesRequest
                    latest_only_flag = arguments.get("latest_only", arguments.get("hide_superseded", False))
                    recent_request = GetRecentMemoriesRequest(
                        app_id=arguments.get("app_id"),
                        project_id=arguments.get("project_id"),
                        ticket_id=arguments.get("ticket_id"),
                        run_id=arguments.get("run_id"),
                        hours=arguments.get("hours", 24),
                        start_time_iso=arguments.get("start_time_iso"),
                        end_time_iso=arguments.get("end_time_iso"),
                        limit=arguments.get("limit", 20),
                        return_format=arguments.get("return_format", "both"),
                        children_depth=arguments.get("children_depth", 0),
                        memory_types=arguments.get("memory_types", []),
                        tags=arguments.get("tags", []),
                        hide_superseded=latest_only_flag
                    )
                    result = await get_recent_memories_handler(recent_request, self.config)
                    
                    # Format response
                    window_desc = ""
                    if recent_request.start_time_iso or recent_request.end_time_iso:
                        start_label = recent_request.start_time_iso or "unbounded"
                        end_label = recent_request.end_time_iso or "now"
                        window_desc = f"{start_label} → {end_label}"
                    else:
                        window_desc = f"last {recent_request.hours} hours"

                    if result.synthesized_summary:
                        response_text = f"## Recent Memories Summary ({window_desc})\n\n{result.synthesized_summary}\n\n"
                    else:
                        response_text = f"## Recent Memories ({window_desc}, {result.total_results} found)\n\n"
                    
                    for i, chunk in enumerate(result.retrieved_chunks, 1):
                        response_text += f"### Memory {i}\n"
                        response_text += f"**Time:** {chunk.metadata.get('timestamp_iso', 'Unknown')}\n"
                        response_text += f"**App/Project:** {chunk.metadata.get('app_id', 'N/A')}/{chunk.metadata.get('project_id', 'N/A')}\n"
                        response_text += f"**Type:** {chunk.metadata.get('type', 'N/A')}\n\n"
                        response_text += f"{chunk.text_chunk}\n\n---\n\n"
                    
                    return [TextContent(type="text", text=response_text)]

                elif name == "get_scope_overview" or name == "get_hierarchy_overview":
                    latest_only_flag = arguments.get("latest_only", arguments.get("hide_superseded", False))
                    overview_request = HierarchyOverviewRequest(
                        app_id=arguments["app_id"],
                        project_id=arguments.get("project_id"),
                        ticket_id=arguments.get("ticket_id"),
                        include_counts=arguments.get("include_counts", True),
                        memory_types=arguments.get("memory_types", []),
                        tags=arguments.get("tags", []),
                        hide_superseded=latest_only_flag,
                        start_time_iso=arguments.get("start_time_iso"),
                        end_time_iso=arguments.get("end_time_iso")
                    )
                    result = await get_hierarchy_overview_handler(overview_request, self.config)

                    response_text = f"## Hierarchy Overview ({result.app_id})\n"
                    response_text += f"Projects: {result.total_projects}, Tickets: {result.total_tickets}, Runs: {result.total_runs}"
                    if result.total_memories:
                        response_text += f", Memories: {result.total_memories}"
                    response_text += "\n\n"

                    if result.tickets:
                        response_text += "### Tickets\n"
                        for ticket in result.tickets:
                            response_text += f"- {ticket.ticket_id}: {ticket.run_count} runs"
                            if ticket.memory_count:
                                response_text += f", {ticket.memory_count} memories"
                            response_text += "\n"
                    elif result.projects:
                        response_text += "### Projects\n"
                        for project in result.projects:
                            response_text += f"- {project.project_id}: {project.ticket_count} tickets, {project.run_count} runs"
                            if project.memory_count:
                                response_text += f", {project.memory_count} memories"
                            response_text += "\n"
                    elif result.runs:
                        response_text += "### Runs\n"
                        for run in result.runs:
                            response_text += f"- {run.run_id}"
                            if run.memory_count:
                                response_text += f": {run.memory_count} memories"
                            response_text += "\n"

                    return [TextContent(type="text", text=response_text)]

                elif name == "export_memories":
                    latest_only_flag = arguments.get("latest_only", arguments.get("hide_superseded", False))
                    export_request = ExportMemoriesRequest(
                        app_id=arguments["app_id"],
                        project_id=arguments.get("project_id"),
                        ticket_id=arguments.get("ticket_id"),
                        run_id=arguments.get("run_id"),
                        cascade=arguments.get("cascade", True),
                        memory_types=arguments.get("memory_types", []),
                        tags=arguments.get("tags", []),
                        start_time_iso=arguments.get("start_time_iso"),
                        end_time_iso=arguments.get("end_time_iso"),
                        hide_superseded=latest_only_flag
                    )
                    result = await export_memories_handler(export_request, self.config)

                    response_text = f"## Export Complete\n"
                    response_text += f"{result.total_memories} memories ({result.total_chunks} chunks)\n\n"
                    for memory in result.memories[:3]:
                        response_text += f"- {memory.original_content_hash}: type={memory.metadata.get('type', 'unknown')}, "
                        response_text += f"project={memory.metadata.get('project_id', '-')}, ticket={memory.metadata.get('ticket_id', '-')}, run={memory.metadata.get('run_id', '-')}\n"
                    if len(result.memories) > 3:
                        response_text += f"...and {len(result.memories) - 3} more\n"

                    return [
                        TextContent(type="text", text=response_text),
                        TextContent(type="text", text=str(result.dict()))
                    ]

                elif name == "get_quick_start":
                    result = await get_quick_start_info_handler(self.config)
                    response_text = "## Quick Start Guidance\n\n"
                    response_text += "### Workflows\n"
                    for workflow in result["workflows"]:
                        response_text += f"- **{workflow['name']}** → {workflow['tool']}\n"
                        response_text += f"  goal: {workflow['goal']}\n"
                        response_text += f"  example: {workflow['example']}\n"
                    response_text += "\n### Tool Selection\n"
                    for tool, desc in result["tool_selection"].items():
                        response_text += f"- {tool}: {desc}\n"
                    response_text += "\n### Parameter Hints\n"
                    for param, desc in result["parameter_hints"].items():
                        response_text += f"- {param}: {desc}\n"

                    return [TextContent(type="text", text=response_text)]
                
                elif name == "list_app_ids":
                    result = await list_app_ids_handler(self.config)
                    return [TextContent(
                        type="text", 
                        text=f"Found {result.total_count} app_ids: {', '.join(result.ids)}"
                    )]
                
                elif name == "list_project_ids":
                    result = await list_project_ids_handler(self.config)
                    return [TextContent(
                        type="text",
                        text=f"Found {result.total_count} project_ids: {', '.join(result.ids)}"
                    )]
                
                elif name == "list_ticket_ids":
                    result = await list_ticket_ids_handler(self.config)
                    return [TextContent(
                        type="text",
                        text=f"Found {result.total_count} ticket_ids: {', '.join(result.ids)}"
                    )]
                
                elif name == "list_memory_types":
                    # Convert arguments to ListMemoryTypesRequest
                    list_request = ListMemoryTypesRequest(
                        app_id=arguments.get("app_id"),
                        project_id=arguments.get("project_id")
                    )
                    result = await list_memory_types_handler(list_request, self.config)
                    
                    response_text = f"## Memory Types in Use ({result.total_types} types found)\n\n"
                    for type_info in result.memory_types:
                        response_text += f"**{type_info.type_name}**: "
                        response_text += f"{type_info.count} memories, "
                        response_text += f"latest version: {type_info.latest_version}, "
                        response_text += f"last updated: {type_info.last_updated}\n"
                    
                    return [TextContent(type="text", text=response_text)]
                
                elif name == "get_memory_type_guide":
                    result = await get_memory_type_guide_handler(self.config)
                    
                    response_text = "## Memory Type Guide\n\n"
                    response_text += "### CREATE Types (Historical Records)\n"
                    for t in result.create_new_types:
                        response_text += f"- `{t}`\n"
                    
                    response_text += "\n### UPDATE Types (Living Documents)\n"
                    for t in result.update_types:
                        response_text += f"- `{t}`\n"
                    
                    response_text += f"\n### Guidelines\n{result.guidelines}"
                    
                    return [TextContent(type="text", text=response_text)]
                
                elif name == "health_check":
                    result = await health_check_handler(self.config)
                    return [TextContent(
                        type="text",
                        text=f"Health check passed: {result['status']}"
                    )]

                elif name == "get_version":
                    return [TextContent(
                        type="text",
                        text=f"Memory Hub MCP Server v{VERSION}"
                    )]

                # Session Management Handlers
                elif name == "session_resume":
                    resume_request = SessionResumeRequest(
                        app_id=arguments["app_id"],
                        project_id=arguments["project_id"],
                        handoff_limit=arguments.get("handoff_limit", 1)
                    )
                    result = await session_resume_handler(resume_request, self.config)

                    response_text = f"## Session: {arguments['app_id']}/{arguments['project_id']}\n\n"
                    if result.is_new_session:
                        response_text += "**New session created**\n\n"

                    state = result.session_state
                    response_text += f"**Active Ticket:** {state.active_ticket or 'None'}\n"
                    response_text += f"**Focus:** {state.focus or 'Not set'}\n"
                    if state.decisions:
                        response_text += f"**Decisions:** {', '.join(state.decisions)}\n"
                    if state.blockers:
                        response_text += f"**Blockers:** {', '.join(state.blockers)}\n"
                    if state.next_steps:
                        response_text += f"**Next Steps:** {', '.join(state.next_steps)}\n"
                    if state.last_commits:
                        response_text += f"**Recent Commits:** {', '.join(state.last_commits[:3])}\n"
                    if state.last_handoff_at:
                        response_text += f"**Last Handoff:** {state.last_handoff_at}\n"

                    # Show ticket history
                    if state.ticket_history:
                        response_text += "\n**Ticket History:**\n"
                        # Sort by timestamp descending
                        sorted_tickets = sorted(state.ticket_history.items(), key=lambda x: x[1], reverse=True)
                        for ticket_id, timestamp in sorted_tickets[:5]:
                            response_text += f"- {ticket_id}: {timestamp}\n"

                    # Show handoffs from ALL tickets
                    if result.handoffs:
                        response_text += f"\n### Handoffs ({len(result.handoffs)})\n"
                        for handoff in result.handoffs:
                            response_text += f"\n**[{handoff.ticket_id}]** ({handoff.timestamp})\n"
                            response_text += f"{handoff.content}\n"

                    if result.recent_memories:
                        response_text += f"\n### Recent Memories ({len(result.recent_memories)})\n"
                        for mem in result.recent_memories[:5]:
                            mem_type = mem.metadata.get('type', 'unknown')
                            response_text += f"- [{mem_type}] {mem.text_chunk[:100]}...\n"

                    return [TextContent(type="text", text=response_text)]

                elif name == "session_handoff":
                    handoff_request = SessionHandoffRequest(
                        app_id=arguments["app_id"],
                        project_id=arguments["project_id"],
                        summary=arguments["summary"],
                        session_updates=arguments.get("session_updates")
                    )
                    result = await session_handoff_handler(handoff_request, self.config)

                    response_text = f"## Handoff Recorded\n\n"
                    response_text += f"**{result.message}**\n"
                    response_text += f"**Stored at:** {result.handoff_stored_at}\n\n"
                    response_text += "### Updated Session State\n"
                    state = result.session_state
                    response_text += f"- Focus: {state.focus or 'Not set'}\n"
                    response_text += f"- Next Steps: {', '.join(state.next_steps) if state.next_steps else 'None'}\n"

                    return [TextContent(type="text", text=response_text)]

                elif name == "session_update":
                    update_request = SessionUpdateRequest(
                        app_id=arguments["app_id"],
                        project_id=arguments["project_id"],
                        updates=arguments["updates"]
                    )
                    result = await session_update_handler(update_request, self.config)

                    response_text = f"## Session Updated\n\n"
                    response_text += f"**{result.message}**\n\n"
                    response_text += f"Updated fields: {', '.join(arguments['updates'].keys())}\n"

                    return [TextContent(type="text", text=response_text)]

                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(
                    type="text",
                    text=f"Error executing {name}: {str(e)}"
                )]
    
    async def run(self):
        """Run the MCP server with stdio transport"""
        try:
            # Initialize core services
            await startup_event(self.config)
            logger.info("Memory Hub core services initialized")
            
            # Initialize HTTP client for internal operations
            self.config.http_client = httpx.AsyncClient()
            
            # Import and run stdio server
            from mcp.server.stdio import stdio_server
            
            async with stdio_server() as (read_stream, write_stream):
                logger.info("Memory Hub MCP Server starting with stdio transport")
                await self.server.run(
                    read_stream, 
                    write_stream,
                    InitializationOptions(
                        server_name="memory-hub",
                        server_version="0.1.0",
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={}
                        )
                    )
                )
        except Exception as e:
            logger.error(f"Error running MCP server: {e}")
            raise
        finally:
            await shutdown_event(self.config)
            logger.info("Shutdown complete.")

def create_server(config: AppConfig) -> MemoryHubMCPServer:
    """Create an instance of the Memory Hub MCP Server"""
    return MemoryHubMCPServer(config) 
