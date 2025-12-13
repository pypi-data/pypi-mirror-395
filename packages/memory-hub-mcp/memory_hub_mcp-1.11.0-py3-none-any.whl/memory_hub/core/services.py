# services.py - Core service functions for Memory Hub MCP Server

import os
import httpx
import logging
from typing import List, Optional
from dataclasses import dataclass, field
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import ResponseHandlingException

from .config import (
    QDRANT_COLLECTION_NAME, 
    EMBEDDING_MODEL_NAME, QUERY_SUMMARIZE_MODEL, MIN_SCORE_THRESHOLD,
    ENABLE_QUANTIZATION, QUANTIZATION_TYPE, QUANTIZATION_QUANTILE,
    HNSW_M, HNSW_EF_CONSTRUCT, ENABLE_TENANT_OPTIMIZATION
)
from .models import RetrievedChunk

# Configure logging
logger = logging.getLogger(__name__)

# Application Configuration
@dataclass
class AppConfig:
    qdrant_url: Optional[str] = None
    lm_studio_url: Optional[str] = None
    qdrant_client: Optional[QdrantClient] = field(default=None, init=False)
    http_client: Optional[httpx.AsyncClient] = field(default=None, init=False)
    
    # Derived properties for endpoint URLs
    @property
    def embedding_model_endpoint(self) -> str:
        base_url = self.lm_studio_url or "http://localhost:1234/v1"
        return f"{base_url}/embeddings"

    @property
    def chat_completions_endpoint(self) -> str:
        base_url = self.lm_studio_url or "http://localhost:1234/v1"
        return f"{base_url}/chat/completions"

async def get_embedding(text: str, client: httpx.AsyncClient, config: AppConfig) -> List[float]:
    try:
        response = await client.post(
            config.embedding_model_endpoint,
            json={"input": text, "model": EMBEDDING_MODEL_NAME}
        )
        response.raise_for_status()
        data = response.json()
        if "data" in data and data["data"] and "embedding" in data["data"][0]:
            return data["data"][0]["embedding"]
        elif "embedding" in data: # Fallback for some Ollama direct API styles
            return data["embedding"]
        else:
            logger.error(f" Unexpected embedding response: {data}")
            raise ValueError("Embedding not found in response")
    except httpx.HTTPStatusError as e:
        logger.error(f" HTTP error getting embedding for '{text[:50]}...': {e.response.text}")
        raise
    except Exception as e:
        logger.error(f" Exception getting embedding: {e}")
        raise

