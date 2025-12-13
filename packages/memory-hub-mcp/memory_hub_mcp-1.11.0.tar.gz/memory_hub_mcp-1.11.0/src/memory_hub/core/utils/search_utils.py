# utils/search_utils.py - Search utility functions for Memory Hub

import re
import json
from typing import List, Set, Dict, Tuple
import httpx
from qdrant_client.http import models

from ..config import (
    QDRANT_COLLECTION_NAME, MAX_KEYWORDS_FALLBACK, MAX_CHUNK_LENGTH_FOR_KEYWORDS,
    QUERY_EXPANSION_SAMPLE_SIZE, QUERY_EXPANSION_MAX_KEYWORDS, EXACT_MATCH_BOOST,
    PARTIAL_MATCH_BOOST, MAX_EXACT_MATCH_BOOST, MAX_PARTIAL_MATCH_BOOST,
    KEYWORD_EXTRACTION_TIMEOUT
)
from ..services import get_embedding, AppConfig

import logging
logger = logging.getLogger(__name__)

def validate_version_logic(chunks: List) -> Dict[str, any]:
    """
    Utility function to validate version-aware search logic.
    Returns analysis of version distribution for debugging.
    """
    from collections import defaultdict
    # Import the safe conversion function
    from ..handlers.memory import safe_int_conversion
    
    memory_groups = defaultdict(list)
    version_stats = {}
    
    for chunk in chunks:
        app_id = chunk.metadata.get('app_id', '')
        project_id = chunk.metadata.get('project_id', '') or 'none'
        ticket_id = chunk.metadata.get('ticket_id', '') or 'none'
        memory_type = chunk.metadata.get('type', '') or 'none'
        version = safe_int_conversion(chunk.metadata.get('version', 1))
        
        memory_key = f"{app_id}|{project_id}|{ticket_id}|{memory_type}"
        memory_groups[memory_key].append((version, chunk.chunk_id))
    
    # Analyze version conflicts
    for memory_key, versions_and_ids in memory_groups.items():
        versions = [v[0] for v in versions_and_ids]
        if len(set(versions)) > 1:  # Multiple versions exist
            max_version = max(versions)
            version_stats[memory_key] = {
                'versions_found': sorted(set(versions)),
                'highest_version': max_version,
                'total_chunks': len(versions_and_ids),
                'conflict_detected': True
            }
    
    return {
        'total_memory_groups': len(memory_groups),
        'groups_with_version_conflicts': len(version_stats),
        'conflict_details': version_stats
    }

async def expand_query_with_keywords(query_text: str, metadata_filters: dict, config: AppConfig) -> str:
    """
    Expand search query by finding related keywords from existing chunks in the same context.
    This helps find semantically related content even if different terminology is used.
    """
    try:
        # Quick search to find related keywords from the same app/project context
        if not metadata_filters:
            return query_text  # Can't expand without context
        
        # Create a simplified filter for context matching
        context_filter = models.Filter(
            must=[models.FieldCondition(key=k, match=models.MatchValue(value=v)) 
                  for k, v in metadata_filters.items()]
        )
        
        # Get a small sample of chunks from the same context
        sample_results = config.qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=await get_embedding(query_text, config.http_client, config),
            query_filter=context_filter,
            limit=QUERY_EXPANSION_SAMPLE_SIZE,
            with_payload=True,
            with_vectors=False
        )
        
        # Extract keywords from top matching chunks
        related_keywords = set()
        for hit in sample_results:
             keywords = hit.payload.get("keywords", [])
             related_keywords.update(keywords)
        
        # Add relevant keywords to query (limit to avoid query bloat)
        if related_keywords:
            keyword_addition = " ".join(list(related_keywords)[:QUERY_EXPANSION_MAX_KEYWORDS])
            expanded = f"{query_text} {keyword_addition}"
            return expanded
        
        return query_text
    
    except Exception as e:
        logger.warning(f" Query expansion failed: {e}")
        return query_text  # Fallback to original query

