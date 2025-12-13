# handlers/list_handlers.py - ID listing endpoint handlers

# Removed FastAPI dependencies for stdio-only MCP server

# Simple exception class to replace FastAPI ValidationError
class ValidationError(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

import logging
from qdrant_client.http import models

logger = logging.getLogger(__name__)
from collections import defaultdict
from ..config import QDRANT_COLLECTION_NAME, SCROLL_BATCH_SIZE
from ..models import ListIdsResponse, ListMemoryTypesRequest, ListMemoryTypesResponse, MemoryTypeInfo
from ..services import AppConfig

async def list_app_ids(config: AppConfig):
    """
    Lists all unique app_ids found in the Memory Hub.
    """
    try:
        logger.info("Listing all app_ids in Memory Hub")
        
        # Use scroll to get all points (Qdrant doesn't have DISTINCT queries)
        all_app_ids = set()
        points_scanned = 0
        offset = None
        
        while True:
            scroll_result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                limit=SCROLL_BATCH_SIZE,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            if not scroll_result[0]:  # No more points
                break
                
            for point in scroll_result[0]:
                points_scanned += 1
                app_id = point.payload.get('app_id')
                if app_id:
                    all_app_ids.add(str(app_id))
            
            offset = scroll_result[1]  # Next offset for pagination
            if offset is None:  # No more pages
                break
        
        unique_app_ids = sorted(list(all_app_ids))
        logger.info(f"Found {len(unique_app_ids)} unique app_ids from {points_scanned} points")
        
        return ListIdsResponse(
            ids=unique_app_ids,
            total_count=len(unique_app_ids),
            points_scanned=points_scanned
        )
        
    except Exception as e:
        logger.error(f"Failed to list app_ids: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to list app_ids: {str(e)}")

async def list_project_ids(config: AppConfig):
    """
    Lists all unique project_ids found in the Memory Hub.
    """
    try:
        logger.info("Listing all project_ids in Memory Hub")
        
        all_project_ids = set()
        points_scanned = 0
        offset = None
        
        while True:
            scroll_result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                limit=SCROLL_BATCH_SIZE,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            if not scroll_result[0]:
                break
                
            for point in scroll_result[0]:
                points_scanned += 1
                project_id = point.payload.get('project_id')
                if project_id:  # Only include non-null project_ids
                    all_project_ids.add(str(project_id))
            
            offset = scroll_result[1]
            if offset is None:
                break
        
        unique_project_ids = sorted(list(all_project_ids))
        logger.info(f"Found {len(unique_project_ids)} unique project_ids from {points_scanned} points")
        
        return ListIdsResponse(
            ids=unique_project_ids,
            total_count=len(unique_project_ids),
            points_scanned=points_scanned
        )
        
    except Exception as e:
        logger.error(f"Failed to list project_ids: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to list project_ids: {str(e)}")

async def list_ticket_ids(config: AppConfig):
    """
    Lists all unique ticket_ids found in the Memory Hub.
    """
    try:
        logger.info("Listing all ticket_ids in Memory Hub")
        
        all_ticket_ids = set()
        points_scanned = 0
        offset = None
        
        while True:
            scroll_result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                limit=SCROLL_BATCH_SIZE,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            if not scroll_result[0]:
                break
                
            for point in scroll_result[0]:
                points_scanned += 1
                ticket_id = point.payload.get('ticket_id')
                if ticket_id:  # Only include non-null ticket_ids
                    all_ticket_ids.add(str(ticket_id))
            
            offset = scroll_result[1]
            if offset is None:
                break
        
        unique_ticket_ids = sorted(list(all_ticket_ids))
        logger.info(f"Found {len(unique_ticket_ids)} unique ticket_ids from {points_scanned} points")
        
        return ListIdsResponse(
            ids=unique_ticket_ids,
            total_count=len(unique_ticket_ids),
            points_scanned=points_scanned
        )
        
    except Exception as e:
        logger.error(f"Failed to list ticket_ids: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to list ticket_ids: {str(e)}")

async def list_memory_types(request: ListMemoryTypesRequest, config: AppConfig):
    """
    Lists all unique memory types found in the Memory Hub, with metadata about each type.
    Can be filtered by app_id and/or project_id.
    """
    try:
        # Build filter if app_id or project_id specified
        filter_conditions = []
        filter_desc = "all memories"
        
        if request.app_id:
            filter_conditions.append(
                models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id))
            )
            filter_desc = f"app_id={request.app_id}"
            
        if request.project_id:
            filter_conditions.append(
                models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id))
            )
            if request.app_id:
                filter_desc += f", project_id={request.project_id}"
            else:
                filter_desc = f"project_id={request.project_id}"
        
        qdrant_filter = models.Filter(must=filter_conditions) if filter_conditions else None
        
        logger.info(f"Listing memory types for {filter_desc}")
        
        # Collect type information
        type_info = defaultdict(lambda: {
            "count": 0,
            "latest_version": 0,
            "last_updated": ""
        })
        
        points_scanned = 0
        offset = None
        
        while True:
            scroll_result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                scroll_filter=qdrant_filter,
                limit=SCROLL_BATCH_SIZE,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            if not scroll_result[0]:  # No more points
                break
                
            for point in scroll_result[0]:
                points_scanned += 1
                memory_type = point.payload.get('type', 'untyped')
                version = int(point.payload.get('version', 1))
                timestamp = point.payload.get('timestamp_iso', '')
                
                # Update type info
                type_info[memory_type]["count"] += 1
                type_info[memory_type]["latest_version"] = max(
                    type_info[memory_type]["latest_version"], 
                    version
                )
                
                # Update last_updated if this timestamp is more recent
                if timestamp > type_info[memory_type]["last_updated"]:
                    type_info[memory_type]["last_updated"] = timestamp
            
            offset = scroll_result[1]
            if offset is None:
                break
        
        # Convert to response format
        memory_types = []
        for type_name, info in sorted(type_info.items()):
            memory_types.append(MemoryTypeInfo(
                type_name=type_name,
                count=info["count"],
                latest_version=info["latest_version"],
                last_updated=info["last_updated"]
            ))
        
        logger.info(f"Found {len(memory_types)} unique memory types from {points_scanned} points")
        
        return ListMemoryTypesResponse(
            memory_types=memory_types,
            total_types=len(memory_types),
            points_scanned=points_scanned
        )
        
    except Exception as e:
        logger.error(f"Failed to list memory types: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to list memory types: {str(e)}")

