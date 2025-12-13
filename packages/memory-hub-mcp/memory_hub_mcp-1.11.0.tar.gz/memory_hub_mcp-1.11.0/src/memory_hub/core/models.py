# models.py - Pydantic models for Memory Hub MCP Server

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any

# --- Pydantic Models ---
class MemoryItemIn(BaseModel):
    content: str = Field(..., description="The content to store in memory")
    metadata: Dict[str, Any] = Field(
        ...,
        description=(
            "Metadata with hierarchical structure. "
            "RULES: app_id is required. "
            "project_id requires app_id. "
            "ticket_id requires both app_id AND project_id. "
            "Example: {app_id: 'crossroads', project_id: 'auth', type: 'api_design'}"
        )
    )
    chunking: bool = Field(
        default=True,
        description=(
            "Enable semantic chunking (default: true). "
            "Set to false for large structured documents (e.g., AutoStack plans, specifications) "
            "that don't need semantic search and should be stored as a single unit."
        )
    )

class MemorySearchRequest(BaseModel):
    query_text: str = Field(..., description="The query text to search for")
    metadata_filters: Dict[str, str] = Field(default_factory=dict, description="Metadata filters for search (scope)")
    keyword_filters: List[str] = Field(default_factory=list, description="List of keywords that results must contain")
    memory_types: List[str] = Field(default_factory=list, description="Restrict results to these memory types (OR logic)")
    tag_filters: List[str] = Field(default_factory=list, description="Restrict results to memories that include any of these tags")
    limit: int = Field(default=10, description="Maximum number of results to return")
    group_by_path: bool = Field(
        default=False,
        description="Display: Group results by hierarchy path (app/project/ticket/run) instead of a flat list"
    )
    hide_superseded: bool = Field(
        default=False,
        alias="latest_only",
        description="Display: When true, remove memories superseded by newer ones in the result set (alias: latest_only)"
    )

    class Config:
        allow_population_by_field_name = True

class RetrievedChunk(BaseModel):
    text_chunk: str
    metadata: Dict[str, Any]
    score: float
    chunk_id: str

class SearchResponse(BaseModel):
    synthesized_summary: Optional[str] = Field(default=None, description="AI-generated summary of results")
    retrieved_chunks: List[RetrievedChunk]
    total_results: int
    grouped_results: Optional[List["PathGroupedResults"]] = Field(
        default=None,
        description="Optional grouping of results by hierarchy path when group_by_path is enabled"
    )

class AddMemoryResponse(BaseModel):
    message: str
    chunks_stored: int
    original_content_hash: str

# --- New Introspection Models ---
class ListIdsResponse(BaseModel):
    ids: List[str] = Field(..., description="List of unique identifiers found")
    total_count: int = Field(..., description="Total number of unique identifiers")
    points_scanned: int = Field(..., description="Number of points scanned to extract IDs")

class MemoryTypeInfo(BaseModel):
    type_name: str = Field(..., description="The memory type name")
    count: int = Field(..., description="Number of memories with this type")
    latest_version: int = Field(..., description="Highest version number for this type")
    last_updated: str = Field(..., description="ISO timestamp of most recent memory")

class ListMemoryTypesResponse(BaseModel):
    memory_types: List[MemoryTypeInfo] = Field(..., description="List of memory types with metadata")
    total_types: int = Field(..., description="Total number of unique memory types")
    points_scanned: int = Field(..., description="Number of points scanned")

class GetProjectMemoriesRequest(BaseModel):
    app_id: str = Field(..., description="Required - Application identifier")
    project_id: Optional[str] = Field(
        None,
        description="Optional - Project identifier. Requires app_id."
    )
    ticket_id: Optional[str] = Field(
        None,
        description="Optional - Ticket identifier. Requires both app_id AND project_id."
    )
    run_id: Optional[str] = Field(
        None,
        description=(
            "Optional - Run identifier (4th hierarchy level). "
            "Requires app_id, project_id, AND ticket_id. "
            "Use for AutoStack multi-run scenarios."
        )
    )
    limit: int = Field(default=50, description="Maximum number of results to return")
    sort_by: str = Field(default="timestamp", description="Sort field: 'timestamp' or 'score'")
    return_format: str = Field(
        default="both",
        description=(
            "Response format: 'summary_only', 'chunks_only', or 'both'. "
            "summary_only: AI-generated summary only (~80%% token reduction). "
            "chunks_only: Raw memory chunks without LLM interpretation. "
            "both: Summary + chunks (default, backward compatible)."
        )
    )
    children_depth: int = Field(
        default=0,
        description=(
            "How many levels of children to include beneath the specified scope. "
            "0 = Only this level (default). "
            "1 = This level + immediate children. "
            "2 = This level + 2 levels down. "
            "-1 = All children (unlimited depth). "
            "Examples at project_id level: "
            "depth=0 → project-level only; "
            "depth=1 → project + tickets; "
            "depth=2 or -1 → project + tickets + runs."
        )
    )
    memory_types: List[str] = Field(
        default_factory=list,
        description="Filtering: Restrict results to these memory types (OR logic)"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Filtering: Restrict results to memories containing at least one of these tags"
    )
    hide_superseded: bool = Field(
        default=False,
        alias="latest_only",
        description="Display: When true, filters out memories that were superseded by newer entries (alias: latest_only)"
    )

    class Config:
        allow_population_by_field_name = True

