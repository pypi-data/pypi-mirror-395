# memory/recent.py - get_recent_memories handler

import logging
from typing import List
from collections import defaultdict

from qdrant_client.http import models

from ...config import (
    QDRANT_COLLECTION_NAME, ENABLE_GEMMA_SUMMARIZATION, MAX_SUMMARIZATION_CHUNKS
)
from ...models import GetRecentMemoriesRequest, RetrievedChunk, SearchResponse
from ...services import synthesize_search_results, AppConfig
from ...utils.validation import validate_hierarchy, HierarchyValidationError

from .utils import (
    ValidationError,
    safe_int_conversion,
    determine_time_bounds,
    parse_iso8601_to_utc,
    limit_by_memory_count,
    chunk_matches_filters,
    filter_superseded_chunks,
)

logger = logging.getLogger(__name__)


async def get_recent_memories(request: GetRecentMemoriesRequest, config: AppConfig):
    """
    Retrieves memories from the last N hours, optionally filtered by app_id/project_id/ticket_id/run_id.
    Perfect for agents resuming work after a break.

    Uses children_depth to control how many levels of children to include:
    - children_depth=0: Only memories at the exact level specified (default)
    - children_depth=1: This level + immediate children
    - children_depth=2: This level + 2 levels down
    - children_depth=-1: All children (unlimited depth)
    """
    try:
        # Validate hierarchical structure if filters provided
        if request.app_id or request.project_id or request.ticket_id or request.run_id:
            try:
                validate_hierarchy(
                    app_id=request.app_id,
                    project_id=request.project_id,
                    ticket_id=request.ticket_id,
                    run_id=request.run_id
                )
            except HierarchyValidationError as e:
                raise ValidationError(status_code=e.status_code, detail=e.detail)

        # Calculate timestamp window
        start_time, end_time = determine_time_bounds(
            hours=request.hours,
            start_time_iso=request.start_time_iso,
            end_time_iso=request.end_time_iso
        )
        logger.info(f"Retrieving recent memories between {start_time.isoformat()} and {end_time.isoformat()}")

        # Get children_depth setting
        children_depth = getattr(request, 'children_depth', 0)

        # Determine max children levels based on current position in hierarchy
        if request.run_id:
            max_children = 0  # run is leaf, no children
        elif request.ticket_id:
            max_children = 1  # can include runs
        elif request.project_id:
            max_children = 2  # can include tickets + runs
        elif request.app_id:
            max_children = 3  # can include projects + tickets + runs
        else:
            max_children = 0  # no scope specified

        # Convert -1 to max, and clamp to available depth
        effective_depth = max_children if children_depth == -1 else min(children_depth, max_children)

        # Build filter conditions based on children_depth
        should_conditions = []

        if request.run_id:
            # Run level - no children possible, just return run-level memories
            # Must explicitly exclude documents with empty/missing run_id
            should_conditions.append(
                models.Filter(
                    must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id)),
                        models.FieldCondition(key="run_id", match=models.MatchValue(value=request.run_id))
                    ],
                    must_not=[
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="run_id"))
                    ]
                )
            )
        elif request.ticket_id:
            # Ticket level - can include runs based on depth
            if effective_depth == 0:
                # Only ticket-level memories (no run_id)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="run_id"))
                    ])
                )
            else:
                # depth >= 1: ticket + all runs
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id))
                    ])
                )
        elif request.project_id:
            # Project level - can include tickets and runs based on depth
            if effective_depth == 0:
                # Only project-level memories
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ])
                )
            elif effective_depth == 1:
                # Project + tickets (no runs)
                # 1. Project-level
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ])
                )
                # 2. Ticket-level (no run_id)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="run_id"))
                    ], must_not=[
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ])
                )
            else:
                # depth >= 2: project + tickets + runs (everything in project)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id))
                    ])
                )
        elif request.app_id:
            # App level - can include projects, tickets, runs based on depth
            if effective_depth == 0:
                # Only app-level memories
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )
            elif effective_depth == 1:
                # App + projects (no tickets)
                # 1. App-level
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )
                # 2. Project-level (no ticket_id)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ], must_not=[
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )
            elif effective_depth == 2:
                # App + projects + tickets (no runs)
                # 1. App-level
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )
                # 2. Project-level (no ticket_id)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ], must_not=[
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )
                # 3. Ticket-level (no run_id)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="run_id"))
                    ], must_not=[
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ])
                )
            else:
                # depth >= 3 or -1: everything in app
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id))
                    ])
                )

        # Note: Qdrant doesn't support direct date range filtering in the same way as other DBs
        # We'll need to fetch all matching records and filter by timestamp in memory
        qdrant_filter = models.Filter(should=should_conditions) if should_conditions else None

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

            # Filter by timestamp
            for point in points:
                timestamp_iso = point.payload.get("timestamp_iso", "")
                if not timestamp_iso:
                    continue
                try:
                    timestamp_dt = parse_iso8601_to_utc(timestamp_iso)
                except ValidationError:
                    continue
                if start_time <= timestamp_dt <= end_time:
                    all_points.append(point)

            if next_offset is None or len(points) < batch_size:
                break

            offset = next_offset

        logger.info(f" Found {len(all_points)} recent memory chunks from the last {request.hours} hours")

        # Convert to RetrievedChunk format
        retrieved_chunks: List[RetrievedChunk] = []
        for point in all_points:
            chunk_content = point.payload.get("text_chunk", "")
            metadata_from_payload = {k: v for k, v in point.payload.items() if k != "text_chunk"}

            retrieved_chunks.append(RetrievedChunk(
                chunk_id=str(point.id),
                text_chunk=chunk_content,
                metadata=metadata_from_payload,
                score=1.0  # No similarity score for time-based retrieval
            ))

        # Apply optional type/tag filters before deduplication
        if request.memory_types or request.tags:
            filtered_chunks = [
                chunk for chunk in retrieved_chunks
                if chunk_matches_filters(chunk.metadata, request.memory_types, request.tags)
            ]
            logger.info(f" Type/tag filters reduced recent memories from {len(retrieved_chunks)} to {len(filtered_chunks)}")
            retrieved_chunks = filtered_chunks

        # Apply version deduplication
        memory_groups = defaultdict(list)
        for chunk in retrieved_chunks:
            app_id = chunk.metadata.get('app_id', '')
            project_id = chunk.metadata.get('project_id', '') or 'none'
            ticket_id = chunk.metadata.get('ticket_id', '') or 'none'
            run_id = chunk.metadata.get('run_id', '') or 'none'
            memory_type = chunk.metadata.get('type', '') or 'none'

            memory_key = f"{app_id}|{project_id}|{ticket_id}|{run_id}|{memory_type}"
            memory_groups[memory_key].append(chunk)

        # Keep only highest version per group
        version_filtered_chunks = []
        for memory_key, chunks_in_group in memory_groups.items():
            if len(chunks_in_group) == 1:
                version_filtered_chunks.extend(chunks_in_group)
            else:
                max_version = max(safe_int_conversion(chunk.metadata.get('version', 1)) for chunk in chunks_in_group)
                highest_version_chunks = [chunk for chunk in chunks_in_group
                                          if safe_int_conversion(chunk.metadata.get('version', 1)) == max_version]
                version_filtered_chunks.extend(highest_version_chunks)

        if request.hide_superseded:
            version_filtered_chunks = filter_superseded_chunks(version_filtered_chunks)

        # Apply limit by memory count (not chunk count)
        retrieved_chunks = limit_by_memory_count(
            version_filtered_chunks,
            request.limit,
            sort_by_timestamp=True
        )

        # Generate summary based on return_format
        synthesized_summary = None
        if request.return_format in ["summary_only", "both"] and ENABLE_GEMMA_SUMMARIZATION and retrieved_chunks:
            try:
                context_prompt = f"Summarize the recent activities and updates from the last {request.hours} hours"
                summary = await synthesize_search_results(
                    context_prompt,
                    retrieved_chunks[:MAX_SUMMARIZATION_CHUNKS],
                    config.http_client,
                    config
                )
                if summary:
                    logger.info(f" LM Studio summary generated successfully for recent memories (return_format={request.return_format}).")
                    synthesized_summary = summary
            except Exception as e:
                logger.warning(f" Recent memories summarization failed: {e}")

        # Return based on requested format
        if request.return_format == "summary_only":
            # Return only summary, empty chunks for token efficiency
            return SearchResponse(
                synthesized_summary=synthesized_summary,
                retrieved_chunks=[],
                total_results=len(retrieved_chunks)
            )
        elif request.return_format == "chunks_only":
            # Return only chunks, no summary
            return SearchResponse(
                synthesized_summary=None,
                retrieved_chunks=retrieved_chunks,
                total_results=len(retrieved_chunks)
            )
        else:  # "both" (default)
            # Return both summary and chunks
            return SearchResponse(
                synthesized_summary=synthesized_summary,
                retrieved_chunks=retrieved_chunks,
                total_results=len(retrieved_chunks)
            )

    except Exception as e:
        logger.error(f" Unexpected error in get_recent_memories: {e}")
        raise ValidationError(
            status_code=500,
            detail=f"Internal server error during retrieval: {str(e)}"
        )
