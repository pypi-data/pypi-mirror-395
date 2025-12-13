# memory/session.py - Session management handlers
#
# Provides atomic session operations for dev-session skill:
# - session_resume: Get full context for incoming agent
# - session_handoff: Record handoff and update session
# - session_update: Partial session state update

import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from qdrant_client.http import models

from ...config import QDRANT_COLLECTION_NAME
from ...models import (
    SessionState,
    SessionResumeRequest,
    SessionResumeResponse,
    SessionHandoffRequest,
    SessionHandoffResponse,
    SessionUpdateRequest,
    SessionUpdateResponse,
    RetrievedChunk,
    MemoryItemIn,
    HandoffInfo,
)
from ...services import AppConfig

from .utils import ValidationError, safe_int_conversion
from .add import add_memory

logger = logging.getLogger(__name__)

# Constants for session storage
SESSION_TICKET_ID = "_session"
SESSION_INDEX_TYPE = "index"
HANDOFF_TYPE = "handoff"

# Allowed fields for session updates
ALLOWED_SESSION_FIELDS = {
    "active_ticket", "focus", "decisions", "blockers",
    "next_steps", "last_commits"
}


async def _get_session_state(
    app_id: str,
    project_id: str,
    config: AppConfig
) -> Optional[SessionState]:
    """
    Retrieves the current session state from Qdrant.
    Returns None if no session exists.

    Note: Only retrieves single-chunk sessions (total_chunks=1).
    Legacy multi-chunk sessions from old skill are ignored.
    """
    try:
        # Query for session at _session/index
        # Filter for total_chunks=1 to ignore legacy multi-chunk sessions
        filter_conditions = models.Filter(
            must=[
                models.FieldCondition(key="app_id", match=models.MatchValue(value=app_id)),
                models.FieldCondition(key="project_id", match=models.MatchValue(value=project_id)),
                models.FieldCondition(key="ticket_id", match=models.MatchValue(value=SESSION_TICKET_ID)),
                models.FieldCondition(key="type", match=models.MatchValue(value=SESSION_INDEX_TYPE)),
                models.FieldCondition(key="total_chunks", match=models.MatchValue(value=1)),
            ]
        )

        results, _ = config.qdrant_client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            scroll_filter=filter_conditions,
            limit=10,
            with_payload=True,
            with_vectors=False
        )

        if not results:
            return None

        # Get the latest version (highest version number)
        latest_point = max(results, key=lambda p: safe_int_conversion(p.payload.get("version", 1), 1))

        # Parse JSON content from text_chunk
        content = latest_point.payload.get("text_chunk", "{}")
        try:
            state_dict = json.loads(content)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse session state JSON for {app_id}/{project_id}, using as-is")
            state_dict = {}

        return SessionState(**state_dict)

    except Exception as e:
        logger.error(f"Error getting session state for {app_id}/{project_id}: {e}")
        return None


async def _save_session_state(
    app_id: str,
    project_id: str,
    state: SessionState,
    config: AppConfig
) -> None:
    """
    Persists session state to Qdrant using add_memory.
    Creates new or updates existing session.
    """
    # Serialize state to JSON
    state_json = state.model_dump_json()

    # Get current version if exists (only single-chunk sessions)
    existing = await _get_session_state(app_id, project_id, config)
    version = 1
    if existing:
        # Find current version and increment (only from single-chunk sessions)
        filter_conditions = models.Filter(
            must=[
                models.FieldCondition(key="app_id", match=models.MatchValue(value=app_id)),
                models.FieldCondition(key="project_id", match=models.MatchValue(value=project_id)),
                models.FieldCondition(key="ticket_id", match=models.MatchValue(value=SESSION_TICKET_ID)),
                models.FieldCondition(key="type", match=models.MatchValue(value=SESSION_INDEX_TYPE)),
                models.FieldCondition(key="total_chunks", match=models.MatchValue(value=1)),
            ]
        )
        results, _ = config.qdrant_client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            scroll_filter=filter_conditions,
            limit=10,
            with_payload=True,
            with_vectors=False
        )
        if results:
            max_version = max(safe_int_conversion(p.payload.get("version", 1), 1) for p in results)
            version = max_version + 1

    # Store using add_memory
    memory_item = MemoryItemIn(
        content=state_json,
        metadata={
            "app_id": app_id,
            "project_id": project_id,
            "ticket_id": SESSION_TICKET_ID,
            "type": SESSION_INDEX_TYPE,
            "version": version,
            "timestamp_iso": datetime.utcnow().isoformat() + "Z"
        },
        chunking=False  # Store as single unit
    )

    await add_memory(memory_item, config)
    logger.info(f"Saved session state v{version} for {app_id}/{project_id}")


