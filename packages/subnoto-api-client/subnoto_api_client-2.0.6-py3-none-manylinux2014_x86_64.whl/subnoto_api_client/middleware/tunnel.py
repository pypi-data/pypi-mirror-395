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

from typing import TYPE_CHECKING

import httpx

from ..types import SubnotoError

if TYPE_CHECKING:
    from ..session import SessionManager


def create_tunnel_middleware(session_manager: "SessionManager"):
    """Create tunnel encryption/decryption middleware"""
    
    async def encrypt_request(request: "httpx.Request") -> None:
        """Encrypt request body before sending"""
        url = str(request.url)
        
        # Skip if not targeting the enclave API
        if "/tunnel/" not in url and "/public/" not in url:
            return
        
        # Skip tunnel handshake endpoint itself
        if "/tunnel/session" in url:
            return
        
        # Ensure session is established
        await session_manager.ensure_session()
        
        # Get request body
        body_content = request.content
        if not body_content or len(body_content) == 0:
            raise SubnotoError("EMPTY_REQUEST_BODY")
        
        # Encrypt the request body
        encrypted_message = session_manager.encrypt_request(body_content)
        
        if not encrypted_message or len(encrypted_message) == 0:
            raise SubnotoError("Empty encrypted message")
        
        # Get session ID
        session_id = session_manager.get_session_id()
        if not session_id:
            raise SubnotoError("Session ID not available")
        
        # Update headers
        request.headers["X-Session-Id"] = session_id
        request.headers["Content-Type"] = "application/octet-stream"
        
        # Remove old Content-Length so httpx recalculates it
        if "Content-Length" in request.headers:
            del request.headers["Content-Length"]
        
        # Add cookies if available
        cookies = session_manager._get_cookies_for_request(url)
        if cookies:
            request.headers["Cookie"] = cookies
        
        # Update request content using stream - httpx handles Content-Length
        request.stream = httpx.ByteStream(encrypted_message)
    
    async def decrypt_response(response: "httpx.Response") -> None:
        """Decrypt response body after receiving"""
        url = str(response.request.url)
        
        # Skip if not targeting the enclave API
        if "/tunnel/" not in url and "/public/" not in url:
            return
        
        # Skip tunnel handshake endpoint itself
        if "/tunnel/session" in url:
            return
        
        # Check if response is encrypted
        is_encrypted = (
            response.headers.get("x-subnoto-encrypted-response") == "true"
            and response.headers.get("content-type") == "application/octet-stream"
        )
        
        if not is_encrypted:
            # Return as-is if not encrypted
            return
        
        # Get encrypted data
        encrypted_data = response.content
        
        if len(encrypted_data) == 0:
            raise SubnotoError("Empty encrypted response")
        
        # Decrypt the response
        decrypted_data = session_manager.decrypt_response(encrypted_data)
        
        # Replace response content with decrypted data
        # Note: httpx.Response is immutable, so we need to modify the stream
        # This is a workaround - in practice, we may need to return a new response
        response._content = decrypted_data
        response.headers["Content-Type"] = "application/json"
        if "x-subnoto-encrypted-response" in response.headers:
            del response.headers["x-subnoto-encrypted-response"]
    
    return {
        "request": encrypt_request,
        "response": decrypt_response
    }

