# config.py - Configuration constants for Memory Hub MCP Server

import os

# --- Qdrant Configuration ---
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION_NAME = "ai_memory_hub_v1"  # Version your collection name

# --- LM Studio Configuration ---
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
EMBEDDING_MODEL_ENDPOINT = f"{LM_STUDIO_BASE_URL}/embeddings"
CHAT_COMPLETIONS_ENDPOINT = f"{LM_STUDIO_BASE_URL}/chat/completions"

# --- Model Names ---
EMBEDDING_MODEL_NAME = "text-embedding-nomic-embed-text-v1.5"  # Or as loaded in LM Studio
QUERY_SUMMARIZE_MODEL = "google/gemma-3-4b"

# --- Search Quality Configuration ---
MIN_SCORE_THRESHOLD = float(os.getenv("MIN_SCORE_THRESHOLD", "0.60"))

# --- Summarization Configuration ---
ENABLE_GEMMA_SUMMARIZATION = os.getenv("ENABLE_GEMMA_SUMMARIZATION", "true").lower() == "true"

# --- Performance Optimization Configuration ---
# Quantization settings for 75% memory reduction
ENABLE_QUANTIZATION = os.getenv("ENABLE_QUANTIZATION", "true").lower() == "true"
QUANTIZATION_TYPE = os.getenv("QUANTIZATION_TYPE", "int8")
QUANTIZATION_QUANTILE = float(os.getenv("QUANTIZATION_QUANTILE", "0.99"))

# HNSW optimization for production workloads
HNSW_M = int(os.getenv("HNSW_M", "32"))              # More connections = better accuracy (default: 16)
HNSW_EF_CONSTRUCT = int(os.getenv("HNSW_EF_CONSTRUCT", "256"))  # Better index quality (default: 100)

# Multi-tenant optimization
ENABLE_TENANT_OPTIMIZATION = os.getenv("ENABLE_TENANT_OPTIMIZATION", "true").lower() == "true"

# --- Search Utility Configuration ---
# Keyword extraction and scoring settings
MAX_KEYWORDS_FALLBACK = int(os.getenv("MAX_KEYWORDS_FALLBACK", "5"))
MAX_CHUNK_LENGTH_FOR_KEYWORDS = int(os.getenv("MAX_CHUNK_LENGTH_FOR_KEYWORDS", "2000"))

# Query expansion settings
QUERY_EXPANSION_SAMPLE_SIZE = int(os.getenv("QUERY_EXPANSION_SAMPLE_SIZE", "5"))
QUERY_EXPANSION_MAX_KEYWORDS = int(os.getenv("QUERY_EXPANSION_MAX_KEYWORDS", "3"))

# Keyword scoring boosts
EXACT_MATCH_BOOST = float(os.getenv("EXACT_MATCH_BOOST", "0.05"))
PARTIAL_MATCH_BOOST = float(os.getenv("PARTIAL_MATCH_BOOST", "0.02"))
MAX_EXACT_MATCH_BOOST = float(os.getenv("MAX_EXACT_MATCH_BOOST", "0.15"))
MAX_PARTIAL_MATCH_BOOST = float(os.getenv("MAX_PARTIAL_MATCH_BOOST", "0.10"))

# Search result processing
SEARCH_RESULT_MULTIPLIER = int(os.getenv("SEARCH_RESULT_MULTIPLIER", "3"))
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "50"))
MAX_SUMMARIZATION_CHUNKS = int(os.getenv("MAX_SUMMARIZATION_CHUNKS", "5"))

# HTTP client settings  
HTTP_CLIENT_TIMEOUT = float(os.getenv("HTTP_CLIENT_TIMEOUT", "30.0"))
KEYWORD_EXTRACTION_TIMEOUT = float(os.getenv("KEYWORD_EXTRACTION_TIMEOUT", "15.0"))

# Qdrant pagination settings
SCROLL_BATCH_SIZE = int(os.getenv("SCROLL_BATCH_SIZE", "100")) 