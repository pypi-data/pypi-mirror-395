# memory/search.py - search_memories handler

import logging
from typing import List
from collections import defaultdict

from qdrant_client.http import models

from ...config import (
    QDRANT_COLLECTION_NAME, ENABLE_GEMMA_SUMMARIZATION,
    SEARCH_RESULT_MULTIPLIER, MAX_SEARCH_RESULTS
)
from ...models import (
    MemorySearchRequest, RetrievedChunk, SearchResponse, PathGroupedResults
)
from ...services import get_embedding, synthesize_search_results, AppConfig
from ...utils.search_utils import (
    expand_query_with_keywords, calculate_keyword_enhanced_score
)
from ...utils.validation import validate_hierarchy, HierarchyValidationError

from .utils import (
    ValidationError,
    safe_int_conversion,
    chunk_matches_filters,
    filter_superseded_chunks,
)

logger = logging.getLogger(__name__)


async def search_memories(search_request: MemorySearchRequest, config: AppConfig):
    """
    Searches memories in Qdrant with keyword-enhanced querying, then uses LM Studio to synthesize results.
    """
    try:
        # Validate input
        if not search_request.query_text or not search_request.query_text.strip():
            raise ValidationError(
                status_code=400,
                detail="query_text is required and cannot be empty"
            )

        # Validate hierarchical structure in metadata_filters
        other_filters = {}
        if search_request.metadata_filters:
            try:
                validate_hierarchy(
                    app_id=search_request.metadata_filters.get("app_id"),
                    project_id=search_request.metadata_filters.get("project_id"),
                    ticket_id=search_request.metadata_filters.get("ticket_id")
                )
            except HierarchyValidationError as e:
                raise ValidationError(status_code=e.status_code, detail=e.detail)

        filters_str = f", filters: {search_request.metadata_filters}" if search_request.metadata_filters else ""
        keyword_str = f", keyword_filters: {search_request.keyword_filters}" if search_request.keyword_filters else ""
        type_str = f", memory_types: {search_request.memory_types}" if search_request.memory_types else ""
        tags_str = f", tags: {search_request.tag_filters}" if search_request.tag_filters else ""
        logger.info(f" Received /search_memories for query: '{search_request.query_text[:50]}...'{filters_str}{keyword_str}{type_str}{tags_str}")

        # Step 1: Expand query with relevant keywords for better semantic matching
        try:
            expanded_query = await expand_query_with_keywords(search_request.query_text, search_request.metadata_filters, config)
            logger.info(f" Expanded query: '{expanded_query[:100]}...'")
        except Exception as e:
            logger.warning(f" Query expansion failed: {e}")
            expanded_query = search_request.query_text

        try:
            query_embedding = await get_embedding(expanded_query, config.http_client, config)
        except Exception as e:
            logger.error(f" Failed to get embedding for search query: {e}")
            raise ValidationError(status_code=500, detail=f"Query embedding failed: {str(e)}")

        # Qdrant metadata filtering:
        # Build the filter condition to search all memories within the specified scope
        qdrant_filter = None
        if search_request.metadata_filters:
            app_id = search_request.metadata_filters.get("app_id")
            project_id = search_request.metadata_filters.get("project_id")
            ticket_id = search_request.metadata_filters.get("ticket_id")
            run_id = search_request.metadata_filters.get("run_id")

            # Extract non-hierarchy filters
            other_filters = {
                k: v for k, v in search_request.metadata_filters.items()
                if k not in ["app_id", "project_id", "ticket_id", "run_id"]
            }

            # Build filter - search all memories within the specified scope
            must_conditions = []

            if run_id:
                # Search only this specific run
                # Must explicitly exclude documents with empty/missing run_id
                must_conditions.extend([
                    models.FieldCondition(key="app_id", match=models.MatchValue(value=app_id)),
                    models.FieldCondition(key="project_id", match=models.MatchValue(value=project_id)),
                    models.FieldCondition(key="ticket_id", match=models.MatchValue(value=ticket_id)),
                    models.FieldCondition(key="run_id", match=models.MatchValue(value=run_id))
                ])
                # Note: must_not for empty run_id will be added to qdrant_filter below
            elif ticket_id:
                # Search all memories in this ticket (includes runs)
                must_conditions.extend([
                    models.FieldCondition(key="app_id", match=models.MatchValue(value=app_id)),
                    models.FieldCondition(key="project_id", match=models.MatchValue(value=project_id)),
                    models.FieldCondition(key="ticket_id", match=models.MatchValue(value=ticket_id))
                ])
            elif project_id:
                # Search all memories in this project (includes tickets and runs)
                must_conditions.extend([
                    models.FieldCondition(key="app_id", match=models.MatchValue(value=app_id)),
                    models.FieldCondition(key="project_id", match=models.MatchValue(value=project_id))
                ])
            elif app_id:
                # Search all memories in this app (includes projects, tickets, runs)
                must_conditions.append(
                    models.FieldCondition(key="app_id", match=models.MatchValue(value=app_id))
                )

            # Add other metadata filters
            for key, value in other_filters.items():
                if key == "tags":
                    tag_values = list(value) if isinstance(value, (list, tuple, set)) else [value]
                    must_conditions.append(models.FieldCondition(key="tags", match=models.MatchAny(any=tag_values)))
                else:
                    must_conditions.append(models.FieldCondition(key=key, match=models.MatchValue(value=value)))

            # Add type and tag filters
            if search_request.memory_types:
                must_conditions.append(models.FieldCondition(
                    key="type",
                    match=models.MatchAny(any=search_request.memory_types)
                ))
            if search_request.tag_filters:
                must_conditions.append(models.FieldCondition(
                    key="tags",
                    match=models.MatchAny(any=search_request.tag_filters)
                ))

            if must_conditions:
                # Add must_not for empty run_id when filtering by specific run_id
                if run_id:
                    qdrant_filter = models.Filter(
                        must=must_conditions,
                        must_not=[models.IsEmptyCondition(is_empty=models.PayloadField(key="run_id"))]
                    )
                else:
                    qdrant_filter = models.Filter(must=must_conditions)

        elif search_request.memory_types or search_request.tag_filters:
            must_conditions = []
            if search_request.memory_types:
                must_conditions.append(models.FieldCondition(
                    key="type",
                    match=models.MatchAny(any=search_request.memory_types)
                ))
            if search_request.tag_filters:
                must_conditions.append(models.FieldCondition(
                    key="tags",
                    match=models.MatchAny(any=search_request.tag_filters)
                ))
            qdrant_filter = models.Filter(must=must_conditions)

        try:
            # Step 2: Get more results initially for keyword-based re-ranking
            search_limit = min(search_request.limit * SEARCH_RESULT_MULTIPLIER, MAX_SEARCH_RESULTS)
            search_results = config.qdrant_client.search(
                collection_name=QDRANT_COLLECTION_NAME,
                query_vector=query_embedding,
                query_filter=qdrant_filter,
                limit=search_limit,
                with_payload=True,  # Crucial: get the metadata and text_chunk back
                with_vectors=False  # Usually don't need vectors in response
            )
        except Exception as e:
            logger.error(f" Qdrant search failed: {e}")
            raise ValidationError(status_code=500, detail=f"Qdrant search failed: {str(e)}")

        retrieved_chunks_for_response: List[RetrievedChunk] = []
        for hit in search_results:
            # The actual text chunk is in the payload, along with all original metadata
            chunk_content = hit.payload.get("text_chunk", "")
            metadata_from_payload = {k: v for k, v in hit.payload.items() if k != "text_chunk"}

            # Step 3: Calculate keyword-enhanced score
            enhanced_score = calculate_keyword_enhanced_score(
                hit.score,
                search_request.query_text,
                metadata_from_payload.get("keywords", [])
            )

            retrieved_chunks_for_response.append(RetrievedChunk(
                chunk_id=str(hit.id),  # Qdrant point ID
                text_chunk=chunk_content,
                metadata=metadata_from_payload,
                score=enhanced_score  # Use enhanced score instead of raw vector score
            ))

        # Step 3.5: Apply explicit type/tag filters before further processing
        if search_request.memory_types or search_request.tag_filters:
            filtered_chunks = []
            for chunk in retrieved_chunks_for_response:
                if chunk_matches_filters(chunk.metadata, search_request.memory_types, search_request.tag_filters):
                    filtered_chunks.append(chunk)
            logger.info(f" Type/tag post-filter reduced results from {len(retrieved_chunks_for_response)} to {len(filtered_chunks)}")
            retrieved_chunks_for_response = filtered_chunks

        # Step 4: Apply keyword filtering if specified
        if search_request.keyword_filters:
            filtered_chunks = []
            for chunk in retrieved_chunks_for_response:
                keywords = chunk.metadata.get("keywords", [])
                all_chunk_keywords = [kw.lower() for kw in keywords]

                # Check if chunk contains at least one of the required keywords
                required_keywords = [kw.lower() for kw in search_request.keyword_filters]
                if any(req_kw in all_chunk_keywords for req_kw in required_keywords):
                    filtered_chunks.append(chunk)

            retrieved_chunks_for_response = filtered_chunks
            logger.info(f" Keyword filtering reduced results from {len(search_results)} to {len(retrieved_chunks_for_response)}")

        # Step 4.5: Version-aware deduplication - prefer highest version within each logical memory group
        memory_groups = defaultdict(list)
        for chunk in retrieved_chunks_for_response:
            # Create a key that uniquely identifies a logical memory
            app_id = chunk.metadata.get('app_id', '')
            project_id = chunk.metadata.get('project_id', '') or 'none'  # Handle None values
            ticket_id = chunk.metadata.get('ticket_id', '') or 'none'
            run_id = chunk.metadata.get('run_id', '') or 'none'
            memory_type = chunk.metadata.get('type', '') or 'none'

            memory_key = f"{app_id}|{project_id}|{ticket_id}|{run_id}|{memory_type}"
            memory_groups[memory_key].append(chunk)

        # Within each group, prefer chunks from the highest version
        version_filtered_chunks = []
        for memory_key, chunks_in_group in memory_groups.items():
            if len(chunks_in_group) == 1:
                # No versioning conflict, keep the chunk
                version_filtered_chunks.extend(chunks_in_group)
            else:
                # Find the highest version in this group
                max_version = max(safe_int_conversion(chunk.metadata.get('version', 1)) for chunk in chunks_in_group)
                highest_version_chunks = [chunk for chunk in chunks_in_group
                                          if safe_int_conversion(chunk.metadata.get('version', 1)) == max_version]
                version_filtered_chunks.extend(highest_version_chunks)

                logger.info(f" Version deduplication for {memory_key}: {len(chunks_in_group)} chunks reduced to {len(highest_version_chunks)} (version {max_version})")

        if search_request.hide_superseded:
            version_filtered_chunks = filter_superseded_chunks(version_filtered_chunks)

        retrieved_chunks_for_response = version_filtered_chunks

        # Step 5: Re-rank by enhanced scores and limit to requested amount
        retrieved_chunks_for_response.sort(key=lambda x: x.score, reverse=True)
        retrieved_chunks_for_response = retrieved_chunks_for_response[:search_request.limit]

        if not retrieved_chunks_for_response:
            logger.info(" No chunks found matching the search criteria.")
            return SearchResponse(retrieved_chunks=[], total_results=0)

        grouped_results = None
        if search_request.group_by_path:
            path_groups = {}
            for chunk in retrieved_chunks_for_response:
                path_parts = [
                    chunk.metadata.get("app_id"),
                    chunk.metadata.get("project_id"),
                    chunk.metadata.get("ticket_id"),
                    chunk.metadata.get("run_id")
                ]
                path_label_parts = [str(part) for part in path_parts if part]
                path_label = "/".join(path_label_parts) if path_label_parts else "unscoped"

                if path_label not in path_groups:
                    path_groups[path_label] = {
                        "app_id": chunk.metadata.get("app_id"),
                        "project_id": chunk.metadata.get("project_id"),
                        "ticket_id": chunk.metadata.get("ticket_id"),
                        "run_id": chunk.metadata.get("run_id"),
                        "chunks": [],
                        "memory_hashes": set(),
                        "top_score": chunk.score
                    }

                group = path_groups[path_label]
                group["chunks"].append(chunk)
                group["memory_hashes"].add(str(chunk.metadata.get("original_content_hash", chunk.chunk_id)))
                group["top_score"] = max(group["top_score"], chunk.score)

            grouped_results = [
                PathGroupedResults(
                    path=path_label,
                    app_id=data["app_id"],
                    project_id=data["project_id"],
                    ticket_id=data["ticket_id"],
                    run_id=data["run_id"],
                    memory_count=len(data["memory_hashes"]),
                    top_score=data["top_score"],
                    chunks=data["chunks"]
                )
                for path_label, data in path_groups.items()
            ]

        # --- New Enhancement: Synthesize search results (configurable) ---
        synthesized_summary = None
        if ENABLE_GEMMA_SUMMARIZATION and search_request.query_text:
            try:
                # Use the http_client from the config object
                summary = await synthesize_search_results(search_request.query_text, retrieved_chunks_for_response, config.http_client, config)
                if summary:
                    logger.info(" LM Studio summary generated successfully.")
                    synthesized_summary = summary
                else:
                    logger.warning(" LM Studio summarization returned no content.")
            except Exception as e:
                logger.warning(f" Search result summarization failed: {e}. Returning raw chunks.")
                # Proceed to return raw chunks if summarization fails
        else:
            logger.info(f" Gemma summarization disabled via ENABLE_GEMMA_SUMMARIZATION=false")

        if synthesized_summary:
            return SearchResponse(
                synthesized_summary=synthesized_summary,
                retrieved_chunks=retrieved_chunks_for_response,  # Still return chunks for reference or if summary is brief
                total_results=len(retrieved_chunks_for_response),
                grouped_results=grouped_results
            )
        else:
            return SearchResponse(
                retrieved_chunks=retrieved_chunks_for_response,
                total_results=len(retrieved_chunks_for_response),
                grouped_results=grouped_results
            )

    except ValidationError:
        # Re-raise ValidationErrors as-is
        raise
    except Exception as e:
        logger.error(f" Unexpected error in search_memories: {e}")
        raise ValidationError(
            status_code=500,
            detail=f"Internal server error during search: {str(e)}"
        )
