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

"""
Simplified transport using pure httpx with signature generation
"""

from typing import TYPE_CHECKING
import httpx

from .middleware.signature_utils import sign_request_headers
from .types import SubnotoError

if TYPE_CHECKING:
    from .session import SessionManager


class TunnelTransport(httpx.AsyncHTTPTransport):
    """Custom transport using httpx for tunnel encryption and signatures"""
    
    def __init__(self, session_manager: "SessionManager", access_key: str, secret_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_manager = session_manager
        self.access_key = access_key
        self.secret_key = secret_key
    
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        """Handle request with encryption and signature"""
        url = str(request.url)
        path = request.url.path
        
        # Skip all processing for handshake requests
        if path == "/tunnel/session":
            return await super().handle_async_request(request)
        
        # For local testing, skip encryption but still sign
        is_local = "localhost" in str(request.url.host) or "127.0.0.1" in str(request.url.host)
        
        # Check if this request needs tunnel encryption
        needs_encryption = not is_local and (
            path.startswith("/tunnel/") or (path.startswith("/public/") and request.method != "GET")
        )
        
        if needs_encryption:
            # Ensure session is established
            await self.session_manager.ensure_session()
            
            # Read original content
            await request.aread()
            original_content = request.content
            
            # Encrypt the content
            encrypted_content = self.session_manager.encrypt_request(original_content)
            
            # Get session ID
            session_id = self.session_manager.get_session_id()
            if not session_id:
                raise SubnotoError("Session ID not available")
            
            # Generate signature headers for ENCRYPTED content
            signature_headers = sign_request_headers(
                url=url,
                method=request.method,
                body_content=encrypted_content,
                access_key=self.access_key,
                secret_key=self.secret_key,
                existing_headers={"content-type": "application/octet-stream"}
            )
            
            # Build new headers without duplicates
            new_headers = dict(signature_headers)
            new_headers["X-Session-Id"] = session_id
            
            # Add cookies
            cookies = self.session_manager._get_cookies_for_request(url)
            if cookies:
                new_headers["Cookie"] = cookies
            
            # Create new request with encrypted content and signature headers
            new_request = httpx.Request(
                method=request.method,
                url=request.url,
                headers=new_headers,
                content=encrypted_content,
                extensions=request.extensions
            )
            
            # Send via parent transport
            response = await super().handle_async_request(new_request)
            
            # Decrypt if needed
            if response.headers.get("x-subnoto-encrypted-response") == "true":
                response_content = await response.aread()
                decrypted_content = self.session_manager.decrypt_response(response_content)
                response = httpx.Response(
                    status_code=response.status_code,
                    headers=response.headers,
                    content=decrypted_content,
                    request=request,
                )
            
            # Store cookies
            self.session_manager._store_cookies(response, url)
            
            return response
        else:
            # No encryption needed, but still sign
            await request.aread()
            body_content = request.content if request.content else b""
            
            # Generate signature headers
            signature_headers = sign_request_headers(
                url=url,
                method=request.method,
                body_content=body_content,
                access_key=self.access_key,
                secret_key=self.secret_key,
                existing_headers=dict(request.headers)
            )
            
            # Build new headers without duplicates
            new_headers = dict(signature_headers)
            
            # Add cookies
            cookies = self.session_manager._get_cookies_for_request(url)
            if cookies:
                new_headers["Cookie"] = cookies
            
            # Create new request with signature headers
            new_request = httpx.Request(
                method=request.method,
                url=request.url,
                headers=new_headers,
                content=body_content,
                extensions=request.extensions
            )
            
            # Send via parent transport
            response = await super().handle_async_request(new_request)
            
            # Store cookies
            self.session_manager._store_cookies(response, url)
            
            return response
