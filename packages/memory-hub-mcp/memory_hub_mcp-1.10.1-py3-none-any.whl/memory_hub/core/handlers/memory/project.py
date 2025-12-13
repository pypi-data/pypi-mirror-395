# memory/project.py - get_project_memories handler

import logging
from typing import List
from collections import defaultdict

from qdrant_client.http import models

from ...config import (
    QDRANT_COLLECTION_NAME, ENABLE_GEMMA_SUMMARIZATION, MAX_SUMMARIZATION_CHUNKS
)
from ...models import (
    GetProjectMemoriesRequest, RetrievedChunk, SearchResponse
)
from ...services import synthesize_search_results, AppConfig
from ...utils.validation import validate_hierarchy, HierarchyValidationError

from .utils import (
    ValidationError,
    safe_int_conversion,
    limit_by_memory_count,
    chunk_matches_filters,
    filter_superseded_chunks,
)

logger = logging.getLogger(__name__)


async def get_project_memories(request: GetProjectMemoriesRequest, config: AppConfig):
    """
    Retrieves memories for a specific app_id/project_id/ticket_id/run_id scope.

    Uses children_depth to control how many levels of children to include:
    - children_depth=0: Only memories at the exact level specified (default)
    - children_depth=1: This level + immediate children
    - children_depth=2: This level + 2 levels down
    - children_depth=-1: All children (unlimited depth)

    Hierarchy: app_id → project_id → ticket_id → run_id

    Examples at project_id level:
    - depth=0: project-level memories only
    - depth=1: project + ticket-level memories (no runs)
    - depth=2 or -1: project + tickets + runs (all children)
    """
    try:
        # Validate input
        if not request.app_id:
            raise ValidationError(
                status_code=400,
                detail="app_id is required"
            )

        # Validate hierarchical structure
        try:
            validate_hierarchy(
                app_id=request.app_id,
                project_id=request.project_id,
                ticket_id=request.ticket_id,
                run_id=request.run_id
            )
        except HierarchyValidationError as e:
            raise ValidationError(status_code=e.status_code, detail=e.detail)

        # Get children_depth (default 0 = exact level only)
        children_depth = getattr(request, 'children_depth', 0)

        # Build filter based on hierarchy level and children_depth
        filter_desc = f"app_id: {request.app_id}"
        should_conditions = []

        # Helper to determine max children levels from current position
        # Hierarchy levels: app(0) -> project(1) -> ticket(2) -> run(3)
        if request.run_id:
            current_level = 3  # run level - no children possible
            max_children = 0
        elif request.ticket_id:
            current_level = 2  # ticket level - can have runs (1 level of children)
            max_children = 1
        elif request.project_id:
            current_level = 1  # project level - can have tickets, runs (2 levels)
            max_children = 2
        else:
            current_level = 0  # app level - can have projects, tickets, runs (3 levels)
            max_children = 3

        # Normalize children_depth: -1 means all, otherwise cap at max_children
        effective_depth = max_children if children_depth == -1 else min(children_depth, max_children)

        filter_desc += f" (children_depth={children_depth}, effective={effective_depth})"
        if request.project_id:
            filter_desc += f", project_id: {request.project_id}"
        if request.ticket_id:
            filter_desc += f", ticket_id: {request.ticket_id}"
        if request.run_id:
            filter_desc += f", run_id: {request.run_id}"

        # Build filter conditions based on current level and effective depth
        if request.run_id:
            # Run level - exact match only (no children possible)
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
            # Ticket level
            if effective_depth == 0:
                # Only ticket-level memories (run_id is empty)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="run_id"))
                    ])
                )
            else:
                # Ticket + all runs (depth >= 1)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id))
                    ])
                )

        elif request.project_id:
            # Project level
            if effective_depth == 0:
                # Only project-level memories (ticket_id is empty)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ])
                )
            elif effective_depth == 1:
                # Project + tickets (but not runs)
                # This requires OR: (ticket_id empty) OR (ticket_id exists AND run_id empty)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ])
                )
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
                # Project + all children (depth >= 2)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id))
                    ])
                )

        else:
            # App level
            if effective_depth == 0:
                # Only app-level memories (project_id is empty)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )
            elif effective_depth == 1:
                # App + projects (but not tickets/runs)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ], must_not=[
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )
            elif effective_depth == 2:
                # App + projects + tickets (but not runs)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="run_id"))
                    ])
                )
            else:
                # App + all children (depth >= 3 or -1)
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id))
                    ])
                )

        logger.info(f"Retrieving memories for {filter_desc}")

        # If single condition, unwrap to avoid unnecessary nesting
        if len(should_conditions) == 1:
            qdrant_filter = should_conditions[0]
            logger.debug(f"Using unwrapped filter (single condition)")
        else:
            qdrant_filter = models.Filter(should=should_conditions)
            logger.debug(f"Using wrapped filter with {len(should_conditions)} should conditions")

        logger.debug(f"Qdrant filter structure: {qdrant_filter}")

        try:
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
                all_points.extend(points)

                if next_offset is None or len(points) < batch_size:
                    break

                offset = next_offset

            logger.info(f"Found {len(all_points)} total memory chunks for {filter_desc}")

        except Exception as e:
            logger.error(f" Qdrant scroll failed: {e}")
            raise ValidationError(status_code=500, detail=f"Qdrant retrieval failed: {str(e)}")

        # Convert to RetrievedChunk format
        retrieved_chunks: List[RetrievedChunk] = []
        for point in all_points:
            chunk_content = point.payload.get("text_chunk", "")
            metadata_from_payload = {k: v for k, v in point.payload.items() if k != "text_chunk"}

            # Log the run_id from Qdrant to verify filtering
            logger.debug(f"Point from Qdrant: run_id={metadata_from_payload.get('run_id', 'NONE')}, type={metadata_from_payload.get('type', 'NONE')}")

            retrieved_chunks.append(RetrievedChunk(
                chunk_id=str(point.id),
                text_chunk=chunk_content,
                metadata=metadata_from_payload,
                score=1.0  # No similarity score needed for direct retrieval
            ))

        # Apply optional type/tag filters before deduplication
        if request.memory_types or request.tags:
            filtered_chunks = [
                chunk for chunk in retrieved_chunks
                if chunk_matches_filters(chunk.metadata, request.memory_types, request.tags)
            ]
            logger.info(f" Type/tag filters reduced project memories from {len(retrieved_chunks)} to {len(filtered_chunks)}")
            retrieved_chunks = filtered_chunks

        # Version-aware deduplication - prefer highest version within each logical memory group
        memory_groups = defaultdict(list)
        for chunk in retrieved_chunks:
            # Create a key that uniquely identifies a logical memory
            app_id = chunk.metadata.get('app_id', '')
            project_id = chunk.metadata.get('project_id', '') or 'none'
            ticket_id = chunk.metadata.get('ticket_id', '') or 'none'
            run_id = chunk.metadata.get('run_id', '') or 'none'
            memory_type = chunk.metadata.get('type', '') or 'none'

            memory_key = f"{app_id}|{project_id}|{ticket_id}|{run_id}|{memory_type}"
            memory_groups[memory_key].append(chunk)

        # Within each group, prefer chunks from the highest version
        version_filtered_chunks = []
        for memory_key, chunks_in_group in memory_groups.items():
            if len(chunks_in_group) == 1:
                version_filtered_chunks.extend(chunks_in_group)
            else:
                # Find the highest version in this group
                max_version = max(safe_int_conversion(chunk.metadata.get('version', 1)) for chunk in chunks_in_group)
                highest_version_chunks = [chunk for chunk in chunks_in_group
                                          if safe_int_conversion(chunk.metadata.get('version', 1)) == max_version]
                version_filtered_chunks.extend(highest_version_chunks)

                logger.info(f" Version deduplication for {memory_key}: {len(chunks_in_group)} chunks reduced to {len(highest_version_chunks)} (version {max_version})")

        if request.hide_superseded:
            version_filtered_chunks = filter_superseded_chunks(version_filtered_chunks)

        # Apply limit by memory count (not chunk count)
        retrieved_chunks = limit_by_memory_count(
            version_filtered_chunks,
            request.limit,
            sort_by_timestamp=(request.sort_by == "timestamp")
        )

        # Generate summary based on return_format
        synthesized_summary = None
        if request.return_format in ["summary_only", "both"] and ENABLE_GEMMA_SUMMARIZATION and retrieved_chunks:
            try:
                # Create a context-aware prompt for summarization
                context_prompt = f"Summarize all memories for {filter_desc}"
                summary = await synthesize_search_results(
                    context_prompt,
                    retrieved_chunks[:MAX_SUMMARIZATION_CHUNKS],
                    config.http_client,
                    config
                )
                if summary:
                    logger.info(f" LM Studio summary generated successfully for project memories (return_format={request.return_format}).")
                    synthesized_summary = summary
            except Exception as e:
                logger.warning(f" Project memories summarization failed: {e}. Returning raw chunks.")

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

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f" Unexpected error in get_project_memories: {e}")
        raise ValidationError(
            status_code=500,
            detail=f"Internal server error during retrieval: {str(e)}"
        )
