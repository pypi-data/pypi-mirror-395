import logging
from typing import Dict, Optional, Any, Literal
import httpx

logger = logging.getLogger(__name__)


class HTTPClientError(Exception):
    """Custom exception for HTTP client errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class HttpClient:
    """Async HTTP client with pooling, DRY error handling, and full params support."""

    def __init__(self, timeout: float = 10.0, read_timeout: float = 30.0):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout, read=read_timeout),
            limits=httpx.Limits(max_connections=50, max_keepalive_connections=25),
            follow_redirects=True,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._client.aclose()

    async def _request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        return_type: Literal["json", "bytes", "response"] = "json",
    ) -> Any:
        try:
            logger.debug(f"{method.upper()} {url} | params={params}")
            resp = await self._client.request(
                method, url, headers=headers, params=params, data=data, json=json
            )
            resp.raise_for_status()
            logger.debug(f"Response: {resp.status_code}")

            if return_type == "json":
                return resp.json()
            elif return_type == "bytes":
                return resp.content
            return resp

        except httpx.HTTPStatusError as e:
            raise HTTPClientError(f"HTTP {e.response.status_code} for {method} {url}", e.response.status_code)
        except httpx.RequestError as e:
            raise HTTPClientError(f"Request error for {method} {url}: {e}")
        except Exception as e:
            raise HTTPClientError(f"Unexpected error for {method} {url}: {e}")

    # Convenience wrappers
    async def get_json(self, url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("GET", url, headers=headers, params=params, return_type="json")

    async def get_bytes(self, url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> bytes:
        return await self._request("GET", url, headers=headers, params=params, return_type="bytes")