async def get_memory_type_guide(config: AppConfig):
    """
    Returns a static guide of recommended memory types for agents to use.
    This helps maintain consistency across different agents and projects.
    """
    from ..models import GetMemoryTypeGuideResponse
    
    return GetMemoryTypeGuideResponse(
        create_new_types=[
            "initialization",
            "code_change", 
            "decision",
            "progress_update",
            "bug_fix",
            "research_finding",
            "test_result",
            "error_log",
            "feature_implementation",
            "refactoring",
            "dependency_change",
            "api_change"
        ],
        update_types=[
            "project_status",
            "todo_list",
            "configuration",
            "team_notes",
            "architecture_overview",
            "api_documentation",
            "deployment_config"
        ],
        guidelines="""Memory Type Guidelines:
        
1. CREATE types (historical records):
   - Use for events that happen over time
   - Each entry preserves history
   - Examples: code_change, bug_fix, decision
   
2. UPDATE types (living documents):
   - Use for current state information
   - Single source of truth that evolves
   - Examples: project_status, todo_list, configuration

3. Naming conventions:
   - Use lowercase with underscores
   - Be specific and descriptive
   - Use singular for UPDATE types (e.g., 'project_status')
   - Use singular for CREATE types too (e.g., 'code_change' not 'code_changes')

4. Custom types:
   - You can create custom types for your specific needs
   - Follow the same CREATE vs UPDATE pattern
   - Document custom types in team_notes"""
    ) 