class UpdateMemoryRequest(BaseModel):
    app_id: str = Field(..., description="Required - Application identifier")
    project_id: Optional[str] = Field(
        None,
        description="Optional - Project identifier (requires app_id)"
    )
    ticket_id: Optional[str] = Field(
        None,
        description="Optional - Ticket identifier (requires app_id AND project_id)"
    )
    run_id: Optional[str] = Field(
        None,
        description="Optional - Run identifier (requires app_id, project_id, AND ticket_id). Used to identify memory to update for AutoStack multi-run scenarios."
    )
    memory_type: Optional[str] = Field(None, description="Optional - Memory type to identify which memory to update")
    new_content: str = Field(..., description="New content to replace the existing memory")
    metadata_updates: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata fields to update")
    create_if_missing: bool = Field(
        default=False,
        description="If true, creates memory if not found instead of raising 404 error"
    )

class DeleteRunMemoriesRequest(BaseModel):
    app_id: str = Field(..., description="Required - Application identifier")
    project_id: str = Field(..., description="Required - Project identifier")
    ticket_id: str = Field(..., description="Required - Ticket identifier")
    run_id: str = Field(..., description="Required - Run identifier to delete all memories for")
    dry_run: bool = Field(False, description="If true, preview deletion without actually deleting")

class GetRecentMemoriesRequest(BaseModel):
    app_id: Optional[str] = Field(None, description="Optional - Filter by application identifier")
    project_id: Optional[str] = Field(
        None,
        description="Optional - Filter by project identifier (requires app_id)"
    )
    ticket_id: Optional[str] = Field(
        None,
        description="Optional - Filter by ticket identifier (requires app_id AND project_id)"
    )
    run_id: Optional[str] = Field(
        None,
        description="Optional - Filter by run identifier (requires app_id, project_id, AND ticket_id). For AutoStack multi-run scenarios."
    )
    hours: int = Field(default=24, description="Number of hours to look back (default: 24)")
    limit: int = Field(default=20, description="Maximum number of results to return")
    return_format: str = Field(
        default="both",
        description=(
            "Response format: 'summary_only', 'chunks_only', or 'both'. "
            "summary_only: AI-generated summary only (~80%% token reduction). "
            "chunks_only: Raw memory chunks without LLM interpretation. "
            "both: Summary + chunks (default, backward compatible)."
        )
    )
    children_depth: int = Field(
        default=0,
        description=(
            "How many levels of children to include beneath the specified scope. "
            "0 = Only this level (default). "
            "1 = This level + immediate children. "
            "2 = This level + 2 levels down. "
            "-1 = All children (unlimited depth). "
            "Examples at project_id level: "
            "depth=0 → project-level only; "
            "depth=1 → project + tickets; "
            "depth=2 or -1 → project + tickets + runs."
        )
    )
    start_time_iso: Optional[str] = Field(
        None,
        description="Optional ISO8601 start time for retrieval window. Overrides hours when provided."
    )
    end_time_iso: Optional[str] = Field(
        None,
        description="Optional ISO8601 end time for retrieval window (defaults to now when start_time_iso is set)."
    )
    memory_types: List[str] = Field(
        default_factory=list,
        description="Filtering: Restrict results to these memory types (OR logic)"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Filtering: Restrict results to memories containing at least one of these tags"
    )
    hide_superseded: bool = Field(
        default=False,
        alias="latest_only",
        description="Display: When true, filters out memories superseded by newer entries (alias: latest_only)"
    )

    class Config:
        allow_population_by_field_name = True