async def _get_latest_handoffs(
    app_id: str,
    project_id: str,
    config: AppConfig,
    limit: int = 1
) -> List[HandoffInfo]:
    """
    Retrieves the most recent handoffs from ALL tickets in the project.
    Returns list of HandoffInfo sorted by timestamp (most recent first).
    """
    try:
        # Search for handoffs across ALL tickets in the project
        filter_conditions = models.Filter(
            must=[
                models.FieldCondition(key="app_id", match=models.MatchValue(value=app_id)),
                models.FieldCondition(key="project_id", match=models.MatchValue(value=project_id)),
                models.FieldCondition(key="type", match=models.MatchValue(value=HANDOFF_TYPE)),
                # Only get single-chunk handoffs (new format)
                models.FieldCondition(key="total_chunks", match=models.MatchValue(value=1)),
            ]
        )

        results, _ = config.qdrant_client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            scroll_filter=filter_conditions,
            limit=limit * 5,  # Get more to account for deduplication
            with_payload=True,
            with_vectors=False
        )

        if not results:
            return []

        # Parse timestamps and sort
        def get_timestamp(point):
            ts = point.payload.get("timestamp_iso", "")
            try:
                return datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except:
                return datetime.min

        # Sort by timestamp descending (most recent first)
        sorted_results = sorted(results, key=get_timestamp, reverse=True)

        # Convert to HandoffInfo list
        handoffs = []
        seen_content_hashes = set()
        for point in sorted_results:
            # Deduplicate by content hash
            content_hash = point.payload.get("original_content_hash", "")
            if content_hash in seen_content_hashes:
                continue
            seen_content_hashes.add(content_hash)

            handoffs.append(HandoffInfo(
                ticket_id=point.payload.get("ticket_id", "_unknown"),
                content=point.payload.get("text_chunk", ""),
                timestamp=point.payload.get("timestamp_iso", "")
            ))

            if len(handoffs) >= limit:
                break

        return handoffs

    except Exception as e:
        logger.error(f"Error getting handoffs for {app_id}/{project_id}: {e}")
        return []


async def _get_recent_ticket_memories(
    app_id: str,
    project_id: str,
    ticket_id: str,
    config: AppConfig,
    hours: int = 24,
    limit: int = 10
) -> List[RetrievedChunk]:
    """
    Get recent memories from a specific ticket (excluding session and handoffs).
    """
    try:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        cutoff_iso = cutoff.isoformat() + "Z"

        filter_conditions = models.Filter(
            must=[
                models.FieldCondition(key="app_id", match=models.MatchValue(value=app_id)),
                models.FieldCondition(key="project_id", match=models.MatchValue(value=project_id)),
                models.FieldCondition(key="ticket_id", match=models.MatchValue(value=ticket_id)),
                models.FieldCondition(
                    key="timestamp_iso",
                    range=models.Range(gte=cutoff_iso)
                ),
            ],
            must_not=[
                # Exclude session index
                models.FieldCondition(key="type", match=models.MatchValue(value=SESSION_INDEX_TYPE)),
            ]
        )

        results, _ = config.qdrant_client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            scroll_filter=filter_conditions,
            limit=limit * 3,  # Get more to account for multiple chunks per memory
            with_payload=True,
            with_vectors=False
        )

        # Convert to RetrievedChunk format
        chunks = []
        seen_hashes = set()
        for point in results:
            content_hash = point.payload.get("original_content_hash", "")
            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)

            chunks.append(RetrievedChunk(
                text_chunk=point.payload.get("text_chunk", ""),
                metadata={k: v for k, v in point.payload.items() if k != "text_chunk"},
                score=1.0,
                chunk_id=str(point.id)
            ))

            if len(chunks) >= limit:
                break

        return chunks

    except Exception as e:
        logger.error(f"Error getting recent memories for {app_id}/{project_id}/{ticket_id}: {e}")
        return []


