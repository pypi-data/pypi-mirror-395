# memory/update.py - update_memory handler

import logging
from datetime import datetime
from collections import defaultdict

from qdrant_client.http import models

from ...config import QDRANT_COLLECTION_NAME
from ...models import MemoryItemIn, UpdateMemoryRequest
from ...services import AppConfig
from ...utils.validation import validate_hierarchy, HierarchyValidationError

from .utils import ValidationError, safe_int_conversion
from .add import add_memory

logger = logging.getLogger(__name__)


async def update_memory(request: UpdateMemoryRequest, config: AppConfig):
    """
    Updates an existing memory by finding it based on app_id/project_id/ticket_id/run_id/type combination,
    then replacing its content and incrementing the version.
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

        # Build filter to find the memory to update
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

        if request.run_id:
            filter_conditions.append(
                models.FieldCondition(key="run_id", match=models.MatchValue(value=request.run_id))
            )

        if request.memory_type:
            filter_conditions.append(
                models.FieldCondition(key="type", match=models.MatchValue(value=request.memory_type))
            )

        # Build filter with must_not for empty run_id when filtering by specific run_id
        if request.run_id:
            qdrant_filter = models.Filter(
                must=filter_conditions,
                must_not=[models.IsEmptyCondition(is_empty=models.PayloadField(key="run_id"))]
            )
        else:
            qdrant_filter = models.Filter(must=filter_conditions)

        # Find existing memory chunks
        existing_points = []
        offset = None

        while True:
            result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                scroll_filter=qdrant_filter,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )

            points, next_offset = result
            existing_points.extend(points)

            if next_offset is None or len(points) < 100:
                break
            offset = next_offset

        if not existing_points:
            if request.create_if_missing:
                # Create new memory with version 1 instead of raising 404
                logger.info(f"Memory not found, creating new (create_if_missing=True)")
                new_metadata = {
                    "app_id": request.app_id,
                    "version": 1,
                    "timestamp_iso": datetime.utcnow().isoformat() + "Z"
                }
                if request.project_id:
                    new_metadata["project_id"] = request.project_id
                if request.ticket_id:
                    new_metadata["ticket_id"] = request.ticket_id
                if request.run_id:
                    new_metadata["run_id"] = request.run_id
                if request.memory_type:
                    new_metadata["type"] = request.memory_type
                new_metadata.update(request.metadata_updates)

                memory_item = MemoryItemIn(
                    content=request.new_content,
                    metadata=new_metadata
                )
                add_result = await add_memory(memory_item, config)

                return {
                    "message": "Memory created (did not exist)",
                    "action": "created",
                    "previous_version": 0,
                    "new_version": 1,
                    "chunks_replaced": 0,
                    "chunks_stored": add_result.chunks_stored,
                    "original_content_hash": add_result.original_content_hash
                }
            else:
                raise ValidationError(
                    status_code=404,
                    detail="No memory found matching the specified criteria"
                )

        # Group by original_content_hash to find unique memories
        memory_groups = defaultdict(list)
        for point in existing_points:
            content_hash = point.payload.get("original_content_hash", "unknown")
            memory_groups[content_hash].append(point)

        # Find the latest version
        max_version = 0
        for points in memory_groups.values():
            for point in points:
                version = safe_int_conversion(point.payload.get("version", 1))
                max_version = max(max_version, version)

        # Prepare new version
        new_version = max_version + 1

        # Delete old chunks
        point_ids_to_delete = [point.id for point in existing_points]
        config.qdrant_client.delete(
            collection_name=QDRANT_COLLECTION_NAME,
            points_selector=models.PointIdsList(points=point_ids_to_delete)
        )

        # Create new memory with updated content
        new_metadata = {
            "app_id": request.app_id,
            "version": new_version,
            "timestamp_iso": datetime.utcnow().isoformat() + "Z"
        }

        # Add optional fields if provided
        if request.project_id:
            new_metadata["project_id"] = request.project_id
        if request.ticket_id:
            new_metadata["ticket_id"] = request.ticket_id
        if request.run_id:
            new_metadata["run_id"] = request.run_id
        if request.memory_type:
            new_metadata["type"] = request.memory_type

        # Apply any additional metadata updates
        new_metadata.update(request.metadata_updates)

        # Create new memory item and add it
        memory_item = MemoryItemIn(
            content=request.new_content,
            metadata=new_metadata
        )

        add_result = await add_memory(memory_item, config)

        return {
            "message": f"Memory updated successfully to version {new_version}",
            "action": "updated",
            "previous_version": max_version,
            "new_version": new_version,
            "chunks_replaced": len(existing_points),
            "chunks_stored": add_result.chunks_stored,
            "original_content_hash": add_result.original_content_hash
        }

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f" Unexpected error in update_memory: {e}")
        raise ValidationError(
            status_code=500,
            detail=f"Internal server error during update: {str(e)}"
        )