class ListMemoryTypesRequest(BaseModel):
    app_id: Optional[str] = Field(None, description="Optional - Filter by application identifier")
    project_id: Optional[str] = Field(None, description="Optional - Filter by project identifier")

class GetMemoryTypeGuideResponse(BaseModel):
    create_new_types: List[str] = Field(..., description="Memory types that should always CREATE new memories")
    update_types: List[str] = Field(..., description="Memory types that should typically be UPDATED")
    guidelines: str = Field(..., description="Guidelines for using memory types")


class PathGroupedResults(BaseModel):
    path: str = Field(..., description="Hierarchy path label (e.g., app/project/ticket/run)")
    app_id: Optional[str] = None
    project_id: Optional[str] = None
    ticket_id: Optional[str] = None
    run_id: Optional[str] = None
    memory_count: int = Field(..., description="Distinct memories represented in this path")
    top_score: float = Field(..., description="Highest score among chunks in this path")
    chunks: List[RetrievedChunk] = Field(default_factory=list, description="Chunks belonging to this path")


class RunSummary(BaseModel):
    run_id: str = Field(..., description="Run identifier")
    memory_count: int = Field(..., description="Distinct memories associated with this run")


class TicketSummary(BaseModel):
    ticket_id: str = Field(..., description="Ticket identifier")
    run_count: int = Field(..., description="Number of runs under this ticket")
    memory_count: int = Field(..., description="Distinct memories under this ticket (including runs)")
    runs: List[RunSummary] = Field(default_factory=list, description="Run summaries for this ticket")


class ProjectSummary(BaseModel):
    project_id: str = Field(..., description="Project identifier")
    ticket_count: int = Field(..., description="Number of tickets under this project")
    run_count: int = Field(..., description="Number of runs across all tickets")
    memory_count: int = Field(..., description="Distinct memories under this project")
    tickets: List[TicketSummary] = Field(default_factory=list, description="Ticket summaries for this project")


class HierarchyOverviewRequest(BaseModel):
    app_id: str = Field(..., description="Required - Application identifier to explore")
    project_id: Optional[str] = Field(None, description="Optional - Project scope to explore children of")
    ticket_id: Optional[str] = Field(None, description="Optional - Ticket scope to explore runs of")
    include_counts: bool = Field(
        default=True,
        description="Include memory/run/ticket counts in the response (disabling can reduce computation)"
    )
    memory_types: List[str] = Field(default_factory=list, description="Restrict counts to these memory types")
    tags: List[str] = Field(default_factory=list, description="Restrict counts to memories containing these tags")
    hide_superseded: bool = Field(
        default=False,
        alias="latest_only",
        description="Display: When true, ignores memories superseded by newer entries (alias: latest_only)"
    )
    start_time_iso: Optional[str] = Field(
        None,
        description="Optional ISO8601 start time to constrain counted memories"
    )

    class Config:
        allow_population_by_field_name = True
    end_time_iso: Optional[str] = Field(
        None,
        description="Optional ISO8601 end time to constrain counted memories (defaults to now when start_time_iso is set)"
    )


class HierarchyOverviewResponse(BaseModel):
    app_id: str
    project_id: Optional[str] = None
    ticket_id: Optional[str] = None
    total_projects: int
    total_tickets: int
    total_runs: int
    total_memories: int
    projects: List[ProjectSummary] = Field(default_factory=list)
    tickets: List[TicketSummary] = Field(default_factory=list)
    runs: List[RunSummary] = Field(default_factory=list)
    filters_applied: Dict[str, Any] = Field(default_factory=dict, description="Echo of filters used to build the overview")


class ExportMemoriesRequest(BaseModel):
    app_id: str = Field(..., description="Required - Application identifier to export")
    project_id: Optional[str] = Field(None, description="Optional - Project identifier")
    ticket_id: Optional[str] = Field(None, description="Optional - Ticket identifier")
    run_id: Optional[str] = Field(None, description="Optional - Run identifier")
    cascade: bool = Field(
        default=True,
        description="Include parent levels alongside the requested scope (mirrors get_project_memories behavior)"
    )
    memory_types: List[str] = Field(default_factory=list, description="Restrict export to these memory types")
    tags: List[str] = Field(default_factory=list, description="Restrict export to memories containing these tags")
    start_time_iso: Optional[str] = Field(None, description="Optional ISO8601 start time to bound export window")
    end_time_iso: Optional[str] = Field(None, description="Optional ISO8601 end time to bound export window")
    hide_superseded: bool = Field(
        default=False,
        alias="latest_only",
        description="Display: When true, omits memories superseded by newer entries (alias: latest_only)"
    )

    class Config:
        allow_population_by_field_name = True


