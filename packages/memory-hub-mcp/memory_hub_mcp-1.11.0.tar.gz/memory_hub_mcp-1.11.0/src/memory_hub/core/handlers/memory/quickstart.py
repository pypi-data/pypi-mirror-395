# memory/quickstart.py - get_quick_start_info handler

import logging

from ...services import AppConfig

from .utils import ValidationError

logger = logging.getLogger(__name__)


async def get_quick_start_info(config: AppConfig):
    """
    Returns quick-start guidance for agents on which tool to use and how.
    """
    try:
        return {
            "workflows": [
                {
                    "name": "Session resume (agent starting)",
                    "tool": "session_resume",
                    "example": {
                        "app_id": "covenant",
                        "project_id": "portal"
                    },
                    "goal": "Get full context: session state + latest handoff + recent memories. Creates session if none exists."
                },
                {
                    "name": "Session handoff (agent ending)",
                    "tool": "session_handoff",
                    "example": {
                        "app_id": "covenant",
                        "project_id": "portal",
                        "summary": "Completed JWT auth implementation. Tests passing. Next: add refresh tokens.",
                        "session_updates": {"focus": "JWT refresh tokens", "next_steps": ["Add refresh endpoint"]}
                    },
                    "goal": "Record comprehensive handoff for next agent. Atomically stores handoff + updates session."
                },
                {
                    "name": "Session update (checkpoint)",
                    "tool": "session_update",
                    "example": {
                        "app_id": "covenant",
                        "project_id": "portal",
                        "updates": {"last_commits": ["abc123: Fix bug"], "decisions": ["Use RS256"]}
                    },
                    "goal": "Quick checkpoint after commits or decisions. Partial session state update."
                },
                {
                    "name": "Browse scope children",
                    "tool": "get_scope_overview (alias: get_hierarchy_overview)",
                    "example": {
                        "app_id": "covenant",
                        "project_id": "portal"
                    },
                    "goal": "See tickets/runs and counts without fetching content."
                },
                {
                    "name": "Load context",
                    "tool": "get_project_memories",
                    "example": {
                        "app_id": "covenant",
                        "project_id": "portal",
                        "memory_types": ["plan"],
                        "latest_only": True,
                        "return_format": "summary_only"
                    },
                    "goal": "Retrieve scope memories (optionally filtered) with summaries."
                },
                {
                    "name": "Time-bounded recap",
                    "tool": "get_recent_memories",
                    "example": {
                        "app_id": "covenant",
                        "hours": 48,
                        "latest_only": True
                    },
                    "goal": "Summarize what changed recently."
                },
                {
                    "name": "Global search",
                    "tool": "search_memories",
                    "example": {
                        "query_text": "LLM prompt safety",
                        "metadata_filters": {"app_id": "covenant"},
                        "memory_types": ["decision"],
                        "group_by_path": True
                    },
                    "goal": "Semantic search grouped by hierarchy path."
                },
                {
                    "name": "Export for analysis",
                    "tool": "export_memories",
                    "example": {
                        "app_id": "covenant",
                        "project_id": "portal",
                        "latest_only": True
                    },
                    "goal": "Get JSON snapshot of memories."
                }
            ],
            "tool_selection": {
                "session_resume": "Agent starting: get session state + handoff + recent memories (one session per project).",
                "session_handoff": "Agent ending: store handoff summary + update session atomically.",
                "session_update": "Quick checkpoint: partial update (commits, decisions, focus, active_ticket).",
                "get_scope_overview": "List children (projects/tickets/runs) and counts for orientation.",
                "get_project_memories": "Pull scoped memories (optionally filtered by type/tags) with cascade control.",
                "get_recent_memories": "Retrieve recent activity within a time window (hours or explicit dates).",
                "search_memories": "Semantic search; combine with scope filters; group_by_path for path context.",
                "add_memory": "Store new memory (set chunking=false for large structured docs).",
                "update_memory": "Replace content with version increment (use memory_type + ids).",
                "export_memories": "Download scoped memories as JSON.",
            },
            "parameter_hints": {
                "latest_only": "Use to hide superseded memories when multiple versions exist.",
                "memory_types": "Filter to specific types (plan, decision, bug_fix, etc.).",
                "tags": "Cross-cutting labels (e.g., auth, ui).",
                "cascade": "true to include parents; false for exact-level/status checks.",
                "group_by_path": "For search: returns grouped results by app/project/ticket/run path."
            }
        }
    except Exception as e:
        logger.error(f" Unexpected error in get_quick_start_info: {e}")
        raise ValidationError(status_code=500, detail="Failed to build quick start guidance")
