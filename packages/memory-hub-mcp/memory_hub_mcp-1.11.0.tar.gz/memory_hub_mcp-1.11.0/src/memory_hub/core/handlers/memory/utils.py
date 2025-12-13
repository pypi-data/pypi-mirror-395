# memory/utils.py - Shared utilities for memory handlers

import re
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Set, Optional
from collections import defaultdict

from ...models import RetrievedChunk
from ...chunking import create_semantic_chunker

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Simple exception class to replace FastAPI ValidationError."""
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


# Initialize semantic chunker
try:
    semantic_chunker = create_semantic_chunker(chunk_size=90)
except Exception as e:
    logger.error(f"Failed to initialize semantic chunker: {e}")
    raise ValidationError(status_code=500, detail="Failed to initialize semantic chunker")


def limit_by_memory_count(chunks: List[RetrievedChunk], limit: int, sort_by_timestamp: bool = True) -> List[RetrievedChunk]:
    """
    Groups chunks by original_content_hash and limits by number of memories (not chunks).

    Args:
        chunks: List of chunks to process
        limit: Number of distinct memories to return
        sort_by_timestamp: Whether to sort memory groups by timestamp

    Returns:
        List of chunks representing the limited number of memories
    """
    if not chunks:
        return []

    # Group chunks by original_content_hash to reconstruct complete memories
    memory_groups_by_hash = defaultdict(list)
    for chunk in chunks:
        content_hash = chunk.metadata.get('original_content_hash', 'unknown')
        memory_groups_by_hash[content_hash].append(chunk)

    # Sort memory groups by timestamp (using the most recent chunk's timestamp in each group)
    if sort_by_timestamp:
        sorted_memory_hashes = sorted(
            memory_groups_by_hash.keys(),
            key=lambda h: max(
                chunk.metadata.get('timestamp_iso', '')
                for chunk in memory_groups_by_hash[h]
            ),
            reverse=True  # Most recent first
        )
    else:
        sorted_memory_hashes = list(memory_groups_by_hash.keys())

    # Apply limit to number of MEMORIES (not chunks)
    limited_memory_hashes = sorted_memory_hashes[:limit]

    logger.info(f"Limiting to {limit} memories (from {len(sorted_memory_hashes)} total memories)")

    # Flatten back to chunks, maintaining chunk order within each memory
    result_chunks = []
    for content_hash in limited_memory_hashes:
        chunks_for_memory = memory_groups_by_hash[content_hash]
        # Sort chunks by chunk_index to maintain proper order
        chunks_for_memory.sort(key=lambda x: x.metadata.get('chunk_index', 0))
        result_chunks.extend(chunks_for_memory)

    logger.info(f"Returning {len(result_chunks)} chunks representing {len(limited_memory_hashes)} memories")

    return result_chunks


def safe_int_conversion(value, default=1):
    """
    Safely convert version field to integer, handling string floats like "1.0".

    Args:
        value: The value to convert (could be int, float, string)
        default: Default value if conversion fails

    Returns:
        int: The converted integer value
    """
    if value is None:
        return default

    try:
        # Handle string values that might be "1.0"
        if isinstance(value, str):
            # Convert string to float first, then to int
            return int(float(value))
        # Handle numeric values
        elif isinstance(value, (int, float)):
            return int(value)
        else:
            logger.warning(f"Unexpected version type {type(value)}: {value}, using default {default}")
            return default
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to convert version '{value}' to int: {e}, using default {default}")
        return default


def parse_iso8601_to_utc(timestamp_str: str) -> datetime:
    """
    Parses an ISO8601 timestamp string into a timezone-naive UTC datetime.
    Raises ValidationError on parse failure.
    """
    try:
        cleaned = timestamp_str.strip()
        if cleaned.endswith("Z"):
            cleaned = cleaned[:-1] + "+00:00"
        dt = datetime.fromisoformat(cleaned)
        # Normalize to UTC and drop tzinfo for comparisons
        if dt.tzinfo:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    except Exception as e:
        raise ValidationError(
            status_code=400,
            detail=f"Invalid ISO8601 timestamp '{timestamp_str}': {e}"
        )


def determine_time_bounds(
    hours: Optional[int] = None,
    start_time_iso: Optional[str] = None,
    end_time_iso: Optional[str] = None
) -> tuple:
    """
    Determines start and end time bounds based on explicit ISO inputs or hours window.
    Returns (start_time, end_time) as datetime objects.
    """
    if start_time_iso or end_time_iso:
        end_time = parse_iso8601_to_utc(end_time_iso) if end_time_iso else datetime.utcnow()
        if start_time_iso:
            start_time = parse_iso8601_to_utc(start_time_iso)
        elif hours is not None:
            start_time = end_time - timedelta(hours=hours)
        else:
            start_time = datetime.min
    elif hours is not None:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
    else:
        start_time = datetime.utcnow() - timedelta(hours=24)
        end_time = datetime.utcnow()

    if start_time > end_time:
        raise ValidationError(status_code=400, detail="start_time must be before end_time")

    return start_time, end_time


def normalize_tags_value(raw_tags: Any) -> List[str]:
    """
    Normalizes tags input (string or iterable) into a sorted list of unique strings.
    """
    if raw_tags is None:
        return []

    tags: Set[str] = set()
    if isinstance(raw_tags, str):
        # Allow comma or whitespace separated inputs
        candidates = re.split(r"[,\s]+", raw_tags)
        tags.update(tag.strip() for tag in candidates if tag.strip())
    elif isinstance(raw_tags, (list, tuple, set)):
        for tag in raw_tags:
            tag_str = str(tag).strip()
            if tag_str:
                tags.add(tag_str)
    else:
        logger.warning(f"Unsupported tags type {type(raw_tags)}; skipping tag normalization")

    return sorted(tags)


def chunk_matches_filters(metadata: Dict[str, Any], memory_types: List[str], tags: List[str]) -> bool:
    """
    Returns True if metadata matches provided memory_types and tags filters.
    """
    if memory_types:
        if metadata.get("type") not in memory_types:
            return False

    if tags:
        metadata_tags_raw = metadata.get("tags", [])
        metadata_tags = normalize_tags_value(metadata_tags_raw)
        if not set(metadata_tags).intersection(tags):
            return False

    return True


def filter_superseded_chunks(chunks: List[RetrievedChunk]) -> List[RetrievedChunk]:
    """
    Removes any chunk whose original_content_hash is referenced by another chunk's
    'supersedes' metadata field within the same result set.
    """
    superseded_hashes: Set[str] = set()
    for chunk in chunks:
        supersedes_value = chunk.metadata.get("supersedes")
        if supersedes_value:
            supersedes_list = supersedes_value if isinstance(supersedes_value, (list, tuple, set)) else [supersedes_value]
            superseded_hashes.update(str(val) for val in supersedes_list if str(val))

    if not superseded_hashes:
        return chunks

    filtered = [
        chunk for chunk in chunks
        if str(chunk.metadata.get("original_content_hash", "")) not in superseded_hashes
    ]
    logger.info(f" Supersession filter removed {len(chunks) - len(filtered)} chunks superseded by newer entries")
    return filtered