async def session_resume(
    request: SessionResumeRequest,
    config: AppConfig
) -> SessionResumeResponse:
    """
    "I'm new, catch me up"

    Returns complete session context for an incoming agent.
    Creates empty session if none exists.
    """
    try:
        logger.info(f"session_resume for {request.app_id}/{request.project_id}")

        # Get existing session or create new
        state = await _get_session_state(request.app_id, request.project_id, config)
        is_new_session = state is None

        if is_new_session:
            # Create new empty session
            now = datetime.utcnow().isoformat() + "Z"
            state = SessionState(
                created_at=now,
                updated_at=now
            )
            await _save_session_state(request.app_id, request.project_id, state, config)
            logger.info(f"Created new session for {request.app_id}/{request.project_id}")

        # Get handoffs from ALL tickets in project (not just active_ticket)
        handoffs = await _get_latest_handoffs(
            request.app_id,
            request.project_id,
            config,
            limit=request.handoff_limit
        )

        # Get recent memories if active_ticket is set
        recent_memories = []
        if state.active_ticket:
            recent_memories = await _get_recent_ticket_memories(
                request.app_id,
                request.project_id,
                state.active_ticket,
                config
            )

        return SessionResumeResponse(
            session_state=state,
            handoffs=handoffs,
            recent_memories=recent_memories,
            is_new_session=is_new_session
        )

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"session_resume failed: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to resume session: {str(e)}")


async def session_handoff(
    request: SessionHandoffRequest,
    config: AppConfig
) -> SessionHandoffResponse:
    """
    "I'm done, context is clearing"

    Records handoff and updates session state atomically.
    """
    try:
        logger.info(f"session_handoff for {request.app_id}/{request.project_id}")

        # Get or create session state
        state = await _get_session_state(request.app_id, request.project_id, config)
        if state is None:
            now = datetime.utcnow().isoformat() + "Z"
            state = SessionState(created_at=now, updated_at=now)

        # Determine target ticket for handoff
        target_ticket = state.active_ticket or "_project"

        # Store handoff memory
        handoff_time = datetime.utcnow().isoformat() + "Z"
        handoff_metadata = {
            "app_id": request.app_id,
            "project_id": request.project_id,
            "ticket_id": target_ticket,
            "type": HANDOFF_TYPE,
            "timestamp_iso": handoff_time,
        }

        handoff_item = MemoryItemIn(
            content=request.summary,
            metadata=handoff_metadata,
            chunking=False  # Store handoff as single unit
        )
        await add_memory(handoff_item, config)
        logger.info(f"Stored handoff for {request.app_id}/{request.project_id}/{target_ticket}")

        # Apply session_updates if provided
        if request.session_updates:
            for key, value in request.session_updates.items():
                if key in ALLOWED_SESSION_FIELDS:
                    setattr(state, key, value)
                else:
                    logger.warning(f"Ignoring invalid session update field: {key}")

        # Update timestamps
        state.last_handoff_at = handoff_time
        state.updated_at = handoff_time

        # Save updated session state
        await _save_session_state(request.app_id, request.project_id, state, config)

        return SessionHandoffResponse(
            message=f"Handoff recorded for ticket '{target_ticket}'",
            session_state=state,
            handoff_stored_at=handoff_time
        )

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"session_handoff failed: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to record handoff: {str(e)}")


async def session_update(
    request: SessionUpdateRequest,
    config: AppConfig
) -> SessionUpdateResponse:
    """
    "Quick checkpoint"

    Partial update to session state.
    """
    try:
        logger.info(f"session_update for {request.app_id}/{request.project_id}")

        # Validate update fields
        invalid_fields = set(request.updates.keys()) - ALLOWED_SESSION_FIELDS
        if invalid_fields:
            raise ValidationError(
                status_code=400,
                detail=f"Invalid session update fields: {invalid_fields}. Allowed: {ALLOWED_SESSION_FIELDS}"
            )

        # Get or create session state
        state = await _get_session_state(request.app_id, request.project_id, config)
        if state is None:
            now = datetime.utcnow().isoformat() + "Z"
            state = SessionState(created_at=now, updated_at=now)

        # Track ticket history when active_ticket changes
        now = datetime.utcnow().isoformat() + "Z"
        if "active_ticket" in request.updates:
            new_ticket = request.updates["active_ticket"]
            # Record timestamp for the new active ticket
            if new_ticket:
                state.ticket_history[new_ticket] = now

        # Apply updates
        for key, value in request.updates.items():
            if key == "last_commits":
                # Cap at 5 most recent commits
                if isinstance(value, list):
                    value = value[:5]
            setattr(state, key, value)

        # Update timestamp
        state.updated_at = now

        # Save updated state
        await _save_session_state(request.app_id, request.project_id, state, config)

        return SessionUpdateResponse(
            message="Session updated successfully",
            session_state=state
        )

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"session_update failed: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to update session: {str(e)}")
