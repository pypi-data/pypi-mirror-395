"""
Core functionality for Memory Hub MCP Server
"""

from .models import (
    MemoryItemIn,
    MemorySearchRequest, 
    SearchResponse,
    AddMemoryResponse,
    ListIdsResponse,
    RetrievedChunk
)

from .services import (
    get_embedding,
    synthesize_search_results,
    startup_event,
    shutdown_event,
    AppConfig
)

__all__ = [
    "MemoryItemIn",
    "MemorySearchRequest", 
    "SearchResponse",
    "AddMemoryResponse",
    "ListIdsResponse",
    "RetrievedChunk",
    "get_embedding", 
    "synthesize_search_results",
    "startup_event",
    "shutdown_event",
    "AppConfig"
] 