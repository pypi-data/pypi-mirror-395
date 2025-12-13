# memory/hierarchy.py - get_hierarchy_overview handler

import logging
from datetime import datetime
from typing import List, Dict, Any, Set

from qdrant_client.http import models

from ...config import QDRANT_COLLECTION_NAME
from ...models import (
    HierarchyOverviewRequest, HierarchyOverviewResponse,
    ProjectSummary, TicketSummary, RunSummary, RetrievedChunk
)
from ...services import AppConfig
from ...utils.validation import validate_hierarchy, HierarchyValidationError

from .utils import (
    ValidationError,
    determine_time_bounds,
    parse_iso8601_to_utc,
    chunk_matches_filters,
    filter_superseded_chunks,
)

logger = logging.getLogger(__name__)


async def get_hierarchy_overview(request: HierarchyOverviewRequest, config: AppConfig):
    """
    Returns a hierarchical overview for a given scope, including child IDs and optional counts.
    - app_id only: returns projects with ticket/run counts
    - app_id + project_id: returns tickets under the project (with run counts)
    - app_id + project_id + ticket_id: returns runs under the ticket
    """
    try:
        if not request.app_id:
            raise ValidationError(status_code=400, detail="app_id is required")

        try:
            validate_hierarchy(
                app_id=request.app_id,
                project_id=request.project_id,
                ticket_id=request.ticket_id
            )
        except HierarchyValidationError as e:
            raise ValidationError(status_code=e.status_code, detail=e.detail)

        # Time window (unbounded unless explicitly provided)
        if request.start_time_iso or request.end_time_iso:
            start_time, end_time = determine_time_bounds(
                hours=None,
                start_time_iso=request.start_time_iso,
                end_time_iso=request.end_time_iso
            )
        else:
            start_time, end_time = datetime.min, datetime.utcnow()

        # Build basic filter
        filter_conditions = [
            models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id))
        ]
        if request.project_id:
            filter_conditions.append(
                models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id))
            )
        if request.ticket_id:
            filter_conditions.append(
                models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id))
            )

        qdrant_filter = models.Filter(must=filter_conditions)

        # Scroll through all matching points
        all_points = []
        offset = None
        batch_size = 100

        while True:
            result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                scroll_filter=qdrant_filter,
                limit=batch_size,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )

            points, next_offset = result

            for point in points:
                ts = point.payload.get("timestamp_iso")
                if not ts:
                    continue
                try:
                    ts_dt = parse_iso8601_to_utc(ts)
                except ValidationError:
                    continue
                if start_time <= ts_dt <= end_time:
                    all_points.append(point)

            if next_offset is None or len(points) < batch_size:
                break

            offset = next_offset

        # Convert to RetrievedChunk for consistent filtering
        retrieved_chunks: List[RetrievedChunk] = []
        for point in all_points:
            metadata = {k: v for k, v in point.payload.items() if k != "text_chunk"}
            retrieved_chunks.append(RetrievedChunk(
                chunk_id=str(point.id),
                text_chunk=point.payload.get("text_chunk", ""),
                metadata=metadata,
                score=1.0
            ))

        # Apply filters
        if request.memory_types or request.tags:
            retrieved_chunks = [
                chunk for chunk in retrieved_chunks
                if chunk_matches_filters(chunk.metadata, request.memory_types, request.tags)
            ]

        if request.hide_superseded:
            retrieved_chunks = filter_superseded_chunks(retrieved_chunks)

        track_counts = request.include_counts

        projects: Dict[str, Dict[str, Any]] = {}
        all_memory_hashes: Set[str] = set()

        for chunk in retrieved_chunks:
            metadata = chunk.metadata
            memory_hash = str(metadata.get("original_content_hash", chunk.chunk_id))
            project_id = metadata.get("project_id")
            ticket_id = metadata.get("ticket_id")
            run_id = metadata.get("run_id")

            if track_counts:
                all_memory_hashes.add(memory_hash)

            # For overview we only care about entries that live at project level or below
            if not project_id:
                continue

            project_entry = projects.setdefault(project_id, {
                "tickets": {},
                "memory_hashes": set()
            })

            if track_counts:
                project_entry["memory_hashes"].add(memory_hash)

            if ticket_id:
                ticket_entry = project_entry["tickets"].setdefault(ticket_id, {
                    "runs": {},
                    "memory_hashes": set(),
                    "run_ids": set()
                })
                if track_counts:
                    ticket_entry["memory_hashes"].add(memory_hash)
                if run_id:
                    run_entry = ticket_entry["runs"].setdefault(run_id, {"memory_hashes": set()})
                    ticket_entry["run_ids"].add(run_id)
                    if track_counts:
                        run_entry["memory_hashes"].add(memory_hash)

        project_summaries: List[ProjectSummary] = []
        for project_id, project_data in sorted(projects.items()):
            ticket_summaries: List[TicketSummary] = []
            for ticket_id, ticket_data in sorted(project_data["tickets"].items()):
                run_summaries: List[RunSummary] = []
                for run_id, run_data in sorted(ticket_data["runs"].items()):
                    run_summaries.append(RunSummary(
                        run_id=run_id,
                        memory_count=len(run_data["memory_hashes"]) if track_counts else 0
                    ))

                ticket_summaries.append(TicketSummary(
                    ticket_id=ticket_id,
                    run_count=len(ticket_data["run_ids"]),
                    memory_count=len(ticket_data["memory_hashes"]) if track_counts else 0,
                    runs=run_summaries
                ))

            project_summaries.append(ProjectSummary(
                project_id=project_id,
                ticket_count=len(ticket_summaries),
                run_count=sum(t.run_count for t in ticket_summaries),
                memory_count=len(project_data["memory_hashes"]) if track_counts else 0,
                tickets=ticket_summaries
            ))

        tickets_scope: List[TicketSummary] = []
        runs_scope: List[RunSummary] = []

        if request.project_id:
            target_project = next((p for p in project_summaries if p.project_id == request.project_id), None)
            if target_project:
                tickets_scope = target_project.tickets
                if request.ticket_id:
                    target_ticket = next((t for t in tickets_scope if t.ticket_id == request.ticket_id), None)
                    if target_ticket:
                        runs_scope = target_ticket.runs

        total_projects = len(project_summaries)
        total_tickets = sum(p.ticket_count for p in project_summaries)
        total_runs = sum(p.run_count for p in project_summaries)
        total_memories = len(all_memory_hashes) if track_counts else 0

        filters_applied = {}
        if request.memory_types:
            filters_applied["memory_types"] = request.memory_types
        if request.tags:
            filters_applied["tags"] = request.tags
        if request.hide_superseded:
            filters_applied["hide_superseded"] = True
        if request.start_time_iso or request.end_time_iso:
            filters_applied["start_time_iso"] = request.start_time_iso
            filters_applied["end_time_iso"] = request.end_time_iso or "now"

        return HierarchyOverviewResponse(
            app_id=request.app_id,
            project_id=request.project_id,
            ticket_id=request.ticket_id,
            total_projects=total_projects,
            total_tickets=total_tickets,
            total_runs=total_runs,
            total_memories=total_memories,
            projects=project_summaries,
            tickets=tickets_scope,
            runs=runs_scope,
            filters_applied=filters_applied
        )

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f" Unexpected error in get_hierarchy_overview: {e}")
        raise ValidationError(
            status_code=500,
            detail=f"Internal server error during hierarchy overview: {str(e)}"
        )