async def synthesize_search_results(query_text: str, chunks: List[RetrievedChunk], client: httpx.AsyncClient, config: AppConfig) -> Optional[str]:
    if not chunks:
        return None
    
    # Limit chunks to prevent context overflow (max 5 chunks for summarization)
    chunks_to_process = chunks[:5]
    
    # Filter chunks by score threshold to reduce noise
    high_quality_chunks = [chunk for chunk in chunks_to_process if chunk.score >= MIN_SCORE_THRESHOLD]
    
    if not high_quality_chunks:
        logger.warning(f"No chunks above score threshold {MIN_SCORE_THRESHOLD} for query: {query_text}")
        # Fall back to top 3 chunks even if below threshold, but flag this
        high_quality_chunks = chunks_to_process[:3]
        quality_warning = f"[LOW CONFIDENCE: All chunks below {MIN_SCORE_THRESHOLD} threshold] "
    else:
        quality_warning = ""
    
    # Build context with aggressive length controls
    context_for_summary = f"Query: \"{query_text}\"\n\nChunks (ordered by relevance score):\n"
    max_context_length = 8000  # Conservative limit for LM Studio context
    
    for i, chunk_obj in enumerate(high_quality_chunks):
        chunk_addition = f"\n--- Chunk {i+1} (Score: {chunk_obj.score:.4f}, ID: {chunk_obj.chunk_id}) ---\n"
        
        # Truncate very long chunks to prevent context overflow
        chunk_text = chunk_obj.text_chunk
        if len(chunk_text) > 2000:
            chunk_text = chunk_text[:2000] + "...[truncated]"
        
        chunk_addition += f"Metadata: {chunk_obj.metadata}\n"
        chunk_addition += f"Content: {chunk_text}\n"
        
        # Check if adding this chunk would exceed our limit
        if len(context_for_summary + chunk_addition) > max_context_length:
            logger.warning(f" Context for summary approaching limit ({max_context_length} chars), stopping at chunk {i}")
            break
            
        context_for_summary += chunk_addition

    # Detect if this is an exact text request
    exact_keywords = ["exact", "exactly", "specific text", "word for word", "precisely", "verbatim", "literal"]
    is_exact_request = any(keyword in query_text.lower() for keyword in exact_keywords)
    
    if is_exact_request:
        system_prompt = "Extract exact text from the chunks. When users request 'exact' content, provide literal quotes from the source material. Preserve original formatting including numbered lists, bullet points, and structure. If the exact requested content is not found in the chunks, state 'The exact text/section requested was not found in the source material.' Do not paraphrase or synthesize when exact text is requested."
    else:
        system_prompt = "Synthesize chunks into direct, factual responses. NO preambles like 'Based on provided information' or 'Here's a summary'. For specific queries, lead with the direct answer. Use chunk scores as confidence indicators - higher scores are more reliable. If chunks contradict each other, note the contradiction and indicate which has higher confidence. Be concise and information-dense. Preserve numbered lists and bullet points when present in source material."
    
    prompt_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": context_for_summary}
    ]
    
    logger.info(f" Sending {len(high_quality_chunks)} chunks to LM Studio for summarization related to query: '{query_text}'")

    try:
        # Add explicit timeout and context length protection
        response = await client.post(
            config.chat_completions_endpoint,
            json={
                "model": QUERY_SUMMARIZE_MODEL,
                "messages": prompt_messages,
                "temperature": 0.3, # Lower temp for factual summarization
                "max_tokens": 1024 
            },
            timeout=30.0  # Explicit timeout for summarization
        )
        response.raise_for_status()
        data = response.json()
        if "choices" in data and data["choices"] and "message" in data["choices"][0] and "content" in data["choices"][0]["message"]:
            summary = data["choices"][0]["message"]["content"]
            # Prepend quality warning if needed
            final_summary = quality_warning + summary if quality_warning else summary
            logger.info(f" Search results summary generated: {final_summary[:100]}...")
            return final_summary
        else:
            logger.error(f" Unexpected LM Studio response: {data}")
            return None
    except httpx.HTTPStatusError as e:
        error_text = e.response.text if hasattr(e.response, 'text') else str(e)
        
        # Handle context length errors specifically
        if "context length" in error_text.lower() or "initial prompt is greater" in error_text.lower():
            logger.error(f" LM Studio context length exceeded - chunks too large for summarization: {error_text}")
            # Don't retry, just return None to fall back to raw chunks
            return None
        else:
            logger.error(f" HTTP error calling LM Studio: {error_text}")
            return None # Fallback to returning raw chunks if summary fails
    except httpx.TimeoutException:
        logger.error(f" LM Studio summarization timed out")
        return None
    except Exception as e:
        logger.error(f" Exception calling LM Studio: {e}")
        return None