class ExportedMemory(BaseModel):
    original_content_hash: str = Field(..., description="Logical memory identifier across chunks")
    metadata: Dict[str, Any] = Field(..., description="Metadata associated with the memory (chunk-level fields stripped)")
    content: str = Field(..., description="Full reconstructed content for this memory")
    chunk_count: int = Field(..., description="Number of chunks that composed this memory")


class ExportMemoriesResponse(BaseModel):
    app_id: str
    project_id: Optional[str] = None
    ticket_id: Optional[str] = None
    run_id: Optional[str] = None
    total_memories: int
    total_chunks: int
    memories: List[ExportedMemory]


# --- Session Management Models ---

class SessionState(BaseModel):
    """Session state structure for project-level context tracking."""
    active_ticket: Optional[str] = Field(None, description="Currently active ticket_id")
    focus: Optional[str] = Field(None, description="Current work focus (free-form)")
    decisions: List[str] = Field(default_factory=list, description="Key decisions made during session")
    blockers: List[str] = Field(default_factory=list, description="Current blockers or issues")
    next_steps: List[str] = Field(default_factory=list, description="Planned next actions")
    last_commits: List[str] = Field(default_factory=list, description="Recent commit SHAs/messages (max 5)")
    last_handoff_at: Optional[str] = Field(None, description="ISO timestamp of last handoff")
    ticket_history: Dict[str, str] = Field(default_factory=dict, description="Map of ticket_id → last activity timestamp")
    created_at: str = Field(default="", description="ISO timestamp when session was created")
    updated_at: str = Field(default="", description="ISO timestamp of last update")


class HandoffInfo(BaseModel):
    """Information about a single handoff."""
    ticket_id: str = Field(..., description="Ticket where this handoff was stored")
    content: str = Field(..., description="Handoff summary content")
    timestamp: str = Field(..., description="ISO timestamp when handoff was created")


class SessionResumeRequest(BaseModel):
    """Request to resume a session - returns full context for incoming agent."""
    app_id: str = Field(..., description="Application identifier")
    project_id: str = Field(..., description="Project identifier")
    handoff_limit: int = Field(1, description="Number of recent handoffs to retrieve (default 1)", ge=1, le=10)


class SessionResumeResponse(BaseModel):
    """Response containing complete session context for resuming work."""
    session_state: SessionState = Field(..., description="Current session state")
    handoffs: List[HandoffInfo] = Field(default_factory=list, description="Recent handoffs from across all tickets in project")
    recent_memories: List[RetrievedChunk] = Field(default_factory=list, description="Recent memories from active ticket")
    is_new_session: bool = Field(False, description="True if session was just created (no prior state)")


class SessionHandoffRequest(BaseModel):
    """Request to record a handoff - agent is ending, context is clearing."""
    app_id: str = Field(..., description="Application identifier")
    project_id: str = Field(..., description="Project identifier")
    summary: str = Field(..., description="Handoff summary content (what was done, next steps, etc.)")
    session_updates: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional partial updates to session state (focus, decisions, blockers, next_steps, active_ticket)"
    )


class SessionHandoffResponse(BaseModel):
    """Response confirming handoff was recorded."""
    message: str = Field(..., description="Confirmation message")
    session_state: SessionState = Field(..., description="Updated session state after handoff")
    handoff_stored_at: str = Field(..., description="ISO timestamp when handoff was stored")


class SessionUpdateRequest(BaseModel):
    """Request for partial session state update - quick checkpoint."""
    app_id: str = Field(..., description="Application identifier")
    project_id: str = Field(..., description="Project identifier")
    updates: Dict[str, Any] = Field(
        ...,
        description="Partial updates to session state. Allowed fields: active_ticket, focus, decisions, blockers, next_steps, last_commits"
    )


class SessionUpdateResponse(BaseModel):
    """Response confirming session update."""
    message: str = Field(..., description="Confirmation message")
    session_state: SessionState = Field(..., description="Updated session state")


# Resolve forward references (Pydantic v2 syntax)
SearchResponse.model_rebuild()