def calculate_keyword_enhanced_score(vector_score: float, query_text: str, keywords: List[str]) -> float:
    """
    Enhance vector similarity score with keyword relevance matching.
    This provides hybrid search combining semantic and lexical matching.
    """
    # Start with the vector similarity score
    enhanced_score = vector_score
    
    # Convert query and keywords to lowercase for matching
    query_lower = query_text.lower()
    all_keywords = [kw.lower() for kw in keywords]
    
    # Keyword matching bonuses
    exact_matches = sum(1 for keyword in all_keywords if keyword in query_lower)
    partial_matches = sum(1 for keyword in all_keywords 
                         if any(word in keyword or keyword in word 
                               for word in query_lower.split()))
    
    # Calculate keyword bonus (up to 20% boost)
    if exact_matches > 0:
        keyword_boost = min(MAX_EXACT_MATCH_BOOST, exact_matches * EXACT_MATCH_BOOST)
    elif partial_matches > 0:
        keyword_boost = min(MAX_PARTIAL_MATCH_BOOST, partial_matches * PARTIAL_MATCH_BOOST)
    else:
        keyword_boost = 0
    
    # Apply keyword boost
    enhanced_score = min(1.0, vector_score + keyword_boost)
    
    return enhanced_score

async def generate_chunk_keywords(chunk_text: str, config: AppConfig) -> List[str]:
    """
    Generate chunk-specific keywords using Gemma LLM.
    
    This provides precise keyword extraction by understanding the semantic content 
    of each chunk and identifying the most searchable terms.
    """
    try:
        # Truncate chunk text if too long to prevent context overflow
        if len(chunk_text) > MAX_CHUNK_LENGTH_FOR_KEYWORDS:
            chunk_text = chunk_text[:MAX_CHUNK_LENGTH_FOR_KEYWORDS] + "..."
            logger.warning(f" Truncated chunk text for keyword extraction ({MAX_CHUNK_LENGTH_FOR_KEYWORDS} chars)")

        prompt = f"""Analyze this text chunk and extract 3-5 specific, relevant keywords that would help someone find this content in a search.

Text chunk:
{chunk_text}

Requirements:
- Return ONLY a JSON array of keywords, nothing else
- Focus on technical terms, proper nouns, and key concepts  
- Avoid generic words like "the", "and", "system"
- Keep keywords short and specific (1-2 words ideal)
- Examples: ["bedrock", "api", "dealership", "recommendations", "inventory"]

Keywords:"""

        # Make request to Gemma with timeout and proper error handling
        try:
            response = await config.http_client.post(
                config.chat_completions_endpoint,
                json={
                    "model": "google/gemma-3-4b",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 100
                },
                timeout=KEYWORD_EXTRACTION_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                
                # Try to parse JSON array from response
                try:
                    keywords = json.loads(content)
                    if isinstance(keywords, list) and len(keywords) <= 5:
                        # Clean and validate keywords
                        cleaned_keywords = [kw.lower().strip() for kw in keywords if isinstance(kw, str) and len(kw) > 2]
                        return cleaned_keywords[:5]
                except json.JSONDecodeError:
                    # Fallback: extract keywords from content if JSON parsing fails
                    keywords = re.findall(r'"([^"]+)"', content)
                    if keywords:
                        return [kw.lower().strip() for kw in keywords[:5]]
            else:
                logger.warning(f" Gemma keyword extraction HTTP error: {response.status_code}")
        
        except httpx.TimeoutException:
            logger.warning(f" Gemma keyword extraction timed out")
        except httpx.HTTPStatusError as e:
            logger.warning(f" Gemma keyword extraction HTTP error: {e}")
        except Exception as e:
            logger.warning(f" Gemma keyword extraction request failed: {e}")
        
        logger.warning(f" Gemma keyword extraction failed, returning empty keywords")
        return []
        
    except Exception as e:
        logger.error(f" Gemma keyword extraction failed: {e}")
        return [] 