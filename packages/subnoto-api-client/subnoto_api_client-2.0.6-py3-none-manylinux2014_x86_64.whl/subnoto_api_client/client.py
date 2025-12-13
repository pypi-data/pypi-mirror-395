# Copyright 2025 Subnoto
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Any, Dict, Optional

import httpx

from .session import SessionManager
from .transport import TunnelTransport
from .types import SubnotoConfig
from .generated.client import Client as GeneratedClient


class GeneratedClientWrapper:
    """Wrapper to make our httpx client compatible with generated client expectations"""
    
    def __init__(self, httpx_client: httpx.AsyncClient):
        self._httpx_client = httpx_client
        self.raise_on_unexpected_status = False
    
    def get_async_httpx_client(self) -> httpx.AsyncClient:
        return self._httpx_client
    
    def get_httpx_client(self) -> httpx.Client:
        raise NotImplementedError("Synchronous client not supported")


class SubnotoClient:
    """
    Subnoto API client with Oak tunnel encryption and HTTP signature authentication
    
    This is a wrapper around the generated OpenAPI client that adds:
    - Oak tunnel encryption for secure communication
    - HTTP signature authentication (RFC 9421)
    - Session management with attestation support
    
    You can use the generated API functions directly:
        from subnoto_api_client.api.utils import post_public_utils_whoami
        response = await post_public_utils_whoami.asyncio(client=client, body={})
    
    Or use the lower-level httpx methods:
        response = await client.get("/public/utils/whoami")
    """
    
    def __init__(self, config: SubnotoConfig):
        self.config = config
        
        # Create session manager first (without http_client)
        self.session_manager = SessionManager(config)
        
        # Create custom transport with tunnel encryption and signatures
        transport = TunnelTransport(
            self.session_manager,
            config.access_key,
            config.secret_key
        )
        
        # Create httpx client with custom transport
        self._client = httpx.AsyncClient(
            base_url=config.api_base_url,
            transport=transport,
            timeout=30.0
        )
        
        # Now give the session manager our signed client for handshakes
        self.session_manager.http_client = self._client
        
        # Create wrapper for generated client compatibility
        self.generated = GeneratedClientWrapper(self._client)
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def close(self) -> None:
        """Close the client and cleanup resources"""
        await self._client.aclose()
        self.session_manager.destroy()
    
    async def get(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Make a GET request"""
        return await self._client.get(path, params=params, headers=headers)
    
    async def post(
        self,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Make a POST request"""
        return await self._client.post(path, json=json, content=data, headers=headers)
    
    async def put(
        self,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Make a PUT request"""
        return await self._client.put(path, json=json, content=data, headers=headers)
    
    async def delete(
        self,
        path: str,
        *,
        headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Make a DELETE request"""
        return await self._client.delete(path, headers=headers)
    
    async def patch(
        self,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Make a PATCH request"""
        return await self._client.patch(path, json=json, content=data, headers=headers)
    
    def get_attestation_results(self) -> Optional[str]:
        """Get attestation results as JSON string"""
        return self.session_manager.get_attestation_results()
    
    def get_attestation_status(self) -> Optional[str]:
        """Get attestation status as JSON string"""
        return self.session_manager.get_attestation_status()