async def startup_event(config: AppConfig):
    """Initialize Qdrant client and collection if it doesn't exist."""
    try:
        # Use URL from config, fall back to environment variable or default from config.py
        qdrant_url = config.qdrant_url or os.getenv("QDRANT_URL", "http://localhost:6333")
        config.qdrant_client = QdrantClient(url=qdrant_url)
        
        collections = config.qdrant_client.get_collections()
        collection_names = [c.name for c in collections.collections]
        if QDRANT_COLLECTION_NAME not in collection_names:
            logger.info(f" Collection '{QDRANT_COLLECTION_NAME}' not found. Creating...")
            
            # Base collection configuration - Nomic embedding size is 768 for v1.5
            collection_params = {
                "collection_name": QDRANT_COLLECTION_NAME,
                "vectors_config": models.VectorParams(
                    size=768, 
                    distance=models.Distance.COSINE
                )
            }
            
            # Add quantization if enabled (75% memory reduction)
            if ENABLE_QUANTIZATION:
                collection_params["quantization_config"] = models.ScalarQuantization(
                    scalar=models.ScalarQuantizationConfig(
                        type=getattr(models.ScalarType, QUANTIZATION_TYPE.upper()),
                        always_ram=True,  # Keep quantized vectors in RAM for speed
                        quantile=QUANTIZATION_QUANTILE
                    ),
                )
                logger.info(f" Quantization enabled: {QUANTIZATION_TYPE} with {QUANTIZATION_QUANTILE} quantile")
            
            # Add optimized HNSW parameters for production workloads
            collection_params["hnsw_config"] = models.HnswConfigDiff(
                m=HNSW_M,
                ef_construct=HNSW_EF_CONSTRUCT,
                on_disk=False  # Keep index in RAM for speed
            )
            
            config.qdrant_client.create_collection(**collection_params)
            
            optimization_features = []
            if ENABLE_QUANTIZATION:
                optimization_features.append("quantization")
            optimization_features.append(f"HNSW(m={HNSW_M}, ef_construct={HNSW_EF_CONSTRUCT})")
            
            logger.info(f" Collection '{QDRANT_COLLECTION_NAME}' created successfully with: {', '.join(optimization_features)}")
            
            # Create field indexes for commonly filtered metadata fields
            logger.info(f" Creating field indexes for optimal filtering performance...")
            
            try:
                # Index app_id with multi-tenant optimization (highest level in hierarchy)
                if ENABLE_TENANT_OPTIMIZATION:
                    config.qdrant_client.create_payload_index(
                        collection_name=QDRANT_COLLECTION_NAME,
                        field_name="app_id",
                        field_schema=models.KeywordIndexParams(
                            type="keyword",
                            is_tenant=True  # Optimize storage for multi-tenant architecture
                        )
                    )
                    logger.info(" Created index for field 'app_id' (multi-tenant optimized)")
                else:
                    config.qdrant_client.create_payload_index(
                        collection_name=QDRANT_COLLECTION_NAME,
                        field_name="app_id",
                        field_schema=models.PayloadSchemaType.KEYWORD
                    )
                    logger.info(" Created index for field 'app_id'")
                
                # Index project_id (also gets tenant optimization as it's commonly filtered)
                if ENABLE_TENANT_OPTIMIZATION:
                    config.qdrant_client.create_payload_index(
                        collection_name=QDRANT_COLLECTION_NAME,
                        field_name="project_id",
                        field_schema=models.KeywordIndexParams(
                            type="keyword",
                            is_tenant=True  # Optimize storage for multi-tenant architecture
                        )
                    )
                    logger.info(" Created index for field 'project_id' (multi-tenant optimized)")
                else:
                    config.qdrant_client.create_payload_index(
                        collection_name=QDRANT_COLLECTION_NAME,
                        field_name="project_id",
                        field_schema=models.PayloadSchemaType.KEYWORD
                    )
                    logger.info(" Created index for field 'project_id'")
                
                # Index the other commonly filtered fields with simple, compatible syntax
                field_indexes = [
                    ("ticket_id", models.PayloadSchemaType.KEYWORD),
                    ("type", models.PayloadSchemaType.KEYWORD),
                    ("version", models.PayloadSchemaType.INTEGER)
                ]                
                for field_name, field_type in field_indexes:
                    try:
                        config.qdrant_client.create_payload_index(
                            collection_name=QDRANT_COLLECTION_NAME,
                            field_name=field_name,
                            field_schema=field_type
                        )
                        logger.info(f" Created index for field '{field_name}'")
                    except Exception as e:
                        logger.warning(f" Failed to create index for '{field_name}': {e}")
                        # Don't fail startup if indexing fails - collection is still usable
                
                logger.info(f" Field indexes created successfully for app_id, project_id, ticket_id, type, version")
            except Exception as e:
                logger.warning(f" Failed to create some field indexes: {e}")
                # Don't fail startup if indexing fails - collection is still usable
        else:
            logger.info(f" Collection '{QDRANT_COLLECTION_NAME}' already exists.")

    except ResponseHandlingException as e:
        # ResponseHandlingException may not have status_code attribute (e.g., SSL errors)
        logger.error(f" Could not connect to Qdrant at {qdrant_url}.")
        logger.info(f"Common causes:")
        logger.info(f"  - Using https:// instead of http:// (Qdrant typically uses HTTP)")
        logger.info(f"  - Qdrant service is not running")
        logger.info(f"  - Network/firewall issue")
        logger.info(f"  - Wrong IP address or port")
        logger.info(f"Error details: {e}")
        raise  # Re-raise to stop server startup
    except Exception as e:
        logger.error(f" Failed to initialize Qdrant. Please check if it's running and accessible. Error: {e}")
        raise # Re-raise to stop server startup

async def shutdown_event(config: AppConfig):
    """Clean up resources on shutdown."""
    if config.http_client:
        await config.http_client.aclose()
        logger.info(" HTTP client closed.")
    if config.qdrant_client:
        config.qdrant_client.close()
        logger.info(" Qdrant client closed.") 