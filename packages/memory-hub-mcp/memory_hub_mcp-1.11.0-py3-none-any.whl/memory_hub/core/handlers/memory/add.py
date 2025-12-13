# memory/add.py - add_memory handler

import hashlib
import uuid
import logging
from datetime import datetime

from qdrant_client.http import models

from ...config import QDRANT_COLLECTION_NAME
from ...models import MemoryItemIn, AddMemoryResponse
from ...services import get_embedding, AppConfig
from ...utils.search_utils import generate_chunk_keywords
from ...utils.validation import validate_hierarchy, HierarchyValidationError

from .utils import (
    ValidationError,
    semantic_chunker,
    safe_int_conversion,
    normalize_tags_value,
)

logger = logging.getLogger(__name__)


async def add_memory(memory_item: MemoryItemIn, config: AppConfig):
    """
    Adds memory content. Chunks content, gets embeddings, and stores in Qdrant.
    Supports flexible 4-level hierarchy: app_id (required), project_id (optional), ticket_id (optional), run_id (optional).
    run_id requires ticket_id - used for AutoStack multi-run scenarios.
    """
    try:
        # Validate that app_id is provided
        if not memory_item.metadata.get("app_id"):
            raise ValidationError(status_code=400, detail="app_id is required in metadata")

        # Validate hierarchical structure
        try:
            validate_hierarchy(
                app_id=memory_item.metadata.get("app_id"),
                project_id=memory_item.metadata.get("project_id"),
                ticket_id=memory_item.metadata.get("ticket_id"),
                run_id=memory_item.metadata.get("run_id")
            )
        except HierarchyValidationError as e:
            raise ValidationError(status_code=e.status_code, detail=e.detail)

        # Normalize metadata types to prevent future conversion issues
        normalized_metadata = dict(memory_item.metadata)

        # Ensure version is stored as integer
        if 'version' in normalized_metadata:
            normalized_metadata['version'] = safe_int_conversion(normalized_metadata['version'])
        else:
            # Default version if not provided
            normalized_metadata['version'] = 1

        # Ensure timestamp_iso is provided if not present
        if "timestamp_iso" not in normalized_metadata:
            normalized_metadata["timestamp_iso"] = datetime.utcnow().isoformat() + "Z"

        # Normalize tags to a predictable list format for filtering/searching
        if "tags" in normalized_metadata:
            normalized_metadata["tags"] = normalize_tags_value(normalized_metadata.get("tags"))

        # Normalize supersession metadata to a list for easier downstream filtering
        if "supersedes" in normalized_metadata:
            supersedes_raw = normalized_metadata.get("supersedes")
            if isinstance(supersedes_raw, (list, tuple, set)):
                normalized_metadata["supersedes"] = [str(val) for val in supersedes_raw if str(val)]
            elif supersedes_raw:
                normalized_metadata["supersedes"] = [str(supersedes_raw)]
            else:
                normalized_metadata["supersedes"] = []

        app_id = normalized_metadata.get('app_id', 'N/A')
        project_id = normalized_metadata.get('project_id', None)
        ticket_id = normalized_metadata.get('ticket_id', None)
        run_id = normalized_metadata.get('run_id', None)

        # Determine hierarchy level for logging
        if run_id:
            level = "run-level"
            context = f"app: {app_id}, project: {project_id}, ticket: {ticket_id}, run: {run_id}"
        elif ticket_id:
            level = "ticket-level"
            context = f"app: {app_id}, project: {project_id}, ticket: {ticket_id}"
        elif project_id:
            level = "project-level"
            context = f"app: {app_id}, project: {project_id}"
        else:
            level = "app-level"
            context = f"app: {app_id}"

        logger.info(f"Received /add_memory for {level} context ({context}), chunking={memory_item.chunking}")

        # Conditional chunking based on chunking parameter
        if memory_item.chunking:
            # Use semantic chunking for searchable content
            try:
                chunks = semantic_chunker(memory_item.content)  # Using actual semchunk
            except Exception as e:
                logger.error(f"Failed to chunk content for {level} context ({context}): {e}")
                raise ValidationError(status_code=500, detail=f"Content chunking failed: {str(e)}")

            if not chunks:
                logger.warning(f"No chunks generated for {level} context ({context}). Content: '{memory_item.content[:100]}'")
                # This might happen if content is very short or only whitespace
                if not memory_item.content.strip():
                    raise ValidationError(status_code=400, detail="Content is empty or only whitespace.")
                # If content is not empty but semchunk didn't chunk, store the original content as a single chunk
                chunks = [memory_item.content.strip()]
        else:
            # Store as single chunk without semantic splitting
            logger.info(f" Chunking disabled - storing as single unit for {level} context ({context})")
            if not memory_item.content.strip():
                raise ValidationError(status_code=400, detail="Content is empty or only whitespace.")
            chunks = [memory_item.content.strip()]

        points_to_upsert = []
        original_content_hash = hashlib.sha256(memory_item.content.encode()).hexdigest()

        for i, chunk_text in enumerate(chunks):
            if not chunk_text:  # Skip empty chunks
                continue
            try:
                embedding = await get_embedding(chunk_text, config.http_client, config)

                # Generate chunk-specific keywords using Gemma
                chunk_keywords = await generate_chunk_keywords(chunk_text, config)

                chunk_metadata = normalized_metadata.copy()  # Start with normalized metadata
                chunk_metadata["original_content_hash"] = original_content_hash
                chunk_metadata["chunk_index"] = i
                chunk_metadata["total_chunks"] = len(chunks)
                chunk_metadata["keywords"] = chunk_keywords  # Use chunk keywords as primary keywords
                # Add the actual chunk text to the payload for Qdrant, so we can retrieve it.
                # Qdrant payload can be any JSON-serializable dict.
                payload = {"text_chunk": chunk_text, **chunk_metadata}

                points_to_upsert.append(models.PointStruct(
                    id=str(uuid.uuid4()),  # Generate unique ID for each chunk point
                    vector=embedding,
                    payload=payload
                ))
            except Exception as e:
                logger.error(f" Failed to process chunk {i} for {level} context ({context}): {e}")
                # Decide on error strategy: skip chunk, fail all? For now, skip faulty chunks.

        if not points_to_upsert:
            logger.error(f" No valid points generated for upsertion for {level} context ({context})")
            raise ValidationError(status_code=500, detail="No data could be prepared for storage after chunking/embedding.")

        try:
            config.qdrant_client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                points=points_to_upsert,
                wait=True  # Wait for operation to complete
            )
            logger.info(f" Successfully upserted {len(points_to_upsert)} points for {level} context ({context})")
            return AddMemoryResponse(
                message=f"Memory added. {len(points_to_upsert)} chunks stored.",
                chunks_stored=len(points_to_upsert),
                original_content_hash=original_content_hash
            )
        except Exception as e:
            logger.error(f" Failed to upsert points to Qdrant for {level} context ({context}): {e}")
            raise ValidationError(status_code=500, detail=f"Storage in Qdrant failed: {str(e)}")

    except Exception as e:
        logger.error(f" Failed to add memory: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to add memory: {str(e)}")
