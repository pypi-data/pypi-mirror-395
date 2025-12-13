# chunking.py - Semantic chunking functionality using semchunk

from typing import List
import semchunk

def create_token_counter():
    """
    Create a simple token counter function for semchunk.
    Using word-based splitting as a reasonable approximation for tokens.
    For more accuracy, you could integrate tiktoken or transformers tokenizers.
    """
    def token_counter(text: str) -> int:
        # Simple word-based token counting
        # This is a reasonable approximation; semchunk will handle the semantic splitting
        return len(text.split())
    
    return token_counter

def create_semantic_chunker(chunk_size: int = 90, min_chunk_size: int = 20):
    """
    Create a semantic chunker using semchunk library with post-processing to merge small chunks.
    
    chunk_size: Target chunk size in tokens (words). For technical documentation,
    80-100 tokens creates optimal granularity for precise retrieval while preserving
    semantic coherence. This typically yields 10-15 chunks for 1000-word documents.
    
    min_chunk_size: Minimum viable chunk size. Chunks smaller than this will be merged
    with adjacent chunks to prevent header-only or fragment chunks.
    """
    token_counter = create_token_counter()
    base_chunker = semchunk.chunkerify(token_counter, chunk_size=chunk_size)
    
    def enhanced_chunker(text: str) -> List[str]:
        """Enhanced chunker that merges small chunks to prevent header-only fragments."""
        raw_chunks = base_chunker(text)
        
        # Merge small chunks with adjacent ones
        merged_chunks = []
        i = 0
        while i < len(raw_chunks):
            current_chunk = raw_chunks[i]
            current_size = token_counter(current_chunk)
            
            # If chunk is too small, try to merge with next chunk
            if current_size < min_chunk_size and i + 1 < len(raw_chunks):
                next_chunk = raw_chunks[i + 1]
                combined = f"{current_chunk} {next_chunk}".strip()
                combined_size = token_counter(combined)
                
                # Only merge if combined chunk doesn't exceed target size
                if combined_size <= chunk_size * 1.2:  # Allow 20% overage for merging
                    merged_chunks.append(combined)
                    i += 2  # Skip next chunk since we merged it
                    continue
            
            merged_chunks.append(current_chunk)
            i += 1
        
        return merged_chunks
    
    return enhanced_chunker 