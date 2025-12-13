# memory/export.py - export_memories handler

import logging
from typing import List
from collections import defaultdict

from qdrant_client.http import models

from ...config import QDRANT_COLLECTION_NAME
from ...models import (
    ExportMemoriesRequest, ExportMemoriesResponse, ExportedMemory, RetrievedChunk
)
from ...services import AppConfig
from ...utils.validation import validate_hierarchy, HierarchyValidationError

from .utils import (
    ValidationError,
    safe_int_conversion,
    determine_time_bounds,
    parse_iso8601_to_utc,
    chunk_matches_filters,
    filter_superseded_chunks,
)

logger = logging.getLogger(__name__)


async def export_memories(request: ExportMemoriesRequest, config: AppConfig):
    """
    Exports memories as reconstructed JSON blobs for the requested scope.
    """
    try:
        if not request.app_id:
            raise ValidationError(status_code=400, detail="app_id is required")

        try:
            validate_hierarchy(
                app_id=request.app_id,
                project_id=request.project_id,
                ticket_id=request.ticket_id,
                run_id=request.run_id
            )
        except HierarchyValidationError as e:
            raise ValidationError(status_code=e.status_code, detail=e.detail)

        start_time, end_time = determine_time_bounds(
            hours=None,
            start_time_iso=request.start_time_iso,
            end_time_iso=request.end_time_iso
        )

        filter_desc = f"app_id: {request.app_id}"
        should_conditions = []

        if not request.cascade:
            if request.run_id:
                filter_desc += f", project_id: {request.project_id}, ticket_id: {request.ticket_id}, run_id: {request.run_id} (exact match)"
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
                filter_desc += f", project_id: {request.project_id}, ticket_id: {request.ticket_id} (ticket + runs)"
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id))
                    ])
                )
            elif request.project_id:
                filter_desc += f", project_id: {request.project_id} (project only)"
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ])
                )
            else:
                filter_desc += " (app-level only)"
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )
        else:
            if request.run_id:
                filter_desc += f", project_id: {request.project_id}, ticket_id: {request.ticket_id}, run_id: {request.run_id} (cascade)"
                should_conditions.extend([
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ]),
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ]),
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="run_id"))
                    ]),
                    # Must explicitly exclude documents with empty/missing run_id
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
                ])
            elif request.ticket_id:
                filter_desc += f", project_id: {request.project_id}, ticket_id: {request.ticket_id} (cascade)"
                should_conditions.extend([
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ]),
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ]),
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id))
                    ])
                ])
            elif request.project_id:
                filter_desc += f", project_id: {request.project_id} (cascade)"
                should_conditions.extend([
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ]),
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="ticket_id"))
                    ])
                ])
            else:
                filter_desc += " (app-level)"
                should_conditions.append(
                    models.Filter(must=[
                        models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id)),
                        models.IsEmptyCondition(is_empty=models.PayloadField(key="project_id"))
                    ])
                )

        qdrant_filter = should_conditions[0] if (not request.cascade and len(should_conditions) == 1) else models.Filter(should=should_conditions)

        try:
            all_points = []
            offset = None
            batch_size = 200

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

            logger.info(f"Exporting {len(all_points)} chunks for {filter_desc}")
        except Exception as e:
            logger.error(f" Qdrant scroll failed during export: {e}")
            raise ValidationError(status_code=500, detail=f"Qdrant retrieval failed: {str(e)}")

        retrieved_chunks: List[RetrievedChunk] = []
        for point in all_points:
            chunk_content = point.payload.get("text_chunk", "")
            metadata_from_payload = {k: v for k, v in point.payload.items() if k != "text_chunk"}
            retrieved_chunks.append(RetrievedChunk(
                chunk_id=str(point.id),
                text_chunk=chunk_content,
                metadata=metadata_from_payload,
                score=1.0
            ))

        if request.memory_types or request.tags:
            retrieved_chunks = [
                chunk for chunk in retrieved_chunks
                if chunk_matches_filters(chunk.metadata, request.memory_types, request.tags)
            ]

        # Version deduplication to keep highest version of each logical memory
        memory_groups = defaultdict(list)
        for chunk in retrieved_chunks:
            app_id = chunk.metadata.get('app_id', '')
            project_id = chunk.metadata.get('project_id', '') or 'none'
            ticket_id = chunk.metadata.get('ticket_id', '') or 'none'
            run_id = chunk.metadata.get('run_id', '') or 'none'
            memory_type = chunk.metadata.get('type', '') or 'none'

            memory_key = f"{app_id}|{project_id}|{ticket_id}|{run_id}|{memory_type}"
            memory_groups[memory_key].append(chunk)

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

        # Reconstruct full memories grouped by original_content_hash
        memory_chunks = defaultdict(list)
        for chunk in version_filtered_chunks:
            content_hash = chunk.metadata.get("original_content_hash", chunk.chunk_id)
            memory_chunks[content_hash].append(chunk)

        exported_memories: List[ExportedMemory] = []
        total_chunks = 0

        for content_hash, chunks_in_memory in memory_chunks.items():
            chunks_in_memory.sort(key=lambda c: c.metadata.get("chunk_index", 0))
            total_chunks += len(chunks_in_memory)
            content = "".join(c.text_chunk for c in chunks_in_memory)
            base_metadata = {
                k: v for k, v in chunks_in_memory[0].metadata.items()
                if k not in ["text_chunk", "chunk_index", "total_chunks", "keywords"]
            }
            exported_memories.append(ExportedMemory(
                original_content_hash=str(content_hash),
                metadata=base_metadata,
                content=content,
                chunk_count=len(chunks_in_memory)
            ))

        return ExportMemoriesResponse(
            app_id=request.app_id,
            project_id=request.project_id,
            ticket_id=request.ticket_id,
            run_id=request.run_id,
            total_memories=len(exported_memories),
            total_chunks=total_chunks,
            memories=exported_memories
        )

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f" Unexpected error in export_memories: {e}")
        raise ValidationError(
            status_code=500,
            detail=f"Internal server error during export: {str(e)}"
        )
