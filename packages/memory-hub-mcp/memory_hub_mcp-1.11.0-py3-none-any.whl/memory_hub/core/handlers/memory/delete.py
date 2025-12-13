# memory/delete.py - delete_run_memories handler

import logging

from qdrant_client.http import models

from ...config import QDRANT_COLLECTION_NAME
from ...models import DeleteRunMemoriesRequest
from ...services import AppConfig
from ...utils.validation import validate_hierarchy, HierarchyValidationError

from .utils import ValidationError

logger = logging.getLogger(__name__)


async def delete_run_memories(request: DeleteRunMemoriesRequest, config: AppConfig):
    """
    Deletes all memories for a specific run_id.
    Requires exact 4-level match: app_id + project_id + ticket_id + run_id.
    This is a destructive operation with no undo capability.

    Args:
        request: DeleteRunMemoriesRequest with app_id, project_id, ticket_id, run_id, and optional dry_run
        config: AppConfig with Qdrant client

    Returns:
        dict with message, deleted_count, deleted_memories, run_id

    Raises:
        ValidationError: If hierarchy is invalid or run_id not found
    """
    try:
        # Validate hierarchical structure - all 4 levels required
        try:
            validate_hierarchy(
                app_id=request.app_id,
                project_id=request.project_id,
                ticket_id=request.ticket_id,
                run_id=request.run_id
            )
        except HierarchyValidationError as e:
            raise ValidationError(status_code=e.status_code, detail=e.detail)

        # Build exact match filter for all 4 levels
        # Must explicitly exclude documents with empty/missing run_id
        qdrant_filter = models.Filter(
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

        # Scroll to find all points to delete
        all_points = []
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
            all_points.extend(points)

            if next_offset is None or len(points) < 100:
                break
            offset = next_offset

        if not all_points:
            raise ValidationError(
                status_code=404,
                detail=f"No memories found for run_id: {request.run_id}"
            )

        # Count distinct memories (by original_content_hash)
        unique_hashes = set(point.payload.get("original_content_hash") for point in all_points)

        # If dry_run, return preview without deleting
        if request.dry_run:
            logger.info(f"DRY RUN: Would delete {len(all_points)} chunks ({len(unique_hashes)} memories) for run_id: {request.run_id}")
            return {
                "message": f"DRY RUN: Would delete all memories for run_id: {request.run_id}",
                "deleted_count": len(all_points),
                "deleted_memories": len(unique_hashes),
                "run_id": request.run_id,
                "dry_run": True
            }

        # Delete all points
        point_ids = [point.id for point in all_points]
        config.qdrant_client.delete(
            collection_name=QDRANT_COLLECTION_NAME,
            points_selector=models.PointIdsList(points=point_ids)
        )

        logger.info(f"Deleted {len(point_ids)} chunks ({len(unique_hashes)} memories) for run_id: {request.run_id}")

        return {
            "message": f"Successfully deleted all memories for run_id: {request.run_id}",
            "deleted_count": len(point_ids),
            "deleted_memories": len(unique_hashes),
            "run_id": request.run_id,
            "dry_run": False
        }

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in delete_run_memories: {e}")
        raise ValidationError(
            status_code=500,
            detail=f"Deletion failed: {str(e)}"
        )
