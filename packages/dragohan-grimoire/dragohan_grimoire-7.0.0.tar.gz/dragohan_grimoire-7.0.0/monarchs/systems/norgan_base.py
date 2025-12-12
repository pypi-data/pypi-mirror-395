"""
💀 N-ORGAN BASE - Hybrid N8N + Python Organ Foundation 💀

Base class for all N-Organs (hybrid systems).

N-Organs = N8N handles I/O + Python handles AI/logic
Communication via synchronous HTTP POST.

Golden Rule: Python = stateless brain. Zero memory.
"""

import asyncio
import httpx
from typing import Dict, Any, List, Optional
from .base import SystemBase, StageResult


class NOrganBase(SystemBase):
    """
    💀 N-ORGAN BASE CLASS 💀

    Foundation for all N-Organs. Adds HTTP capabilities to SystemBase.

    Features:
    - HTTP client with retry logic
    - 4-Layer Guardian error handling
    - Request/response validation
    - Connection pooling and cleanup
    """

    def __init__(self, runs_dir: str = "./runs"):
        super().__init__(runs_dir)
        self._http_client: Optional[httpx.AsyncClient] = None

    async def _get_http_client(self) -> httpx.AsyncClient:
        """Lazy-load HTTP client with connection pooling"""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(
                timeout=30.0,
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
        return self._http_client

    async def http_post_with_retry(
        self,
        url: str,
        json_data: dict,
        max_retries: int = 3
    ) -> dict:
        """
        POST request with exponential backoff retry

        Args:
            url: Target URL
            json_data: JSON payload
            max_retries: Maximum retry attempts

        Returns:
            dict: Response JSON

        Raises:
            httpx.HTTPError: If all retries fail
        """
        client = await self._get_http_client()

        for attempt in range(max_retries):
            try:
                print(f"   🔄 HTTP POST attempt {attempt + 1}/{max_retries}...")
                response = await client.post(url, json=json_data)
                response.raise_for_status()
                print(f"   ✅ HTTP POST successful")
                return response.json()

            except httpx.TimeoutException as e:
                print(f"   ⏱️  Timeout on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # 1s, 2s, 4s

            except httpx.HTTPStatusError as e:
                print(f"   ❌ HTTP {e.response.status_code} on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)

            except httpx.RequestError as e:
                print(f"   ❌ Request error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)

    def validate_request_schema(self, data: dict, required_fields: List[str]):
        """
        Validate required fields are present

        Args:
            data: Data to validate
            required_fields: List of required field names

        Raises:
            ValueError: If any required fields are missing
        """
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

    def validate_response_schema(self, data: dict, required_fields: List[str]):
        """
        Validate response has required fields

        Args:
            data: Response data to validate
            required_fields: List of required field names

        Raises:
            ValueError: If any required fields are missing
        """
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"Response missing fields: {', '.join(missing)}")

    async def close(self):
        """Cleanup HTTP connections"""
        if self._http_client:
            print("   🔌 Closing HTTP client...")
            await self._http_client.aclose()
            self._http_client = None

    def __del__(self):
        """Cleanup on deletion"""
        if self._http_client:
            try:
                asyncio.run(self.close())
            except:
                pass  # Best effort cleanup
