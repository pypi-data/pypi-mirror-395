# utils/dependencies.py - Shared dependencies for Memory Hub endpoints

import httpx
from ..config import HTTP_CLIENT_TIMEOUT

async def get_http_client():
    """HTTP client dependency for async requests to LM Studio."""
    async with httpx.AsyncClient(timeout=HTTP_CLIENT_TIMEOUT) as client:
        yield client 