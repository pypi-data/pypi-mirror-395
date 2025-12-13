# handlers/health_handlers.py - Health check endpoint handler

from ..config import QDRANT_COLLECTION_NAME
from ..services import AppConfig
import httpx

async def health_check(config: AppConfig):
    """Health check endpoint."""
    qdrant_status = {}
    lm_studio_status = {}
    overall_status = "healthy"

    # 1. Check Qdrant Connection
    try:
        if not config.qdrant_client:
            raise ValueError("Qdrant client not initialized")
            
        collection_info = config.qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
        indexed_fields = list(collection_info.payload_schema.keys()) if hasattr(collection_info, 'payload_schema') and collection_info.payload_schema else []
        
        qdrant_status = {
            "status": "healthy",
            "collection": QDRANT_COLLECTION_NAME,
            "points_count": collection_info.points_count if hasattr(collection_info, 'points_count') else "unknown",
            "indexed_fields": indexed_fields,
        }
    except Exception as e:
        overall_status = "degraded"
        qdrant_status = {"status": "error", "error": str(e)}

    # 2. Check LM Studio Connection
    try:
        if not config.http_client:
            raise ValueError("HTTP client not initialized")
        
        # Use the base URL for a simple health check
        response = await config.http_client.get(config.lm_studio_url)
        response.raise_for_status()
        
        lm_studio_status = {"status": "healthy", "url": config.lm_studio_url}
        
    except httpx.RequestError as e:
        overall_status = "degraded"
        lm_studio_status = {"status": "error", "url": config.lm_studio_url, "error": f"Request failed: {e}"}
    except Exception as e:
        overall_status = "degraded"
        lm_studio_status = {"status": "error", "url": config.lm_studio_url, "error": str(e)}

    return {
        "status": overall_status,
        "dependencies": {
            "qdrant": qdrant_status,
            "lm_studio": lm_studio_status
        }
    } 